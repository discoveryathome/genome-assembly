# Time-boxed contributor trial

Started 2026-10-20 20:08:08 UTC. Target: 30–60 minutes including setup friction, experimentation, verification and assessment. Base: e79fd3f02f8f4e1b771bd13b3b9c7afc11a4bbc3. User explicitly requested the contributor trial; the prior scope-confirmation pause is resolved by this instruction. No publication authorized. Existing unsandboxed-build permission continues to apply.

Assigned task (no random task draw): test window101, then at most one evidence-driven bounded follow-up; assess featured-pilot suitability. Frozen primary experiment settings remain unchanged. Candidate is a parameter test, not novel algorithm work. Existing scaffold and literature work preceded this trial and do not count as contributor accomplishments during it.

Success criteria for featured suitability: a verified useful result within the time box, an understandable progress demonstration, feasible home-PC resource cost, plausible repeatable improvement opportunities, and a material role for reasoning beyond compute sweeps. A failed candidate plus a counterexample can be useful research but does not alone demonstrate hill-climbing headroom.

20:08 — Verifier unit tests passed (3). Started pinned screened source builds.
20:09 — Corrected an untested telemetry parser: upstream logs say `indexed N positions`, not `collected N minimizers`. Scientific settings unchanged.

```discover
{"v":0,"kind":"claim","task":"overlap-seeding-01","scope":"30–60 minute local contributor trial and featured-pilot suitability assessment","base":"e79fd3f02f8f4e1b771bd13b3b9c7afc11a4bbc3","posted_at":"2026-10-20T20:08:08Z","expires":"2026-10-20T21:08:08Z"}
```

20:16 — Pinned source builds completed; initial build elapsed 417.23 s. Hifiasm 0.25.0-r726, bundled minimap2 2.28-r1209. No assembler source changes.
20:17 — End-to-end QUAST startup failed because default Python 3.14 lacks distutils. Preserved failure logs, added early runtime detection and selected installed /usr/bin/python3 (3.9.6). No global package installs.
20:18 — QUAST positive control passed; length-preserving inversion rejected with 2 structural errors and unchanged N50 (250,000 bp). Started original frozen size tier.
20:21 — Original development warmup: Hifiasm 88.403 s internal elapsed versus 16.817 s CPU; external process timer 89.522 s. A five-second macOS sample was collected only during this excluded warmup; Rosetta has many unsymbolicated frames, so no dominant-stage percentage is claimed. Both sizing variants yielded identical primary FASTA and the same circular-closure duplication/error metrics.
20:22 — One bounded size-only pivot: preserved original attempt and stopped it before any complete measured pair. New configs/starter.json froze 60/100/80 kbp genomes and new seeds before their generation. Kept coverage, read length/error models, repeat lengths, candidate, thread setting, thresholds and all 5 A/B plus 2 A/A pairs unchanged. Original configs/experiment.json remains untouched as the larger validation tier. No tuning on heldouts.
20:28 — Public explainer rendered and its labeled control verified in Chrome: flipping the middle block changes structural-error count from 0 to 2 while length remains 250,000. A responsive-preview attempt timed out under host/browser load; viewport override was reset. Desktop rendering and the actual interaction were verified.
20:30 — Development matrix complete: median paired wall speedup 1.3806, CPU speedup 1.1096; A/A wall deviation up to 20.12%. Primary and all-GFA equality held for all A/B pairs. Quality and memory screening passed; performance screening failed. Holdouts now running. No claim of universal exactness or native-host speedup.

20:42 — Repeat-rich heldout completed with byte-identical primary/all-GFA outputs and equal quality in all five candidate pairs. Median paired CPU speedup 1.0725; wall-time screening failed. GC/error-shifted heldout started. The candidate was not retuned.

20:46 — All 42 measured assemblies and six warmups completed. All cases pass quality/memory and finite output-identity checks; all fail performance screening. Packaged pinned baseline and raw-file hash inventory. Offline verifier passed, including deterministic input regeneration. CPU reductions 9.88%, 6.76%, 5.99% remain exploratory.

20:49 — All four task-card first steps and Discovery validation passed. Deliberate FASTA evidence corruption was rejected; the original bytes were restored and hash checked. Fresh local clone verification under Python 3.9.6 regenerated the inputs and passed. Added explicit full-replay comparison against the archived unchanged baseline, including every GFA; a deliberately false baseline hash is rejected.

20:50:34 — Trial finished after 42 minutes 26 seconds. Final source verified from a fresh local checkout under Python 3.9.6, including unchanged-baseline identity. All card first steps and Discovery structural validation passed. Preview server stopped; local verification clones removed after logs were preserved. No performance promotion or external publication.

```discover
{"v":0,"kind":"done","task":"overlap-seeding-01","scope":"30\u201360 minute local contributor trial and featured-pilot suitability assessment","base":"e79fd3f02f8f4e1b771bd13b3b9c7afc11a4bbc3","artifact":"reports/trial/ASSESSMENT.md","posted_at":"2026-10-20T20:50:34Z"}
```

```discover
{"v":0,"kind":"handoff","task":"overlap-seeding-01","scope":"Native profiling and exact differential fixture for one overlap-seeding kernel","base":"9243b586f0dbb2a951d3bf41b34ef543354d6d0d","posted_at":"2026-10-20T20:50:34Z","request":{"question":"Can a profiled seed/chaining operation become a tractable source-level improvement challenge?","first_step":"Read reports/trial/NEXT-SESSION.md and run python3 scripts/first_step.py overlap-seeding","success_test":"Reproducible native profile, stage cost and an exact differential trace fixture; no unsupported performance promotion","track":"overlap-seeding","est_minutes":45}}
```

