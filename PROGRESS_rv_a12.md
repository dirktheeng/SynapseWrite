# Reviewer a12: robustness log

## Tools built
- host/engine_check.h, compiled with -DCHECK into build/engine_check.wasm. The shipped wasm stayed byte identical after adding the hooks (cmp checked).
- gen/a12_dbg.py writes build/dbg.bin: every AND argument that is not trivially boolean, plus the region map.
- test/fuzz_lib.js (world), test/fuzz.js (seeded event fuzz), test/fuzz_inv.js (invariants), test/fuzz_caps.js (limits), test/fuzz_selftest.js (planted faults must be seen).

## Firefox and WebKit
Tried: PLAYWRIGHT_BROWSERS_PATH=build/pwx playwright install firefox webkit. Blocked by the egress proxy (403 on playwright.download.prss.microsoft.com). Chromium untouched.

## Runs
- First trace, seed 100 mix: HANG in GBR after a flipped docx: the bit reader runs past the end of the file forever.
- Seed 1003 mix: HANG in CC1: dist code above 29 gives dist 0, min(copy,dist)=0, the copy never advances.
