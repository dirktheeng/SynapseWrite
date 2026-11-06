# cmp1: compact and fast

## Baseline (bd00ad8)
- Page 3,795,433 bytes; net.bin.gz 2,819,120 (streams 2.02 MB gz, PDF font ROM 523 K gz).
- Connections F 1,078,331 + R 928,667 = 2,006,998. Neurons 533,330.
- By group (F+R): glyph weights (outline edges) 1,556,433 (77.6 %), glyph metrics 58 K, compiled control 52 K, pixel records 49 K, docx crc 42 K, glyph unit 40 K.
- Glyph unit stats: 217,735 outline edges, 187,252 knots, 6,130 programs.
- Edges per event (node, test/eprof.js, same events as bench.js): type at end 2,489 / 3,021; wheel 823,788; select all 885,724; left 827,430; type at top 115,653; down 78,246; enter 827,845; undo 882,102; paste 1900 4,659,376; init 1,629,134.
- a01_format open: 9,912,561 edges, 466,299 ticks. docx reader 4.12 M (Huffman decode one bit per tick: X_D3 1.08 M, GBL 0.66 M, PX1 0.37 M), ramp bank 1.16 M, compiled control 1.08 M, outline edges 1.04 M, coverage 0.71 M, glyph unit 0.70 M.
- Repaint per char: state C1 fan 69, glyph unit fin fan 66.
- t4 (browser): wheel 839,439, select all 900,090, jump 840,728, enter 839,065, undo 875,096 edges.

## 1. Monotone chains for outline edges
Why: an outline was one neuron per edge plus one threshold per vertex height, so knots were as many as edges.
What: gen/glyphnet.py chains(): each contour is cut where its height turns or runs flat; one neuron carries a whole
chain: x = X0*s + m0*dy(Y0) + sum of slope changes times relu(dy(Yk)). Thresholds only at chain ends; the ramps
relu(dy) are shared within a face by the duplicate merger.
Runs:
- First try: 212 K neurons, 1.01 M connections, page 2.77 MB, but 0, 3, 8, o drawn thin at 11 pt. Math checked
  in python against edges: identical. CHMAX sweep: 1, 2, 4 fine; 6 nearly; 10, 16 bad: drift grows with chain length.
- Cause 1: vertex heights are not on the height map's 1/256 steps, so dy errs at each vertex and slopes up to 300
  turn that into pixels. Fix: yq() moves vertices onto those steps (qchains).
- Cause 2: when snapping, each band of the height map stretches by its own factor; a chain through an overshoot
  band drifts by that factor times its travel. Splitting at every knot: correct, 3.22 MB, 88 K chains. Splitting
  only at the bases of the overshoot bands (0, x height, cap): 3,059,077 bytes, 247 K neurons; screenshots
  side by side with the base (digits, o, gbdpqs, @&%, OQCGS at 11 pt) match.

## 2. FLOPs (coordinator's new measure, test/flops.js)
Per char of a repaint, three pulled wires read a lazy list as long as the size table (69 sizes): rise (2 per size,
269,660 work in select all), kern (269,660) and adv (140,700).
- rise: the size sums are plain wires read behind the sup and sub flags.
- kern: the per size gates now read behind kanyb, with an offset so the gated sum stays positive.
- adv: sel_sum(), groups of 8 sizes, each behind a gate on the group's one hot sum.
Run: select all 9.74 M to 7.34 M FLOPs, jump 10.28 to 7.34, enter 10.42 to 7.46, undo 10.95 to 7.82,
wheel 12.23 to 8.70, click 12.48 to 8.95, typing repeat 80,866 to 70,499, background layout 1.07 G to 0.76 G.
Page 3,059,481.

## 3. More size and FLOP work
- sel_sum through the size tree's groups of 8 (SZG: tree nodes three levels above the leaves), for adv and kern;
  the script size path behind vflag. Select all 7.34 to 6.75 M, jump 6.61 M, wheel 7.83 M.
- rv_tabw (tab width, 29 stop thresholds) read behind the tab flag: select all 6.42 M, jump 6.21 M, enter 6.27 M,
  undo 6.58 M, wheel 7.34 M, click 7.59 M, typing repeat 68,363, background layout 546 M.
- SLOPE_BITS 9 to 8: wtab 68 K to 51 K gz; page 3,059,209 to 2,991,165. Title style text compared with the base: same.
- Huffman decode: limit and offset per code length in tables (hb+320+2*len) built in BE; X_D3 reads one cell
  pair per bit and no longer carries first and index. a01_format open 9,225,834 to 8,981,411 edges, same ticks.
- getn: a field the current byte still holds is taken in one tick. 8,981,411 to 8,936,561 edges, 466,299 to 454,606 ticks.
- Two builds byte identical; audit 67 of 67.

## 4. Merge of main (features) and glyph quality pass
- Merged /root/readme main. Conflicts in gen/app.py: size_hot now uses F1_SPLIT (small caps and hidden text);
  sel_sum follows the same split (script or small capital size behind step(vflag+F1_SMCL+F1_HID), hidden text no size)
  and adv keeps F1_SPX. PROVENANCE.md taken from main (generated). After merge: page 3,001,761.
- Chain starts on a 1/512 em grid: page 2,988,005.
- Screenshots at 9, 11 (Carlito, Arimo, Tinos), 14 (Open Sans, Caladea, Caveat) and 36 pt, side by side with the
  base: Arimo and Tinos 0 and the Caladea o were drawn thin. Python model of the snapped map (scratch sim.py) found
  why: a vertex lying exactly on a knot did not split the chain, and other bands (xh to cap, cap to ascent) also stretch.
- Fix: split at every knot (also at a vertex on a knot), then rejoin pieces while the summed net travel over band
  height stays under 0.3 (under about 0.15 px of drift at any size). Worst vertex error over all ASCII at 12 to 24 ppem
  is now on the order of the old per edge model's own end mismatch (old 2.2 px, new 4.2 px, both on Arimo @).
  Screenshots again: all lines match the base by eye; 212 pixels differ by more than 40 levels on the whole screen.
- Page 2,919,845; neurons 235,022; connections F 455,438 + R 649,784 = 1,105,222 (base 2,006,998, minus 45 percent).
- FLOPs: typing repeat 80,866 to 69,995 (0.87); select all 9.74 M to 6.48 M; jump 10.28 to 6.29; Enter 10.42 to 6.35;
  undo 10.95 to 6.66; wheel 12.23 to 7.44; click 12.48 to 7.68; background layout 1.07 G to 0.56 G.
- a01_format open 9,912,561 to 8,928,039 edges (target 7 M not reached).
