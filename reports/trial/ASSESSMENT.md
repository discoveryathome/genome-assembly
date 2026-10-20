# Featured-pilot assessment

**Recommendation: retain as an incubated pilot; do not lead the inaugural featured lineup with its current formulation.** The public story and hardware accessibility are compelling. The trial supplies a runnable research loop and a concrete parameter candidate, but does not establish repeatable source-level hill climbing or an independently confirmed performance improvement.

## What this trial tests

The contributor session began at 20:08:08 UTC on 2026-10-20. Scaffolding, shallow source clones and the literature brief existed beforehand and are not credited as work accomplished in this time box. This was a trial on a prepared pilot, not a blind orientation test of a fresh contributor. The task was assigned explicitly; there was no random task selection. The owner authorized screened local builds and will maintain the MIT pilot. Nothing was published.

The bounded target is minimizer occurrence indexing and downstream overlap seeding/chaining, not an entire human assembly pipeline. The only candidate change is Hifiasm's existing minimizer window, 51 to 101. Both arms run the identical pinned binary with one thread and the same other arguments. Increasing the window samples fewer seeds and can lose sensitivity. This is a quality-risking parameter optimization, not a new algorithm or a proof of exactness.

The original 250–400 kbp tier was too slow for the complete matrix on this heavily loaded host. A single size-only pivot froze a new 60/100/80 kbp tier and new seeds before generating its reads. Candidate, coverage, read lengths, error models, repeat sizes, repetition counts and gates stayed fixed. The initial attempt is preserved; it is not included in the final matrix. Development is followed by repeat-rich and GC/error-shifted heldouts, without tuning on their results. Once published, these heldouts become regression inputs.

## Measured result

All 42 measured assemblies and six warmups completed. Indexed seed occurrences, summed across indexing passes, fell by 48.4–48.9%; these are a work proxy, not a count of all overlap comparisons. Median paired CPU reductions were **9.88% development, 6.76% repeat heldout, and 5.99% GC/error heldout**. Every A/B pair had byte-identical primary FASTA/GFA and all emitted GFA outputs. All quality and memory gates passed. **All three performance screening gates failed; no candidate was promoted.** Maximum A/A CPU deviations were 1.66%, 4.83% and 6.01%, respectively, so the smallest CPU change is especially uncertain.

The assemblies used **48.0–82.9 MiB peak RSS** and **3.80–11.61 CPU seconds** each. All 42 measured runs together used 285.20 CPU seconds versus 1,094.52 elapsed assembly seconds. QUAST and setup are additional. Median peak RSS A→B was 62.9→58.6, 69.5→63.2 and 64.5→55.8 MiB; these noisy process measurements include translation overhead. Both heldouts had 100% reference coverage, zero QUAST misassemblies and one full-length contig in both arms. The development case retained one reported relocation and duplication ratio 1.211.

Final details are in [the measured report](../experiment/REPORT.md), summary.json, case-table.json and trial-totals.json. baseline.json pins unchanged outputs, quality, resources, binaries and input hashes. Observed paired wall speedups were 1.381×, 1.131× and 1.069×, with A/A deviations up to 20.1%, 16.0% and 53.9%; those wall gains are not credible performance claims.

A full matrix has 42 measured assemblies and six excluded warmups: two A/A pairs and five A/B pairs per dataset. Assemblies run serially with fresh intermediate files; QUAST evaluates every output outside the assembly timer. Alternating AB/BA order, same-binary controls, CPU seconds, wall time, per-process peak RSS and seed counts are recorded. A five-second warmup profile contains unsymbolicated Rosetta frames; it does not establish a precise dominant-stage fraction.

**Timing caveat:** this eight-core ARM Mac had load averages around 60–85 from unrelated work and ran Hifiasm under Rosetta. Other jobs were not stopped. Interleaving cannot remove that contention, thermal effects or heterogeneous-core placement. Wall-time gains must not be advertised as product performance. CPU ratios and deterministic work-count reductions are exploratory diagnostics. Native idle-host replication is required even if a numerical screening gate passes.

## Accuracy and demonstration

QUAST tracks extensive/local misassemblies, reference base coverage, duplication, N50/NG50/NGA50, contigs, mismatch/indel rates and unaligned sequence. The gate rejects any deterioration in these metrics; missing or non-finite metrics fail closed. Memory growth is capped separately. Matching QUAST metrics is not treated as output identity: primary FASTA/GFA and all emitted GFA hashes are compared separately.

The real verifier control changes an internal DNA segment's orientation while preserving total length and N50. QUAST changes from zero to two structural errors, and the candidate is rejected. The public explainer in ../demo/genome-quality.html uses these measured control values: a viewer can flip the segment and see why a seemingly complete assembly can still be wrong. The blocks are schematic DNA intervals, not genes. This demonstrates trustworthy checking, not an optimization speedup.

