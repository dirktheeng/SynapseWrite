# rv_a11: compliance with the rules
- Read glue.js and engine.c line by line. Glue held: key name table, lower casing under Ctrl, Ctrl+V/C/X tests, pointer type state, button test on moves, touch diff with newline test and sentinel, touch scroll clamp and accumulator, file names, paste cap.
- Added gen/rv_a11_input.py: a raw event layer under IDLE. Direct cooked kinds still work so the headless tools are unchanged.
- Glue now sends key code units, length, modifier bits, button mask, pointer type unit, touch y and count, field text. Commands come back from neurons.
- Build 2: unified image row and block copy into one port (pixel word cell, alpha never touched, network paints ids first). Clip1 now means rows cut at the bottom, so the engine has no zero special case. Pixel read takes x and y as two neurons. Packed word order flipped to the screen's own in png reader, png writer, pdf writer.
- Audit run against the pre-change glue and engine: 18 checks fail, as they should. New code 67 of 67.
- Screen check first read the right end of each line: 22 false alarms in 31 ticks, because lines leave id 0 at the right. Dump of the line table showed the left end is always 1. Moved there: 0 false alarms in the test, damage repaired.
- t3_pic 'resize redo' failed twice on my build (one pixel column at x=319, frame color vs black caret, so a blink phase difference); baseline clone passed once. Comparing runs under load.
