import docx
from docx.shared import Pt,RGBColor,Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH as A, WD_COLOR_INDEX as H
d=docx.Document()
d.add_heading('Résumé of Tests',0)
d.add_heading('Première section',1)
p=d.add_paragraph('Normal text with ');r=p.add_run('bold');r.bold=True;p.add_run(', ');r=p.add_run('italic');r.italic=True;p.add_run(', ');r=p.add_run('strike');r.font.strike=True;p.add_run(', H');r=p.add_run('2');r.font.subscript=True;p.add_run('O, x');r=p.add_run('2');r.font.superscript=True;p.add_run(', ');r=p.add_run('highlighted');r.font.highlight_color=H.YELLOW;p.add_run(' and ');r=p.add_run('custom color');r.font.color.rgb=RGBColor(0x12,0x80,0xC0);p.add_run('. “Curly” — dashes – ñ ü € ©.')
d.add_paragraph('Bullet item').style='List Bullet'
d.add_paragraph('Bullet 2').style='List Bullet 2'
d.add_paragraph('Number one').style='List Number'
d.add_paragraph('Number two').style='List Number'
p=d.add_paragraph('Indented paragraph with spacing. '*6);p.paragraph_format.left_indent=Inches(0.5);p.paragraph_format.first_line_indent=Inches(0.25);p.paragraph_format.space_before=Pt(12);p.paragraph_format.space_after=Pt(18);p.paragraph_format.line_spacing=1.5;p.alignment=A.JUSTIFY
d.add_paragraph('Quote text here','Quote')
d.add_heading('Heading two',2)
d.add_paragraph('The end.')
import sys;d.save(sys.argv[1])
