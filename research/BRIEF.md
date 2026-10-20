# Research brief (LOCAL pilot)

Question: Does changing only Hifiasm's minimizer window from 51 to 101 reduce overlap-seeding work and total assembly time on 250–400 kbp synthetic haploid genomes, without degrading reference-based quality?

Progress, in order: (1) no added extensive/local structural errors; no loss of genome fraction, NGA50, NG50 or N50; no added mismatch/indel rate or duplication error; (2) at least 10% median paired runtime reduction above A/A variability; (3) peak RSS no more than 5% worse. Exact output preservation is a separate, stronger claim checked with hashes. Parameter changes are quality-risking by construction even if tested outputs happen to match.

Evidence: pinned source commits and compiler flags; deterministic input hashes; one development and two untouched validation read sets; warmup, alternating A/A and A/B pairs, single thread, fresh output directories; raw time/RSS/phase logs; QUAST alignment-based quality; verifier positive and negative controls. No human data or wet-lab work.

Maintainer: workspace owner, explicitly volunteered in chat. Review capacity not yet declared. Original pilot code MIT; dependencies keep their licenses. Local only; no hub consent or external posting.

## Frontier and claims

The user's research question is open and makes no numerical claim. Hifiasm and QUAST are confirmed available from their upstream repositories. The strongest relevant established capability is accurate phased assembly using HiFi reads, extended to HiFi plus ultralong reads with double graphs. These papers do not establish a universal best time/memory result for our miniature workload. There is no verified record for this exact benchmark; unchanged Hifiasm is the control, not a claimed global optimum.

- Cheng et al. 2021, phased assembly graphs: https://doi.org/10.1038/s41592-020-01056-5
- Cheng et al. 2024, double graphs: https://doi.org/10.1038/s41592-024-02269-8 . Relevant frontier context; hybrid human assembly is outside this pilot.
- Hifiasm parameters: https://hifiasm.readthedocs.io/en/latest/parameter-reference.html . Minimizer window and repeat seed filtering affect computational work. Pinned CommandLines.cpp confirms default window 51; htab.cpp builds the minimizer occurrence index and anchor.cpp processes seeds for overlaps.
- Hifiasm source: https://github.com/chhylp123/hifiasm/tree/ec9a8b222d149d25b7355e83765698640d59b189
- Gurevich et al. 2013, QUAST: https://doi.org/10.1093/bioinformatics/btt086
- QUAST manual: https://quast.sourceforge.net/docs/manual.html . Genome fraction, misassembly breakpoints, duplication, N50/NG50/NGA50 and mismatch/indel rates measure different failure modes.
- QUAST-LG (2018): https://doi.org/10.1093/bioinformatics/bty266 . Large/repetitive genomes need additional evaluation; not evidence that this small pilot generalizes to them.
- QUAST source: https://github.com/ablab/quast/tree/38373fb6454604197d45b047ae61f82e68b61a74

## Settled boundaries and uncertainties

N50 alone is not an accuracy check: misjoins can increase it. Fewer seeds can lose overlap sensitivity. Reducing repeat seeds is not generally lossless. `-f0` is documented for small genomes and belongs in BOTH arms; comparing against the 16-GB default Bloom filter would exaggerate the contribution. `-l0` is appropriate to these haploid synthetic inputs; no claim about diploid phasing. Faster parameter settings already exist; testing window 101 is an experiment, not a novel algorithm claim.

Synthetic substitution/indel errors are not a calibrated PacBio error model. Two independent holdouts test only limited distribution shifts, not real species, metagenomes or human genomes. Held-out means never used to choose candidate settings, not secret. Once inspected, they become regression sets for future work, which must add fresh holdouts.

Environment: Apple Silicon Mac, 24 GiB RAM. Unchanged Hifiasm requires x86 SIMD; build an x86_64 executable and run via installed Rosetta. All comparisons share that binary. Native x86/Linux and native ARM performance remain untested.

## Screen and authorization

User explicitly allowed screened local builds/benchmarks without a sandbox. Hifiasm screen: no findings. QUAST screen: 48 findings, zero high; predominantly committed optional binaries. Do not run those binaries or setup.py. Compile bundled minimap2 source directly and run quast.py with optional gene/read/KMC features disabled. Disable bundled simplejson native speedup to avoid importing a committed binary. No global installs. All generated files remain here.
