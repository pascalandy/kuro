# Kuro kickoff decision-trail audit — final status

Audit state: 2026-09-06, after architecture commit `d922b4f` and before publication of the pending runtime/docs commit.

## Result

All actionable trail-audit findings are resolved. The decision trail is internally consistent with the implementation, retained evidence, and stated laboratory scope. I found no unsupported claim about physical sound quality, jitter, NAS behavior, the two-computer path, USB, DDC, I2S, DAC, analog output, or listening results.

## Remediations verified

- `docs/kickoff/todo.md` marks every Architect and Arena phase complete, including an explicit no-scrap conclusion: the selected design was retained because implementation and review found no repeated architectural friction.
- `docs/kickoff/decisions.tsv` adds a final-build verification row linking `implementation-review.md` and `renderer-build.md`, plus a scrap-assessment row that leaves physical audio and product acceptance open.
- `docs/kickoff/implementation-review.md` labels its original script line references as locations in the pre-fix working tree.
- `scripts/test_build_lab_mpd.py` is a portable retained regression entry point accepting `--archive`. It covers interrupted download/extraction cleanup and retry, valid reuse, modified and extra source rejection, and preservation of an invalid cached archive. The real MPD build was also rerun successfully against `/tmp/kuro-mpd-lab-final.ezgJVq`; the stubbed regression is not being used as a substitute for compilation.
- `docs/kickoff/evidence/` retains compact Go, stall, audio, and HTTP JSON evidence. The committed report hashes match the observed raw reports: Go `4a19a5744270cca10a8fdbd0081b992074c4dbe69336a012e36b7fec402b40fa`; audio `65cf04550d0276f12c4b3ce1dc62c550a6af87f88c08c35210b29a008648ecc7`. `verification.md` clearly says these extracts do not replace the full temporary artifacts.
- The audio evidence still distinguishes WAV admitted by Go from FLAC transported by the separate Python loopback origin. All three retained FIFO comparisons report 192,000 bytes, 48,000 frames, and PCM SHA-256 `24d01720643e20bd7f7e09cc52f5370a5aeb12c6536adba0198b1e7951144ff5`.
- `.github/workflows/kickoff.yml` uses pinned verified release SHAs for checkout v7.0.1 and setup-go v7.0.0, disables setup-go caching, and contains the expected docs, formatting, vet, race, run, and verify steps.

## Remaining known limits

Remote GitHub Actions execution remains pending until publication; the current record does not claim that it has run. The next product phase still needs exact hardware inventory, a clean installation, the real NAS and two-computer network path, MPD behavior under real progressive delays, ALSA format negotiation, USB/DDC/I2S/DAC observations, analog measurements, and controlled listening against the Aurender reference. These are correctly presented as future evidence rather than defects or completed work.
