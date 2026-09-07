# Sound-quality pivot: grounded architecture constraints

## Baseline and authority

The committed baseline is still documentation-only. There is no Kuro application or measured audio behavior. The fuller repository grounding is in [initial repository grounding](initial-grounding.md).

The current contract arrived in commit `f6d65a1` and merged through PR #1 as `8b1b956`. PR #1 says the earlier plan mixed reference inventory with product commitments, so two interviews replaced it with 40 scoped decisions. It also says every product scenario remains future evidence and no Kuro software or product test exists. This is direct evidence that local-only audio, shared output, and no LAN listener were product-scope decisions, not conclusions from transport, jitter, or listening tests.

The new user instruction is now the highest product authority: sound quality is paramount, and the working target is `NAS -> Kuro server -> separate Linux living-room renderer computer -> USB -> DDC -> I2S over HDMI -> Terminator DAC`. The user's reference setup is Aurender local music controlled by Conductor 5, then DDC and Terminator DAC over I2S/HDMI. Kuro is intended to replace the streamer role, not reproduce the Aurender software or hardware. I refer to this instruction below as `USER-SQ-2026-09-06`; that is a session provenance label, not a repository KD identifier. Exact hardware revisions and input specifications remain unknown. The next documentation change should give this instruction a real KD identifier and amend the affected KD, KB, KV, and roadmap entries. KD-038 already assigns scope acceptance to the user and requires explicit arbitration rather than silent scope reduction (`.scratch/cadrage-kuro/issues/03-reviser-cadrage-second-entretien.md:94-96`).

## Old versus new

| Area | Prior contract and source | New authority | Grounded status |
| --- | --- | --- | --- |
| Primary playback path | U-M1 uses local shared system output. `KD-001`, `KD-020`, `KD-039`; `docs/cadrage-courant.md:39-41` | Core path uses a separate Linux living-room computer as renderer, then USB DDC and I2S/HDMI into the Terminator DAC. `USER-SQ-2026-09-06` | Direct contradiction. Shared output on the Kuro server cannot remain the only U-M1 target. Whether server-local playback remains a secondary path is unknown. |
| Network role | U-M1 does not listen on the LAN; control is restricted to the local session user. `KD-022`; `docs/cadrage-courant.md:55-57` | Kuro server and living-room renderer computer must exchange control and audio across the LAN. `USER-SQ-2026-09-06` | Direct contradiction if the selected transport requires an inbound server, renderer listener, or discovery traffic. Preserve least access as a security goal, then restate it per chosen protocol. Do not infer a general LAN control API. |
| NAS role | Kuro consumes an already-mounted NAS path and does not manage NAS protocol, credentials, or mounting. `KD-005`; ticket 01 lines 32-34 | NAS remains the upstream music source. `USER-SQ-2026-09-06` | Compatible. Network input storage and network audio output are separate concerns. No reason yet to make Kuro mount the NAS itself. |
| Network audio scope | Multiroom and network endpoints were deferred. `KD-007`, `KB-004`; ticket 01 lines 40-42 and `docs/backlog.md:12` | One separate Linux renderer computer is part of the core path. `USER-SQ-2026-09-06` | Partially readmits KB-004 for one renderer and one listening path. It does not admit synchronized rooms, several independent zones, remote access, or generic endpoint support. |
| Audio priority | Gapless on a selected stereo PCM corpus is required; exclusive mode, bit-perfect, hardware volume, and DSP were deferred. `KD-014`, `KD-020`, `KD-039`, `KB-003`; `docs/backlog.md:11,31` | Sound quality is paramount; deep transport and jitter research is required. `USER-SQ-2026-09-06` | Reopens transport, bit transparency, clocking, resampling, buffering, and volume-path evidence before language or stack adoption. It does not by itself add DSD, multichannel, DSP, or universal format support. |
| Failure behavior | Output loss stops playback with no silent fallback; return does not auto-resume. `KD-011`, `KD-039`; `docs/validation.md:37-43` | The renderer computer, USB DDC, I2S link, and DAC form the downstream path. `USER-SQ-2026-09-06` | Preserve the observable stop and no-auto-resume rule unless explicitly changed. Redefine "output loss" across the server-renderer session and renderer audio-device states. |
| Offline operation | All U-M1 functions work indefinitely without Internet; NAS needs only the LAN. `KD-009`, `KD-024`; `docs/cadrage-courant.md:55` | Core playback uses local network equipment. `USER-SQ-2026-09-06` | Compatible. Do not let transport selection introduce mandatory cloud accounts or Internet validation. |
| Mobile and remote control | Mobile remains a conditional U-M4 study after desktop stability. `KD-031`; `docs/roadmap.md:27-37` | No mobile requirement was added. | Unchanged. A LAN renderer computer is not authorization for phone playback, remote access, downloads, or a mobile controller. |
| Roon compatibility | Roon is comparison material only; no parity or access to private mechanisms is assumed. `KD-032`; `README.md:30` | The requested topology resembles server-to-renderer systems. | Unchanged. Do not assume RAAT availability, compatibility, or a Roon clone. Evaluate only transports Kuro can lawfully implement and validate. |

