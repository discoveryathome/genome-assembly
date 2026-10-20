# Efficient genome assembly through a bounded overlap-seeding experiment

Can we reconstruct genomes from reads more efficiently without losing assembly accuracy or completeness? This pilot narrows the question to Hifiasm's minimizer occurrence index and its downstream overlap-seeding workload on small synthetic haploid circles.

The candidate changes only the minimizer window from 51 to 101. It is an existing-parameter optimization, not a newly invented algorithm. See research/BRIEF.md for the literature, verified claims, settled boundaries and hardware limitations. No universal best assembler or global time/memory bound is claimed. Upstream phased-graph and double-graph results establish capabilities under their stated conditions; the pinned unchanged Hifiasm executable is our empirical baseline.

## Experimental contract

The precise settings, dataset definitions, pair counts and numerical thresholds are frozen in configs/starter.json (60/100/80 kbp). The original 250–400 kbp configs/experiment.json is retained as a larger validation tier; only its sizing warmups ran. The single size-only pivot is documented in reports/trial/SESSION.md. Both arms use one thread, `-f0` for small genomes, `-l0` for haploid inputs and the same primary-output mode. This isolates minimizer sampling; no human pipeline tuning occurs. Hypothesis: larger windows reduce seed occurrence storage and downstream seed matching/chaining. Runtime alone cannot attribute a mechanism; inspect seed counts and cumulative phase log markers. Do not call this the dominant bottleneck without profiling evidence.

The verifier precedes candidate research. It rejects additional extensive/local misassemblies, lost reference fraction, degraded N50/NG50/NGA50, increased mismatch/indel rates, added unaligned sequence/contigs, or worse duplication error. All required QUAST metrics must be present and finite. A reference-as-assembly positive control and a length-preserving inversion negative control exercise the aligner. Unit checks exercise missing/NaN metrics and deceptive length/contiguity improvements.

Performance requires at least 10% median paired speedup, greater than twice observed maximum A/A deviation, a bootstrap lower bound above 1, and no more than 5% median peak RSS growth. These are screening gates, not proof of statistical significance. A/A primary and all-GFA identity must hold. Five A/B pairs and two A/A pairs are modest: independent replay is needed for promotion.

Quality equality, primary byte equality, and all-GFA byte equality are different claims. Changing the minimizer window is intrinsically a sensitivity tradeoff. Matching finite outputs does not prove exact preservation on arbitrary inputs; a true exact optimization needs semantic reasoning and adversarial tests in addition to hashes.

One development input and two frozen heldouts test basic distribution shifts. They are synthetic, nonhuman, and small enough for a laptop. They do not establish biological, metagenomic, diploid or large-genome generalization. No BUSCO/gene completeness is implied by reference base coverage. Future sessions must generate new heldouts before tuning and keep a record of attempted variants.

## Runnable paths

- `python3 scripts/bootstrap.py --allow-unsandboxed` fetches exact pinned source revisions, screens, and builds locally. Use this flag only with owner permission; otherwise run in a sandbox with `--sandboxed`.
- `python3 scripts/test_quality.py` runs the fail-closed unit checks.
- `python3 scripts/benchmark.py --control-only --out reports/control-replay` runs the positive and negative QUAST examples.
- `python3 scripts/benchmark.py --out reports/replay-001` runs the complete controlled experiment, refusing an existing output directory.
- `python3 scripts/verify.py reports/experiment` recomputes the recorded verdict from archived evidence without a build.
- `python3 tools/discover.pyz validate .` checks the local Discovery records.

Bootstrap requires Git, Python ≥3.9, a QUAST interpreter with distutils (Python 3.9–3.11; detected automatically or selected with QUAST_PYTHON), C/C++ compiler, make, zlib development headers, 10 GiB free before builds, and network access to the pinned GitHub repositories and Discovery helper. Working space is expected below 2 GiB. On this ARM Mac, Hifiasm uses a source-built x86_64 executable under Rosetta; minimap2 is built natively. Linux/x86 support is provided by the harness but not validated by the initialization run. No committed upstream executable is run; the optional simplejson extension is removed locally. No optional gene/KMC/read-mapping tools are enabled.

## Short-session contribution tracks

Priority revision 1. Tracks: reproduce (35), verifier (30), overlap-seeding (25), literature (10). See discover/catalog.json and discover/priority-log.md for bounded cards. Typical sessions are 30–60 minutes: 20% orientation, at least 25% verification and packaging. A useful outcome may be a regression test, failed candidate, independent replay or focused source profile. An entire human genome assembly pipeline is out of scope.

Before proposing an algorithm change, measure the targeted stage, estimate the best possible total speedup, and write down what exactness requires. Start with one development case; allow one bounded pivot. Never tune on the two published holdouts. Memory and quality regressions must be reported even if runtime improves.

## Maintenance, review and credit

The workspace owner explicitly agreed to maintain this local pilot and selected MIT for original code. Review capacity per week remains undeclared; no public donor intake is enabled. The maintainer accepts/rejects contributions, reviews changes to verifier/frontier with particular care, and controls publication. No hubs consent record exists. Local reports are author-checked only until independent replay and maintainer review.

Credit is recorded in CONTRIBUTORS.md and result packages, including contributions that find reproducible negative results. Dependency authors retain their attribution and licenses. Algorithm novelty requires a literature audit. Review capacity, not donated compute alone, will determine sustainable throughput.

Every result package contains README.md, TASK.json, SOURCES.json and VERIFY.json, with exact commands, hashes, environment, limitations and next questions. Local findings/handoffs end with a fenced discover JSON block; the initial private GitHub push is owner-authorized. Hub submission remains unauthorized; no hub PR or consent record should be created.
