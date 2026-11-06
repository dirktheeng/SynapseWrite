# Merge 3 progress log: Tier 3 into master (Tier 4 + performance + Tier 1 + Tier 2)
Started merge; conflicts in PARITY, app.py, docx_read, nn, pdf_write, ui, e2e.
Plan and why:
- Bank map rebuilt with a comment at its head. FILE 53M, BANK 61M. Save goes to SAVEB (32M up); everything above it only matters while reading, so a large save may run over it. RELB, AUXB moved out of the OUTB range, since a big document would overwrite them during its own scan. ZT, HFB, FORD, FORD2, RIDB, FNB moved out of MKT, STY and the hash table.
- Slot: Tier 3's FNHT 3693 overlapped PIND; moved to 3683. Comment text back to 380 characters at 3700..4080, since FNT is gone. Reader comment store stride 512 to hold them.
- Undo: Tier 1 op 6, Tier 2 op 7, Tier 3's swap is op 8.
- Button: T3 commands raw 9 under TB(9,tab) for tabs 1..4, no hover highlight as all share the id. Moved: table tools x 770, header and footer x 1030 on Insert; orientation, margins, sections x 964 on Layout; Update Table and Delete Comment under their tabs' first buttons.
- Tier 1's margin menu now writes Tier 3's section record (Moderate is a new section op 8), so margins save. t1_mo, t1_mv gone.
- Zip: one table driven writer: zstatic (deflated at build), zdyn/zdend (work buffer then deflate network), pictures stored. All names and CRC in ZT, central directory from ZT.
- Member walk on open: rels, footnotes, comments, numbering, styles, document, by ztarget.
- First line offset stored as 0 or PFO+offset, pf_val at use. Registers t2d and t1_pdd held negative constants, which cannot be overwritten correctly: r-relu(r+M-M) leaves a negative r in place. Both now hold 1000+delta.
- Name collisions found by reading: off_, nv2, fsi, pfc, trk, lx, zret, TB, qpw, qph, zo.
First full e2e after the merge: 201/201 (before merge 3 additions). Added: PDF footnotes, table of contents dots and numbers, table rules in pixel coordinates.
Found while merging: T3 tests clicked one spot twice within 500 ms, which is now a double click, so they wait 550 ms. A non boolean register in a rule condition (wdd, value 2) fired two rules at once; now a step. Removed the memset of the bank in engine alloc, as fresh wasm memory is zero and 244 MB was being touched at load. Fixtures p_a.png and p_rgb.png are now in test/fixtures and copied by make.sh.
Final run on a fresh build: e2e 210/210, tier2 49/49, t3_table 9/9, t3_pic 9/9, t3_misc 13/13, t4_docx 18/18, t4_pdf 7/7, roundtrip 3 true, t16 picture 325 ms, audit no failures. t4 latency: type at end 1.1 ms, wheel 15.8, select all 18.6, jump to top 18.3, type at top 3.6, down 2.9, enter at top 20.3, undo 18.7; paste of 1900 paragraphs 1358 ms is not an interactive measure. Page 3,318,180 bytes, 413,206 neurons, 2,372,568 eager edges.
