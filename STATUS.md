# Local pilot status

Completed the frozen starter experiment: 42 measured assemblies, six excluded warmups, one development dataset and two heldouts. All candidate outputs match the unchanged baseline byte for byte at the primary FASTA/GFA and all-GFA levels. All quality and memory gates pass. All three performance screens fail; no speedup is promoted. See reports/trial/ASSESSMENT.md and reports/experiment/REPORT.md.

Window 51→101 is an existing parameter change, not a novel algorithm. Indexed seed counts fell about 49%; exploratory CPU reductions were 6–10%. Severe host contention and Rosetta prevent a portable performance claim. The original larger config had only sizing warmups; its preserved incomplete attempt is separate from the fully measured 60–100 kbp starter tier.

The runnable harness has source/binary/input pins, actual QUAST positive and structural-error negative controls, fail-closed quality checks, A/A noise controls, paired timing, per-process peak RSS, source snapshots and an offline evidence verifier. Independent full replay, real nonhuman read validation, circular-closure evaluation review and repeatable source-level improvement remain open. Published holdouts are now regression inputs.

Recommendation: incubate; do not lead the inaugural featured lineup with the current broad assembler task. The next contribution is scoped in reports/trial/NEXT-SESSION.md. The user agreed to maintain the pilot and selected MIT for original code; weekly review capacity and scientific acceptance are still outstanding. The trial itself was LOCAL. The owner subsequently authorized a private GitHub repository and initial push at https://github.com/discoveryathome/genome-assembly. No hub PR or listing is authorized.

Final check: the 42-minute-26-second trial passed fresh-checkout evidence verification under Python 3.9.6, including explicit unchanged-baseline identity. All four task entry checks and Discovery structural validation pass. Corrupted evidence and a deliberately false baseline are rejected. See reports/trial/COMPLETION.json. These checks are author-run, not independent review.
