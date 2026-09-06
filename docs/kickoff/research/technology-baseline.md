# Kuro local Linux technology baseline

Status: baseline captured on 2026-09-06. The newer sound-quality framing replaces local output as the core transport: Kuro server -> external streamer -> DAC. This file does not research that network path, clocks, jitter, DAC behavior, or a final server language. It remains evidence for the Linux catalog, UI, service lifecycle, local prototype, and packaging work. It makes no architecture choice.

## Product constraints that shape every candidate

The current cadrage requires a service that stays active when its window closes, explicit **Quit**, session-user-only control, offline operation, unchanged media sources, resumable scans, durable state, and a clean reproducible installation. The accepted PCM formats and gapless transitions still require a measured corpus. API support alone does not meet those criteria.

A useful boundary for all three candidates is one long-lived service that owns the queue, playback state, catalog writes, and SQLite connection. Windows are clients. A single held `GtkApplication` can remain alive without a window because `g_application_hold()` increments its use count, but it does not give the window and service separate process lifecycles. [GApplication lifecycle](https://docs.gtk.org/gio/class.Application.html) and [`g_application_hold()`](https://docs.gtk.org/gio/method.Application.hold.html).

On this machine, `systemd --user` is running. A user service can own the long-lived process independently of any UI. systemd recommends `Type=exec` for long-running services when precise readiness is unnecessary, and `Type=notify` or `Type=dbus` when clients need a reliable ready point. [systemd service source documentation](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml).

## Read-only inventory of the target machine

Observed versions are local facts, not clean-install requirements or product proofs.

| Area | Observed capability |
| --- | --- |
| Host | Omarchy 4.0.2, Arch-derived, Linux 7.1.9-arch1-2, x86_64 |
| Session | systemd 261.2-1 running as user manager; D-Bus 1.16.2; `/run/user/1000` mode `0700` |
| Rust | `rustc` 1.98.0 and `cargo` 1.98.0 from `~/.cargo`; no Arch `rust` or `cargo` package |
| Python | Python 3.14.7, PyGObject 3.56.3; GI imports for GTK, GStreamer, GstPbutils, and Gio succeed |
| Native UI | GTK 4.22.4 and libadwaita 1.9.3 headers and pkg-config files are present |
| Audio framework | GStreamer 1.28.6 headers and GI bindings; PipeWire 1.6.8 and `pipewiresink` present |
| GStreamer registry | `playbin`, `playbin3`, `uridecodebin3`, Vorbis and Opus decoders present; checked FLAC, MP3, AAC, ALAC decoders and WAV parser absent |
| GTK media sink | GTK 3 `gtksink` 1.28.6 present; GTK 4 `gtk4paintablesink` absent. An audio-only player does not need a video sink. |
| mpv path | mpv 0.41.0, libmpv API 2.5.0, headers and shared library present; PipeWire output listed |
| FFmpeg path | FFmpeg 9.0.1; local decoder registry contains FLAC, MP3, AAC, ALAC, PCM, Vorbis, and Opus |
| Catalog | SQLite 3.53.4; FTS5 compile option is enabled and an in-memory FTS5 table worked |
| Desktop web UI | Node 26.7.0, npm 11.19.0, WebKitGTK 4.1 API version 2.52.6 and headers present; Tauri CLI absent |
| Missing build tools | `meson`, `ninja`, `pnpm`, and `bun` absent; this does not prevent all candidate builds |

No command scanned the user's music, opened an audio stream, emitted sound, installed a package, or changed machine configuration.

## Candidate A: native GTK plus GStreamer

This path has the smallest installed dependency gap for a native Linux UI. Python and GI can support a fast prototype. Rust bindings could use the same native libraries, but no Rust GTK or GStreamer crate has been fetched or built here.

`playbin3` exists locally. GStreamer's design pre-rolls the next item and switches sources at end of stream. The application supplies the next URI through `about-to-finish`. [GStreamer gapless design](https://gstreamer.freedesktop.org/documentation/additional/design/playback-gapless.html) and [`playbin`](https://gstreamer.freedesktop.org/documentation/playback/playbin.html).

That documentation is an implementation mechanism, not proof of Kuro's gapless requirement. The local registry cannot currently decode most of the candidate corpus through the factories checked above. Even after the decoder closure is supplied, tests must measure homogeneous transitions for the accepted formats, the chosen sink, the external transport if applicable, local and NAS fixtures, queue changes near end of stream, and underruns. None of those tests has run.

`GstDiscoverer` supports blocking and asynchronous discovery of information from URIs. It is available through GstPbutils on this machine. [GstDiscoverer API](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html). Its presence does not prove tag fallback rules, malformed-file isolation, cancellation, performance at 20,000 albums, or that application code never writes media.

Service separation still needs two processes: a headless service with GStreamer, SQLite, and IPC, plus a GTK client. GTK's application hold is suitable only for a smaller lifecycle prototype where that process separation is intentionally deferred.

## Candidate B: Rust service plus desktop web UI

The installed Rust toolchain, Node, and WebKitGTK satisfy key local prerequisites for a Tauri 2 experiment. Tauri's current Arch prerequisites name `webkit2gtk-4.1`, `base-devel`, OpenSSL, appindicator, librsvg, and related tools. [Tauri Linux prerequisites](https://tauri.app/start/prerequisites/). The missing Tauri CLI and unfetched Cargo or npm dependencies mean no Tauri build has been proved.

Each Tauri application has one core process that owns its windows and system access, plus WebView processes. To give Kuro's service a lifecycle independent of that desktop application, use a separate Rust service process and treat the Tauri application as a client. Tauri's built-in webview IPC capabilities constrain frontend access to commands, but they do not replace the service-to-UI protocol. [Tauri process model](https://tauri.app/concept/process-model/), [IPC](https://tauri.app/concept/inter-process-communication/), and [capabilities](https://tauri.app/security/capabilities/).

The service can use GStreamer, libmpv, or another audio library. The web UI choice does not settle audio behavior. It adds WebKitGTK and a frontend dependency graph to the clean-install and license closure. The installed WebKitGTK package alone is 133.55 MiB and declares many licenses in Arch metadata. That number describes this package, not a future Kuro artifact.

This candidate fits a strong typed service and a flexible UI, but the useful proof is a built, offline artifact that starts the user service, closes and reopens the window without losing state, and survives a clean user session. No such artifact exists.

## Candidate C: mpv-based prototype

mpv is the shortest installed path to exercise queue control, target files, and a playback process independent of the UI. Upstream recommends JSON IPC over a Unix-domain socket when controlling an mpv process and recommends `--no-config` or a separate config directory to avoid user CLI settings. It also says that the IPC protocol is not secure. [mpv manual, controlling mpv](https://mpv.io/manual/stable/#using-mpv-from-other-programs-or-scripts).

The local default is `--gapless-audio=weak`. mpv says this normally keeps the device open for files with the same settings, may reopen it when decoder output changes, and can run out of buffered audio when the next source starts slowly. `yes` keeps the first output parameters and may resample later files. [mpv `gapless-audio`](https://mpv.io/manual/master/#options-gapless-audio). Those modes need measurements. Their names do not establish sample-accurate transitions or sound quality, especially for NAS and an external streamer path.

The subprocess and JSON protocol are good prototype boundaries. They do not prove catalog import, metadata rules, persistent identity, recovery, or packaging. libmpv offers a typed C API and is installed, but embedding it increases integration work and keeps the same FFmpeg and mpv dependency questions.

## Local IPC permissions

The D-Bus session bus is a realistic common protocol for GTK/Gio and Rust. D-Bus authenticates Unix clients with credentials and can report a connection's Unix user. Its session bus supports single-owner names, activation, and policy. [D-Bus specification](https://dbus.freedesktop.org/doc/dbus-specification.html). Here, the bus socket is mode `0666` inside `/run/user/1000`, whose mode is `0700`; the containing directory limits path access to this user.

A private filesystem Unix socket under `$XDG_RUNTIME_DIR/kuro/` is the smaller alternative for JSON or another protocol. Set the directory to `0700` and the socket to `0600`, and verify peer credentials. systemd's `SocketMode=` defaults to `0666`, so Kuro must set it explicitly if systemd owns the socket. [systemd socket source documentation](https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml).

Both mechanisms authorize the session user, not one trusted UI process. Any process running as that Unix user may call the exposed API. Keep the API narrow, validate all requests at the service boundary, and never expose arbitrary mpv commands or file paths. A loopback TCP listener does not carry Unix peer credentials. D-Bus itself deprecates TCP on Unix for this reason. A local HTTP design therefore adds origin, token, and request-forgery controls to meet the stated user-only boundary.

## Metadata and source integrity

The scanner must open media for reading and write only application-owned catalog and artwork paths. Use fixture media on a read-only mount, hash every source before and after the scan, inject malformed files and interrupted NAS reads, and fail the proof on any source change. Run the same fixture through whichever parser is selected. `GstDiscoverer`, FFprobe, libavformat, or a Rust tag crate being described as a reader is insufficient evidence.

SQLite is suitable for an early catalog experiment across all candidates. The local build supports FTS5, and the default `unicode61` behavior matched the in-memory query `joga` against `Jóga`. [SQLite FTS5](https://www.sqlite.org/fts5.html). This one query does not prove the required fields, stable ordering, accent handling across the corpus, 95th-percentile latency, backup, restore, or interruption behavior.

## Packaging and license evidence limits

GTK and GStreamer core use LGPL terms. GStreamer warns that plugin dependencies can change the effective license and recommends checking each shipped plugin with `gst-inspect-1.0`. [GTK overview](https://docs.gtk.org/gtk4/overview.html) and [GStreamer licensing](https://gstreamer.freedesktop.org/documentation/frequently-asked-questions/licensing.html).

The installed Arch FFmpeg is configured with `--enable-gpl` and Arch labels package `2:9.0.1-1` as GPL-3.0-only. FFmpeg explains that enabling GPL parts changes FFmpeg from LGPL to GPL. [FFmpeg legal page](https://ffmpeg.org/legal.html). The installed mpv package declares both GPL-2.0-or-later and LGPL-2.1-or-later, while upstream says the whole default build is GPLv2+ and that an LGPL build requires excluding GPL-only files. Linked libraries can still affect the result. [mpv copyright and license notes](https://github.com/mpv-player/mpv/blob/master/Copyright).

Tauri itself is MIT or Apache-2.0, but its own architecture document tells distributors to verify all upstream licenses. [Tauri architecture and license](https://github.com/tauri-apps/tauri/blob/dev/ARCHITECTURE.md). SQLite's delivered core is public domain. [SQLite copyright](https://www.sqlite.org/copyright.html).

No application license follows from these facts. KB-010 needs the exact shipped artifact, locked dependency graph, native libraries, codec plugins, build flags, notices, source-offer duties, and distribution method. Depending on host packages and bundling them are different cases. Patent or codec-distribution conclusions also remain open.

## Minimum evidence before an architecture decision

1. Build one small service boundary that persists queue state in SQLite and survives UI close and reopen.
2. Exercise both D-Bus and a permissioned Unix socket with an unauthorized-user test, a malformed request, a stale client, and explicit **Quit**.
3. Scan only a synthetic read-only metadata corpus, then measure cancellation, malformed files, path relocation, NAS loss, memory, and search latency.
4. Measure the accepted audio transitions on the eventual Kuro server -> streamer -> DAC path. Keep local GStreamer and mpv results labeled as local prototype results.
5. Produce one pinned package in a clean Omarchy or Arch VM. Verify offline install, user-service startup, window lifecycle, uninstall with data retention, and restore.
6. Generate the bill of materials and license record from that exact artifact.

Until those results exist, the installed machine supports all three experiments to different degrees. It proves none of the three as the U-M1 architecture.
