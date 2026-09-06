> Historical kickoff attempt, superseded by the sound-quality transport requirement before arena selection. See [scope change](scope-addendum.md).

# Kuro architecture arena grounding

## What exists today

The baseline is commit `8b1b956` on `main`. It contains a reconciled product brief, its decision record, an archived earlier planning corpus, one generated TSV, and two Python documentation tools. It contains no application source, dependency manifest, build configuration, package, automated product test, or executable Kuro service. The README says this directly: no Kuro software exists yet, no stack or license has been chosen, and technical studies must precede those choices (`README.md:3-5`, `README.md:28-30`).

The current worktree has moved to `kickoff/architecture-arena` and contains untracked `docs/kickoff/` work from the orchestrated kickoff. I treated committed `8b1b956` as the ground truth for this report so concurrent arena edits could not change the baseline under inspection.

The active documents are the root README and glossary plus the Markdown and TSV files directly under `docs/`. The 36 files under `docs/archive/p1-p5/` are a byte-preserved snapshot of commit `c478909`, not current direction (`README.md:19-24`, `docs/archive/p1-p5-source.md:3-11`). I did not use archived architectural proposals to infer a design.

## Current product contract

Kuro is a personal music library and player for one user's Linux Omarchy session. U-M1 must handle local files and an already-mounted NAS, roughly 20,000 albums and 3 TB, local browsing and search, playlists and a queue, shared local audio, the selected gapless guarantee, persistence, restorable backup, unchanged source files, and indefinite operation without Internet after installation (`docs/cadrage-courant.md:7-11`, `docs/cadrage-courant.md:53-59`).

U-M1 is split into demonstrations, not separately acceptable releases:

1. U-M1.A imports a local folder and plays an album through shared system output.
2. U-M1.B adds retrieval, stable views and ordering, navigation context, playlists, and queue operations.
3. U-M1.C adds restart behavior, mounted-NAS behavior, backup and failed-restore recovery, then full-scale and packaging proof.

The whole U-M1 passes only when the ten historical MVP criteria and all current contracts pass together (`docs/roadmap.md:3-13`). KV-001 through KV-013 describe future evidence, but none has run because the product does not exist (`docs/validation.md:1-3`).

Later scope is deliberately narrow. U-M2 considers favorites, local filters, and optionally shuffle, repeat, and MPRIS. U-M3 considers voluntary organization of editions, box sets, and perhaps internal metadata corrections. U-M4 authorizes only a mobile study after desktop acceptance and stability conditions (`docs/roadmap.md:15-37`). Those are not kickoff implementation scope.

The historical inventory has 195 functions, but inventory presence is not a commitment (`.scratch/cadrage-kuro/issues/03-reviser-cadrage-second-entretien.md:68-70`). The generated current disposition classifies 37 as `engage`, 16 as `partiel`, 132 as `differe`, 6 as `hors_portee`, and 4 as `etude`. Fifty-three rows are assigned to U-M1. This classification is useful for coverage checks, not as 195 equal-priority requirements.

## Contracts that should shape architecture from day one

- Music sources are read-only. Kuro never modifies or deletes media or source images (`docs/cadrage-courant.md:23-27`, `.scratch/cadrage-kuro/issues/01-definir-usages-et-limites.md:96-98`).
- A configured source, a catalog reference, durable application data, and reconstructible data are distinct concepts (`CONTEXT.md:5-32`). A catalog reference survives an explicit root relocation when its relative path is unchanged and survives tag changes at the same path. Internal rename or replaced content may create a new item; Kuro must not silently reconcile by name, tags, or presumed fingerprint (`docs/cadrage-courant.md:15-21`).
- Missing, explicitly removed, and re-added sources have different behavior. Missing NAS media keep references. Removing a source hides its media but preserves unavailable queue and playlist references. Re-adding the same path does not reactivate it silently (`docs/cadrage-courant.md:17-21`, `docs/validation.md:13-19`).
- Scans must be cancellable and resumable. Already-cataloged items remain usable, one invalid file does not stop the scan, concurrent scan requests are coalesced or deferred, and a successful scan never interprets an absent NAS as deletion (`docs/cadrage-courant.md:13-15`, `docs/validation.md:9-11`).
- Metadata fallbacks, stable ordering, copy and edition separation, accent-insensitive search, and visible source context are observable behavior, not UI decoration (`docs/cadrage-courant.md:23-31`).
- Queue commands have exact effects. Playback replaces the queue and starts, `Jouer ensuite` and `Ajouter` mutate without starting, duplicate entries are valid, removal of the current item stops playback, and unavailable items are skipped at most once per traversal (`docs/cadrage-courant.md:33-41`).
- Initial audio is stereo PCM through the system's shared output. The exact guaranteed formats and gapless threshold remain open. No DSD, multichannel, exclusive mode, hardware-volume control, or DSP belongs to U-M1 (`docs/cadrage-courant.md:43-49`, `docs/validation.md:41-43`).
- Window close leaves a per-user session service alive. Explicit Quit stops it. Restart restores queue and the best recorded position but does not resume sound (`docs/cadrage-courant.md:51-53`, `docs/validation.md:45-47`).
- Backup covers durable choices and known metadata, not media, source images, caches, indexes, or secrets. Restore is a confirmed replacement, starts silent, and must leave the old state recoverable on invalid input, incompatibility, or interruption (`docs/cadrage-courant.md:55-59`, `docs/validation.md:49-53`).
- Kuro must work without an account or Internet, must not listen on the LAN, must restrict local control to the session user, and must redact diagnostics before export (`docs/cadrage-courant.md:53-59`). Keyboard access, visible focus, accessible labels, zoom, and track seeking belong to U-M1 (`docs/cadrage-courant.md:57-59`).

