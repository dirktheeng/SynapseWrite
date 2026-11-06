"""Subsets the openly licensed font families to the characters the editor can show. The bytes wait in a read only
part of the memory bank; a PDF copies out only the faces it used."""
import io,zlib
import rom
from fontTools.ttLib import TTFont
from fontTools import subset
WANT={c:ord(rom.cp1252(c)) for c in rom.CODES if c!=127}    # WinAnsi code to unicode
def _graft(f,x,uni,o):
    "Adds glyphs from the Latin extended file of the same face to the subset."
    s=subset.Subsetter(o);s.populate(unicodes=sorted(uni&set(x.getBestCmap())));s.subset(x)
    gl=f['glyf'];xg=x['glyf'];xc=x.getBestCmap();nm=lambda g:'x_'+g
    for g in x.getGlyphOrder():
        if g=='.notdef': continue
        gg=xg[g]
        if gg.isComposite():
            for comp in gg.components: comp.glyphName=nm(comp.glyphName)
        gl[nm(g)]=gg; f['hmtx'][nm(g)]=x['hmtx'][g]
    f.setGlyphOrder(gl.glyphOrder)
    f['post'].formatType=3.0
    for t in f['cmap'].tables:
        if t.isUnicode():
            for u,g in xc.items(): t.cmap[u]=nm(g)
def _name(fi,bo,it):
    return rom.FAM_NAMES[fi].replace(' ','')+('-'+('Bold' if bo else '')+('Italic' if it else '') if bo or it else '')
def face_blob(i,fi,bo,it,first):
    """The three PDF objects of one face, numbered first, first+1, first+2. Returns the bytes and the offsets of the last two."""
    w,st=(700 if bo else 400),('italic' if it else 'normal')
    f=TTFont(io.BytesIO(rom._load(rom.FAM[fi],'latin',w,st)),recalcTimestamp=False)
    want=set(WANT.values())|{0x2022}
    o=subset.Options();o.hinting=False;o.layout_features=[];o.name_IDs=[1];o.notdef_outline=True;o.drop_tables+=['GSUB','GPOS','GDEF','kern','meta','DSIG','FFTM','name','OS/2','gasp','prep','fpgm','cvt ']
    s=subset.Subsetter(o);s.populate(unicodes=sorted(want&set(f.getBestCmap())));s.subset(f)
    rest=want-set(f.getBestCmap())
    if rest: _graft(f,TTFont(io.BytesIO(rom._load(rom.FAM[fi],'latin-ext',w,st)),recalcTimestamp=False),rest,o)
    f['post'].formatType=3.0
    b=io.BytesIO();f.save(b);ttf=b.getvalue();zd=zlib.compress(ttf,9)
    upm=f['head'].unitsPerEm;cm=f.getBestCmap();hm=f['hmtx'];k=1000/upm
    wd=[round(hm[cm[WANT[c]]][0]*k) if c in WANT and WANT[c] in cm else 0 for c in range(32,256)]
    h=f['head'];hh=f['hhea'];tag='ABCD'+chr(65+i//26)+chr(65+i%26)+'+'+_name(fi,bo,it)
    fo,de,ff=first,first+1,first+2
    a=(f'{fo} 0 obj\n<</Type/Font/Subtype/TrueType/BaseFont/{tag}/FirstChar 32/LastChar 255/Widths[{" ".join(map(str,wd))}]/Encoding/WinAnsiEncoding/FontDescriptor {de} 0 R>>\nendobj\n').encode()
    fl=32+(64 if it else 0)
    b_=(f'{de} 0 obj\n<</Type/FontDescriptor/FontName/{tag}/Flags {fl}/FontBBox[{round(h.xMin*k)} {round(h.yMin*k)} {round(h.xMax*k)} {round(h.yMax*k)}]/ItalicAngle {-12 if it else 0}/Ascent {round(hh.ascent*k)}/Descent {round(hh.descent*k)}/CapHeight {round(hh.ascent*k*0.8)}/StemV 80/FontFile2 {ff} 0 R>>\nendobj\n').encode()
    c=(f'{ff} 0 obj\n<</Length {len(zd)}/Length1 {len(ttf)}/Filter/FlateDecode>>\nstream\n').encode()+zd+b'\nendstream\nendobj\n'
    return a+b_+c,len(a),len(a)+len(b_)
def ext_blob(i,v,p,first):
    "One page of extended characters as a simple font: codes 128 to 255, named so a reader knows each one's Unicode value."
    m=rom.ext_page(v,p); w,st=(700 if v[1] else 400),('italic' if v[2] else 'normal')
    subs=[]
    for l,(sub,g) in m.items():
        if sub not in subs: subs.append(sub)
    f=TTFont(io.BytesIO(rom._load(rom.FAM[0],subs[0] if subs else 'latin',w,st)))
    o=subset.Options();o.hinting=False;o.layout_features=[];o.name_IDs=[1];o.notdef_outline=True;o.drop_tables+=['GSUB','GPOS','GDEF','kern','meta','DSIG','FFTM','name','OS/2','gasp','prep','fpgm','cvt ']
    us={p+l for l in m}; s=subset.Subsetter(o);s.populate(unicodes=sorted(us&set(f.getBestCmap())));s.subset(f)
    rest=us-set(f.getBestCmap())
    for sub in subs[1:]:
        q=rest&set(TTFont(io.BytesIO(rom._load(rom.FAM[0],sub,w,st))).getBestCmap())
        if q: _graft(f,TTFont(io.BytesIO(rom._load(rom.FAM[0],sub,w,st))),q,o); rest-=q
    f['post'].formatType=3.0
    b=io.BytesIO();f.save(b);ttf=b.getvalue();zd=zlib.compress(ttf,9)
    upm=f['head'].unitsPerEm;cm=f.getBestCmap();hm=f['hmtx'];k=1000/upm
    wd=[round(hm[cm[p+l]][0]*k) if p+l in cm else 0 for l in range(128)]
    dif=' '.join(f'/uni{p+l:04X}' for l in range(128))
    h=f['head'];hh=f['hhea'];tag='ABCD'+chr(65+i//26)+chr(65+i%26)+f'+Carlito{p:04X}'+('-Bold' if v[1] else '-Italic' if v[2] else '')
    fo,de,ff=first,first+1,first+2
    a=(f'{fo} 0 obj\n<</Type/Font/Subtype/TrueType/BaseFont/{tag}/FirstChar 128/LastChar 255/Widths[{" ".join(map(str,wd))}]/Encoding<</BaseEncoding/WinAnsiEncoding/Differences[128 {dif}]>>/FontDescriptor {de} 0 R>>\nendobj\n').encode()
    fl=32+(64 if v[2] else 0)
    b_=(f'{de} 0 obj\n<</Type/FontDescriptor/FontName/{tag}/Flags {fl}/FontBBox[{round(h.xMin*k)} {round(h.yMin*k)} {round(h.xMax*k)} {round(h.yMax*k)}]/ItalicAngle {-12 if v[2] else 0}/Ascent {round(hh.ascent*k)}/Descent {round(hh.descent*k)}/CapHeight {round(hh.ascent*k)}/StemV 80/FontFile2 {ff} 0 R>>\nendobj\n').encode()
    c=(f'{ff} 0 obj\n<</Length {len(zd)}/Length1 {len(ttf)}/Filter/FlateDecode>>\nstream\n').encode()+zd+b'\nendstream\nendobj\n'
    return a+b_+c,len(a),len(a)+len(b_)
