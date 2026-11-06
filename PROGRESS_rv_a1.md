# rv_a1 progress: application chrome look
## Baseline
Built page copied from /root/annword/build (rebuild needs 1.4 GB and is OOM killed when many agents build, first make.sh was killed after 5 min).
Captured every tab, menus and File screen with real clicks, viewed each. Findings:
- Insert: most buttons text only, 2x2/3x3/4x4 share one icon, shading swatches unlabeled inside Tables, Page Number nearly overflows.
- Layout: text only Portrait/Normal/etc, tiny plain - and + glyphs with no button shape, line values float as loose text, chevron touches Margins and Line labels, Page Break and Section share an icon, everything crammed into one Paragraph group.
- References, Review: Update Table and Delete Comment are text only and float.
- Title bar: search box text background (51,119,204) differs from box (68,119,187), a halo; on hover also. Search not centered, red PDF icon clashes with white icons.
- File: 12 px bold nav without icons, hover draws a blue box around the text, caption not centered.
- Ruler: ticks at 1/6, 1/2, 5/6 inch (uneven), stop at 6 in, and static so they ignore margins.
- Chevrons off center in their buttons. Status 100% one px above the left text.
- Scrollbar judged fine: current Word also hides arrows until hover. Adding arrows would change thumb scale and the drag test constant, not done.
## After first build
Build OK: 3,391,652 byte page, 2,461,755 edges. test/rv_a1.js 38/38. Viewed all tabs and File from the real build; they match the preview. Narrow margins now move the ruler scale. Next: full suites one at a time.
