# imp3 progress log
Started from master f0ade7f. Order: tier 1 find, zoom and view, ribbon and ruler, clipboard; tier 2; exact line heights; repaint cost.
Baseline build: 3,220,027 byte page, 444,066 neurons, 942,629 stored edges.

## Find across paragraphs
Typed ^p (as in Word) or a pasted newline is a paragraph mark in the query; replacement ^p splits. A query with a mark has one candidate start per paragraph (paragraph length minus the characters before the first mark), so a search costs a read per paragraph plus the compare. One matcher (IMP3_X, return table IMP3_XR) serves walker, counter and highlight; a query with no mark takes the old paths unchanged. First build failed: names xret, xb, xl, qmk collide with t3 and pdf registers; renamed. Second run: replace wrote NUL because RP3 passed R1 on a tick late; rule moved into RP3. test/imp3.js: 8/8. Screenshot imp3_find1 shows both matches tinted in both paragraphs, "2 found".
