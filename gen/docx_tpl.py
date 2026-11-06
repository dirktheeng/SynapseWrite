"""Literal bytes of the styles and numbering parts of a .docx. The zip container is written by the network."""
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
def _def(d):
    c=zlib.compressobj(9,zlib.DEFLATED,-15); return c.compress(d)+c.flush()
STY_H=XH+b'<w:styles '+W_NS+b'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Carlito" w:hAnsi="Carlito"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
STY_T=b'</w:styles>'
def settings():
    "word/settings.xml: Word writes this part in every file. The separators are the ones footnotes.xml defines; compatibility mode 15 is current Word."
    return XH+b'<w:settings '+W_NS+b'><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'
