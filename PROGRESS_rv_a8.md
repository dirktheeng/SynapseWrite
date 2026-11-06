# Reviewer a8: load, payload, weight format, engine efficiency
Baseline 10efbe6: page 3,380,864 bytes, net.bin.gz 2,516,248, raw blob 17,589,641, 419,463 neurons, 2,457,201 edges.
Tool: test/rv_a8_load.js times load phases with CDP CPU throttling 1x, 4x, 6x. Machine is loaded, so take minimum of runs.

## Baseline phases at 6x (ms): wall 2478, domInteractive 1955, gunzip 383, first dispatch 117, wasm 2.5.
First guess was the HTML parser. A synthetic page with 3.3 MB of base64 costs only 170 to 450 ms at 6x (attribute 170, script text 360, JS string 450, see scratch ht.py).
So most of domInteractive was the glue's first statement: Uint8Array.from(atob(s),callback) runs a JS iterator and callback per byte.
Plain loop: 6x wall 2478 -> 1759. Plain loop plus payload in a data attribute rather than a JS string: 1362.

## Where the bytes are (gz of edge streams by source group, whole net)
glyph weights 1292 KB, pdf writer 659 KB (font bytes as token chain, reviewer a9 moved these to a bank ROM), spell 190 KB, glyph patch 75 KB, tier3 51 KB, ribbon 44 KB.
The glyph part belongs to the fonts agent and goes away with its branch, so the format is judged both with and without glyph groups.

## Format experiments on the edge streams (gz bytes)
old dz+wz 2,100,890 whole. First target relative to source, base 128: dz 948 KB. First target relative to previous neuron's first target: 746 KB. Weights: escape, base 128 and split byte planes all within 1%, kept base 128.
xz on the same body is 25% smaller, mostly long range matches and context. Rejected a custom entropy decoder: gunzip is native, a wasm range decoder would cost more CPU at load than the bytes save on a phone.

## Pruning
Duplicates (same act, bias, inputs): 3261 neurons. Dead (nothing depends on them): 4726 neurons, including those made dead by the duplicates. Never-firing analysis found only 2 dead states, PN0 and BR, and 7 edges, not worth a pass. Remaining never firing neurons are aligned plane cells.
Framebuffers at all 12 fbdump checkpoints pixel identical to baseline.

## Neuron numbering
The engine needs only a topological numbering with registers first, not layers. finish() now treats even lstart ranges as registers and odd ranges as feed forward (recurrent targets are those not above the source). See gen/rv_a8_order.py.
Three numberings through a cache model (engine copy with every neuron and synapse access run through a simulated 32 KB L1 and 512 KB L2). L1 misses, layer order / post order / creation order: paste 10128k / 5301k / 4604k, enter5 22858k / 20522k / 15802k, wheel5 11107k / 10113k / 7824k. Creation order kept. All pixel identical. It costs 180 KB gz on the whole net because glyph planes compress better in layer order (2.28 vs 2.47 MB), but is 18 KB smaller on the edges outside glyph groups, which is what remains after the glyph branch.

## Engine
One record per neuron (bias, acc, input start, output start, split, act) and one per synapse, so a visit touches one line rather than six. Cache model on top of creation order: paste 4604k -> 1962k L1 misses, enter5 15802k -> 7413k, wheel5 7824k -> 3805k, png 1406k -> 679k. Port enables nobody else reads numbered last: a further 5%. Wall clock on bench under load 15 could not separate it from the old layout, within noise; not worse.
Display copy moved into the engine (show): runs in compiled code from the first frame, where the JS loop started in the interpreter. Image shares wasm memory, no second copy in JS.

## Final, paired runs under load 30+ (min of 3, two rounds), ms
base / new: x1 3961 / 1447, x4 4096 / 1663, x6 3376 / 1914. Page 3,380,088 -> 3,315,624 bytes. Raw blob 17,589,641 -> 8,777,165. Neurons 419,463 -> 414,7xx. Pixel identical at 12 checkpoints.
Suites run while the machine was at load 30+: failures that came and went between runs were download timeouts and short waits.
