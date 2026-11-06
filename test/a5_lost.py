"""Compares the marker words of a source .docx (as LibreOffice reads it) with those in the saved copy.
Usage: a5_lost.py src.docx saved.docx"""
import sys,re,zipfile
def txt(fn):
    z=zipfile.ZipFile(fn); o=''
    for n in z.namelist():
        if re.match(r'word/(document|footnotes|endnotes|comments|header\d*|footer\d*)\.xml$',n):
            o+=' '+re.sub(r'<[^>]+>','',re.sub(r'</w:p>',' ',z.read(n).decode('utf8','replace')))
    return set(re.findall(r'\bM\d{3,6}\b',o))
a,b=txt(sys.argv[1]),txt(sys.argv[2])
print(sys.argv[1].split('/')[-1],'markers',len(a),'lost',len(a-b),sorted(a-b)[:40])
