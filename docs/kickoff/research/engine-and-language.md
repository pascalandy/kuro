# Kuro server language and renderer path for sound quality

Status: primary-source research, 2026-09-06. This report is input to kickoff synthesis, not an arena decision or an adoption decision. Its recommendations remain candidates.

## Scope and direct answer

The target is now a NAS read by the Kuro server, a dedicated Linux computer in the living room, USB to a DDC, I2S over HDMI to a Denafrips Terminator DAC, and then the analog system. The user called the DDC maker "Dynafripp," but that name and the maker remain unverified. The exact computer, Linux release, DDC model, Terminator revision, USB mode, and I2S pin map remain unknown. The current Aurender system is a listening reference, not a protocol requirement.

Use Rust for Kuro's eventual catalog, control, and file service if the team accepts Rust after the prototype. Keep the renderer engine out of that service. Rust's lack of a garbage collector is useful for predictable resource accounting and failure isolation, but it does not improve DAC jitter by itself. [Rust ownership provides memory safety without a GC](https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html).

For the first renderer proof, use an unmodified MPD process on the living-room computer. Put a small Kuro renderer agent in front of it. The agent downloads and verifies whole source files into an application-owned local cache, then controls MPD over a Unix socket. MPD can add arbitrary absolute local files through a local socket, and its input cache can prefetch queued songs if direct HTTP playback is later tested. [MPD protocol](https://mpd.readthedocs.io/en/stable/protocol.html) and [MPD input cache](https://mpd.readthedocs.io/en/stable/user.html#configuring-the-input-cache).

Do not write a SlimProto server or an ALSA playback loop. If a future endpoint requires Squeezelite, run Lyrion Music Server and integrate through its control API. If MPD cannot meet the measured format and gapless contract, test a GStreamer renderer through its maintained Rust bindings before considering custom real-time code.

## Recommended signal and control path

```text
NAS mounted read-only on Kuro server
  -> Kuro byte service: original file, length, SHA-256, byte ranges
  -> renderer agent: .part download, verify, atomic cache commit
  -> MPD queue adapter: current and next staged file only
  -> MPD decoder and ALSA hw output
  -> USB DDC
  -> I2S-over-HDMI clock, word-select, and sample data
  -> Terminator DAC

Kuro catalog and queue -> renderer-agent control -> MPD Unix socket
```

This path is deliberately store-and-play. Once the renderer has verified a complete file, NAS latency, Ethernet packet timing, Kuro scheduling, and Kuro GC policy are outside the active playback path. They can delay preparation of a later track, but they cannot modulate samples already staged on the renderer.

Stage at least the current and next tracks before starting an album. Keep Kuro's queue authoritative. Mirror only the short playback window into MPD, use MPD song IDs for changes, and reject stale MPD events with a Kuro playback-session revision. This limits the second queue to an adapter state instead of creating a second durable authority.

## What the server language can and cannot change

| Layer | Failure that matters | Relation to sound |
| --- | --- | --- |
| NAS and byte service | read error, changed file during transfer, truncation, wrong range | Prevents or delays a verified stage. A matching whole-file digest proves byte equality only. |
| Kuro runtime | delayed request, blocked worker, process crash, memory exhaustion | Can miss prefetch deadlines. With a completed local stage it is disconnected from sample timing. |
| Renderer engine and ALSA | conversion, software gain, bad gapless transition, xrun | Can change samples or create clicks, silence, or a dropout. ALSA documents that late feeding causes an underrun. [ALSA PCM interface](https://www.alsa-project.org/alsa-doc/alsa-lib/pcm.html). |
| USB DDC and I2S | clock mode, FIFO behavior, clock phase noise, pin-map mismatch | This is the converter-side timing boundary. It must be established from the exact hardware manuals and measurements. |
| DAC analog output | converter response, noise, jitter-induced sidebands | This is where an analog SQ or audibility claim must be measured and listened for. |

General-purpose Linux, Tokio, Go, and normal C or C++ threads provide no hard real-time guarantee here. That does not matter for Kuro's staged file service. It matters if Kuro is allowed to feed small PCM buffers directly to the device, which this design avoids.

## Language comparison for the bounded Kuro server

| Choice | File and control service | Runtime and scheduling | Existing engine integration | Cost and verdict |
| --- | --- | --- | --- | --- |
| Rust | Strong fit. Model media IDs, transfer digests, queue occurrences, and playback revisions as distinct types. Axum publishes a static-file example and `tower-http` supplies range-aware file services. [Axum example](https://github.com/tokio-rs/axum/blob/main/examples/static-file-server/src/main.rs), [`ServeFile`](https://docs.rs/tower-http/latest/tower_http/services/struct.ServeFile.html) | No tracing GC. Tokio tasks use cooperative scheduling, so blocking NAS reads or hashes must use `spawn_blocking` or a bounded dedicated pool. [Tokio tasks](https://docs.rs/tokio/latest/tokio/task/) | MPD and LMS are process protocols. GStreamer has project-maintained safe Rust bindings. [gstreamer-rs](https://github.com/GStreamer/gstreamer-rs) | Recommended for Kuro. It minimizes memory-unsafety risk without claiming real-time or audible superiority. More crates and slower initial delivery than Go must be measured. |
| Go | Excellent fit. The standard library's `http.ServeContent` handles ranges, validators, and seekable files. [Go `net/http`](https://pkg.go.dev/net/http#ServeContent) | The runtime schedules goroutines and includes a concurrent GC with brief stop-the-world transitions and other documented latency sources. [Go GC guide](https://go.dev/doc/gc-guide) | Process protocols are easy. GStreamer is available through the separate `go-gst` binding and cgo. [GStreamer bindings list](https://gstreamer.freedesktop.org/bindings/) | Best fallback if implementation speed and a small dependency graph dominate. GC pauses are an observable service-tail risk, not a DAC-jitter argument. Whole-file staging makes them irrelevant during playback. |
| C or C++ | Capable, but HTTP, request validation, cancellation, and safe path handling demand more application code or libraries. | Direct OS threads and explicit allocation avoid a managed runtime. They still share Linux scheduler and I/O delays. | Native GStreamer API is C; a C++ binding exists. MPD itself is C and C++, but it is a daemon rather than an embeddable playback library. [GStreamer Linux build docs](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html) | Use only if Kuro must embed GStreamer at its C API boundary or maintainers have much stronger C++ expertise. It provides no SQ advantage for an out-of-process renderer and raises memory and concurrency review cost. |

The decisive Rust advantage is domain and memory safety in a long-lived service. The decisive Go advantage is a complete HTTP server in the standard library. Neither language changes decoded samples when both implementations deliver the same verified file.

## Existing renderer engines

| Engine | Maintained evidence and transport | Fit for Kuro | Material limits |
| --- | --- | --- | --- |
| MPD | The stable documentation build identifies itself as 0.24.15. The official 0.24 download index has the 0.24.15 source archive and signature dated 2026-08-27, and upstream has a `v0.24.15` tag. The separate `master` branch declares unreleased 0.25 and C++23. [Stable docs](https://mpd.readthedocs.io/en/stable/), [0.24 downloads](https://www.musicpd.org/download/mpd/0.24/), [`master` source](https://github.com/MusicPlayerDaemon/MPD) | Best first renderer. Run it only on the living-room computer and control it through a permissioned Unix socket. Feed verified local cache paths. | Its queue and state must stay adapter-local. Its HTTP output is an encoded broadcast stream that recommends a fixed format, so it is the wrong path for untouched source delivery. [HTTP output](https://mpd.readthedocs.io/en/stable/plugins.html#httpd) |
| Squeezelite with LMS | Squeezelite 2.0.x is active and advertises USB DAC output, large stream and PCM buffers, selectable rates, an output-thread real-time priority, optional resampling, and software or hardware volume. It receives control from LMS and pulls media from it. [Squeezelite manual](https://ralph-irving.github.io/squeezelite.html) | A valid appliance-style alternative if hardware support or mature multiroom behavior makes the LMS ecosystem desirable. | SlimProto carries encoded formats or PCM, buffering, gain, transitions, and sync controls. Its own documentation warns that lengths are stale and names the Perl source as authoritative. Do not reimplement it. [SlimProto reference](https://lyrion.org/reference/slimproto-protocol/) |
| GStreamer | The local baseline has GStreamer 1.28.6. A typical pipeline prefers the audio sink's clock, and `GstAudioBaseSink` schedules samples through a ring buffer. [GStreamer clocks](https://gstreamer.freedesktop.org/documentation/application-development/advanced/clocks.html), [audio-sink design](https://gstreamer.freedesktop.org/documentation/additional/design/audiosinks.html) | Second renderer experiment if MPD fails. Use `playbin3` or an explicit decode pipeline, a real ALSA sink, and the Rust bindings. | GStreamer gives mechanisms, not a gapless or bit-perfect result. Record the selected clock, negotiated caps, every converter or resampler, queue levels, and xruns. An `identity` element can count bytes and check timestamps without changing buffers. [identity](https://gstreamer.freedesktop.org/documentation/coreelements/identity.html) |

MPD's built-in HTTP output decodes and then invokes an encoder. Its source calls `OpenEncoder` and `EncodeAndPlay`, so even FLAC output is a new representation rather than the untouched source file. [MPD HTTP output source](https://github.com/MusicPlayerDaemon/MPD/blob/master/src/output/plugins/httpd/HttpdOutputPlugin.cxx). Kuro should serve source bytes itself and let the endpoint decode.

Squeezelite's default software volume and optional resampler are transformations. If that path is tested, fix digital gain at unity or use an identified downstream volume control, omit `-u` and `-R`, publish supported device rates with `-r`, and capture its effective ALSA format. Do not infer those settings from option names. Verify the exact command line and output logs.

## Source bytes, lossless decode, and PCM are different proofs

Untouched file transfer means that the complete staged file has the same byte length and SHA-256 as the file Kuro opened on the read-only NAS mount. It preserves audio frames, tags, artwork, padding, and every other byte. It does not prove what the renderer does after opening the file.

Lossless decode means that a codec reconstructs its encoded PCM samples. FLAC is formally specified as lossless, and its `STREAMINFO` may contain an MD5 of the unencoded interleaved samples. That MD5 checks decoded audio, not the whole file or its metadata. [RFC 9639](https://datatracker.ietf.org/doc/html/rfc9639).

Verbatim PCM means that decoded sample words reach a named checkpoint without resampling, gain, channel remapping, clipping, dithering, or format truncation. A PCM digest is meaningful only with a canonical byte order, signedness, interleaving, channel order, sample rate, valid-bit depth, and treatment of codec delay or padding. A source-file digest cannot prove this.

For MPD, start with no global output format, crossfade off, ReplayGain off, volume normalization off, and no software mixer. Select the exact ALSA `hw:` device only after enumeration. MPD says that it attempts bit-perfect playback by default but may choose a nearby format when hardware rejects the source format. Its own checklist requires verbose conversion logs and the active ALSA `hw_params`. [MPD bit-perfect checklist](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback).

Treat "no `output: converting` log line" and matching `/proc/asound/.../hw_params` as digital-path evidence. Neither observation proves the USB DDC's output clock quality or the DAC's analog result.

## Reversible transport-integrity proof

Build `kuro-transport-probe` as a small Rust workspace outside the product modules. It must have no decoder and no ALSA access. Use Axum plus `tower-http::ServeFile`, pin every crate, and expose only fixture media IDs rather than caller-supplied paths.

1. Generate two tiny FLAC fixtures and one larger arbitrary binary fixture under a disposable directory. Mount or chmod that fixture tree read-only for the server process.
2. At scan time, record media ID, byte length, SHA-256, and a source-stat token. Keep the digest a transfer property. Do not turn it into Kuro's unresolved catalog identity.
3. Serve `GET` and one byte-range resume route with `Content-Length`, `Accept-Ranges`, a strong digest ETag, and no `Content-Encoding`. Open only the resolved file below the configured source root.
4. On the renderer side, stream to a `.part` file while hashing. Require the manifest length and SHA-256. Rename atomically to a digest-named cache file only after both match.
5. Queue the verified absolute path into MPD through its Unix socket. Stage the next file before starting the current one. Never give MPD the NAS path or a live Kuro HTTP stream in this proof.
6. Record source hash before and after, served-byte count, range offsets, renderer hash, stage duration, retries, Kuro CPU and memory, and whether the source stat changed while open.
7. Exercise clean transfer, killed connection and resume, one flipped cached byte, truncated response, a source mutation attempt, simultaneous catalog load, and Kuro termination after stage completion.
8. Pass only if both fixture source hashes remain unchanged, each accepted cache file matches its manifest, every corrupt or partial file is rejected, MPD plays after Kuro is stopped, and no `.part` file enters the MPD queue.

This proves the Kuro-to-renderer file boundary and its independence from playback. It does not prove gapless output, decoded PCM equality, USB integrity, jitter, or audibility. Add those as separate experiments rather than stretching the checksum claim.

## Clock and jitter interpretation for the stated hardware chain

USB packet arrival time is not automatically the DAC sample clock. USB Audio defines asynchronous endpoints as paced by a free-running device clock or a clock external to USB, rather than USB start-of-frame timing. Confirm that the exact DDC exposes an asynchronous playback endpoint before applying this model. [USB Audio class specification library](https://www.usb.org/documents?search=Audio+2.0).

After USB, I2S carries serial clock, word select, and serial data. The device acting as I2S controller generates the clock signals, and the target uses them to latch data. [NXP I2S specification](https://www.nxp.com/docs/en/user-manual/UM11732.pdf). The exact DDC mode therefore matters more to converter timing than whether Kuro used Rust or Go several buffers upstream.

Denafrips says that its DDC and DAC products use an adaptive FIFO and reclocking, and it warns that source and DAC I2S pinouts must match. This is vendor documentation, not a measured result for the user's unnamed DDC. [Denafrips support](https://www.denafrips.com/support/1000). Record the model, firmware, clock mode, I2S pin map, sample-rate family behavior, and whether the DDC or DAC is I2S controller.

Jitter audibility has no single threshold independent of spectrum, signal, and converter. A controlled 2005 study reported random-jitter detection thresholds of several hundred nanoseconds for trained listeners in their preferred conditions. That result does not set a pass line for this hardware or for correlated jitter. [Ashihara et al., DOI 10.1250/ast.26.50](https://www.jstage.jst.go.jp/article/ast/26/1/26_1_50/_article).

To claim an SQ improvement, measure the Terminator's analog output with a declared stimulus and analyzer, then run a level-matched, time-aligned, blinded comparison. A network trace, file hash, process priority, or subjective sighted comparison cannot substitute for that evidence.

## Dependency, version, and licensing record

- Rust 1.98.0 is installed locally. Axum 0.8.9 and Tokio 1.53.1 are current in their upstream pages, but no Kuro Cargo lockfile or clean build exists. Pin the experiment and retain its SBOM.
- Go 1.27.0 is installed locally. A Go probe could use only the standard library. The Go source license is BSD-style. [Go license](https://github.com/golang/go/blob/master/LICENSE).
- MPD's stable documentation, official 0.24 download index, and `v0.24.15` tag agree on 0.24.15 as the released stable line observed on 2026-09-06. The download index dates its archive and signature to 2026-08-27. The `master` manifest and `NEWS` instead describe unreleased 0.25, so they are development metadata rather than the stable documentation version. Pin the renderer package and inspect its compiled decoder, input, output, resampler, and library list. MPD source files identify GPL-2.0-or-later. [Stable docs](https://mpd.readthedocs.io/en/stable/), [0.24 downloads](https://www.musicpd.org/download/mpd/0.24/), [`v0.24.15` tag](https://github.com/MusicPlayerDaemon/MPD/tree/v0.24.15), and [HTTP source header](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.15/src/output/plugins/httpd/HttpdOutputPlugin.cxx).
- Squeezelite states GPL-3.0-or-later plus an OpenSSL permission and separate notices for optional bundled code. LMS says its Perl code is GPLv2 while bundled modules and ancillary material have separate terms. [Squeezelite license](https://github.com/ralph-irving/squeezelite/blob/master/LICENSE.txt) and [LMS license notice](https://github.com/LMS-Community/slimserver/blob/public/9.0/License.txt).
- GStreamer core uses LGPL-2.1-or-later, while plugin dependencies can change the effective license. Upstream directs distributors to inspect each plugin. The Rust bindings are MIT or Apache-2.0. [GStreamer licensing](https://gstreamer.freedesktop.org/documentation/frequently-asked-questions/licensing.html) and [Rust bindings](https://github.com/GStreamer/gstreamer-rs).

These are inventory facts, not legal conclusions and not a Kuro license choice. The exact delivered artifact, build flags, codec libraries, optional plugins, firmware, notices, and distribution method remain adoption inputs.

## Open facts that can change the choice

- Exact DDC and Terminator models, revisions, firmware, USB descriptors, supported PCM formats, I2S mode, and pin map.
- Living-room computer hardware, Linux distribution, USB controller topology, local storage budget, and whether it runs any other workload.
- Accepted source formats, maximum sample rate and bit depth, gapless corpus, volume location, and whether DSP or resampling is ever allowed.
- LAN throughput and outage profile, largest track, desired start latency, and cache-retention budget.
- Whether Kuro must support one renderer only or future independent zones. Multiroom synchronization is a separate clock-distribution problem.
- Exact MPD, GStreamer, Squeezelite, or LMS artifact and dependency closure chosen for testing.

Research stopped after each consequential claim had an official specification, upstream manual, maintained source, license notice, or a stated evidence gap. Another broad search would not decide the hardware clock mode or audibility without the exact devices and measurements.
