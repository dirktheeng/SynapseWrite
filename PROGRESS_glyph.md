# Progress log: directly programmed glyph network (glyphnet branch)

Started from 6b81d32. Rules: no training, fitting, or search. Weights are written from font outlines.

## Step 0: read nn.py, rom.py, app.py glyph section, engine.c
Building the shipping network in the background so its real glyph cost can be measured.

## Step 1: network written and running on the real engine
gen/glyphnet.py builds a Net; one tick is one sample line (K=4 per pixel row). Glyph register, tree over outline heights,
edge neurons with line coefficients, interval coloured slot wires, shared ramp bank R_q=relu(q-x), winding sum, clamp, accumulate, block write port.
Bugs found by tracing: height and address registers kept a residue from the final tick. Fixed by gating on done.
First look: ROM shows the wide gaps after m (hinted ink narrower than the unhinted advance). The network does not.

## Step 2: stem width trial
Rounding stem widths to whole pixels makes 11 and 13 pt thin and 14 pt suddenly heavy (1 px then 2 px). Keeping the true width with only the left edge
on a whole pixel ("light") keeps weight even across sizes, so this is the default. wround=True keeps the other form.
Synthetic bold and slant: added a one shear layer and a one offset control written from the family's stems and italic angle.

## Step 3: measurements (test/glyphnet_measure.py, build/glyph/measure.json, averaged over 4 faces of both families, ASCII)
Error is sum |a-b| / reference ink, against an 8x8 point sampled unhinted raster.
pt: network no snap / network snapped / ROM: 9: .036/.204/.286, 11: .032/.177/.350, 13: .031/.168/.258, 14: .028/.150/.226, 18: .021/.147/.235, 36: .014/.078/.125.
Snapped error is intended movement. ROM 13 pt uses the same PIL rule; the ROM does not ship that size.
First draw work (visits+reads+edges): 11 pt 24.4K, 36 pt 135K. Quiet machine, Carlito regular: 9 pt 173, 11 pt 157, 13 pt 194, 14 pt 201, 18 pt 358, 36 pt 647 us per glyph, including JS injection.
Shipping: C1 tick 1533 work per glyph including layout, about 8.4 us per glyph in a 1000 glyph repaint (8.44 ms). Idle tick 7 work.
Weights: Carlito 157.7K, Caladea 191.7K ASCII; ROM ink for the same 425K, 460K. All 224 codes without composites: 404K, 487K against ROM 739K, 788K.
gz: Carlito 416 KB, Caladea 495 KB ASCII; 971 KB, 1149 KB all codes. Shipping 2472 KB; shipping with no ink and no plane 1184 KB, so ROM ink costs about 1288 KB.
Synthetic against real: bold .19 Carlito, .45 Caladea; italic .52 to .55 Carlito, .81 to .93 Caladea, as the real italics are different letterforms.
Hit path bug: neurons read only by ports became pull neurons and never fired; fixed with net.keep. Hit path: 11 pt 7 us, 732 work, 36 pt 66 us, 5413 work.

## Step 4: looking at the sheets
Carlito 11 to 18 pt snapped is clean and even; no gaps after m. 9 pt with x snap has uneven spacing, y only is better.
Caladea with x snap at 11 pt: m reads like rn. y only looks good. Use x snap for Carlito upright only, at 11 to 18 pt.
Crossbars (e, H) stay gray over two rows, as only metric heights are snapped.
Synthetic Q at 18 pt shows a gray streak under the next letters: a miter defect in the synthetic path only.
