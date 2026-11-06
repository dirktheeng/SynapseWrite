"""Strict package checker for saved .docx files: every XML part against the ISO 29500 transitional schemas,
content types and relationships resolved both ways. Word is not available, so this is the strictest stand-in here.
Usage: a5_validate.py file.docx ... ; exit status 1 on any finding."""
import sys,zipfile,posixpath,re,os
import lxml.etree as E
S='/mnt/skills/public/docx/scripts/office/schemas/'
ISO=S+'ISO-IEC29500-4_2016/'; OPC=S+'ecma/fouth-edition/'
_c={}
def schema(p):
    if p not in _c: _c[p]=E.XMLSchema(E.parse(p))
    return _c[p]
CT_BY='application/vnd.openxmlformats-officedocument.wordprocessingml.'
def check(fn):
    bad=[]; z=zipfile.ZipFile(fn)
    if z.testzip(): bad.append('zip crc '+z.testzip())
    names=z.namelist()
    if names[0]!='[Content_Types].xml': bad.append('[Content_Types].xml is not the first member: '+names[0])
    if len(set(names))!=len(names): bad.append('duplicate members')
    for i in z.infolist():
        if i.flag_bits&1: bad.append('encrypted flag '+i.filename)
    ct=E.fromstring(z.read('[Content_Types].xml'))
    for err in []: pass
    try: schema(OPC+'opc-contentTypes.xsd').assertValid(ct)
    except Exception as ex: bad.append('content types: %s'%ex)
    NS='{http://schemas.openxmlformats.org/package/2006/content-types}'
    dfl={d.get('Extension').lower():d.get('ContentType') for d in ct.findall(NS+'Default')}
    ovr={o.get('PartName'):o.get('ContentType') for o in ct.findall(NS+'Override')}
    for o in ovr:
        if o[1:] not in names: bad.append('override for missing part '+o)
    for n in names:
        if n=='[Content_Types].xml': continue
        if '/'+n not in ovr and n.rsplit('.',1)[-1].lower() not in dfl: bad.append('no content type for '+n)
    # relationships
    RN='{http://schemas.openxmlformats.org/package/2006/relationships}'
    reached=set()
    for n in names:
        if not n.endswith('.rels'): continue
        r=E.fromstring(z.read(n))
        try: schema(OPC+'opc-relationships.xsd').assertValid(r)
        except Exception as ex: bad.append('rels %s: %s'%(n,ex))
        base=posixpath.dirname(posixpath.dirname(n))
        ids=set()
        for x in r:
            if x.get('Id') in ids: bad.append('duplicate rel id %s in %s'%(x.get('Id'),n))
            ids.add(x.get('Id'))
            if x.get('TargetMode')=='External': continue
            t=x.get('Target'); t=t[1:] if t.startswith('/') else posixpath.normpath(posixpath.join(base,t))
            reached.add(t)
            if t not in names: bad.append('%s points to missing %s'%(n,t))
    for n in names:
        if n=='[Content_Types].xml' or n.endswith('.rels'): continue
        if n not in reached: bad.append('part not reached by any relationship: '+n)
    # main part content type, rels of ids used in document
    if ovr.get('/word/document.xml')!=CT_BY+'document.main+xml': bad.append('document.xml content type')
    for part,kind in (('word/styles.xml','styles'),('word/numbering.xml','numbering'),('word/settings.xml','settings'),('word/footnotes.xml','footnotes'),('word/endnotes.xml','endnotes'),('word/comments.xml','comments'),('word/fontTable.xml','fontTable')):
        if part in names and ovr.get('/'+part)!=CT_BY+kind+'+xml': bad.append('%s has content type %s'%(part,ovr.get('/'+part)))
    for n in names:
        if re.match(r'word/(header|footer)\d*\.xml',n):
            k='header' if 'header' in n else 'footer'
            if ovr.get('/'+n)!=CT_BY+k+'+xml': bad.append(n+' content type')
    if 'word/settings.xml' not in names: bad.append('no word/settings.xml (allowed by the schema; Word always writes one)')
    w=schema(ISO+'wml.xsd')
    for n in names:
        if not re.match(r'word/[^/]*\.xml$',n): continue
        try: doc=E.fromstring(z.read(n))
        except Exception as ex: bad.append('not well formed %s: %s'%(n,ex)); continue
        if not w.validate(doc):
            for er in list(w.error_log)[:8]: bad.append('%s line %d: %s'%(n,er.line,er.message[:300]))
    # id cross references Word refuses to open when broken
    doc=z.read('word/document.xml').decode()
    rels=z.read('word/_rels/document.xml.rels').decode() if 'word/_rels/document.xml.rels' in names else ''
    for rid in set(re.findall(r'(?:r:id|r:embed|r:link)="([^"]+)"',doc)):
        if 'Id="%s"'%rid not in rels: bad.append('document uses undefined relationship '+rid)
    def ids(part,tag):
        return re.findall(r'<w:%s [^>]*w:id="(-?\d+)"'%tag,z.read(part).decode()) if part in names else []
    fnids=set(ids('word/footnotes.xml','footnote'))
    for i in re.findall(r'<w:footnoteReference [^>]*w:id="(\d+)"',doc):
        if i not in fnids: bad.append('footnote reference %s has no note'%i)
    cids=set(ids('word/comments.xml','comment'))
    for i in re.findall(r'<w:commentReference [^>]*w:id="(\d+)"',doc):
        if i not in cids: bad.append('comment reference %s has no comment'%i)
    a=re.findall(r'<w:(?:ins|del) [^>]*w:id="(\d+)"',doc)
    if len(a)!=len(set(a)): bad.append('duplicate annotation ids in ins or del')
    # Word needs the separator notes if settings point at them, and a final paragraph in every cell
    if re.search(r'</w:tbl></w:tc>',doc): bad.append('table cell ends in a table with no paragraph')
    if re.search(r'<w:tc>(<w:tcPr>.*?</w:tcPr>)?</w:tc>',doc): bad.append('empty table cell')
    # grid columns against cells per row
    for tb in E.fromstring(doc.encode()).iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl'):
        WN='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        g=len(tb.find(WN+'tblGrid')) if tb.find(WN+'tblGrid') is not None else -1
        for tr in tb.findall(WN+'tr'):
            nc=0
            for tc in tr.findall(WN+'tc'):
                sp=tc.find(WN+'tcPr/'+WN+'gridSpan'); nc+=int(sp.get(WN+'val')) if sp is not None else 1
            if nc!=g: bad.append('table row has %d grid cells, grid has %d'%(nc,g))
    return bad
if __name__=='__main__':
    st=0
    for f in sys.argv[1:]:
        b=check(f); print(f,'OK' if not b else 'FINDINGS %d'%len(b))
        for x in b: print('   ',x)
        st|=bool(b)
    sys.exit(st)
