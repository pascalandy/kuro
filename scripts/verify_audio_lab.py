#!/usr/bin/env python3
"""Silent Go WAV playback and separate Python loopback FLAC transfer/decode proof."""
import argparse
from contextlib import contextmanager
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import select
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import wave


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def quote(value):
    return json.dumps(str(value))


def run(command, out, label, commands):
    commands.append(command)
    with (out / (label + '.stdout')).open('wb') as stdout, (out / (label + '.stderr')).open('wb') as stderr:
        subprocess.run(command, stdout=stdout, stderr=stderr, check=True, timeout=30)


@contextmanager
def origin(encoded, out):
    objects = {'/' + path.name: path.read_bytes() for path in encoded}
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            self.request.settimeout(2)
            super().setup()

        def log_message(self, *_):
            pass

        def do_GET(self):
            self.connection.settimeout(2)
            data = objects.get(self.path)
            record = {'method': 'GET', 'path': self.path, 'request_headers': dict(self.headers),
                      'status': 200 if data is not None else 404}
            requests.append(record)
            if data is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'audio/flac')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('ETag', '"' + digest(data) + '"')
            self.end_headers()
            try:
                self.wfile.write(data)
                record['bytes_sent'] = len(data)
            except (BrokenPipeError, ConnectionResetError, TimeoutError) as error:
                record['error'] = str(error)

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    server.daemon_threads = False
    thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.05}, daemon=True)
    thread.start()
    try:
        yield ['http://127.0.0.1:' + str(server.server_port) + '/' + path.name for path in encoded]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
        (out / 'http-origin.json').write_text(json.dumps(requests, indent=2) + '\n')


def receive(url, original, destination):
    expected = original.read_bytes()
    # Ignore proxy environment settings for this private loopback origin.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=5) as response:
        require(response.status == 200, 'FLAC HTTP status mismatch')
        require(int(response.headers['Content-Length']) == len(expected), 'FLAC HTTP length mismatch')
        received = response.read(len(expected) + 1)
        destination.write_bytes(received)
        record = {'url': url, 'status': response.status, 'headers': dict(response.headers),
                  'bytes': len(received), 'sha256': digest(received),
                  'expected_bytes': len(expected), 'expected_sha256': digest(expected)}
    destination.with_suffix('.http.json').write_text(json.dumps(record, indent=2) + '\n')
    require(received == expected, 'FLAC HTTP received bytes differ from encoded source')
    return record


def sources(proof):
    manifest = json.loads((proof / 'manifest.json').read_text())
    fixtures = manifest['fixtures']
    require([f['id'] for f in fixtures] == ['track-1', 'track-2'], 'expected track-1 then track-2')
    masters, accepted = [], []
    for fixture in fixtures:
        track = fixture['id']
        pcm = (proof / 'fixtures' / (track + '.pcm')).read_bytes()
        wav = proof / 'fixtures' / (track + '.wav')
        ready = proof / 'ready' / ('clean-' + track + '.wav')
        require(len(pcm) > 0 and len(pcm) % 4 == 0, 'invalid PCM frame count')
        require(digest(pcm) == fixture['pcm_sha256'], 'master PCM hash mismatch')
        original = wav.read_bytes()
        require(len(original) == fixture['bytes'], 'master WAV size mismatch')
        require(digest(original) == fixture['sha256'], 'master WAV hash mismatch')
        require(ready.read_bytes() == original, 'accepted WAV differs from master')
        for path in (wav, ready):
            with wave.open(str(path), 'rb') as reader:
                require((reader.getnchannels(), reader.getsampwidth(), reader.getframerate(), reader.getcomptype()) == (2, 2, 48000, 'NONE'), 'unexpected WAV format')
                require(reader.getnframes() * 4 == len(pcm), 'PCM length differs from WAV')
                require(reader.readframes(reader.getnframes()) == pcm, 'WAV PCM differs from master')
        masters.append(pcm)
        accepted.append(ready.resolve())
    return masters, accepted


class MPD:
    def __init__(self, path):
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.settimeout(1)
        try:
            self.socket.connect(str(path))
            self.reader = self.socket.makefile('rb')
            require(self.reader.readline().startswith(b'OK MPD '), 'invalid MPD greeting')
        except BaseException:
            self.socket.close()
            raise

    def command(self, command):
        self.socket.sendall((command + '\n').encode())
        lines = []
        while True:
            line = self.reader.readline().decode().rstrip('\n')
            if line == 'OK':
                return lines
            require(line and not line.startswith('ACK'), 'MPD command failed: ' + line)
            lines.append(line)

    def close(self):
        self.reader.close()
        self.socket.close()


