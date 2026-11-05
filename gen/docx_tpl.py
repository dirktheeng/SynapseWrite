"""Literal bytes of a minimal .docx. Static members use the zip stored method."""
import zlib,struct
CT=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
RL=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
FILES=[(b'[Content_Types].xml',CT),(b'_rels/.rels',RL)]
DOC=b'word/document.xml'
def lh(name,crc,sz): return struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,0x21,crc,sz,sz,len(name),0)+name
def static_part():
    b=b''; 
    for n,d in FILES: b+=lh(n,zlib.crc32(d),len(d))+d
    at=len(b)+14
    b+=lh(DOC,0,0)
    return b,at,None
def xml_parts():
    return (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>',
            b'<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
P_OPEN=b'<w:p><w:pPr><w:jc w:val="'
P_MID=b'"/></w:pPr>'
R_CLOSE=b'</w:t></w:r>'
def central(docstart):
    out=[];off=0
    def cd(name,crc,sz,o): return struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,20,20,0,0,0,0x21,crc,sz,sz,len(name),0,0,0,0,0,o)
    for n,d in FILES:
        out.append(cd(n,zlib.crc32(d),len(d),off)+n); off+=30+len(n)+len(d)
    hdr=cd(DOC,0,0,off)+DOC
    out.append(hdr[:16]); out+=[('c',i) for i in range(4)]; out+=[('s',i) for i in range(4)]; out+=[('s',i) for i in range(4)]
    out.append(hdr[28:])
    out.append(struct.pack('<IHHHH',0x06054b50,0,0,3,3))
    out+=[('end',i) for i in range(4)]; out+=[('o',i) for i in range(4)]
    out.append(b'\0\0')
    return out
