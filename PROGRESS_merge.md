# Merge log: a6 and a7 onto integ (fonts + a1..a5)
## region()
Added region(name,start,end,space='bank') to gen/nn.py; it asserts no two declared ranges overlap in one space. Declared the bank map in app.py from the brief and the constants; slot cell offsets use space='slot'. Checked by hand that an overlap raises. a9's ROM and a10's ROM not taken, so not declared.
## a6 decisions
- Math mark: one definition, is_math(D) in app.py: family MATHFAM=1 (Caladea, raw field MATHRAW=128) AND flag nop. All three uses in a6 are boolean via is_math. Consequence: Caladea text with noProof set reads as math on save. Same conflation as a6's own design under old styles; recorded as a known limit.
- Reader: _eqstyle could not return a cell in one tick under interning. It now interns the record during the state and hands flags over; state A6E_IS inserts with ROUT+flags. oret is set before A6E_IS. m:r now uses ics:t2ps and resets rnop like w:r.
- _qst records use rom.lit(9) and MATHRAW. a6's size literal 9 is the old index for 9 pt.
- Style cells: all decode sites moved to rs, RSC, RSR. A6S_TD and A6S_IG1 waiting states removed, a read lasts one tick.
- PDF: OROOT=3+3*NFC, FIRST=OROOT+1. Catalog /Outlines names OROOT. /F6 replaced by the name of FACES.index((1,0,1)), marked used in PUS at A6Q_P1. ExtGState added before the per face font resources. A6P_B0 chains to A4_QL rather than T2_PM, so a4 borders still draw. qhl stays on PD_F.
- Menu: decode width 21 in T1_M0, T1_MK, T1_MR; rows 12 (a3), 9,10,11 (a4), 20 (a6).
- Keys: ContextMenu is 141 (undefined in cp1252, so no typed character can reach it). 138 and 140 are Windows-1252 letters, and 136 is Insert.
- Right click, both a3 and a6 built it: a6's glue contextmenu dispatch removed. RVA3_CM2 keeps a3's menu for a selection or a click past the word's end; otherwise it asks A6S_0 with a6cm. A word with nothing to offer goes to a3's menu through A6S_NO, so right click always opens one. Menu key on a correct word opens a3's menu at the caret. Spelling off also goes to a3's menu.
- Duplicate a5 and a6 math text: a5 read m:t as plain text, a6 reads it as equation characters. Kept a6, removed a5's rule.
- a5 regression found by a4.js (borders and shading survive reopen): a5 gated w:shd on a5tcp, which dropped a4's paragraph shading. Now tcPr, or in document.xml outside tblPr and outside a cell.
- SVr: a6em close first, then a4 tab, then math (a tab never counts as math), then fields, merge field, default.
- Dictionary persists: glue reads localStorage to e.bset at load, and copies h.dsave cells with e.bget when commanded.
## a6 test edits
- rv_a3.js 'menu select all then bold': 'abc' to 'cat', since a flagged word now gets suggestions; intent unchanged.
- rv_a6_eq.js: Control+Home before the two reference images, since open leaves the caret at the document start.
- a5_docx.js: 72 pt regex now 144 per the brief; math text check strips tags, since math is written one m:r per character.
## a6 test runs
t4_docx 18/18, t4_pdf 7/7, tier2 49/49, rv_a6 6/6, rv_a6_pdf 4/4, rv_a6_track 17/17, rv_a6_eq 7/9 then 9/9 after the test edit, rv_a3 48/49 then 49/49, e2e 210/210 (before the shading fix), a4 49/50 then 50/50 after the shading fix, a5_docx see below.
