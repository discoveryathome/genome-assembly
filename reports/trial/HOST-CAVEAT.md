# Host contention observed

At 20:09:28 UTC, uptime reported load averages 60.49 / 39.04 / 27.83 on an eight-core Mac. A read-only process snapshot showed unrelated Lean processes and other active applications. These jobs were not stopped or modified. The two compiler jobs were our only concurrent heavy pilot work, and benchmarks will start after builds finish.

This is not an idle controlled-performance environment. Alternating same-binary A/A and A/B repetitions, CPU seconds and deterministic seed counts can diagnose some effects but do not remove contention, thermal or heterogeneous-core effects. Raw timings are LOCAL exploratory evidence, not a publishable speedup claim. An idle native-x86 replay is required before promoting any performance improvement. Quality and artifact-identity checks are unaffected by this caveat unless A/A output itself proves unstable.
