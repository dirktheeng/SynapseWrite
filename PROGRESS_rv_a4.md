# Reviewer a4 progress log: functional gaps against Word in Tier 2 and 3
Started from 10efbe6. Read the memory map, nn.py, PARITY, Tier 1 to 3 logs.

## Findings before any change
Absent: format painter, clear formatting, change case, keep with next and keep lines, paragraph borders and shading, real tab characters and stops,
ruler dragging, right indent, merged cells, header rows, grid picker, page number formats. Tab key inserted 4 spaces.
Alpha ids are exhausted on Home (only 1 raw id could be argued free), so a new command needs another route.

## Plan and why
1. Extension id: raw 35 is only used in the find bar (y>=174). In the ribbon (y<150) alpha 235 now means "look at the pointer": regions in gen/rv_a4_btn.py
   pick the command in A4_X and also give each its own hover key in T1_HV1 (235+100*(i+1)). This removes the 8 bit limit for every tab with one id.
2. Slot cells past the comment text (3700+380=4080): 4084-4087 tab stops, 4090 keep next, 4091 keep lines, 4092 border bits, 4093 header row, 4094 right indent.
3. Keep with next: at the paragraph start, a walker sums heights of the chain of keep paragraphs plus the first two lines of the follower.
   A dirty follower is laid out on the spot by pointing the normal R2 path at it and returning through LF (A4_KL). Built in headings keep with next, as in Word.
4. Shading reuses the cell shade cell. Margins are repainted white per line, borders are 1 px rects. Same border and shade neighbours join as in Word.
