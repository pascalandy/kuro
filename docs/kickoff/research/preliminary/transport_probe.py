#!/usr/bin/env python3
"""Bounded localhost transport probe. This does not drive audio hardware."""

from __future__ import annotations

import hashlib
import io
import json
import socket
import struct
import subprocess
import tempfile
import threading
import time
import wave
from pathlib import Path


RATE = 48_000
CHANNELS = 2
WIDTH = 2
FRAMES = RATE * 2
PCM_CHUNK_FRAMES = 480
PCM_CHUNK_BYTES = PCM_CHUNK_FRAMES * CHANNELS * WIDTH


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_pcm() -> bytes:
    state = 0x1234ABCD
    out = bytearray()
    for _ in range(FRAMES * CHANNELS):
        state = (1_664_525 * state + 1_013_904_223) & 0xFFFFFFFF
        sample = ((state >> 16) & 0xFFFF) - 32768
        out.extend(struct.pack("<h", sample))
    return bytes(out)


def make_wav(pcm: bytes) -> bytes:
    out = io.BytesIO()
    with wave.open(out, "wb") as stream:
        stream.setnchannels(CHANNELS)
        stream.setsampwidth(WIDTH)
        stream.setframerate(RATE)
        stream.writeframes(pcm)
    return out.getvalue()


def decoded_pcm(wav_bytes: bytes) -> bytes:
    with wave.open(io.BytesIO(wav_bytes), "rb") as stream:
        assert stream.getparams()[:4] == (CHANNELS, WIDTH, RATE, FRAMES)
        return stream.readframes(FRAMES)


def loopback_transfer(payload: bytes, *, stall: bool) -> tuple[bytes, list[float]]:
    ready = threading.Event()
    address: list[tuple[str, int]] = []

    def serve() -> None:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            address.append(listener.getsockname())
            ready.set()
            connection, _ = listener.accept()
            with connection:
                for index in range(0, len(payload), PCM_CHUNK_BYTES):
                    chunk_number = index // PCM_CHUNK_BYTES
                    if stall and chunk_number == 5:
                        time.sleep(0.200)
                    connection.sendall(payload[index : index + PCM_CHUNK_BYTES])
                    time.sleep(0.003)

    thread = threading.Thread(target=serve)
    thread.start()
    ready.wait()
    received = bytearray()
    arrivals: list[float] = []
    with socket.create_connection(address[0]) as connection:
        while len(received) < len(payload):
            wanted = min(PCM_CHUNK_BYTES, len(payload) - len(received))
            chunk = bytearray()
            while len(chunk) < wanted:
                part = connection.recv(wanted - len(chunk))
                if not part:
                    raise RuntimeError("loopback stream ended early")
                chunk.extend(part)
            received.extend(chunk)
            arrivals.append(time.monotonic())
    thread.join()
    return bytes(received), arrivals


def modeled_underruns(arrivals: list[float]) -> int:
    prebuffer_chunks = 4
    start = arrivals[prebuffer_chunks - 1]
    period = PCM_CHUNK_FRAMES / RATE
    underruns = 0
    for consumed_index in range(len(arrivals)):
        deadline = start + consumed_index * period
        available = sum(arrival <= deadline for arrival in arrivals)
        if available <= consumed_index:
            underruns += 1
    return underruns


def main() -> None:
    pcm = make_pcm()
    wav_bytes = make_wav(pcm)
    with tempfile.TemporaryDirectory(prefix="kuro-sq-probe-") as temp_dir:
        temp = Path(temp_dir)
        source_wav = temp / "source.wav"
        source_flac = temp / "source.flac"
        received_flac = temp / "received.flac"
        decoded_wav = temp / "decoded.wav"
        source_wav.write_bytes(wav_bytes)
        subprocess.run(
            ["flac", "--silent", "--force", "-o", source_flac, source_wav],
            check=True,
        )
        flac_bytes = source_flac.read_bytes()
        transferred_flac, _ = loopback_transfer(flac_bytes, stall=True)
        received_flac.write_bytes(transferred_flac)
        subprocess.run(
            ["flac", "--silent", "--decode", "--force", "-o", decoded_wav, received_flac],
            check=True,
        )
        smooth_pcm, smooth_arrivals = loopback_transfer(pcm, stall=False)
        stalled_pcm, stalled_arrivals = loopback_transfer(pcm, stall=True)
        result = {
            "boundary": "127.0.0.1 only; no NAS, renderer, DAC, or analogue capture",
            "format": {"rate_hz": RATE, "channels": CHANNELS, "sample_width_bits": WIDTH * 8},
            "file_transport": {
                "source_sha256": sha256(flac_bytes),
                "received_sha256": sha256(transferred_flac),
                "pass": flac_bytes == transferred_flac,
            },
            "decoded_pcm": {
                "source_sha256": sha256(pcm),
                "decoded_received_sha256": sha256(decoded_pcm(decoded_wav.read_bytes())),
                "pass": pcm == decoded_pcm(decoded_wav.read_bytes()),
            },
            "timing_model": {
                "period_ms": 10,
                "prebuffer_ms": 40,
                "smooth_loopback_payload_pass": pcm == smooth_pcm,
                "smooth_modeled_underrun_periods": modeled_underruns(smooth_arrivals),
                "stalled_loopback_payload_pass": pcm == stalled_pcm,
                "stalled_modeled_underrun_periods": modeled_underruns(stalled_arrivals),
                "deliberate_stall_ms": 200,
                "warning": "arrival timestamps feed a consumer model; no audio device was opened",
            },
            "versions": {
                "python": subprocess.check_output(["python3", "--version"], text=True).strip(),
                "flac": subprocess.check_output(["flac", "--version"], text=True).strip(),
            },
        }
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
