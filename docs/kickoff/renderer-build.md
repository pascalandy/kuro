# MPD laboratory build

The renderer probe uses MPD 0.24.15 from the official release archive. The
reproducible build entry point is [`scripts/build_lab_mpd.sh`](../../scripts/build_lab_mpd.sh).
It accepts one absolute output directory and keeps the archive, extracted
source, Python environment, build tree, and resulting binary there. It is
idempotent: downloads and source extraction use temporary paths before atomic
rename. An existing archive is verified before reuse, and source contents and
permissions must match a fresh extraction of that archive, except for the root
`build-lab` directory. An existing Meson tree is reconfigured. A mismatched
archive or source tree is preserved and rejected; use a fresh output directory
to rebuild without overwriting local edits.

```sh
scripts/build_lab_mpd.sh /tmp/kuro-mpd-lab
```

The script pins MPD 0.24.15 and SHA-256
`524c70bce3fcd268016156bdc97abcf5be1904f0c6fd622688999123e3c4c457`, and
installs exactly Meson 1.12.0 and Ninja 1.13.2 into the output directory's
Python virtual environment. Meson 1.12.0 accepts the packaged Ninja version
directly, so no wrapper or global tool override is needed. No system package,
service, configuration, or installed MPD is changed.

The configured laboratory feature set is deliberately narrow:

- FLAC decoder and WAV decoder through libsndfile;
- HTTP/HTTPS input through libcurl (also exposes the other libcurl protocols);
- `null`, FIFO, and pipe output plugins;
- local Unix socket and TCP control;
- no ALSA, PipeWire, PulseAudio, JACK, OpenAL, systemd, database, resampler,
  HTTP streaming output, or physical output path.

The host used for this probe had development metadata for `fmt`, `libgcrypt`,
`flac`, `sndfile`, `libcurl`, and the transitive libraries selected by MPD.
The script checks the five direct development packages and lets Meson report
any further missing headers or libraries clearly. It does not install system
dependencies. A clean machine therefore needs those distribution development
packages, a C/C++ toolchain, Python virtual environments, curl, tar, sha256sum,
pkg-config, and network access to the official MPD host and Python package
index. Package availability and dependency versions remain host packaging
inputs; the script pins the MPD archive and build-tool versions only.

The observed artifact was:

```text
Music Player Daemon 0.24.15 (0.24.15)
Decoder plugins: oggflac, flac, sndfile (wav ...), pcm
Output plugins: null fifo pipe
Input plugins: file archive curl
Protocols: file:// ftp:// ftps:// gopher:// http:// https:// scp:// sftp://
Other features: epoll tcp unix local socket
```

`oggflac`, archive, and the extra libsndfile formats are transitive capabilities
of the selected MPD source/development libraries. The build does not claim
that every listed input or format has been independently exercised here.

The prior silent smoke fixture decoded a 0.25-second 44.1 kHz stereo 16-bit
FLAC through a Unix socket and FIFO, producing 44,100 bytes. That test proves
local decode and capture only. It does not establish ALSA negotiation, USB DDC
behavior, I2S timing, gapless transitions, or analog sound quality. A later
lab may compare this same binary's HTTP input against whole-file staging while
keeping the FIFO capture and physical output disabled.

The output directory contains the runnable binary at
`mpd-0.24.15/build-lab/mpd`; generated binaries and build trees are intentionally
excluded from the repository.

Run the retry and source-integrity regression checks with the archive from a
normal build directory:

```sh
python3 scripts/test_build_lab_mpd.py --archive /tmp/kuro-mpd-lab/mpd-0.24.15.tar.xz
```

The test uses a temporary output directory and leaves the supplied archive
untouched. It checks real archive hashes and source contents, injects download
and extraction failures, and stubs package checks and build tools. It performs
no download or compilation.
