#!/usr/bin/env python3
"""Test build-script retries using a local archive, without compiling or downloading.

SHA verification, successful tar extraction and source integrity checks are real.
Curl, package checks and build tools are stubbed; tar can inject a partial failure.
"""

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True,
                        help="Existing pinned MPD 0.24.15 release archive")
    args = parser.parse_args()
    archive = args.archive.resolve()
    if not archive.is_file():
        parser.error(f"archive is not a file: {archive}")
    real_tar = shutil.which("tar")
    if real_tar is None:
        parser.error("tar is required")
    real_tar = str(Path(real_tar).resolve())
    script = Path(__file__).resolve().with_name("build_lab_mpd.sh")
    with tempfile.TemporaryDirectory(prefix='kuro-build-atomic-test.') as tmp:
        root = Path(tmp)
        out = root / 'output'
        out.mkdir()
        stubs = root / 'stubs'
        stubs.mkdir()
        def executable(path, text):
            path.write_text('#!/bin/bash\nset -eu\n' + text)
            path.chmod(0o755)
        executable(stubs / 'pkg-config', 'exit 0\n')
        executable(stubs / 'curl', '''while [[ $# -gt 0 ]]; do
    if [[ "$1" == --output ]]; then dest=$2; shift; fi
    shift
    done
    if [[ -f "$KURO_TEST_CONTROL/fail-curl" ]]; then printf partial > "$dest"; exit 18; fi
    cp "$KURO_TEST_ARCHIVE" "$dest"
    ''')
        executable(stubs / 'tar', '''if [[ -f "$KURO_TEST_CONTROL/fail-tar" ]]; then
    mkdir -p "$4/mpd-0.24.15"
    printf partial > "$4/mpd-0.24.15/meson.build"
    exit 2
    fi
    exec "$KURO_TEST_TAR" "$@"
    ''')
        cached_archive = out / 'mpd-0.24.15.tar.xz'
        venv = out / 'venv/bin'
        venv.mkdir(parents=True)
        executable(venv / 'python', 'exit 0\n')
        executable(venv / 'meson', '''if [[ "$1" == setup ]]; then mkdir -p "$2"; fi
    if [[ "$1" == compile ]]; then
    printf '#!/bin/bash\\nprintf "fake MPD for lifecycle test\\\\n"\\n' > "$3/mpd"
    chmod +x "$3/mpd"
    fi
    ''')
        env = dict(os.environ, PATH=str(stubs)+':'+os.environ['PATH'], KURO_TEST_CONTROL=str(root),
                   KURO_TEST_ARCHIVE=str(archive), KURO_TEST_TAR=real_tar)
        def run(success, needle='', exit_code=None):
            result = subprocess.run(['bash', str(script), str(out)], env=env, text=True, capture_output=True)
            check((result.returncode == 0) == success, result.stderr + result.stdout)
            if exit_code is not None:
                check(result.returncode == exit_code, f"expected exit {exit_code}, got {result.returncode}: {result.stderr}")
            check(needle in result.stderr, result.stderr)
            check(not list(out.glob('.mpd-*')), f'temporary paths leaked: {list(out.iterdir())}')
        (root / 'fail-curl').touch()
        run(False, exit_code=18)
        check(not cached_archive.exists(), 'failed download published an archive')
        (root / 'fail-curl').unlink()
        (root / 'fail-tar').touch()
        run(False, exit_code=2)
        check(cached_archive.exists(), 'verified archive was not retained')
        check(not (out / 'mpd-0.24.15').exists(), 'failed extraction published a source tree')
        (root / 'fail-tar').unlink()
        run(True)
        run(True)
        source_file = out / 'mpd-0.24.15/meson.build'
        original = source_file.read_bytes()
        source_file.write_bytes(original + b'\n# local edit\n')
        run(False, 'source tree differs')
        check(source_file.read_bytes() == original + b'\n# local edit\n', 'local edit was overwritten')
        source_file.write_bytes(original)
        extra = out / 'mpd-0.24.15/extra-local.txt'
        extra.write_text('local')
        run(False, 'source tree differs')
        check(extra.read_text() == 'local', 'extra source file was overwritten')
        extra.unlink()
        run(True)
        cached_archive.write_text('invalid user cache')
        run(False, 'cached archive hash mismatch')
        check(cached_archive.read_text() == 'invalid user cache', 'invalid cached archive was overwritten')
    print('PASS: interrupted download/extraction cleanup and retry; known archive/source reuse; modified/extra source rejection; invalid cached archive preserved. Build tools stubbed; SHA, extraction and integrity checks real.')


if __name__ == "__main__":
    main()
