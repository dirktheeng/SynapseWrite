# ---- provenance record, written at build: every sub-network, its purpose, and the generator files that wrote it ----
PURPOSE={
 'bank and port wiring':'The memory, image and event ports and their shared wires.',
 'raw event interpretation':'Turns raw browser events (key name code units, button masks, pointer types, field text, touch positions) into cooked events and browser commands.',
 'file output command':'Selects the length, data base and file name the glue saves.',
 'glyph network':'Selects and addresses a character cell for drawing.',
 'glyph patch':'Assembles glyph coverage into a color patch for the patch port.',
 'glyph metrics':'Character advance and kerning trees.',
 'glyph weights (font outlines)':'Font outlines stored as weights, drawn by the glyph network.',
 'shared control registers':'Editor state registers and the selection order comparators.',
 'event dispatch':'Routes each cooked event to its handler; timer, wheel and move handling.',
 'pointer':'Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen.',
 'character maps':'Unicode to internal code tables and back (Windows-1252 block).',
 'key handling':'Maps each key and modifier to its editing command.',
 'screenshot hit test':'Reads object ids from the screen image and maps a click to a document position; also the blink tick check of the screen against the line table.',
 'edit primitives':'Character and paragraph insert and delete with undo logging.',
 'undo':'Undo and redo walkers over the log.',
 'range walker':'Walks a selection for copy, cut, delete and formatting.',
 'find and replace':'Search automaton over the document and replace.',
 'paste':'Inserts clipboard text with paragraph splitting.',
 'layout and paint':'Walks paragraphs, places lines and words, draws text, selection, pictures.',
 'spell dictionary':'Word list stored as an automaton in weights, with word marks.',
 'line breaking':'Greedy line breaker and alignment.',
 'chrome':'Autoscroll, caret, scrollbar and status bar.',
 'ribbon actions':'Maps button ids to commands.',
 'docx writer':'Writes the document XML parts.',
 'docx reader':'Unzips, inflates and parses document XML.',
 'png reader':'Decodes PNG files to pixel words.',
 'pdf writer':'Writes PDF objects, text and pictures.',
 'tier 4 features':'Tracked changes, fields, equations, mail merge.',
 'docx deflate':'LZ77 with fixed Huffman compression for the zip container.',
 'docx reader tier 4':'Reads tracked marks and fields.',
 'tier 2':'Styles, paragraph commands, lists and typed sizes.',
 'docx reader tier 2':'Reads styles, numbering, run and paragraph properties.',
 'tables':'Table scan, insert, row and column edits, shading, border hit zones and drag.',
 'sections':'Section records, breaks and page setup.',
 'zip container':'Zip member table, central directory, and table XML for saving.',
 'docx reader tier 3':'Reader additions for parts walking.',
 'pdf tables':'PDF page size, table rules and shading.',
 'pictures':'Picture handles, resizing by resampling, PNG writing, and reading pictures from a file.',
 'notes and balloons':'Wrapped text, comment balloons and footnotes.',
 'headers and footers':'Header and footer strings and their edit bar.',
 'table of contents':'Builds and updates the table of contents.',
 'docx writer tier 3':'Writes section properties, tabs, markers, comments, notes, headers and footers.',
 'docx reader notes':'Reads note, comment and header parts.',
 'tier3':'Remaining tier 3 commands and undo op 8.',
 'late commands':'File screen, table and picture ribbon commands, clipboard notices.',
 'screen check':'Compares one line of the screen id plane against the line table on each blink tick and repairs by repainting.',
 'ribbon display list':'Token chain whose weights hold each ribbon draw item.',
}
_edges={g_:sum(len(net.inp[i_]) for i_ in ids_) for g_,ids_ in net.groups.items()}
_gfiles={}
for (g_,f_),k_ in net.src.items(): _gfiles.setdefault(g_,{})[f_]=k_
_prov={k_:dict(neurons=len(v_),inputs=_edges[k_],purpose=PURPOSE.get(k_,''),files=_gfiles.get(k_,{})) for k_,v_ in net.groups.items()}
json.dump(dict(neurons=len(net.act),edges=len(dst),layers=c['L'],states=len(fsm.states),groups=_prov),open('../build/provenance.json','w'),indent=1)
with open('../PROVENANCE.md','w') as _f:
    _f.write('# Provenance of the SynapseWrite network\n\nWritten by gen/rv_a11_prov.py at every build, from net.groups. Every weight comes from the listed generator files; none is trained, fitted or searched.\n\n')
    _f.write(f'{len(net.act)} neurons, {len(dst)} edges, {c["L"]} layers, {len(fsm.states)} control states.\n\n| Sub-network | Purpose | Generator files (neurons) | Neurons | Inputs |\n|---|---|---|---|---|\n')
    for k_,v_ in _prov.items():
        _f.write('| %s | %s | %s | %d | %d |\n'%(k_,v_['purpose'] or 'NO PURPOSE RECORDED',', '.join(f'gen/{a_} ({b_})' for a_,b_ in sorted(v_['files'].items(),key=lambda q:-q[1])),v_['neurons'],v_['inputs']))