## Contracts to preserve through the pivot

- Sources remain read-only. NAS absence, scan cancellation, and invalid files must not delete durable catalog references. `KD-010`, `KD-016`, `KD-021`, `KD-029`, `KD-036`.
- Catalog identity still follows configured source and relative path rules. Never merge silently by filename, tags, or assumed fingerprint. `KD-013`, `KD-028`, `KB-022`.
- Queue, playlists, stopped-state restart, backup content, and failure-atomic restore remain durable product behavior. `KD-004`, `KD-006`, `KD-012`, `KD-018`, `KD-030`, `KD-034`, `KD-035`.
- No account, mandatory telemetry, or cloud check is introduced. Diagnostics remain redacted. `KD-009`, `KD-022`, `KD-024`.
- Scale remains about 20,000 albums and 3 TB. The new audio priority does not silently lower that target. `KD-001`, `KD-015`, `KD-038`.

## Research gates before choosing architecture or language

The transport study should compare lawful, implementable paths between the Kuro server and one Linux renderer computer. It must trace the full chain through the renderer's audio stack, USB output, DDC, I2S-over-HDMI link, and Terminator DAC while preserving unknown exact device revisions. It must distinguish network packet timing and buffer underruns from USB transfer behavior and sample-clock behavior at the DAC, identify where buffering and clock recovery occur, detect resampling or format conversion, test gapless transitions, state volume semantics, and define failure and reconnect behavior. "Jitter" is not yet a measurable Kuro requirement; the study must name the mechanism, observation point, equipment, and threshold before claiming an improvement.

Language selection remains KB-011, but sound quality changes its weighting. Compare languages only against the transport candidates and their maintained libraries, real-time and concurrency behavior, memory safety at media boundaries, FFI cost where native audio stacks are unavoidable, reproducible Omarchy packaging, diagnostics, and the ability to build deterministic measurement harnesses. Do not choose a language from general preference or UI convenience before the transport evidence exists.

The first arena result should be an evidence package, not a broad player implementation: a server-to-Linux-renderer transport matrix, the trust boundary for one renderer, an end-to-end measurement plan through USB DDC and I2S/HDMI, a language comparison tied to those transports, and narrow disposable probes using synthetic audio. Multiroom synchronization, mobile, remote Internet access, DSP, library UI breadth, and real NAS, DDC, or DAC reconfiguration stay outside this round.

## What is known, inferred, and unknown

Direct evidence says the old scope chose local shared output, prohibited a LAN listener, deferred bit-perfect and network output questions, and never tested Kuro or Roon (`KD-020`, `KD-022`, `KD-025`, `KD-039`; `docs/sources-cadrage.md:3`). Direct current authority makes one separate Linux living-room renderer computer core and puts sound quality first.

The evidence suggests the old network exclusions were a way to bound the first release: PR #1 describes the whole change as separating commitments from a broad historical inventory, and ticket 01 puts multiroom in a backlog ordered by use. No source says network audio was rejected for measured sound-quality, latency, security, or feasibility reasons.

Known hardware roles are a separate Linux living-room renderer computer, USB into a DDC, then I2S over HDMI into a Terminator DAC. Unknowns include the computer hardware and Linux distribution, DDC and Terminator revisions, supported USB and I2S input specifications, server hardware and OS details beyond Omarchy, wired or wireless LAN, required PCM rates and depths, tolerance for transcoding, desired volume-control point, required bit transparency, accepted measurement gear, and whether server-local playback should survive as a fallback. These must remain questions rather than candidate-specific assumptions.

## Sources consulted

- Source control: `git log`, `git blame`, pickaxe searches, commit `f6d65a1`, merge `8b1b956`, and GitHub PR #1. Found one reconciliation wave and no application history.
- Local issue record and active docs: KD-001 through KD-040, KB-003, KB-004, KB-011, KB-012, current roadmap and validation. Found direct delegated scope decisions but no transport or jitter experiment.
- Archived plans: not used for architecture. The active record explicitly marks them historical.
- Team chat, mail, infrastructure, error tracking, and analytics: not searched. The repository has no application runtime, and the task explicitly excludes unrelated personal sources. No claim here depends on them.
- External transport and audio sources: intentionally left to the deep-research arena. This report establishes the questions and decision lineage; it does not preempt that evidence.