def capture(mpd, files, expected, out, label, commands):
    directory = out / label
    directory.mkdir()
    # Short, mode-0700 socket path, independent of the caller's output path length.
    with tempfile.TemporaryDirectory(prefix='kuro-mpd-') as private:
        private = Path(private)
        fifo, endpoint = private / 'pcm', private / 'control'
        os.mkfifo(fifo, 0o600)
        config = directory / 'mpd.conf'
        config.write_text('\n'.join([
            'bind_to_address ' + quote(endpoint),
            'auto_update "no"',
            'replaygain "off"',
            'audio_output {', ' type "fifo"', ' name "silent proof"',
            ' path ' + quote(fifo), ' format "48000:16:2"',
            ' mixer_type "none"', '}', '',
        ]))
        descriptor = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
        client = None
        process = None
        protocol = []
        command = [str(mpd), '--no-daemon', '--stderr', str(config)]
        commands.append(command)
        try:
            with (directory / 'stdout.log').open('wb') as stdout, (directory / 'stderr.log').open('wb') as stderr, (directory / 'capture.pcm').open('wb') as sink:
                process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                           env={k: v for k, v in os.environ.items()
                                                if not k.startswith('LISTEN_') and not k.lower().endswith('_proxy')})
                deadline = time.monotonic() + 10
                while client is None:
                    require(process.poll() is None, 'MPD exited during startup; inspect stderr.log')
                    require(time.monotonic() < deadline, 'MPD startup timed out')
                    try:
                        client = MPD(endpoint)
                    except (FileNotFoundError, ConnectionRefusedError):
                        time.sleep(0.02)
                def send(text):
                    response = client.command(text)
                    protocol.append({'command': text, 'response': response})
                    return response
                outputs = send('outputs')
                require(sum(line.startswith('outputid:') for line in outputs) == 1 and 'outputname: silent proof' in outputs, 'unexpected audio outputs')
                for path in files:
                    send('add ' + quote(path.as_uri() if isinstance(path, Path) else path))
                send('crossfade 0')
                send('random 0')
                send('repeat 0')
                send('play')
                deadline = time.monotonic() + len(expected) / 192000 + 15
                next_status, stopped_at, count = 0, None, 0
                while True:
                    now = time.monotonic()
                    require(now < deadline, 'FIFO playback timed out')
                    require(process.poll() is None, 'MPD exited during playback')
                    readable, _, _ = select.select([descriptor], [], [], 0.02)
                    if readable:
                        data = os.read(descriptor, 65536)
                        if data:
                            sink.write(data)
                            count += len(data)
                            require(count <= len(expected), 'MPD produced extra PCM bytes')
                        else:
                            time.sleep(0.01)
                    if now >= next_status:
                        status = send('status')
                        require(not any(line.startswith('error:') for line in status), 'MPD playback error')
                        if 'state: stop' in status and stopped_at is None:
                            stopped_at = now
                        next_status = now + 0.1
                    if stopped_at is not None and now - stopped_at >= 0.3:
                        break
                send('stop')
        finally:
            if client is not None:
                client.close()
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            os.close(descriptor)
            (directory / 'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
    actual = (directory / 'capture.pcm').read_bytes()
    result = {'bytes': len(actual), 'frames': len(actual) // 4, 'sha256': digest(actual),
              'expected_bytes': len(expected), 'expected_sha256': digest(expected)}
    (directory / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    require(actual == expected, label + ': FIFO PCM differs from exact master concatenation')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof-dir', required=True, type=Path)
    parser.add_argument('--mpd', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(mode=0o700, parents=False, exist_ok=False)
    out = args.out.resolve()
    commands = []
    result = {'passed': False, 'python_version': sys.version,
              'scope': 'Go transported WAV. A separate Python loopback HTTP origin transports generated FLAC for verified receive/decode and direct MPD HTTP playback. FIFO captures test ordered PCM bytes only; no progressive timing, ALSA, USB, DDC, DAC, jitter or sound-quality proof.'}
    try:
        mpd = args.mpd.resolve(strict=True)
        flac = shutil.which('flac')
        require(flac is not None, 'flac executable is required')
        run([str(mpd), '--version'], out, 'mpd-version', commands)
        run([flac, '--version'], out, 'flac-version', commands)
        masters, accepted = sources(args.proof_dir.resolve())
        encoded = []
        result['flac'] = []
        for index, pcm in enumerate(masters, 1):
            source = args.proof_dir.resolve() / 'fixtures' / ('track-' + str(index) + '.pcm')
            destination = out / ('track-' + str(index) + '.flac')
            run([flac, '--force-raw-format', '--endian=little', '--sign=signed', '--channels=2', '--bps=16', '--sample-rate=48000', '-o', str(destination), str(source)], out, 'encode-' + str(index), commands)
            encoded.append(destination)
        expected = b''.join(masters)
        result['wav_fifo'] = capture(mpd, accepted, expected, out, 'wav-fifo', commands)
        with origin(encoded, out) as urls:
            received = []
            for index, (pcm, original, url) in enumerate(zip(masters, encoded, urls), 1):
                transferred = out / ('track-' + str(index) + '.received.flac')
                http = receive(url, original, transferred)
                decoded = out / ('track-' + str(index) + '.decoded.pcm')
                run([flac, '--decode', '--force-raw-format', '--endian=little', '--sign=signed', '-o', str(decoded), str(transferred)], out, 'decode-' + str(index), commands)
                require(decoded.read_bytes() == pcm, 'FLAC transfer/decode mismatch')
                result['flac'].append({'bytes': len(pcm), 'frames': len(pcm) // 4, 'pcm_sha256': digest(pcm), 'flac_sha256': digest(original.read_bytes()), 'http': http})
                received.append(transferred)
            require(all(local.read_bytes() == source.read_bytes() for local, source in zip(received, encoded)),
                    'received FLAC changed before MPD enqueue')
            result['flac_fifo'] = capture(mpd, received, expected, out, 'flac-fifo', commands)
            result['http_flac_fifo'] = capture(mpd, urls, expected, out, 'http-flac-fifo', commands)
        require(sources(args.proof_dir.resolve()) == (masters, accepted), 'source artifacts changed during proof')
        result['passed'] = True
    except Exception as error:
        result['error'] = str(error)
    finally:
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
