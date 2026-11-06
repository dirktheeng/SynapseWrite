"""Literal bytes of a minimal .docx. Static members use the zip stored method."""
import zlib,struct
XH=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
CT=XH+b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>'
RL=XH+b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
DR=XH+b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'
W_NS=b'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
NUMRUNS=20   # numId 1 is bullets; numId 2 up to 1+NUMRUNS are numbered lists that each restart
def _lvl(i,fmt,txt,left):
    return ('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="%s"/><w:lvlText w:val="%s"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="360"/></w:pPr></w:lvl>'%(i,fmt,txt,left)).encode()
def numbering():
    a=XH+b'<w:numbering '+W_NS+b'>'
    a+=b'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'+_lvl(0,'bullet','•'.encode('ascii','xmlcharrefreplace').decode(),720)+_lvl(1,'bullet','o',1440)+_lvl(2,'bullet','–'.encode('ascii','xmlcharrefreplace').decode(),2160)+b'</w:abstractNum>'
    a+=b'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="multilevel"/>'+_lvl(0,'decimal','%1.',720)+_lvl(1,'lowerLetter','%2.',1440)+_lvl(2,'lowerRoman','%3.',2160)+b'</w:abstractNum>'
    a+=b'<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    for i in range(NUMRUNS):
        a+=b'<w:num w:numId="%d"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'%(2+i)
    return a+b'</w:numbering>'
FILES=[(b'[Content_Types].xml',CT),(b'_rels/.rels',RL),(b'word/_rels/document.xml.rels',DR),(b'word/numbering.xml',numbering())]
STY=b'word/styles.xml'; DOC=b'word/document.xml'
def _def(d):
    c=zlib.compressobj(9,zlib.DEFLATED,-15); return c.compress(d)+c.flush()
def lh(name,crc,sz,us,m=8): return struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,m,0,0x21,crc,sz,us,len(name),0)+name
def static_part():
    "Static members (deflated at build time), then the local header of styles.xml with its crc and sizes left as a hole."
    b=b''
    for n,d in FILES: z=_def(d); b+=lh(n,zlib.crc32(d),len(z),len(d))+z
    at=len(b)+14
    b+=lh(STY,0,0,0)
    return b,at
def doc_header(): return lh(DOC,0,0,0)
STY_H=XH+b'<w:styles '+W_NS+b'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Carlito" w:hAnsi="Carlito"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
STY_T=b'</w:styles>'
def xml_parts():
    return (XH+b'<w:document '+W_NS+b'><w:body>',
            b'<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
R_CLOSE=b'</w:t></w:r>'
def central():
    out=[];off=0
    def cd(name,crc,sz,us,o): return struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,20,20,0,8,0,0x21,crc,sz,us,len(name),0,0,0,0,0,o)
    for n,d in FILES:
        z=_def(d); out.append(cd(n,zlib.crc32(d),len(z),len(d),off)+n); off+=30+len(n)+len(z)
    h=cd(STY,0,0,0,off)+STY
    out.append(h[:16]); out+=[('c1',i) for i in range(4)]; out+=[('s1',i) for i in range(4)]; out+=[('u1',i) for i in range(4)]; out.append(h[28:])
    h=cd(DOC,0,0,0,0)+DOC
    out.append(h[:16]); out+=[('c2',i) for i in range(4)]; out+=[('s2',i) for i in range(4)]; out+=[('u2',i) for i in range(4)]; out.append(h[28:42]); out+=[('o2',i) for i in range(4)]; out.append(h[46:])
    n=len(FILES)+2
    out.append(struct.pack('<IHHHH',0x06054b50,0,0,n,n))
    out+=[('end',i) for i in range(4)]; out+=[('o',i) for i in range(4)]
    out.append(b'\0\0')
    return out
