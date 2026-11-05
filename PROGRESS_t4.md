# Tier 4 progress log
Baseline: 142,109 neurons, 1.70 M edges, 2.9 MB page; e2e 43/43 before any change.
## Dictionary
Source: npm wordlist-english 1.2.1 (MIT package, SCOWL data, permissive notice kept in gen/words_en.COPYRIGHT). Levels up to 60, all dialects, ASCII alphabetic: 79,339 words.
Merging identical subtrees gives 28,393 nodes and 61,952 edges, far smaller than a plain trie. Level 70 would be 46,767 nodes for mostly obscure words, so it was not used.
## Design decisions
- Token walks the automaton in lockstep with paint. C1 now loops on itself (one tick per char) so a one-tick token needs no hold neuron.
- Style word extended to 18 bits: ins 11, del 12, field kind 13-14, sup 15, sub 16, noProof 17.
- Button ids are scarce, so T4 buttons reuse ids scoped by tab (id + tab decides the command).
## Files
- Save: XML is emitted into OUTB, CRC computed on the way, then a greedy LZ77 plus fixed Huffman network writes the zip member. 400 paragraphs: 87,469 to 2,296 bytes; zip CRC passes and our own inflate re-reads it byte identically.
- Bug found by test: fldSimple keyword offset was 22, the attribute value starts at 23. Fixed.
- Reader: two zip passes, styles.xml first. cs is now an overlay on the paragraph style value, not a sum, so a style bit plus a direct bit cannot carry.
