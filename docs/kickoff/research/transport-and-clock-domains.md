# Kuro network transport and clock-domain research

Status: primary-source research input, 2026-09-06. The recommendations in this report are candidates for synthesis, not an arena decision or an adopted Kuro architecture.

Date: 2026-09-06. Scope: the proposed first listening path is NAS -> Kuro server -> a dedicated Linux renderer computer in the living room -> USB -> the user's DDC -> I2S carried on an HDMI cable -> Denafrips Terminator DAC. The user called the DDC maker "Dynafripp," but that name and the maker remain unverified. The exact DDC model, Terminator revision, USB synchronization type, supported rates, and I2S pin map remain unknown. The Aurender is a listening reference, not a required Kuro endpoint.

## Candidate recommendation in one paragraph

Build the first SQ prototype around a renderer-local audio process whose output follows the ALSA/USB audio device's pace. Compare two open implementations on the same living-room computer: MPD controlled by a thin Kuro renderer agent, and LMS plus Squeezelite as a reference implementation. Add an optional content-addressed local staging mode to MPD so the same output pipeline can play with no live file traffic. Do not choose a protocol by audiophile reputation. Choose after the exact USB/DDC clock mode is known and after matched tests show bit path, actual ALSA format, xruns, transition integrity, and the DAC's analog result. Keep UPnP/OpenHome as a compatibility adapter, not the first SQ baseline. Defer timed multi-room transports such as Sendspin or Snapcast because they deliberately correct clock drift in the sample stream. Temporarily putting the Kuro server beside the DDC and connecting it by USB can isolate the network hop, but it is a diagnostic and must not collapse the product's separate-renderer architecture.

## What is established, and what is inferred

### Established by specifications or source