## What the scripts actually do

`scripts/build_disposition.py` is a deterministic generator, not a product build. It reads the archived 195-row function inventory and writes `docs/disposition-fonctions.tsv` (`scripts/build_disposition.py:10-20`, `scripts/build_disposition.py:28-32`). All classifications are hard-coded calls grouped by the 15 archived domains (`scripts/build_disposition.py:41-149`). `assign()` rejects assigning one function twice (`scripts/build_disposition.py:34-39`), and the final set comparison rejects missing or unknown IDs (`scripts/build_disposition.py:151-154`). It preserves archive row order and prefixes each current scope statement with the historical function name (`scripts/build_disposition.py:156-170`).

I ran the generator against a copied input under `/tmp`, then compared its result byte for byte with the checked-in TSV. They match, with SHA-256 `3dfb7a713ca57ba1208435506954188a78a944c74f81351b8728850bd1ef5227`.

`scripts/verify_docs.py` is a read-only consistency checker. Its checks are:

- Reconstruct the expected archive file list from fixed commit `c478909`, require exactly 36 files, compare every archived byte to Git, verify the SHA-256 manifest, and require provenance to name the commit (`scripts/verify_docs.py:15-17`, `scripts/verify_docs.py:44-100`).
- Resolve local Markdown links and anchors across active docs, `.scratch`, and the mirrored archive. Archived links are resolved as if they still lived at their original paths, then mapped into the archive (`scripts/verify_docs.py:102-165`).
- Check TSV column widths and file-looking path references (`scripts/verify_docs.py:167-204`).
- Parse KD definitions from decision-ticket headings, KB definitions from backlog rows, and KV definitions from validation headings (`scripts/verify_docs.py:206-221`).
- Require the current TSV schema, exactly 195 unique IDs matching the archived inventory, allowed disposition and step values, valid KD/KB/KV references, a KV for every engaged or partial U-M1 row, a KB for every deferred, study, or partial row, nonempty scope, and at least one KD source per row (`scripts/verify_docs.py:223-285`).
- Require all identifiers used by active docs to be defined, all Wayfinder tickets to be resolved, map links to exist, and ticket dependencies to be known and acyclic (`scripts/verify_docs.py:287-337`).

The checker runs those stages in that order, prints counts, prints every accumulated error, and exits 1 on any error (`scripts/verify_docs.py:339-356`). On an isolated clone of the committed baseline it passes with 36 snapshot files, 36 matching archived files, 798 local links, 620 TSV file references, 273 KD references, 161 KB references, and 62 KV references. Both scripts also pass Python bytecode compilation.

The checker does not prove product behavior, detect semantic contradictions in prose, validate URLs, or verify that `build_disposition.py` reproduces the checked-in TSV. That final generator comparison is why I ran the separate byte-for-byte check.

## Unknowns the kickoff must leave explicit

The active backlog intentionally leaves these decisions open:

- License and obligations of the eventual distributed artifact, KB-010.
- Application stack and internal process split, KB-011. The docs require a session service and desktop behavior, but do not prescribe language, toolkit, database, IPC, or audio library.
- Exact PCM format matrix, output hardware, homogeneous gapless corpus, and measurable gapless threshold, KB-012.
- Target hardware, representative corpus, import-time and memory budgets, KB-013. The 300 ms search p95 and one-second first page are design goals, not measured acceptance results (`docs/cadrage-courant.md:61-63`).
- NAS mount details and interruption behavior on the real target, KB-014.
- Reproducible Linux packaging outside the development machine, KB-015.
- Detection and identity behavior when audio content changes at the same path, KB-022 (`docs/backlog.md:25-37`).

There is also no supplied synthetic audio corpus, accepted target machine profile, DAC/output identifier, packaging environment, or exact UI layout. An arena candidate should state assumptions around those inputs and avoid turning them into product decisions.

## Recommended arena boundary

Give each arena candidate the same task: propose a U-M1 architecture and prove its riskiest claims with a disposable, reproducible spike. Require a short component and data model, explicit ownership of durable versus reconstructible state, process and IPC boundaries, scan cancellation and restart semantics, catalog-reference rules, audio-library choice, and a mapping from architecture seams to KV-001 through KV-013.

Bound implementation to synthetic files under a temporary directory. A candidate may build narrow probes for local tag extraction and incremental cataloging, accent-insensitive search, shared-output playback and a homogeneous gapless transition, persisted stopped-state restart, and atomic snapshot replacement. It must not touch the user's music, configure the real NAS or audio hardware, publish packages, implement U-M2 through U-M4, or claim scale and gapless results without the required corpus and hardware.

Ask candidates to return comparable evidence: exact commands, dependency versions, raw probe results, what failed, and which KB questions remain. The arena winner should be the design with the clearest contract boundaries and strongest measured risk reduction, not the largest codebase.

The bounded kickoff outcome is a reviewed architecture decision package plus a small retained proof harness for KB-011. The current user request authorizes autonomous design, bounded implementation, and commits. Full U-M1 acceptance still belongs to the user, and stack adoption requires the technical evidence listed in KB-011. The kickoff must not claim that limited experiments close those studies or silently reduce product scope (`docs/backlog.md:3`, `docs/backlog.md:39`, `.scratch/cadrage-kuro/issues/03-reviser-cadrage-second-entretien.md:94-96`).
