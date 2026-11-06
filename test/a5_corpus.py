"""Deterministic .docx corpus for the fidelity review. python-docx files, with raw XML where it has no API.
Usage: a5_corpus.py OUTDIR. Every text carries a unique marker word (Mnnn) so lost content can be counted."""
import sys,os,io,copy,struct,zlib,zipfile,re
import docx
from docx.shared import Pt,Inches,RGBColor,Cm
from docx.enum.text import WD_BREAK,WD_ALIGN_PARAGRAPH as A,WD_COLOR_INDEX as HC,WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.enum.section import WD_SECTION,WD_ORIENT
from docx.oxml.ns import qn,nsdecls
from docx.oxml import parse_xml,OxmlElement
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
docx.Document.__init__
def png(w,h,c=(200,40,40)):
    raw=b''.join(b'\0'+bytes(((x*c[0]//w)&255,(y*c[1]//h)&255,c[2]))*1 if False else b'\0'+b''.join(bytes((x*255//w,y*255//h,c[2])) for x in range(w)) for y in range(h))
    def ch(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
    return b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b'')
def jpeg():
    from PIL import Image
    b=io.BytesIO(); Image.new('RGB',(120,80),(30,120,200)).save(b,'JPEG'); b.seek(0); return b
def save(d,n): d.save(os.path.join(OUT,n+'.docx'))
def W(xml): return parse_xml(xml.replace('<w:','<w:',1).replace('>',' '+nsdecls('w')+'>',1) if 'xmlns:w' not in xml else xml)
# 01 plain runs and formats
d=docx.Document(); d.add_heading('M101 Format sampler',0)
p=d.add_paragraph('M102 plain ');r=p.add_run('M103 bold');r.bold=True;p.add_run(' ');r=p.add_run('M104 italic');r.italic=True;p.add_run(' ');r=p.add_run('M105 under');r.underline=True
p=d.add_paragraph();
for sz in (8,9,10,11,12,14,16,18,20,24,28,36,48,72):
    r=p.add_run('M1%d '%(10+sz)); r.font.size=Pt(sz)
p=d.add_paragraph('M106 centered');p.alignment=A.CENTER
p=d.add_paragraph('M107 right');p.alignment=A.RIGHT
p=d.add_paragraph('M108 justified '*12);p.alignment=A.JUSTIFY
p=d.add_paragraph();r=p.add_run('M109 Courier');r.font.name='Courier New';r=p.add_run(' M110 Times');r.font.name='Times New Roman';r=p.add_run(' M111 Arial');r.font.name='Arial'
p=d.add_paragraph('M112 fancy "quotes" & <angle> — dash € café éè αβγ 中文 \U0001F600 end')
save(d,'a01_format')
# 02 tables
d=docx.Document(); t=d.add_table(2,3); t.style='Table Grid'
for i in range(2):
    for j in range(3): t.cell(i,j).text='M2%d%d start table'%(i,j)
d.add_paragraph('M201 between')
t=d.add_table(3,3); t.style='Light Grid Accent 1'
for i in range(3):
    for j in range(3): t.cell(i,j).text='M3%d%d styled'%(i,j)
d.add_paragraph('M202 merge')
t=d.add_table(4,4); t.style='Table Grid'
for i in range(4):
    for j in range(4): t.cell(i,j).text='M4%d%d'%(i,j)
t.cell(0,0).merge(t.cell(0,1)); t.cell(1,2).merge(t.cell(3,2)); t.cell(2,0).merge(t.cell(3,1))
d.add_paragraph('M203 twelve columns')
t=d.add_table(2,12); t.style='Table Grid'
for i in range(2):
    for j in range(12): t.cell(i,j).text='M5%d%02d'%(i,j)
d.add_paragraph('M204 cell paragraphs')
t=d.add_table(2,2); t.style='Table Grid'
c=t.cell(0,0); c.text='M601 first para'; c.add_paragraph('M602 second para'); c.add_paragraph('M603 third para')
c=t.cell(0,1); c.text='M604'; r=c.paragraphs[0].add_run(' bold'); r.bold=True
c=t.cell(1,0); c.text='M605 shaded'; c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:val="clear" w:color="auto" w:fill="FFC000"/>'%nsdecls('w')))
t.cell(1,1).text='M606 '+'long cell text '*30
d.add_paragraph('M205 long table')
t=d.add_table(120,3); t.style='Table Grid'
for i in range(120):
    t.cell(i,0).text='M7%03d'%i
d.add_paragraph('M206 after')
t=d.add_table(1,2); t.cell(0,0).text='M207 table at end'; t.cell(0,1).text='M208'
save(d,'a02_tables')
# 03 lists
d=docx.Document()
for s,x in (('List Bullet','M301'),('List Bullet 2','M302'),('List Bullet 3','M303'),('List Number','M304'),('List Number','M305'),('List Number 2','M306'),('List Number 3','M307'),('List','M308'),('List Continue','M309')):
    d.add_paragraph(x+' item',style=s)
d.add_paragraph('M310 body')
np_=d.part.numbering_part.element
absn=parse_xml('<w:abstractNum %s w:abstractNumId="77"><w:multiLevelType w:val="multilevel"/><w:lvl w:ilvl="0"><w:start w:val="3"/><w:numFmt w:val="upperRoman"/><w:lvlText w:val="%%1)"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl><w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="upperLetter"/><w:lvlText w:val="(%%2)"/><w:lvlJc w:val="left"/></w:lvl><w:lvl w:ilvl="4"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%%1.%%2.%%5"/><w:lvlJc w:val="left"/></w:lvl></w:abstractNum>'%nsdecls('w'))
np_.insert(0,absn)
np_.append(parse_xml('<w:num %s w:numId="77"><w:abstractNumId w:val="77"/></w:num>'%nsdecls('w')))
for lv,x in ((0,'M311'),(0,'M312'),(1,'M313'),(4,'M314'),(0,'M315')):
    p=d.add_paragraph(x+' custom'); p._p.get_or_add_pPr().append(parse_xml('<w:numPr %s><w:ilvl w:val="%d"/><w:numId w:val="77"/></w:numPr>'%(nsdecls('w'),lv)))
save(d,'a03_lists')
# 04 headings
d=docx.Document()
d.add_paragraph('M401 Title',style='Title'); d.add_paragraph('M402 Subtitle',style='Subtitle')
for i in range(1,10): d.add_heading('M41%d Heading level'%i,i); d.add_paragraph('M42%d body'%i)
d.add_paragraph('M403 quote',style='Quote'); d.add_paragraph('M404 intense',style='Intense Quote'); d.add_paragraph('M405 caption',style='Caption')
p=d.add_paragraph();p.add_run('M406 emphasis',style='Emphasis');p.add_run(' M407 strong',style='Strong')
save(d,'a04_headings')
# 05 pictures
d=docx.Document()
d.add_paragraph('M501 before'); d.add_picture(io.BytesIO(png(200,100)),width=Inches(2))
d.add_paragraph('M502 jpeg next'); d.add_picture(jpeg(),width=Inches(2))
p=d.add_paragraph('M503 text before pic '); p.add_run().add_picture(io.BytesIO(png(60,60,(10,200,10))),width=Inches(0.6)); p.add_run(' M504 text after pic')
d.add_paragraph('M505 in table'); t=d.add_table(1,2); t.cell(0,0).paragraphs[0].add_run().add_picture(io.BytesIO(png(40,40)),width=Inches(.5)); t.cell(0,1).text='M506'
p=d.add_paragraph('M507 big'); d.add_picture(io.BytesIO(png(1400,900)),width=Inches(6))
d.add_paragraph('M508 after')
save(d,'a05_pictures')
# package surgery helper
def patch(src,dst,edit=None,add=None,ct=None,rels=None):
    z=zipfile.ZipFile(src); o=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
    for i in z.infolist():
        b=z.read(i.filename)
        if edit and i.filename in edit: b=edit[i.filename](b.decode()).encode()
        if i.filename=='[Content_Types].xml' and ct: b=b.decode().replace('</Types>',ct+'</Types>').encode()
        if i.filename=='word/_rels/document.xml.rels' and rels: b=b.decode().replace('</Relationships>',rels+'</Relationships>').encode()
        o.writestr(i.filename,b)
    for k,v in (add or {}).items(): o.writestr(k,v)
    o.close()
NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
XH='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
def bodyfile(n,body,add=None,ct=None,rels=None,base=None):
    tmp=os.path.join(OUT,'_tmp.docx'); (base or docx.Document()).save(tmp)
    def ed(x): return re.sub(r'<w:body>.*?(<w:sectPr.*</w:body>)',lambda m:'<w:body>'+body+m.group(1),x,flags=re.S)
    patch(tmp,os.path.join(OUT,n+'.docx'),{'word/document.xml':ed},add,ct,rels); os.remove(tmp)
def P(t): return '<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>'%t
# 06 footnotes and endnotes
def note(k,i,t): return '<w:%s w:id="%d"><w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:%sRef/></w:r><w:r><w:t xml:space="preserve"> %s</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve"> bold part</w:t></w:r></w:p></w:%s>'%(k,i,k,t,k)
FN=XH+'<w:footnotes %s><w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote><w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>%s</w:footnotes>'%(NS,''.join(note('footnote',i,'M60%d note text'%i) for i in range(1,5))+'<w:footnote w:id="5"><w:p><w:r><w:t>M605 para one</w:t></w:r></w:p><w:p><w:r><w:t>M606 para two</w:t></w:r></w:p></w:footnote>')
EN=XH+'<w:endnotes %s><w:endnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:endnote><w:endnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p></w:endnote>%s</w:endnotes>'%(NS,note('endnote',1,'M611 endnote text'))
body=''.join('<w:p><w:r><w:t xml:space="preserve">M61%d para</w:t></w:r><w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="%d"/></w:r><w:r><w:t xml:space="preserve"> M62%d tail</w:t></w:r></w:p>'%(i,i,i) for i in range(1,6))+'<w:p><w:r><w:t xml:space="preserve">M631 endnote here</w:t></w:r><w:r><w:endnoteReference w:id="1"/></w:r></w:p>'
bodyfile('a06_notes',body,{'word/footnotes.xml':FN,'word/endnotes.xml':EN},'<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/><Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/>','<Relationship Id="rId91" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/><Relationship Id="rId92" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes" Target="endnotes.xml"/>')
# 07 comments
d=docx.Document()
p1=d.add_paragraph('M701 commented'); d.add_comment(p1.runs,text='M702 comment body',author='Ann Example',initials='AE')
p2=d.add_paragraph('M703 start '); r1=p2.add_run('M704 mid'); r2=p2.add_run(' M705 end'); d.add_comment(r1,text='M706 partial',author='Bo')
d.add_comment(r2,text='M707 second on para',author='Cy')
c=d.add_comment(d.add_paragraph('M708 long').runs,text='M709 '+'long comment '*50,author='Di')
c.add_paragraph('M710 second comment paragraph')
d.add_paragraph('M711 end')
save(d,'a07_comments')
# 08 sections
d=docx.Document(); d.add_paragraph('M801 first portrait');
s=d.add_section(WD_SECTION.CONTINUOUS); d.add_paragraph('M802 continuous '*30)
s=d.add_section(WD_SECTION.NEW_PAGE); s.orientation=WD_ORIENT.LANDSCAPE; s.page_width,s.page_height=s.page_height,s.page_width; d.add_paragraph('M803 landscape '*40)
s=d.add_section(WD_SECTION.NEW_PAGE); s.orientation=WD_ORIENT.PORTRAIT; s.page_width,s.page_height=Inches(8.27),Inches(11.69); s.left_margin=Inches(.5); s.right_margin=Inches(2); s.top_margin=Inches(2); d.add_paragraph('M804 a4 odd margins '*40)
s=d.add_section(WD_SECTION.ODD_PAGE); c_=s._sectPr.find(qn('w:cols'));
if c_ is None: c_=OxmlElement('w:cols'); s._sectPr.append(c_)
c_.set(qn('w:num'),'3'); c_.set(qn('w:space'),'360'); d.add_paragraph('M805 three columns '*80)
save(d,'a08_sections')
# 09 headers and footers
d=docx.Document(); s=d.sections[0]; s.header.paragraphs[0].text='M901 default header'; s.footer.paragraphs[0].text='M902 default footer'
s.different_first_page_header_footer=True; s.first_page_header.paragraphs[0].text='M903 first header'; s.first_page_footer.paragraphs[0].text='M904 first footer'
d.settings.odd_and_even_pages_header_footer=True; s.even_page_header.paragraphs[0].text='M905 even header'; s.even_page_footer.paragraphs[0].text='M906 even footer'
p=s.footer.add_paragraph('M907 page '); p._p.append(parse_xml('<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>'%nsdecls('w'))); p._p.append(parse_xml('<w:r %s><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'%nsdecls('w'))); p._p.append(parse_xml('<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>'%nsdecls('w'))); p._p.append(parse_xml('<w:r %s><w:t>1</w:t></w:r>'%nsdecls('w'))); p._p.append(parse_xml('<w:r %s><w:fldChar w:fldCharType="end"/></w:r>'%nsdecls('w')))
for i in range(60): d.add_paragraph('M91%02d body paragraph '%i*3)
s2=d.add_section(WD_SECTION.NEW_PAGE); s2.header.is_linked_to_previous=False; s2.header.paragraphs[0].text='M908 second section header'
t=s2.footer.add_table(1,2,Inches(4)) if False else None
d.add_paragraph('M909 section two')
save(d,'a09_headers')
# 10 tracked changes
A1='w:author="Ann" w:date="2024-05-01T10:00:00Z"'
body=('<w:p><w:r><w:t xml:space="preserve">M1001 keep </w:t></w:r><w:ins w:id="1" %s><w:r><w:t>M1002 inserted</w:t></w:r></w:ins><w:del w:id="2" %s><w:r><w:delText xml:space="preserve">M1003 deleted</w:delText></w:r></w:del></w:p>'%(A1,A1)
+'<w:p><w:pPr><w:rPr><w:ins w:id="3" %s/></w:rPr></w:pPr><w:r><w:t>M1004 paragraph mark inserted</w:t></w:r></w:p>'%A1
+'<w:p><w:pPr><w:rPr><w:del w:id="4" %s/></w:rPr></w:pPr><w:r><w:t>M1005 paragraph mark deleted</w:t></w:r></w:p>'%A1
+'<w:p><w:r><w:rPr><w:b/><w:rPrChange w:id="5" %s><w:rPr><w:i/></w:rPr></w:rPrChange></w:rPr><w:t>M1006 format changed</w:t></w:r></w:p>'%A1
+'<w:p><w:pPr><w:jc w:val="center"/><w:pPrChange w:id="6" %s><w:pPr><w:jc w:val="right"/></w:pPr></w:pPrChange></w:pPr><w:r><w:t>M1007 para change</w:t></w:r></w:p>'%A1
+'<w:p><w:moveFrom w:id="7" %s><w:r><w:t>M1008 moved from</w:t></w:r></w:moveFrom><w:moveTo w:id="8" %s><w:r><w:t>M1009 moved to</w:t></w:r></w:moveTo></w:p>'%(A1,A1)
+'<w:p><w:ins w:id="9" %s><w:del w:id="10" %s><w:r><w:delText>M1010 ins then del</w:delText></w:r></w:del></w:ins></w:p>'%(A1,A1)
+P('M1011 end'))
bodyfile('a10_tracked',body)
# 11 hyperlinks and fields
HY='http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink'
body=('<w:p><w:r><w:t xml:space="preserve">M1101 see </w:t></w:r><w:hyperlink r:id="rIdH1" w:history="1"><w:r><w:rPr><w:color w:val="0000FF"/><w:u w:val="single"/></w:rPr><w:t>M1102 external link</w:t></w:r></w:hyperlink><w:r><w:t xml:space="preserve"> M1103 after</w:t></w:r></w:p>'
+'<w:p><w:hyperlink w:anchor="bm1"><w:r><w:t>M1104 internal</w:t></w:r></w:hyperlink></w:p><w:p><w:bookmarkStart w:id="0" w:name="bm1"/><w:r><w:t>M1105 target</w:t></w:r><w:bookmarkEnd w:id="0"/></w:p>'
+'<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> HYPERLINK "http://example.org" </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>M1106 field link</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
+'<w:p><w:r><w:t xml:space="preserve">Page </w:t></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>7</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r><w:r><w:t xml:space="preserve"> M1107 of date </w:t></w:r><w:fldSimple w:instr=" DATE \\@ &quot;M/d/yyyy&quot; "><w:r><w:t>1/2/2020</w:t></w:r></w:fldSimple></w:p>'
+'<w:p><w:fldSimple w:instr=" REF bm1 "><w:r><w:t>M1108 simple ref</w:t></w:r></w:fldSimple></w:p>'
+'<w:p><w:fldSimple w:instr=" AUTHOR "><w:r><w:t>M1109 author</w:t></w:r></w:fldSimple></w:p>'
+'<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/></w:docPartObj></w:sdtPr><w:sdtContent><w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>M1110 Contents</w:t></w:r></w:p><w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:hyperlink w:anchor="bm1"><w:r><w:t>M1111 entry</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>3</w:t></w:r></w:hyperlink></w:p><w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>'
+'<w:p><w:sdt><w:sdtPr/><w:sdtContent><w:r><w:t>M1112 inline sdt</w:t></w:r></w:sdtContent></w:sdt><w:smartTag w:uri="x" w:element="y"><w:r><w:t xml:space="preserve"> M1113 smart</w:t></w:r></w:smartTag></w:p>'
+P('M1114 end'))
bodyfile('a11_links',body,None,None,'<Relationship Id="rIdH1" Type="%s" Target="http://example.org/" TargetMode="External"/>'%HY)
# 12 tabs and breaks
d=docx.Document()
p=d.add_paragraph('M1201 tab\tM1202 two\tM1203 three')
p=d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Inches(2),WD_TAB_ALIGNMENT.CENTER); p.paragraph_format.tab_stops.add_tab_stop(Inches(5),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS); p.add_run('M1204 l\tM1205 c\tM1206 r')
p=d.add_paragraph('M1207 line'); p.add_run().add_break(); p.add_run('M1208 after break'); p.add_run().add_break(WD_BREAK.PAGE); p.add_run('M1209 after page break')
p=d.add_paragraph('M1210 col'); p.add_run().add_break(WD_BREAK.COLUMN); p.add_run('M1211 after column')
p=d.add_paragraph(); p.add_run('M1212 hard'); p._p.append(parse_xml('<w:r %s><w:noBreakHyphen/><w:t>nb</w:t><w:softHyphen/><w:t>sh</w:t><w:cr/><w:t>M1213 cr</w:t><w:sym w:font="Wingdings" w:char="F0E0"/></w:r>'%nsdecls('w')))
d.add_page_break(); d.add_paragraph('M1214 end')
p=d.add_paragraph('M1215 keep'); p.paragraph_format.keep_with_next=True; p.paragraph_format.page_break_before=True; p.paragraph_format.widow_control=False
p=d.add_paragraph(''); p=d.add_paragraph('   M1216 leading spaces   and   gaps   ')
save(d,'a12_tabs')
# 13 nested tables
d=docx.Document(); d.add_paragraph('M1301 before')
t=d.add_table(2,2); t.style='Table Grid'; t.cell(0,0).text='M1302 outer'
n=t.cell(0,1).add_table(2,2); n.style='Table Grid'; n.cell(0,0).text='M1303 inner'; n.cell(0,1).text='M1304'; n.cell(1,0).text='M1305'; n.cell(1,1).text='M1306'
t.cell(0,1).add_paragraph('M1307 after inner')
t.cell(1,0).text='M1308'; t.cell(1,1).text='M1309'
n2=n.cell(1,1).add_table(1,1); n2.cell(0,0).text='M1310 third level'
d.add_paragraph('M1311 after')
save(d,'a13_nested')
# 14 theme fonts and colors
TH='w:asciiTheme="%s" w:hAnsiTheme="%s" w:eastAsiaTheme="%s" w:cstheme="%s"'
def tr(t,x): return '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'%(x,t)
body=('<w:p>'+tr('M1401 major ','<w:rFonts '+TH%(('majorHAnsi',)*2+('majorEastAsia','majorBidi'))+'/>')+tr('M1402 minor ','<w:rFonts '+TH%(('minorHAnsi',)*2+('minorEastAsia','minorBidi'))+'/>')+'</w:p>'
+'<w:p>'+tr('M1403 accent1 ','<w:color w:val="4F81BD" w:themeColor="accent1"/>')+tr('M1404 accent2 ','<w:color w:val="C0504D" w:themeColor="accent2" w:themeShade="BF"/>')+tr('M1405 themeonly ','<w:color w:themeColor="accent3"/>')+tr('M1406 tint ','<w:color w:themeColor="accent1" w:themeTint="99" w:val="95B3D7"/>')+tr('M1407 auto ','<w:color w:val="auto"/>')+tr('M1408 lower ','<w:color w:val="ff00aa"/>')+'</w:p>'
+'<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="DBE5F1" w:themeFill="accent1" w:themeFillTint="33"/></w:pPr>'+tr('M1409 paragraph shade','')+'</w:p>'
+'<w:p>'+tr('M1410 run shade','<w:shd w:val="clear" w:color="auto" w:fill="FFFF00"/>')+tr(' M1411 caps','<w:caps/>')+tr(' M1412 smallcaps','<w:smallCaps/>')+tr(' M1413 hidden','<w:vanish/>')+tr(' M1414 dbl','<w:dstrike/>')+tr(' M1415 dblu','<w:u w:val="double"/>')+tr(' M1416 uoff','<w:u w:val="none"/>')+tr(' M1417 bfalse','<w:b w:val="false"/><w:i w:val="off"/>')+tr(' M1418 btrue','<w:b w:val="true"/><w:i w:val="1"/>')+tr(' M1419 sz9','<w:sz w:val="9"/>')+tr(' M1420 sz144','<w:sz w:val="144"/>')+tr(' M1421 sz25','<w:sz w:val="25"/>')+'</w:p>'
+'<w:p>'+tr('M1422 attr order','<w:rFonts w:hAnsi="Georgia" w:ascii="Georgia"/>')+tr(' M1423 cs only','<w:rFonts w:cs="Times New Roman"/>')+tr(' M1424 sq',"<w:color w:val='FF0000' />")+'</w:p>'
+"<w:p w:rsidR='00AA' w:rsidRDefault='00BB'><w:pPr><w:jc w:val='center' /></w:pPr><w:r w:rsidRPr='00CC'><w:t xml:space='preserve'>M1425 single quotes</w:t></w:r></w:p>"
+'<w:p>\n  <w:pPr>\n    <w:spacing w:before="240" w:after="240" w:line="480" w:lineRule="auto"/>\n  </w:pPr>\n  <w:r>\n    <w:t>M1426 pretty printed</w:t>\n  </w:r>\n</w:p>'
+'<w:p><w:pPr><w:spacing w:line="300" w:lineRule="exact"/><w:ind w:start="720" w:end="720"/><w:jc w:val="start"/></w:pPr>'+tr('M1427 exact start '*12,'')+'</w:p>'
+'<w:p><w:r><w:t>M1428 &#x41;&#66;&#xe9;&#233; &quot;q&quot; &apos;a&apos; &amp;amp; &lt;x&gt;</w:t></w:r></w:p>'
+P('M1429 end'))
def theme_fix(x): return x
bodyfile('a14_theme',body)
# 15 alternate content, text box, drawing shapes, math, ruby, custom xml
MC='xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
body=('<w:p %s><w:r><w:t xml:space="preserve">M1501 before box </w:t></w:r><w:r><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="1" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="column"><wp:posOffset>0</wp:posOffset></wp:positionH><wp:positionV relativeFrom="paragraph"><wp:posOffset>0</wp:posOffset></wp:positionV><wp:extent cx="914400" cy="914400"/><wp:wrapNone/><wp:docPr id="1" name="T"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"><wps:wsp><wps:cNvSpPr/><wps:spPr/><wps:txbx><w:txbxContent><w:p><w:r><w:t>M1502 in box</w:t></w:r></w:p></w:txbxContent></wps:txbx><wps:bodyPr/></wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing></mc:Choice><mc:Fallback><w:pict><v:shape><v:textbox><w:txbxContent><w:p><w:r><w:t>M1503 fallback</w:t></w:r></w:p></w:txbxContent></v:textbox></v:shape></w:pict></mc:Fallback></mc:AlternateContent></w:r><w:r><w:t xml:space="preserve"> M1504 after box</w:t></w:r></w:p>'%MC
+'<w:p %s><m:oMathPara><m:oMath><m:r><m:t>x=M1505</m:t></m:r></m:oMath></m:oMathPara></w:p>'%MC
+'<w:p><w:r><w:t xml:space="preserve">M1506 ruby </w:t></w:r><w:r><w:ruby><w:rubyPr><w:rubyAlign w:val="center"/></w:rubyPr><w:rt><w:r><w:t>M1507 top</w:t></w:r></w:rt><w:rubyBase><w:r><w:t>M1508 base</w:t></w:r></w:rubyBase></w:ruby></w:r></w:p>'
+'<w:p><w:customXml w:element="z"><w:r><w:t>M1509 custom</w:t></w:r></w:customXml><w:r><w:rPr><w:rtl/></w:rPr><w:t xml:space="preserve"> M1510 rtl</w:t></w:r></w:p>'
+'<w:p/><w:p><w:pPr/></w:p><w:p><w:r/></w:p><w:p><w:r><w:t/></w:r></w:p>'+P('M1511 end'))
bodyfile('a15_alt',body)
# 16 large text file with many runs: about 1 MB of document XML
d=docx.Document()
for i in range(3000):
    p=d.add_paragraph('M16%04d '%i+'the quick brown fox jumps over the lazy dog ')
    r=p.add_run('with a bold part '); r.bold=True
    if i%200==0: d.add_heading('M17%04d section'%i,1)
save(d,'a16_large')
# 17 oversize file carrying a big stored picture
d=docx.Document(); d.add_paragraph('M1801 start')
import random; rnd=random.Random(5)
b=bytes(rnd.getrandbits(8) for _ in range(3*600*600))
raw=b''.join(b'\0'+b[y*1800:(y+1)*1800] for y in range(600))
def ch(t,x): return struct.pack('>I',len(x))+t+x+struct.pack('>I',zlib.crc32(t+x))
d.add_picture(io.BytesIO(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',600,600,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b'')),width=Inches(3))
d.add_paragraph('M1802 end')
save(d,'a17_bigpic')
# 18 small file with no styles part, no settings, stored members, ordering oddities
Z=zipfile.ZipFile(os.path.join(OUT,'a18_minimal.docx'),'w',zipfile.ZIP_STORED)
Z.writestr('[Content_Types].xml',XH+'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
Z.writestr('_rels/.rels',XH+'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
Z.writestr('word/document.xml',XH+'<w:document %s><w:body>%s</w:body></w:document>'%(NS,P('M1901 minimal')+P('M1902 no section')))
Z.close()
# 19 long paragraph past the limits and long run of runs
d=docx.Document(); d.add_paragraph('M2001 '+'word '*400+'M2002 mid '+'word '*400+' M2003 end of very long paragraph'); d.add_paragraph('M2004 next')
p=d.add_paragraph()
for i in range(300): r=p.add_run('r%d '%i); r.bold=i%2==0
d.add_paragraph('M2005 after')
save(d,'a19_long')

# 20 to 26: damaged and odd packages must end the open, never hang
good=open(os.path.join(OUT,'a01_format.docx'),'rb').read()
open(os.path.join(OUT,'a20_trunc.docx'),'wb').write(good[:len(good)//2])
rg=random.Random(9); open(os.path.join(OUT,'a21_noise.docx'),'wb').write(bytes(rg.getrandbits(8) for _ in range(20000)))
open(os.path.join(OUT,'a22_empty.docx'),'wb').write(b'')
b_=bytearray(good); zi=zipfile.ZipFile(io.BytesIO(good)).getinfo('word/document.xml'); o_=zi.header_offset+30+len(zi.filename)+40
for k in range(60): b_[o_+k]^=0xA5
open(os.path.join(OUT,'a23_baddeflate.docx'),'wb').write(bytes(b_))
Z=zipfile.ZipFile(os.path.join(OUT,'a24_nodoc.docx'),'w'); Z.writestr('hello.txt','no main part'); Z.close()
Z=zipfile.ZipFile(os.path.join(OUT,'a25_unclosed.docx'),'w',zipfile.ZIP_DEFLATED); Z.writestr('word/document.xml','<w:document xmlns:w="x"><w:body><w:p><w:r><w:t>M2501 open <w:tbl><w:tr><w:tc w:'); Z.close()
d=docx.Document(); st=d.styles
from docx.enum.style import WD_STYLE_TYPE
for i in range(260): st.add_style('Extra %d'%i,WD_STYLE_TYPE.PARAGRAPH)
p=d.add_paragraph('M2601 last style'); p.style=st['Extra 259']; d.add_paragraph('M2602 normal')
save(d,'a26_manystyles')
body=('<w:p w:rsidR="00A1" w14:paraId="1A2B3C4D" w14:textId="77777777" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"><w:pPr><w:rPr><w:rFonts w:hint="eastAsia"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:hint="eastAsia" w:ascii="Georgia" w:hAnsi="Georgia"/><w:lang w:val="en-GB"/></w:rPr><w:t>M2701 hint first</w:t></w:r><w:proofErr w:type="spellStart"/><w:r><w:lastRenderedPageBreak/><w:t xml:space="preserve"> M2702</w:t></w:r><w:proofErr w:type="spellEnd"/></w:p>'
+'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:jc w:val="right"/></w:tblPr><w:tblGrid><w:gridCol w:w="4000"/><w:gridCol w:w="4000"/></w:tblGrid><w:tr><w:trPr><w:jc w:val="right"/></w:trPr><w:tc><w:tcPr><w:tcW w:w="8000" w:type="dxa"/><w:gridSpan w:val="2"/><w:shd w:val="clear" w:color="auto" w:fill="FFFF00"/></w:tcPr><w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="00FF00"/></w:pPr><w:r><w:t>M2703 span</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>M2704</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>M2705</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:p><w:r><w:t>M2706 short row</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
+P('M2707 end')+'<w:tbl><w:tblGrid><w:gridCol w:w="4000"/></w:tblGrid><w:tr><w:tc><w:p><w:r><w:t>M2708 table last</w:t></w:r></w:p></w:tc></w:tr></w:tbl>')
bodyfile('a27_wordlike',body)
print(sorted(os.listdir(OUT)))
