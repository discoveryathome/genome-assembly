# A useful next 45-minute contribution

Task: establish a native profile and trace boundary for one overlap-seeding kernel. This is a preparation task, not permission to claim an optimization without measurement. Use an idle native-x86 host if available; preserve this report as the prior exploratory run.

Read AGENTS.md, DISCOVERY.md and ASSESSMENT.md, then run `python3 scripts/first_step.py overlap-seeding`. Target the pinned source, not a newer checkout. Inspect `htab.cpp:356–399` (`worker_pt_gen` and `ha_pt_gen`) and `anchor.cpp:93–178` (`ha_get_new_candidates`), following actual call paths in the native profile. The former builds occurrence offsets/storage; the latter gathers, sorts and converts anchors before chaining. Source locations are orientation hints, not proof that these functions dominate this dataset.

Spend the first ten minutes verifying the existing evidence and obtaining a profile of the development input. Report total runtime and stage attribution without summing cumulative timestamps. If the selected operation consumes a negligible fraction of total time, package that finding and stop pursuing it. Use Amdahl's law to state the maximum plausible end-to-end gain.

For a significant operation, record a minimal input/output trace and the invariants an exact replacement must maintain: minimizer identity and multiplicity, read/strand coordinates, occurrence counts, anchor sort ordering and ties, and downstream chaining input. Reuse only development input for choosing the approach. Include empty lists, repeated keys, large occurrence counts and orientation boundary cases. Do not change repeat filtering, seed sampling, scoring or tie-breaking under the label “exact.”

A good deliverable is a trace-driven differential checker and an honest cost profile with one bounded next hypothesis. A small candidate is optional if time remains. Before any performance promotion, run fresh processes in balanced order with A/A controls, report peak RSS, compare all GFA outputs, and pass QUAST gates on new frozen heldouts. At least the last ten minutes belong to verification and packaging. No unrestricted grid search, entire-pipeline rewrite or human data is needed.

This task becomes easier after a maintainer packages the native trace fixture. Its current preparation cost is part of why the pilot is not yet ready for an inaugural donor-facing promise of quick algorithmic wins.
