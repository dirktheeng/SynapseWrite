# PROGRESS imp6

Base: main at 041931a. Baseline build: page 3,791,181 bytes.

## 1. Zip CRC check on open
Why: PARITY .docx open row: no CRC check, so a corruption that still inflates to the stated size opens with wrong text.
What: gen/imp6_crc.py, group 'zip crc check'. After the dry inflate of the main part (IMP_V1 in a12_guard), the network reads the CRC from the central directory entry (offset 16), runs the inflated bytes at OUTB through the save CRC network (A7_CR, the four byte table walk), and continues to OP0 only if CRC plus stored CRC is all ones in both halves. Otherwise IMP_VF refuses with the message and keeps the document. A part cut at the output limit is not checked.
Run: test/imp6.js crc, first try 9 passed, 0 failed: a stored part with one changed byte and a deflated part with a wrong CRC field are both refused, the document stays and edits on; the right CRC opens, stored and deflated; a 400 paragraph file opens.
