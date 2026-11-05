# Compares framebuffers from two builds. Usage: python3 test/fbcmp.py dirA dirB
import sys,glob,numpy as np,os
a,b=sys.argv[1:3]
for f in sorted(glob.glob(a+'/fb_*.raw'),key=lambda p:int(p.split('_')[-1][:-4])):
    A=np.fromfile(f,dtype=np.uint8).reshape(800,1280,4).astype(int);B=np.fromfile(b+'/'+os.path.basename(f),dtype=np.uint8).reshape(800,1280,4).astype(int)
    d=np.abs(A-B)[...,:3]; print(os.path.basename(f),'rgb max diff',d.max(),'pixels differing',(d.max(axis=2)>0).sum(),'over 1:',(d.max(axis=2)>1).sum(),'alpha diffs',(A[...,3]!=B[...,3]).sum())
