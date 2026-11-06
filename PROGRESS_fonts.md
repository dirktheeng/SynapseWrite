# Progress log: glyph network integration and more fonts (fonts branch)

## Start
Baseline master at 10efbe6 merged with glyphnet. Baseline build: 3,380,860 byte page, 419,462 neurons, 2.46M edges, gz 2,516,245.

## Plan after reading the code
The paint and layout FSM issues about 40 kinds of draws, including chains of thousands of one tick tokens in the ribbon. Stalling each site is impractical.
So the glyph unit is its own clock domain in the same network: a draw is a new port kind that copies its arguments, runs the glyph domain until its done neuron fires, then returns. That is the stall: the paint state does not advance while the generator runs. The engine gains about 15 lines and no application logic.
The hit path also lives in that domain, so the main network still spends one tick per glyph.
Row plane: the hit path reads the store one pixel row per tick into a single row plane, far fewer neurons than the old 24x28 and 60x64 planes.
Flush: the tag table holds an address, the store block header holds the key. A stale tag fails the key compare, so flush is only a bump pointer reset.
