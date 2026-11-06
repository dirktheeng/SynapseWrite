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
