# Genome assembly efficiency — Discovery@Home LOCAL pilot

Can a wider Hifiasm minimizer window reduce overlap-seeding work without losing accuracy or completeness? This pilot compares window 51 against 101 with the same pinned executable on three small synthetic read datasets. It measures structural errors, reference completeness, contiguity, base errors, runtime and peak memory. No human genomic data is used.

The established research frontier includes [Hifiasm phased assembly graphs](https://doi.org/10.1038/s41592-020-01056-5) and [double graphs](https://doi.org/10.1038/s41592-024-02269-8). These establish powerful assembly capabilities, not a universal fastest configuration for this workload. [QUAST](https://doi.org/10.1093/bioinformatics/btt086) supplies the reference-based evaluation. See [research brief](research/BRIEF.md) for claim status and limitations.

## Run

Requires Python 3.9+, Git, make, C/C++ compiler and zlib headers. macOS ARM uses installed Rosetta for source-built x86 Hifiasm. Linux x86 is supported in code but needs independent validation. Keep 10 GiB free before builds; working files are expected below 2 GiB. All downloads/builds remain in this directory.

```sh
# First review the source-screen reports. The current owner authorized unsandboxed execution.
python3 scripts/bootstrap.py --allow-unsandboxed
python3 scripts/test_quality.py
python3 scripts/benchmark.py --control-only --out reports/control-replay
python3 scripts/benchmark.py --out reports/replay-001
python3 scripts/verify.py reports/replay-001
```

Inside a sandbox, substitute `--sandboxed` for `--allow-unsandboxed`. The harness refuses to overwrite an experiment directory. It never reuses assembly intermediate caches. Each run has commands, logs, per-process resources, GFA/FASTA, and QUAST TSV reports. Build provenance records compiler flags and binary hashes. Runtime excludes QUAST evaluation.

After an archived experiment exists, its evidence is checked without rebuilding:

```sh
python3 scripts/verify.py reports/experiment
python3 tools/discover.pyz validate .
```

The verifier includes reference-as-assembly and inversion controls, fail-closed quality parsing, A/A controls, balanced interleaving and deterministic input regeneration. Exact primary output and all-GFA equality are recorded separately from quality equality. Window tuning can change sensitivity; passing a finite benchmark does not prove algorithmic equivalence.

Read [AGENTS.md](AGENTS.md) and [DISCOVERY.md](DISCOVERY.md) for bounded 30–60 minute contribution tasks. The workspace owner agreed to maintain the local pilot; review capacity remains undeclared. No repository, hub listing or external post is created. Original code is MIT; dependencies retain their own licenses.
