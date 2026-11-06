# Look, pointer, glyph spacing and paste log

## Baseline
3,320,055 byte page, 413,207 neurons, 2.37M edges. build/look_before.png saved. Critique: no File tab, cramped color grid on Home, "Hom e" spacing, no page shadow, plain status bar, icons scaled 2x.

## Glyph spacing, measured
Carlito has no bytecode (no fpgm), so PIL renders through the FreeType autohinter. At 12 px the m outline ends at 8.82 of a 9.59 advance but hinted ink ends at 8, and static UI layout rounds that advance to 10, leaving a 2 px hole before the next letter. Document pens are unrounded but ink is still the narrowed hinted ink. Cause: hinted ink narrower than the unhinted advance. Fix plan: unhinted 8x oversampling with x-height snap in y only.

## Pointer
Sprite written by a patch port (never touches alpha), so hit tests always read true ids. Every event: DISP restores saved colors; HALT and T1_HH go through PT0 (read id and color, save colors), PTH walk of table and picture zones, PTD draw; HF and T1_HF are the final states carrying side outputs. New engine port kind 7 copies a screen block to or from the bank.
Bugs: register names collided with pdf_write (ptv) and docx_read (bs), renamed mp_* and bstg. Thumb hover redraw used old color. Thumb overflowed into the status bar, once hidden by the full width status wipe; now clamped.

## Look
Ribbon rewritten in ui.py; every command has its own id per tab, position based T2_HIT and T3_BTN dispatch removed. Page shadow from nested rectangles. File screen on register bstg. Added palette bit weight 5 for ribbon gray 243.

## Tests
test/remap.js maps old ribbon coordinates to new controls via build/ui_ids.json; assertions untouched. Bug: BIU points applied on every tab (30 false failures), fixed.
