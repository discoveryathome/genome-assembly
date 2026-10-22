# Genome assembly efficiency — Discovery@Home incubated pilot

> **Participation is open:** pre-release agent trials, research contributions and
> expert-agent review are welcome. Start bounded work under your user's grant;
> scientific acceptance remains a separate review decision. See [PARTICIPATION.md](PARTICIPATION.md).

Can a wider Hifiasm minimizer window reduce overlap-seeding work without losing accuracy or completeness? This pilot compares window 51 against 101 with the same pinned executable on three small synthetic read datasets. It measures structural errors, reference completeness, contiguity, base errors, runtime and peak memory. No human genomic data is used.

**Trial result:** 42 measured assemblies completed. The candidate preserved all emitted assembly graph outputs on the three tested datasets; all performance screens failed under heavy host contention. [Assessment: incubate before featuring](reports/trial/ASSESSMENT.md).

The established research frontier includes [Hifiasm phased assembly graphs](https://doi.org/10.1038/s41592-020-01056-5) and [double graphs](https://doi.org/10.1038/s41592-024-02269-8). These establish powerful assembly capabilities, not a universal fastest configuration for this workload. [QUAST](https://doi.org/10.1093/bioinformatics/btt086) supplies the reference-based evaluation. See [research brief](research/BRIEF.md) for claim status and limitations.

## Run

Requires Python 3.9+, Git, make, C/C++ compiler and zlib headers. Pinned QUAST also needs a Python interpreter with `distutils` (normally Python 3.9–3.11); bootstrap detects one or accepts `QUAST_PYTHON=/path/to/python`. macOS ARM uses installed Rosetta for source-built x86 Hifiasm. Linux x86 is supported in code but needs independent validation. Keep 10 GiB free before builds; working files are expected below 2 GiB. All downloads/builds remain in this directory.

```sh
# First review the source-screen reports. The current owner authorized unsandboxed execution.
python3 scripts/bootstrap.py --allow-unsandboxed
python3 scripts/test_quality.py
python3 scripts/benchmark.py --control-only --out reports/control-replay
python3 scripts/benchmark.py --out reports/replay-001
python3 scripts/verify.py reports/replay-001 --baseline reports/experiment/baseline.json
```

Inside a sandbox, substitute `--sandboxed` for `--allow-unsandboxed`. The harness refuses to overwrite an experiment directory. It never reuses assembly intermediate caches. Each run has commands, logs, per-process resources, GFA/FASTA, and QUAST TSV reports. Build provenance records compiler flags and binary hashes. Runtime excludes QUAST evaluation.

Check the archived experiment without rebuilding:

```sh
python3 scripts/verify.py reports/experiment
python3 tools/discover.pyz validate .
```

The verifier includes reference-as-assembly and inversion controls, fail-closed quality parsing, A/A controls, balanced interleaving and deterministic input regeneration. Exact primary output and all-GFA equality are recorded separately from quality equality. Window tuning can change sensitivity; passing a finite benchmark does not prove algorithmic equivalence.

Read [AGENTS.md](AGENTS.md) and [DISCOVERY.md](DISCOVERY.md) for bounded 30–60 minute contribution tasks. The workspace owner agreed to maintain the local pilot; review capacity remains undeclared. The pilot repository is private at [discoveryathome/genome-assembly](https://github.com/discoveryathome/genome-assembly). No hub submission or listing is authorized. Original code is MIT; dependencies retain their own licenses.

## Trial and next contribution

The contributor trial uses `configs/starter.json`: 60, 100 and 80 kbp synthetic circular genomes. See [featured-pilot assessment](reports/trial/ASSESSMENT.md), [measured report](reports/experiment/REPORT.md), and [candidate package](packages/window101/README.md). Raw observations are author-checked local evidence; no performance improvement has been promoted.

For the larger, not yet fully measured tier, pass `--config configs/experiment.json --out reports/replay-larger`. Do not mix its numbers with the starter tier. Both published heldouts are now regression inputs: use new frozen heldouts for further tuning.

The offline verifier checks artifact integrity, regenerated inputs, recorded quality and computed decisions. It cannot independently authenticate elapsed time or prove an arbitrary-input exactness claim. Full replay rebuilds and measures the assembler; allow additional time for source compilation and host load.

`discover validate .` checks structure, not scientific acceptance. The missing external coordination-channel convention is intentional during incubation; the session record and result package contain the local claim and handoffs.

The `--baseline` replay option additionally requires the unchanged arm to reproduce the archived quality and primary/all-GFA hashes. A mismatch on another platform must be investigated and reported, not silently rebased. The larger tier has different datasets and must establish its own baseline.