* TCP exposes a reliable, ordered byte stream. Network packet timing can vary even when the recovered file bytes do not. See the IETF's [TCP specification, RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html) and RTP's separate definition of [interarrival jitter, RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.html).
* USB Audio has explicit clock domains. An asynchronous isochronous endpoint consumes data at a rate locked to an external or free-running internal clock and cannot lock to USB start-of-frame. Synchronous and adaptive endpoints behave differently. See USB-IF's current [USB Audio 2.0 specification, sections 3.10 and 3.11](https://www.usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf).
* Sampling-clock jitter at the converter can create signal-dependent error. Analog Devices gives the idealized limit `SNR = 20 log10(1/(2*pi*f*tj))` and an FFT measurement method in [MT-007](https://www.analog.com/media/en/training-seminars/tutorials/MT-007.pdf). AES treats converter jitter susceptibility, spectra, and PLL transfer as separate measurements in [AES-12id-2020](https://aes.org/publications/standards-store/?id=57).
* Denafrips says its DDC/DAC products use an adaptive FIFO and reclocking, and warns that its HDMI-shaped I2S port is not HDMI AV and has no industry-standard pinout. That is a manufacturer claim, not a measurement of this user's units. See [Denafrips support: FIFO and I2S](https://www.denafrips.com/support/1000).

### Engineering inference, to be tested on this chain

* With enough buffering and no underrun, Ethernet packet arrival time does not directly set the D/A conversion edge. The last clock domain and any clock recovery or reclocking between renderer, DDC, and DAC matter. This follows from the TCP and USB clock models, but does not prove that two streamers have identical analog output.
* A different streamer can still change the result through sample processing, output format, clock implementation, USB behavior, power or ground coupling, RF activity, or an endpoint bug. The user's reported streamer differences and past Roon result are valid observations, but the available evidence does not identify their cause.
* Local staging should leave decoded samples unchanged while reducing network activity and underflow exposure. If staging changes a repeatable analog measurement or blinded result on the otherwise identical renderer, the next investigation is physical coupling or scheduling, not a claim that HTTP changed the file.
* "Bit-perfect" is necessary for isolating transport effects, but it does not measure conversion-clock jitter or analog noise. A PCM hash and ALSA format log cannot replace an analog capture at the DAC output.

## Where the clocks are likely to live

```text
NAS storage clock        irrelevant to sample timing once bytes are buffered
        |
Kuro HTTP/TCP delivery   variable packet arrival, integrity and underflow domain
        |
renderer decode buffer   PCM content and transform boundary
        |
ALSA + USB host buffer   paced by the audio device/driver relationship
        |
USB DDC                  possible clock master if its descriptor says asynchronous
        |
I2S BCLK/LRCLK/MCLK      DDC supplies serial audio timing
        |
Terminator FIFO/reclock  possible new clock domain; exact revision/config required
        |
DAC conversion clock     timing that directly reaches analog conversion
```

The word "possible" is intentional. Read the real USB descriptors and manuals before assigning clock ownership. The USB-IF spec permits asynchronous, adaptive, and synchronous endpoints. Denafrips' general support page cannot establish the behavior of an unidentified DDC and Terminator revision.

## Transport comparison

| Path | Data and queue ownership | Formats, buffering, and rate behavior | Gapless and SQ-relevant constraints | Fit for Kuro now |
| --- | --- | --- | --- | --- |
| Kuro agent + MPD | Kuro keeps the durable queue. A small local agent projects a short generation-tagged window into MPD over its Unix socket. MPD's [`addid` command](https://mpd.readthedocs.io/en/stable/protocol.html#the-queue) accepts a file or URL, so it can pull Kuro HTTP URLs or play staged local files. | MPD has a [4 MiB internal audio buffer](https://mpd.readthedocs.io/en/stable/user.html#buffer-settings) by default and can output directly to ALSA `hw`. It tries native format first but will convert if hardware rejects it. Its own [bit-perfect checklist](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback) requires `hw`, no software volume, no ReplayGain, no forced format, plus log and `/proc/asound/.../hw_params` verification. | MPD supports a continuous queue, but same-rate and rate-change boundaries still need capture tests. Native-rate changes may reopen/relock the chain. A staged file makes a clean live-network versus quiet-network experiment possible. | Best first architecture. It is small, observable, and does not make MPD's catalog authoritative. MPD queue IDs are transient across restart according to the protocol docs, so Kuro must reconcile by its own generation and media IDs. |
| LMS + Squeezelite | LMS owns the player queue and sends SlimProto control. Squeezelite opens a separate TCP stream connection to the supplied server address and sends the supplied request header, so "server-push PCM" is incomplete shorthand. LMS may direct-stream or transcode; see the [LMS protocol-handler notes](https://github.com/LMS-Community/slimserver/blob/d1d0a683d8301c04e64be0425e0aec51fc4e8397/DEVELOPERS.md) and Squeezelite's [`strm`/stream connection code](https://github.com/ralph-irving/squeezelite/blob/c7c4248ddd70e47dbfeba0bf4a8a7ec08d8a995c/slimproto.c). | Current Squeezelite defaults to 2048 KiB stream and 3445 KiB output buffers, supports multiple device rates, and makes resampling optional. See its [2026 man page](https://github.com/ralph-irving/squeezelite/blob/c7c4248ddd70e47dbfeba0bf4a8a7ec08d8a995c/doc/squeezelite.1). Its ALSA code disables resampling for `hw`, but if a requested rate fails it retries as `plughw` with resampling. See [`output_alsa.c`](https://github.com/ralph-irving/squeezelite/blob/c7c4248ddd70e47dbfeba0bf4a8a7ec08d8a995c/output_alsa.c). Software gain is the default when no hardware mixer is selected, so unity gain must be proven. | It decodes ahead into one output buffer and marks the next track inside that buffer. This is a credible homogeneous-rate gapless path, not a guarantee for this DDC or rate changes. SlimProto synchronization can insert silence or skip frames for grouped playback. | Excellent reference and fast prototype. Less attractive as Kuro's final core because LMS becomes a second queue/catalog authority. Implementing a new SlimProto server from source behavior would add protocol and GPL integration work without first proving SQ. |
| UPnP AV or DLNA-profiled renderer | Kuro can serve media, act as control point, and give a renderer an HTTP URI. The renderer performs HTTP GET and decides whether to fetch immediately or on Play. See UPnP Forum [AVTransport:3 Annex A](https://upnp.org/specs/av/UPnP-av-AVTransport-v3-Service.pdf). | The renderer advertises protocol/container capabilities. DLNA adds profile and byte/time-range fields to `protocolInfo`; it does not define the device's converter clock. See OCF's [UPnP AV and DLNA tutorial](https://openconnectivity.org/wp-content/uploads/2015/11/UPnP_AV_tutorial_July2014.pdf). The decoder, buffer, DSP, and physical output remain implementation-specific. A generic "HTTP streamer" does not imply every AVTransport action or native-rate output. | `SetNextAVTransportURI` enables prefetch for a seamless transition, but the action is allowed, not required. The spec does not promise zero missing or repeated samples. See [AVTransport:3 action table and section 5.4.3](https://upnp.org/specs/av/UPnP-av-AVTransport-v3-Service.pdf). | Useful compatibility adapter after an actual target advertises and passes a capability probe. Too much endpoint variability for the first controlled SQ baseline. |
| OpenHome Playlist renderer | The renderer owns a device-resident queue of URI and metadata entries. The service exposes Insert, Delete, Read, IdArray, TracksMax, and ProtocolInfo. See the reference [Playlist1 service](https://github.com/openhome/ohPipeline/blob/942497b74f9c30d6288a56ac73fb18c738a14c3c/OpenHome/Av/ServiceXml/OpenHome/Playlist1.xml). | The OpenHome reference pipeline has separate HTTP, buffering, codec, decoded-audio, and driver stages. Its current [codec source](https://github.com/openhome/ohPipeline/tree/942497b74f9c30d6288a56ac73fb18c738a14c3c/OpenHome/Media/Codec) includes FLAC, ALAC, WAV, AIFF, AAC, MP3, Opus, Vorbis, PCM, and DSD handlers. That does not promise the same build or rate limits in every branded renderer. | OpenHome's published architecture targets managed on-device playlists and gapless playback. See the official [OpenHome platform description](http://openhome.org/pages/about/platform.html). This is stronger queue behavior than baseline UPnP, but only on endpoints that advertise the OpenHome services. Kuro must treat the endpoint queue as a projection or reconcile two authorities. | Plausible for compatible products and for a renderer adapter later. It adds no advantage over direct MPD control on the first dedicated Linux renderer. |
| Sendspin or Snapcast | Server produces timed PCM/FLAC/Opus chunks; clients buffer, decode, and schedule against a server clock. | Sendspin negotiates codec/rate/depth per player and may switch per track. Its current spec requires drift tracking. Snapcast similarly time-stamps chunks over TCP. | Both permit or prescribe sample insertion/deletion or asynchronous resampling to stay synchronized. Sendspin says insertion/deletion is bit-exact except at correction moments. See the current [Sendspin playback synchronization rules](https://github.com/Sendspin/spec/blob/8c9577ea8719ad082d051ec13cc73ef15ed68948/README.md#playback-synchronization) and [Snapcast design](https://github.com/badaix/snapcast#how-does-it-work). | Good later for multi-room. For one SQ-first endpoint, their clock-drift corrections add a variable the first prototype does not need. The Sendspin spec repository inspected at this commit has no explicit license file, so public specification should not be mistaken for cleared implementation terms. |

## RAAT boundary

Roon's own description says RAAT performs decoding and expensive DSP on the server, lets the audio device own the audio clock, targets about 1 ms multi-room synchronization, and ships an SDK to hardware makers. See Roon's [RAAT design goals](https://help.roonlabs.com/portal/en/kb/articles/raat) and [Roon Ready program](https://help.roonlabs.com/portal/en/kb/articles/roon-ready). Roon also says its signal-path view cannot identify every step after handoff to hardware. See [Signal Path](https://help.roonlabs.com/portal/en/kb/articles/signal-path).

No public RAAT audio protocol specification or reusable server/endpoint implementation was found in Roon's official public repositories. Its public `node-roon-api-transport` controls zones; it is not the RAAT audio transport. RAAT therefore cannot be Kuro's open transport base without a separate vendor relationship and license. The user's earlier Roon result does not establish that device-clock ownership, server decoding, or network delivery caused that result.

## Candidate Kuro seam

Keep one transport-neutral `PlaybackPlan` from Kuro to a renderer adapter:

* Kuro queue generation, ordered catalog-reference IDs, current offset, and a short look-ahead window.
* Source URL or staged content hash, byte length, source codec/container, channels, bit depth, sample rate, and allowed byte ranges.
* An explicit transform policy. Start with `native-only`: no DSP, ReplayGain, crossfade, software volume, rate conversion, or channel conversion. Reject unsupported formats instead of silently adapting them.
* Expected transition class: homogeneous gapless, sample-rate change, clock-family change, or unsupported.

Require the renderer to report an `ActualSignalPath` for every start and transition:

* decoder name/version and decoded PCM format;
* requested and actual ALSA device, access mode, format, rate, channels, period, and buffer;
* whether any gain, filter, channel conversion, format conversion, or resampler ran;
* USB device identity and synchronization type when discoverable;
* buffer low-water marks, xruns, reconnects, late starts, device reopen/relock, and samples inserted, dropped, or duplicated.

This report is more valuable than a "bit-perfect" badge. MPD's documentation is unusually candid: real-time scheduling reduces xrun probability and does not itself improve audio quality. See [MPD buffer and real-time notes](https://mpd.readthedocs.io/en/stable/user.html#buffer-settings).

## Decisive probes before choosing

1. **Inventory the real clock path.** On the renderer, record `lsusb -v`, `/proc/asound/cards`, `/proc/asound/card*/stream*`, `aplay -l`, and `aplay -D hw:X,Y --dump-hw-params`. Confirm the DDC model, USB synchronization descriptor, native rates/depths, current I2S pin configuration, Terminator revision, and whether the DDC or DAC accepts an external clock. Do not infer these from the brand.
2. **Build a native-format matrix.** Play generated, licensed PCM fixtures at every relevant rate and depth through MPD and Squeezelite. Lock both to the same `hw` device, unity or no mixer, no ReplayGain/DSP/resampler. Save application logs and live ALSA `hw_params`. A rejected format is a useful result; silent fallback fails the first policy.
3. **Prove decoded samples before hardware.** Add a renderer test sink that hashes or stores the exact interleaved PCM delivered to the ALSA boundary. Compare MPD and Squeezelite against a trusted offline decode. This detects sample processing but makes no jitter claim.
4. **Measure transitions.** Use complementary track pairs whose concatenation is a continuous waveform. Capture DAC analog output for same-rate boundaries, 44.1-family changes, 48-family changes, and family crossings. Count added silence, missing/duplicated samples, relock transients, and time to stable output. Keep homogeneous gapless as a separate guarantee from rate-changing transitions.
5. **Separate live network traffic from endpoint implementation.** In the MPD path, compare Kuro HTTP streaming with content-addressed local staging on the same computer. After staging the whole test sequence, stop file traffic or disconnect the renderer network after control setup. Keep software, USB port, DDC, cable, DAC settings, level, and track order identical. Record Ethernet activity, CPU wakeups, xruns, USB/ALSA parameters, and analog output.
6. **Compare implementations on one box.** Randomize MPD versus Squeezelite trials, level-match at the analog output, and capture each run. First compare decoded PCM and negotiated format. Then compare DAC-output spectra, noise, and null residual with a suitable ADC or audio analyzer. A listening ABX can supplement the capture. Neither result alone assigns a cause.
7. **Stress buffering separately.** Apply controlled delay, jitter, loss, and server stalls to the file link. Find each path's underflow boundary and inspect xruns or discontinuities. Do not conflate tolerance to a bad network with steady-state conversion quality.

Stop the architecture comparison when one path passes the native matrix and transition contract, produces no unexplained sample transforms, survives the accepted network envelope, and has no repeatable analog or blinded disadvantage on the actual DDC/DAC chain. Until then, retain both MPD and Squeezelite adapters behind the same Kuro plan and telemetry contract.

## Source and research limits

Primary sources inspected: USB-IF Audio 2.0 April 2025; UPnP AVTransport:3; IETF TCP/RTP clock documents; current MPD documentation and source; LMS public/9.2 and Squeezelite source at the commits linked above; OpenHome service/reference pipeline; Sendspin and Snapcast specifications/source; Roon's official RAAT pages; Denafrips support; AES and converter measurement references. Repository heads were checked on 2026-09-06. No user media, NAS, computer, DDC, DAC, or Aurender was accessed. Public documents describe mechanisms and capabilities. They do not rank protocol sound quality or measure the user's chain.
