# PROGRESS feat2

Branch feat2 in /root/feat2, from main fd5f1e0. Task: more equation structures (drawn, edited, saved and read as OMML), then the PDF gaps of PARITY.md.

## Baseline (fd5f1e0, measured here)
- ./make.sh: page build/index.html 3,806,957 bytes.
- test/a5_docx.js a01 open: 9,943,745 edges (limit 10 M).
- test/flops.js with build/engine_count.wasm: saved to /tmp/claude-0/flops_base.json for comparison with docs/flops_baseline.json.

## Step 1: equation structures
Design: the rv_a6 record (one character, code 300 and up, standing for a 64 cell record) gains kinds 3 to 7, chosen by keywords in the linear form, so the existing scan, delete and insert, layout, paint, writer and PDF dispatch carry them:
- `root(n)(x)` kind 3: root with an index. `sum(a)(b)`, `prod(a)(b)`, `int(a)(b)` kind 4: n-ary with lower and upper limit stacked. `hat( bar( tilde( dot( vec(` kind 5: accents. `left( left[ left| right) right] right|` kind 6: delimiters, each its own record, drawn as tall as its line, so they grow around a fraction, sum or matrix between them. `mat(a&b)(c&d)` kind 7: two row matrix.
- Record cell 6 holds the sub kind, cell 7 the symbol width. Why: no new memory region; EQT and its 690 records are unchanged.
- Writer: OMML m:rad with m:deg, m:nary (chr, limLoc undOvr, sub, sup, then m:e holding the math that follows), m:acc with chr, m:d (begChr, endChr) whose m:e holds the math up to the closing record, m:m with m:mr and m:e per column. Open delimiters and sums are a stack in one register (two bits a level); a closing delimiter closes the sums inside it first; the end of the math zone closes the rest; a stray closing delimiter writes nothing, so the XML always nests.
- A delimiter or n-ary is never made the base of a script (it would break nesting).
- Reader: all math tags now go through two prefix patterns, '<m:' and '</m:' (the second already existed as a threshold pair), and are told apart in their own states (gen/feat2_eqrd.py). Why: the shared window comparator costs every tag of every file; this removes the 13 math patterns from it. Each structure is typed back as its linear form, then the scan at </m:oMath> builds the records, so a saved file reopens to the same records.
- PDF: the sum sign and integral are stroked paths, the product sign rects, accents paths or rects, delimiters curves or lines as tall as the line.
- First build: "state defined twice": my sub-state names collided with the internal names of _ptext and _qdraw; renamed with an underscore. Second build ok, page 3,826,521 bytes.
- Probe (scratch script, typed `A root(3)(x+1) and sum(i=1)(n) k and hat(v) bar(y) vec(F) tilde(a) dot(b) left( (a)/(b) right) mat(a&b)(c&d) z`, Equation): screen and PDF (pdftoppm at 96 dpi) both show every form; viewed zoomed. qpdf clean. Saved XML has the expected elements. Sum sign in PDF touched its upper limit: moved its top down one pixel.
- test/feat2.js eq, first run 19/24: the image checks read the ruler (region started too high); the reopened screen differed by the closing parenthesis of a delimiter typed open (saved closed, so it reads back closed: now asserted on its own and the pixel check covers the closed forms); "undo brings it back" compared whole screens and the caret moved (now: the same math saved, and at most 2 differing columns); PDF delimiter strokes are antialiased (threshold 200). Then 25/25.
- rv_a6_eq.js 9/9. a5_docx: open of a01 9,931,697 edges (was 9,943,745): the reader's two prefix patterns replaced 13 math patterns in the shared window.

## Step 2: PDF gaps
- Small caps: a small capital run is its own chunk (the network's small capital flag joins the chunk test) and takes the script size, as on screen.
- Character spacing: the chunk's spacing is written as `Tc` before BT when it differs from what is in force (reset per page), as pixels to two decimals (floor networks give the whole and hundredths parts; registers hold offsets, since they keep no negatives).
- Run shading: after the chunk, `q /M gs r g b rg x y w h re f Q` with the exact color (three decimals), as highlight is drawn.
- Double strike: two 1 pixel lines at 3 and 7 above the baseline.
- Links: each printed chunk of an external link records a box (region 'feat2 PDF link boxes' 1376000-1377000, 200 per page). Each page now has a third object, its /Annots array, written after its content stream: URI actions with the target unescaped (&amp; to &) and PDF string escapes; rects in points. The page tree steps by three objects.
- First build: an undefined state name (F2P_A6), fixed. First run of test/feat2.js pdf 7/10: -10 twips was printed as no spacing (G_ of a negative value is zero; now built from nonnegative terms); the test's regex for /Rect did not allow the line breaks of qpdf --qdf; pdftotext splits letters spaced 3 pt apart, so the spaced word is now measured from the line start to the plain word. Then 10/10. Viewed build/feat2/effects_pdf.png zoomed: small capitals, two strike lines, spaced letters, yellow shade, link underline all as on screen.

## Numbers (after step 2)
- Page 3,832,385 bytes (base 3,806,957, +25,428).
- Two builds byte identical (cmp).
- test/flops.js: every event within +0.88% of docs/flops_baseline.json (main itself is +0.88% on background layout; feat2 adds at most 0.03% over main).
