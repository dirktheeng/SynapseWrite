# Reviewer a10 progress: consolidating data-format and text networks

Baseline at 10efbe6: 419,463 neurons, 2,457,201 edges, 2410 FSM states, 2,516,217 gz bytes.
Biggest groups: pdf writer 130,347 (a token per embedded font byte), spell dictionary 90,510, tier3 15,492.

Regression: test/a10_regress.js runs one long event script through the engine only and prints a screen hash after
each step and a hash of each saved docx and PDF. Function is unchanged only if every hash equals the baseline's.
Baseline: total ticks 4,676,921, edges 1,166,866,562. save 426,728 ticks 135.8M edges. pdf 552,909 ticks 321.4M edges.

## Plan, largest first
1. String ROM and one literal emitter, block copy where no CRC is needed. Return dispatch without the priority chain.
2. One number writer (T2_NV, NUM7, T3_NZ, two digit patch loops, a t4 one).
3. Spell automaton as a memory table, walked one read per letter, instead of a neuron per node and per edge.
4. Window comparator as a threshold bank over packed words instead of three neurons per pattern char.
5. Little endian field writer, lookup tables for inflate, deflate and color.

## Log
- Literal ROM, numbers, spell, comparator each passed the hash regression (PDF compared with the embedded fonts masked: pdf_fonts.py subsets carry the build time, so two builds differ there regardless).
- Field writer first failed: the big endian shift used a weight of 2^39 on bit 31, which nn.compile treats as a gate enable, and low bytes were lost. The regression hashes caught it. Fixed with an intermediate gate. Worth knowing for anyone writing large weights.
- CO0 threshold bank: a 31 input step pushes (over PULLMAX), making the whole bank push. Using the sum directly keeps it lazy.
