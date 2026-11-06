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
# List formats: marker table (0 decimal, 1 letters, 2 roman), capitals, opening and closing character, bullet, menu label.
LFMT=[(0,0,0,46,0,'1. 2. 3.'),(0,0,0,41,0,'1) 2) 3)'),(0,0,40,41,0,'(1) (2) (3)'),(1,0,0,46,0,'a. b. c.'),(1,0,0,41,0,'a) b) c)'),(1,1,0,46,0,'A. B. C.'),(1,1,0,41,0,'A) B) C)'),
 (2,0,0,46,0,'i. ii. iii.'),(2,0,0,41,0,'i) ii) iii)'),(2,1,0,46,0,'I. II. III.'),(2,1,0,41,0,'I) II) III)'),(0,0,0,0,0,'1 2 3'),
 (0,0,0,0,127,'\x7f Round bullet'),(0,0,0,0,111,'o Circle'),(0,0,0,0,150,'\x96 Dash'),(0,0,0,0,62,'> Arrow'),(0,0,0,0,42,'* Star'),(0,0,0,0,183,'\u00b7 Dot'),(0,0,0,0,167,'\u00a7 Section')]
FMTRUNS=8    # numIds per format, so numbers can restart as the screen's do
def _fmtlvl(f):
    tb,up,pre,suf,bul,_=f
    if bul: return 'bullet',{127:'&#8226;',150:'&#8211;',183:'&#183;',167:'&#167;',62:'&gt;'}.get(bul,chr(bul))
    fm=(['decimal','upperLetter' if up else 'lowerLetter','upperRoman' if up else 'lowerRoman'])[tb]
    return fm,(chr(pre) if pre else '')+'%%%d'+(chr(suf) if suf else '')
def numbering():
    a=XH+b'<w:numbering '+W_NS+b'>'
    a+=b'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'+_lvl(0,'bullet','•'.encode('ascii','xmlcharrefreplace').decode(),720)+_lvl(1,'bullet','o',1440)+_lvl(2,'bullet','–'.encode('ascii','xmlcharrefreplace').decode(),2160)+b'</w:abstractNum>'
    a+=b'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="multilevel"/>'+_lvl(0,'decimal','%1.',720)+_lvl(1,'lowerLetter','%2.',1440)+_lvl(2,'lowerRoman','%3.',2160)+b'</w:abstractNum>'
    n0=b'<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    for i in range(NUMRUNS):
        n0+=b'<w:num w:numId="%d"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'%(2+i)
    b=b''
    for i,f in enumerate(LFMT):
        fm,tx=_fmtlvl(f); ab=2+i
        a+=b'<w:abstractNum w:abstractNumId="%d"><w:multiLevelType w:val="multilevel"/>'%ab+b''.join(_lvl(l,fm,(tx%(l+1) if '%' in tx else tx),720*(l+1)) for l in range(3))+b'</w:abstractNum>'
        for k in range(FMTRUNS):
            b+=b'<w:num w:numId="%d"><w:abstractNumId w:val="%d"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'%(NUMRUNS+2+i*FMTRUNS+k,ab)
    return a+n0+b+b'</w:numbering>'
def _def(d):
    c=zlib.compressobj(9,zlib.DEFLATED,-15); return c.compress(d)+c.flush()
STY_H=XH+b'<w:styles '+W_NS+b'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Carlito" w:hAnsi="Carlito"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
STY_T=b'</w:styles>'
def settings():
    "word/settings.xml: Word writes this part in every file. The separators are the ones footnotes.xml defines; compatibility mode 15 is current Word."
    return XH+b'<w:settings '+W_NS+b'><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'
