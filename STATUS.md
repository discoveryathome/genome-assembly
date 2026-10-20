# Initialization status

Prepared, not yet executed. This is not a completed pilot or a performance claim.

Owner authorized screened local builds/benchmarks on the unsandboxed machine and agreed to maintain the local pilot under MIT. A subsequent research-scope confirmation is pending, as requested by start.md step 3. Proposed scope: compare Hifiasm minimizer windows 51 and 101, treating the candidate as a quality-risking parameter optimization.

Completed: literature brief; shallow pinned source clones; static screens; frozen experiment config; original Python bootstrap, generator, benchmark, quality-gate and evidence-verifier code; documentation and provisional Discovery records. Hifiasm screen has no findings; QUAST has 48 findings and zero high, mainly optional committed binaries. No upstream build or benchmark has run. The helper hash was verified before helper execution.

Next after confirmation:
1. Run unit verifier checks, fix failures without changing frozen scientific gates.
2. Build with scripts/bootstrap.py, capture compiler/binary provenance; Hifiasm x86_64 under Rosetta and QUAST's bundled minimap2 natively.
3. Exercise true-reference and deliberately inverted-assembly QUAST controls.
4. Commit frozen config/harness and run development then heldouts, with no tuning on heldouts.
5. Check output hashes, raw phase/seed counters, quality, RSS, paired speedups and A/A noise; retain negative findings.
6. Add pinned measured baseline, full report, result package and short-session feasibility assessment.
7. Validate Discovery files, execute every card's first_step, and verify from a fresh local clone. Report total folder size and limitations; publish nothing.

The source clones, build recipes and reports must stay inside this folder. Do not run committed upstream binaries. The unexecuted harness may need portability fixes; do not describe it as validated until checks pass.
