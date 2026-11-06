# Progress log: glyph network integration and more fonts (fonts branch)

## Start
Baseline master at 10efbe6 merged with glyphnet. Baseline build: 3,380,860 byte page, 419,462 neurons, 2.46M edges, gz 2,516,245.

## Plan after reading the code
The paint and layout FSM issues about 40 kinds of draws, including chains of thousands of one tick tokens in the ribbon. Stalling each site is impractical.
So the glyph unit is its own clock domain in the same network: a draw is a new port kind that copies its arguments, runs the glyph domain until its done neuron fires, then returns. That is the stall: the paint state does not advance while the generator runs. The engine gains about 15 lines and no application logic.
The hit path also lives in that domain, so the main network still spends one tick per glyph.
Row plane: the hit path reads the store one pixel row per tick into a single row plane, far fewer neurons than the old 24x28 and 60x64 planes.
Flush: the tag table holds an address, the store block header holds the key. A stale tag fails the key compare, so flush is only a bump pointer reset.

## Step 1: edge network replaces stored ink
Built gen/glyphnet.py as a GlyphUnit in domain 1 of the application network (nn.py gained Net.domain; engine gained port kinds 8 call, 9 domain marker, 10 read through index).
Bugs on the way, found by tracing registers around the failing tick: a port enable given as a two term expression silently used its first neuron (fired on every s1, zeroed bank cell 0); a held colour line loaded and cleared in the same tick stayed set (the glyph after a space drew white); the row counter kept +1 after each draw, so only the first glyph ever was one row high.
Weight file: gz was 3058 KB with two families, because each neuron's first target was an absolute index. New format: varint streams, deltas by position in the input list, bias and weight dictionaries, then per height thresholds instead of a per glyph tree, coordinates on a 1/1024 em grid, slopes to 9 significant bits, flatness 0.15 px at 36 pt. Same two families: gz 1340 KB, page 1,816,289 bytes (master 3,380,860).
Ink tree, face_program, the two coverage planes are gone. A single row plane with 180 columns replaces them.

## Step 2: interned style table
Cell = table index (bits 0 to 18) plus the five per character flags at the old positions (ins, del, field kind, no proof). The flags stay in the cell because track changes and fields set them per character and would otherwise intern on every keystroke. Record = 24 bits, same layout as the old cell for bold, italic, underline, color, strike, script, highlight; size field 7 bits, font field 3 bits. So 8 families is a hard limit of this record.
Record 0 is the default (size field 0 means 11 pt), which keeps every ins_st:0 and cs:0 as written.
The interner is a second small FSM in domain 1 (memo of the last value, then a linear scan), returning through the call port. 4096 records. Overflow: returns the caller's fallback index, so formatting is not applied, and the status bar says so.
A style port (kind 10) reads a cell and its record in the same tick, so paint and layout stay one tick per character.
