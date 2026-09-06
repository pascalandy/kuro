# Preliminary transport probe

Status: executed research artifact from 2026-09-06. This disposable probe predates the retained Go prototype and does not report its results. See the [current verification record](../../verification.md).

[`transport_probe.py`](transport_probe.py) transfers synthetic FLAC and PCM over localhost. [`transport-probe-result.json`](transport-probe-result.json) preserves the observed output. The probe opened no audio device and used no NAS, Kuro server, living-room renderer, DDC, DAC, or analog capture.

From the repository root, rerun it with:

```sh
python3 docs/kickoff/research/preliminary/transport_probe.py \
  | tee /tmp/kuro-preliminary-result.json
```

The timing count depends on process scheduling. A rerun can therefore produce a different modeled underrun count while the transferred bytes remain identical.
