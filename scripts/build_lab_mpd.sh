#!/usr/bin/env bash
set -euo pipefail

readonly MPD_VERSION="0.24.15"
readonly MPD_URL="https://www.musicpd.org/download/mpd/0.24/mpd-${MPD_VERSION}.tar.xz"
readonly MPD_SHA256="524c70bce3fcd268016156bdc97abcf5be1904f0c6fd622688999123e3c4c457"
readonly MESON_VERSION="1.12.0"
readonly NINJA_VERSION="1.13.2"

usage() {
    printf 'Usage: %s OUTPUT_DIR\n' "$0" >&2
    printf 'Builds an isolated MPD lab artifact under OUTPUT_DIR.\n' >&2
}

if [[ $# -ne 1 ]]; then
    usage
    exit 2
fi

out_dir=$1
if [[ "$out_dir" != /* ]]; then
    printf 'error: OUTPUT_DIR must be an absolute path (got %s)\n' "$out_dir" >&2
    exit 2
fi
mkdir -p "$out_dir"
if [[ ! -d "$out_dir" || ! -w "$out_dir" ]]; then
    printf 'error: OUTPUT_DIR is not writable: %s\n' "$out_dir" >&2
    exit 1
fi

for command_name in curl sha256sum tar python3 pkg-config mktemp; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'error: required host command is missing: %s\n' "$command_name" >&2
        exit 1
    fi
done

for pkg in fmt libgcrypt flac sndfile libcurl; do
    if ! pkg-config --exists "$pkg"; then
        printf 'error: required development package is missing: %s\n' "$pkg" >&2
        printf 'Install the distribution development package, then rerun; this script does not install system packages.\n' >&2
        exit 1
    fi
done

download_tmp=""
extract_tmp=""
cleanup() {
    [[ -z "$download_tmp" ]] || rm -f -- "$download_tmp"
    [[ -z "$extract_tmp" ]] || rm -rf -- "$extract_tmp"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

archive="$out_dir/mpd-${MPD_VERSION}.tar.xz"
if [[ -e "$archive" || -L "$archive" ]]; then
    actual_sha=$(sha256sum "$archive" | awk '{print $1}')
    if [[ "$actual_sha" != "$MPD_SHA256" ]]; then
        printf 'error: cached archive hash mismatch: %s\n' "$archive" >&2
        printf 'expected %s, got %s; use a fresh OUTPUT_DIR.\n' "$MPD_SHA256" "$actual_sha" >&2
        exit 1
    fi
else
    download_tmp=$(mktemp "$out_dir/.mpd-download.XXXXXXXX")
    curl --fail --location --proto '=https' --tlsv1.2 --silent --show-error \
        --output "$download_tmp" "$MPD_URL"
    actual_sha=$(sha256sum "$download_tmp" | awk '{print $1}')
    if [[ "$actual_sha" != "$MPD_SHA256" ]]; then
        printf 'error: downloaded archive hash mismatch: got %s\n' "$actual_sha" >&2
        exit 1
    fi
    mv -T -- "$download_tmp" "$archive"
    download_tmp=""
fi

source_dir="$out_dir/mpd-${MPD_VERSION}"
extract_tmp=$(mktemp -d "$out_dir/.mpd-source.XXXXXXXX")
tar -xf "$archive" -C "$extract_tmp"
pristine_dir="$extract_tmp/mpd-${MPD_VERSION}"
if [[ ! -f "$pristine_dir/meson.build" ]]; then
    printf 'error: expected source tree was not extracted: %s\n' "$pristine_dir" >&2
    exit 1
fi
if [[ -e "$source_dir" || -L "$source_dir" ]]; then
    python3 - "$pristine_dir" "$source_dir" <<'PYTHON'
import hashlib
import stat
import sys
from pathlib import Path


def manifest(root):
    entries = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] == "build-lab":
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            content = str(path.readlink())
        elif stat.S_ISREG(mode):
            content = hashlib.sha256(path.read_bytes()).hexdigest()
        elif stat.S_ISDIR(mode):
            content = None
        else:
            raise SystemExit(f"error: unsupported source entry: {path}; use a fresh OUTPUT_DIR")
        entries[str(relative)] = (stat.S_IFMT(mode), stat.S_IMODE(mode), content)
    return entries


pristine, source = map(Path, sys.argv[1:])
if source.is_symlink() or not source.is_dir() or manifest(pristine) != manifest(source):
    raise SystemExit(f"error: source tree differs from pinned archive: {source}; use a fresh OUTPUT_DIR")
PYTHON
else
    mv -T -- "$pristine_dir" "$source_dir"
fi
rm -rf -- "$extract_tmp"
extract_tmp=""

venv_dir="$out_dir/venv"
if [[ ! -x "$venv_dir/bin/python" ]]; then
    python3 -m venv "$venv_dir"
fi
"$venv_dir/bin/python" -m pip install --disable-pip-version-check --quiet \
    "meson==${MESON_VERSION}" "ninja==${NINJA_VERSION}"

build_dir="$source_dir/build-lab"
meson_args=(
    --buildtype=release
    -Ddocumentation=disabled -Dsystemd=disabled -Dsmbclient=disabled
    -Dzeroconf=disabled -Dchromaprint=disabled -Dfluidsynth=disabled
    -Dgme=disabled -Dmikmod=disabled -Dmodplug=disabled -Dmpcdec=disabled
    -Dsidplay=disabled -Dshine=disabled -Dtwolame=disabled -Dwildmidi=disabled
    -Dwavpack=disabled -Dzzip=disabled -Dcdio_paranoia=disabled
    -Dpipewire=disabled -Dpulse=disabled -Djack=disabled -Dopenal=disabled
    -Dao=disabled -Dshout=disabled -Dupnp=disabled -Ddatabase=false
    -Dneighbor=false -Dnfs=disabled -Dlibsamplerate=disabled -Dsoxr=disabled -Dalsa=disabled
    -Ddbus=disabled -Dpcre=disabled -Dnlohmann_json=disabled -Dsqlite=disabled
    -Dzlib=disabled -Dffmpeg=disabled -Dflac=enabled -Dsndfile=enabled
    -Dvorbis=disabled -Dopus=disabled -Dmpg123=disabled -Dopenmpt=disabled
    -Dlibmpdclient=disabled -Dcue=false -Ddsd=false -Dfifo=true -Dpipe=true
    -Drecorder=false -Dhttpd=false -Dsnapcast=false -Dsndio=disabled
    -Doss=disabled -Dsolaris_output=disabled -Diconv=disabled -Dicu=disabled
    -Dsyslog=disabled -Dinotify=false -Dio_uring=disabled -Ddaemon=true
    -Dtcp=true -Dipv6=disabled -Dlocal_socket=true -Dtest=false
    -Dcurl=enabled -Dexpat=enabled -Dwebdav=disabled -Dqobuz=disabled
)

export PATH="$out_dir:$venv_dir/bin:$PATH"
if [[ -d "$build_dir" ]]; then
    "$venv_dir/bin/meson" setup "$build_dir" "$source_dir" --reconfigure "${meson_args[@]}"
else
    "$venv_dir/bin/meson" setup "$build_dir" "$source_dir" "${meson_args[@]}"
fi
"$venv_dir/bin/meson" compile -C "$build_dir" -j2

mpd_path="$build_dir/mpd"
if [[ ! -x "$mpd_path" ]]; then
    printf 'error: build completed without executable: %s\n' "$mpd_path" >&2
    exit 1
fi
printf 'archive=%s\narchive_sha256=%s\nmeson=%s\nninja=%s\nmpd=%s\n' \
    "$archive" "$MPD_SHA256" "$MESON_VERSION" "$NINJA_VERSION" "$mpd_path"
"$mpd_path" --version
