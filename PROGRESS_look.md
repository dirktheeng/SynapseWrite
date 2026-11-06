# Look, pointer, glyph spacing and paste log

## Baseline
3,320,055 byte page, 413,207 neurons, 2.37M edges. build/look_before.png saved. Critique: no File tab, cramped color grid on Home, "Hom e" spacing, no page shadow, plain status bar, icons scaled 2x.

## Glyph spacing, measured
Carlito has no bytecode (no fpgm), so PIL renders through the FreeType autohinter. At 12 px the m outline ends at 8.82 of a 9.59 advance but hinted ink ends at 8, and static UI layout rounds that advance to 10, leaving a 2 px hole before the next letter. Document pens are unrounded but ink is still the narrowed hinted ink. Cause: hinted ink narrower than the unhinted advance. Fix plan: unhinted 8x oversampling with x-height snap in y only.
