"""All measurements for the report. Writes build/glyph/measure.json and appends to the progress log by hand."""
from glyphnet_common import *
import pickle
F4=lambda fi:[(fi,b,i) for b in (0,1) for i in (0,1)]
R={}
def log(*a): print(*a,flush=True)
# --- networks
stats={}
for fi,fam in enumerate(('carlito','caladea')):
    stats[fam]=build(fam,F4(fi),gn.ASCII); log(fam,{k:v for k,v in stats[fam].items() if k!='per'})
    stats[fam+'_all']=build(fam+'_all',F4(fi),[c for c in rom.CODES]); log(fam,'all codes',{k:v for k,v in stats[fam+'_all'].items() if k!='per'})
    stats[fam+'_synth']=build(fam+'_synth',[(fi,0,0)],gn.ASCII,synth=True,xsnap=False); log(fam,'synth',{k:v for k,v in stats[fam+'_synth'].items() if k!='per'})
R['nets']={k:{a:b for a,b in v.items() if a!='per'} for k,v in stats.items()}
for fam in ('carlito','caladea'):
    p=stats[fam]['per']; e=[v['edges'] for v in p.values()]; R['nets'][fam]['edges_per_glyph']=sum(e)/len(e); R['nets'][fam]['max_edges']=max(e)
    R['nets'][fam]['weights_per_glyph']=stats[fam]['weights']/len(p)
# --- ROM weights
romw={}
for fi,fam in enumerate(('carlito','caladea')):
    asc=tot=0
    for f in F4(fi):
        for si,pt in enumerate(rom.PTS):
            for cl,pts in rom.face_program(*f,si):
                tot+=len(pts)
                if cl[0]<127: asc+=len(pts)
    romw[fam]=dict(ascii=asc,all=tot); log('ROM weights',fam,asc,tot)
R['rom_weights']=romw
# --- errors and cost
tab={}
for fi,fam in enumerate(('carlito','caladea')):
  for fx,f in enumerate(F4(fi)):
    for pt in PTSZ:
        G=geom(pt,fi); C=gn.ASCII[1:]
        refs=[ref_raster(*f,c,pt) for c in C]; bms=[rom_bitmap(*f,c,pt) for c in C]
        dn=[draw(c,fx,pt,(0,0),fi=fi) for c in C]; ds=[draw(c,fx,pt,(1,1),fi=fi) for c in C]
        rn,_,ms0=run(fam,dn); rs,_,ms1=run(fam,ds); _,info,_=run(fam,ds,count=True)
        rn=[pad(x,G) for x in rn]; rs=[pad(x,G) for x in rs]
        ink=sum(r.sum() for r in refs)
        E=lambda A,B:float(sum(np.abs(a-b).sum() for a,b in zip(A,B))/ink)
        RMS=lambda A,B:float(math.sqrt(sum(((a-b)**2).sum() for a,b in zip(A,B))/sum((r>0).sum() for r in refs)))
        n=len(C)
        tab[f'{fam}/{f[1]}{f[2]}/{pt}']=dict(net_ref=E(rn,refs),snap_ref=E(rs,refs),rom_ref=E(bms,refs),net_rom=E(rn,bms),snap_rom=E(rs,bms),rms_net=RMS(rn,refs),rms_rom=RMS(bms,refs),
          ticks=sum(i['t'] for i in info)/n,visits=sum(i['op'][0]+i['op'][2] for i in info)/n,reads=sum(i['op'][1]+i['op'][3] for i in info)/n,edges=sum(i['ed'] for i in info)/n,us=ms1*1000/n)
        log(fam,f,pt,{k:round(v,3) for k,v in tab[f'{fam}/{f[1]}{f[2]}/{pt}'].items()})
        pickle.dump(tab,open(f'{OUT}/tab.pkl','wb'))
R['tab']=tab
# --- synth against real faces
syn={}
for fi,fam in enumerate(('carlito','caladea')):
    for name,flags,real in (('bold',dict(bold=1),(fi,1,0)),('italic',dict(slant=1),(fi,0,1)),('bolditalic',dict(bold=1,slant=1),(fi,1,1))):
        for pt in (11,18,36):
            G=geom(pt,fi); C=gn.ASCII[1:]
            res,_,_=run(fam+'_synth',[draw(c,0,pt,(0,0),fi=fi,**flags) for c in C]); res=[pad(x,G) for x in res]
            refs=[ref_raster(*real,c,pt) for c in C]; ink=sum(r.sum() for r in refs)
            syn[f'{fam}/{name}/{pt}']=float(sum(np.abs(a-b).sum() for a,b in zip(res,refs))/ink); log('synth',fam,name,pt,round(syn[f'{fam}/{name}/{pt}'],3))
R['synth']=syn
json.dump(R,open(f'{OUT}/measure.json','w'),indent=1)
# --- cache hit path on the real engine
ch=ord('m')
for pt,W,H in ((11,rom.SW,rom.SH),(36,rom.LW,rom.LH)):
    gn.cache_blit_net(W,H,f'{OUT}/blit{W}.bin.gz')
    res,_,_=run('carlito',[draw(ch,0,pt,(1,1),fi=0)]); G=geom(pt); pad(res[0],G).astype(np.float32).tofile(f'{OUT}/cov{W}.f32')
    o=subprocess.check_output(['node','test/glyphnet_cache.js',f'{OUT}/blit{W}.bin.gz',f'{OUT}/cov{W}.f32',str(W),str(H),'20000'],cwd=ROOT).decode(); log(pt,o)
    R[f'blit{pt}']=o
json.dump(R,open(f'{OUT}/measure.json','w'),indent=1)
log('done')