The development baseline is not a perfect reconstruction. Its circular input produces duplicated closure sequence, and QUAST reports a relocation associated with its linear representation. Completeness can be 100% while duplication and structural metrics remain imperfect. We retain these scores rather than masking them or correcting output using the known reference. A domain reviewer should settle circular-assembly evaluation before public rankings. Reference base coverage is not gene/BUSCO completeness.

## Fit against the featured-project criteria

**Tangible progress: conditional.** This session builds the dependencies, fixes Python/QUAST compatibility and telemetry, exercises a deceptive negative control, and completes a frozen comparison. These are useful contributions. An existing parameter has little novelty, and a finite parameter sweep will exhaust easy gains. We have not yet demonstrated a sequence of accepted algorithm improvements.

**Hill climbing: not yet established.** A mature assembler has many interacting heuristics, repeated graph transformations and tie-breaking rules. Whole-project orientation is expensive (roughly 165,000 C++ source lines in this pin). A narrow kernel with captured input traces and exact differential tests could expose smaller steps: fewer allocations, redundant lookups, unnecessary sorts or improved data locality. Those are hypotheses for profiling, not defects found by this trial. A source-level contribution should preserve anchors, scores and ordering where required, then pass end-to-end heldouts. Approximate algorithms belong on a separate quality-versus-resource frontier.

**Public appeal: strong.** Reconstructing a genome from overlapping fragments is easy to explain as rebuilding a shredded book with repeated paragraphs. Show a fixed read set, reconstruction errors/completeness, and resource savings side by side. Keep the quality control visible so a faster but wrong assembly cannot win. Real nonhuman microbial examples would make this more vivid. No claims of cures, new biology or better human genomes follow from this toy benchmark.

**Home-PC feasibility: strong for this tier, not yet a universal onboarding result.** These synthetic workloads use only tens of MiB of assembler memory and seconds of CPU per assembly. Dependency download/build and compatibility took a substantial fraction of the trial; the first source build took 417 seconds on this contended host. Native Linux/x86 code paths have not been independently exercised. QUAST requires a compatible Python runtime; the preflight now detects that before expensive builds. Large genomes and real HiFi datasets remain untested.

**Agent intelligence: useful, with the central claim unproven.** Reasoning mattered for detecting a misleading length-only score, diagnosing the runtime incompatibility, separating CPU from wall time, preserving failed attempts, and recognizing circular-closure artifacts. The candidate itself could have been selected by a simple parameter sweep. This trial therefore does not show that stronger agents outperform cheaper agents or ordinary autotuning at algorithm discovery. A controlled comparison of subsequent sessions is needed.

**Potential scientific value: plausible but unvalidated.** An exact optimization of a frequently used assembly kernel could matter broadly. A synthetic miniature speedup may not transfer to real reads or larger repeat graphs. There is no novel algorithm, real-read replication or upstream acceptance in this package. The most credible current result is a reproducible experiment and bounded candidate/negative finding.

## What would change the recommendation

1. Replay on an idle native x86 machine, preserving pins, seeds and gates. Report resource variation and reject gains within noise; do not select the most favorable run.
2. Add a small public nonhuman long-read dataset with a suitable reference and provenance/license. Have a domain reviewer resolve circular-closure scoring and specify realistic repeat/error stress cases. Freeze new heldouts before tuning.
3. Profile and extract one expensive seeding/chaining operation with replayable traces and a readable exactness contract. Make its differential checker and end-to-end regression gate runnable in minutes. Keep the full assembler as the integration test.
4. Run three fresh 45-minute contributor sessions with comparable environments. A proposed launch gate is at least two independently reproduced useful source-level improvements or substantive counterexamples, with at least one accepted resource improvement and no quality regression. Record orientation time, attempted candidates, review effort and failures. This is a proposed criterion, not an achieved score.
5. Establish maintainer review capacity and demonstrate a one-command start on a second ordinary machine. Ownership is agreed; throughput and independent review are still unknown.

If these checks succeed, feature the scoped challenge as “make genome reconstruction more efficient while proving the pieces still fit.” Until then, it is a promising supporting research pilot, not evidence that donors can reliably move a public performance curve in their first session.

## Evidence and verification limits

The raw reports, commands, source snapshots, binary/input hashes and derived summaries are archived. Offline verification regenerates inputs, checks evidence integrity, recomputes quality/resource decisions and checks output identity. It does not authenticate timings independently or prove arbitrary-input equivalence. A fresh local clone can recheck these computations; independent full replay and maintainer scientific review remain outstanding. No external acceptance is implied by local tests passing.
