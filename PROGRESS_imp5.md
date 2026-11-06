# PROGRESS imp5

Base: main at b1e876b. Baseline build: page 3,787,439 bytes, gz weights 2,813,152.

## 1. Side scroll by wheel and by dragging the thumb
Why: PARITY Zoom row said the thumb cannot be dragged and the wheel does not move sideways.
What: glue now encodes the wheel's raw sideways delta (ev_a = deltaX+1000) and raw modifier bits (Ctrl 1, Shift 2), as it already did for mousedown; it interprets nothing.
Network: gen/imp5_wheel.py. In WH, zoom now keys on modifier bit 0 only; Shift (bit 1) on a wide page routes the vertical delta into the slide register hsv; a sideways delta at least as large as the vertical one does the same. Both go through V8_HS0, which clamps and repaints. A press on the thumb (the default branch of V8_HC) now holds v8dg with press x and slide; MV with v8dg sets hsv = slide at press + travel / k, k the same per zoom scale that draws the thumb; mouse up clears v8dg.
Run: test/imp5.js side: 8 passed, 0 failed first try (thumb 0..952 to 226..1178 on Shift+wheel 300; drag of 150 px moves thumb exactly 150 px; past the end clamps at 1261). Screenshot build/imp5_d1.png looked right.
