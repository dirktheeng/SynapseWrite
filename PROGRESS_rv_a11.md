# rv_a11: compliance with the rules
- Read glue.js and engine.c line by line. Glue held: key name table, lower casing under Ctrl, Ctrl+V/C/X tests, pointer type state, button test on moves, touch diff with newline test and sentinel, touch scroll clamp and accumulator, file names, paste cap.
- Added gen/rv_a11_input.py: a raw event layer under IDLE. Direct cooked kinds still work so the headless tools are unchanged.
- Glue now sends key code units, length, modifier bits, button mask, pointer type unit, touch y and count, field text. Commands come back from neurons.
