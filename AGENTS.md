# Genome assembly pilot

Read DISCOVERY.md, configs/starter.json, discover/frontier.json and the latest report before work. This is LOCAL mode: no repository creation, posting, pushing or hub consent. Original code is MIT; dependencies retain upstream licenses.

One session owns one bounded task. Use the Discovery helper's seeded picker when no task was assigned; record seed and base commit. Do not spawn subagents unless the user explicitly asks. Screen any new external source before execution, and get owner permission if the session is unsandboxed. This initialization session already has that permission.

Do not silently change pins, frozen datasets, quality gates or candidate parameters. Candidate tuning uses development inputs only. Published holdouts are now regression inputs: new tuning requires new heldouts. Run scripts/test_quality.py before changes and scripts/verify.py on submitted evidence. Never claim exactness from matching QUAST scores. Record primary GFA/FASTA hashes and all GFA hashes separately. No speed claims from cached overlap files, omitted errors, changed threads or unrecorded binaries.

Keep builds and data in this directory. No global installs. No restricted human data, wet-lab or biological design work. If a bounded task fails, package the failure with a reproducible counterexample. Contributions require maintainer review; do not promote your own work to maintainer-reviewed.
