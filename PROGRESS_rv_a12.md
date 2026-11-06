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
- Scratchpad was shared with other agents and a frozen build vanished; baseline now lives in build/base (pre fix commit) with its own build.
- Background runs must use the tool's background mode; a detached subshell gets stopped after minutes (cost one run).
- Reader fixes: zip validator before reset, ip and ob limits in inflate, dist check, PNG chunk bounds, zero size PNG refused, sentinel after each member so unterminated attribute scans stop, tick budget steering the token out through guarded back edges (reach 1458 states, 707 edges).
- Invariant false alarms traced to the test: start text was undoable (fixed by opening a saved file first), Ctrl+Home leaves a small residual scroll (normalized by wheel), early stop on no-op undo (fixed count).
- Real invariant bug: Ctrl+Enter wrote PBRK without a log entry. Redo lost the page break. Now logged as op 6.
- Undo of a user merge restored the second paragraph with the first paragraph's properties (shrunk trace: style, Delete at the end of the paragraph, undo). The second paragraph's properties now go through the existing op 8 metadata chain before the merge.
