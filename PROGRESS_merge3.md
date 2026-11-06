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
