# Window101 contributor trial

This package compares the unchanged pinned Hifiasm executable at minimizer windows 51 and 101. The optimization is an existing parameter change; no novel assembly algorithm is claimed. See ../../reports/experiment/REPORT.md for the complete measured cases and ../../reports/trial/ASSESSMENT.md for featured-pilot suitability.

The original size tier remains in configs/experiment.json. Its sizing warmups are preserved in reports/initial-sizing-attempt, not counted as performance evidence. The completed controlled trial uses configs/starter.json: new frozen seeds, 60/100/80 kbp circular synthetic genomes, one development and two held-out cases, five paired A/B comparisons and two paired A/A comparisons per case. All quality gates and candidate settings remain fixed. No real human or other biological reads are used.

Recheck archived evidence with `python3 scripts/verify.py reports/experiment`. Full replay commands and permissions are in VERIFY.json. A candidate can fail the acceptance gate while the research package itself verifies successfully. Findings are author-checked/local-only, not independently checked or maintainer accepted. The owner has agreed to maintain the pilot but has not reviewed these results.

Host load was severe, and Hifiasm ran as source-built x86_64 under Rosetta. CPU seconds and seed counts are diagnostic. No public speedup claim should be based on these wall times. Existing baseline structural errors and duplicated circular closure remain visible in the quality report; they were not removed to improve scores.

Open next questions, their first steps and blockers are in TASK.json. Highest priority: independent native replay, a focused exact-preserving kernel challenge, and validation on public nonhuman reads with reviewed circular-assembly scoring. After viewing these holdouts, new tuning must use fresh holdouts.

Credit: workspace owner (question and local maintenance), Codex (harness fixes, experiment and assessment), and upstream Hifiasm/QUAST/minimap2 authors (tools and algorithms). Original pilot code is MIT; upstream licenses apply to upstream code.
