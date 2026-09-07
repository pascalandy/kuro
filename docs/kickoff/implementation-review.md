# Implementation review

Read-only independent review of the uncommitted laboratory implementation after architecture commit d922b4f. Reviewed runtime, CLI, independent tests, model, audio proof, builder, contracts and plan. Re-read the reservation tightening while reviewing.

Final status: all actionable findings below are resolved. The initial review found a builder retry defect and a source-provenance limitation. The final delta review records the corrections and independent evidence checks.

## Initial findings, resolved

The line numbers in these initial findings refer to the pre-fix working tree inspected during review. They are historical locations, not references to the corrected script below.

1. P2: interrupted download prevents a normal rerun. `scripts/build_lab_mpd.sh:55-56` sends curl output straight to the final archive. If curl writes some bytes and fails, the next invocation enters lines 47-52, rejects that partial archive and exits without retrying. Reproduced with a temporary curl shim that writes `interrupted archive` to its `--output` path and exits 18. First script invocation exited 18; second exited 1 with cached SHA mismatch. Reproduction directory: `/tmp/kuro-build-review-flecybxs`. Download to a temporary sibling, verify it, then rename it to the final archive; remove the temporary on failure. This does not invalidate a completed build, but contradicts the intended rerunnable build workflow.

2. P3: archive checksum does not establish the reused source tree. `scripts/build_lab_mpd.sh:64-70` treats the presence of `meson.build` as sufficient to reuse extraction. Changes to extracted source survive every run while the printed archive hash still describes the original release. Interrupted extraction that already produced `meson.build` also skips repair. This is explicit in renderer-build.md, so it is a reproducibility limitation rather than concealed provenance. Either verify the extracted source against the pinned archive, use a separate fresh source extraction, or avoid calling this a reproducible pinned-source build on reused directories. No full rebuild was run in this review.

## Initial FLAC transport gap, resolved

`verify_audio_lab.py` encodes FLAC, decodes the same local file, then gives local FLAC paths to MPD. It never transports encoded FLAC. The implementation plan explicitly asks to transport the encoded file before decoding. The script accurately labels its actual scope, including that Go transported WAV, so its success is valid for codec/FIFO observations but does not complete that plan item. Resolve by implementing the separate transfer or recording the deviation in the final synthesis.

The lack of NAS, two real machines, USB, DDC, I2S, DAC, clock measurements and listening evidence is already explicit and is not a defect in this loopback/silent lab.

## Verified behavior

- `go test ./...` and `go test -race ./...` passed using the Go test cache for the reviewed source state.
- Fresh `go run ./cmd/kuro-transport-lab run --out /tmp/kuro-review-proof-20260906` passed all seven cases.
- Fresh `python3 scripts/verify_audio_lab.py --proof-dir /tmp/kuro-review-proof-20260906 --mpd /tmp/arena-kuro-sq/mpd-build/mpd-0.24.15/build-min4/mpd --out /tmp/kuro-review-audio-20260906` passed. Both WAV and FLAC FIFO captures equal the 192,000-byte, 48,000-frame master concatenation, SHA-256 `24d01720643e20bd7f7e09cc52f5370a5aeb12c6536adba0198b1e7951144ff5`.
- Verify checks canonical fixture hashes, exact received bodies, actual ready paths, rejection bodies, raw response fragments, recorded HTTP status/range/validator/length, trace consistency, recalculated model outcomes, expected case count, ready directory contents and absence of partial files. Report booleans are not consumed.
- Corrupt/truncate/changed-etag cases demand the exact injected failure evidence and no admission. The changed validator response is preserved separately and never concatenated into the partial object.
- Sources are generated read-only and origin faults mutate newly read buffers. Receiver checks size/validator/hash, closes and syncs the partial, then renames within the same output filesystem.
- Updated receive reserves before creating a partial. Resume uses the same reservation; budget denial preserves current reservation. The budget remains a two-object laboratory window, not a complete accounting system for retained audit artifacts.
- Model deadlines remain fixed after progressive start, arrivals on a deadline count, final partial periods are bounded, and dimensions/times/large schedules have explicit rejection bounds. No arithmetic overflow path found with validated input bounds.
- FIFO configuration declares one explicit FIFO sink and a private Unix socket. Subprocess commands use argument arrays, capture sizes and wall time are bounded for the actual MPD, and final cleanup terminates/kills/reaps MPD and closes the descriptor. No physical output was selected.

The review made no repository edits. Only temporary test outputs and this review file were written.

## Final delta review after corrections

Both builder findings are resolved. Download now uses an owned temporary sibling, checks the pinned SHA before atomic publication, and cleans temporary files on failure. Extraction uses a fresh temporary directory before publication. Reusing existing sources now requires an exact manifest match with fresh extraction, including path sets, file types, permissions, file hashes and symlink targets. Only the generated root build-lab tree is excluded; similarly named nested source paths are still checked. These checks establish pinned source provenance, while host dependencies and generated build state remain ordinary build inputs rather than a claim of bit-for-bit reproducible binaries.

Independently reran `/tmp/kuro-build-atomic-check.py`. It passed download and extraction interruption/retry, valid reuse, modified/extra source rejection and invalid cached archive preservation. Build tools are stubbed in this check; SHA, tar and source comparison are real. Reviewed cleanup and ownership of temporary paths; no unresolved issue found in the requested change scope.

The FLAC plan gap is resolved. The script now serves fixed generated FLAC objects on a Python 127.0.0.1 listener, receives and byte-compares them, decodes the received files and compares PCM, and separately passes HTTP URLs directly to MPD for a third FIFO capture. It disables proxy environment effects for the private requests. This is a separate FLAC transport proof and does not claim Go's fault-injection coverage for FLAC or any measured progressive timing advantage.

Independently read raw artifacts under `/tmp/kuro-audio-http-proof-002`, using PCM masters from `/tmp/kuro-transport-builder-proof-002`. Each encoded FLAC equals its received file; each decoded PCM equals its track master. WAV, staged FLAC and direct HTTP FLAC FIFO captures all equal the master concatenation: 192,000 bytes, SHA-256 `24d01720643e20bd7f7e09cc52f5370a5aeb12c6536adba0198b1e7951144ff5`. The origin log contains both Python and MPD requests for each track. These conclusions came from reading and comparing artifacts, not trusting result.json success fields.

Re-read the budget delta. It reserves before partial creation, keeps retries in one transfer reservation, checks the exact expected reservation map during Verify, and retains the current object on denial. No new defect found.

Final conclusion: no unresolved actionable findings within the loopback transport, silent codec/FIFO and isolated builder scope reviewed. Physical playback, two-machine behavior, NAS and sonic quality remain explicitly unproved.
