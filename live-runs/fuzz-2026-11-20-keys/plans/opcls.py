#!/usr/bin/env python3
# opcls.py RUNDIR [OWNX OWNY [XMAX]] : locate the fake player in each other-player test shot by diff against 00-base.
# Own player is drawn at the screen centre (x=30); 16 px per tile. Masks: HUD, own player, block NPC counter.
import sys,os
from PIL import Image, ImageChops
d=sys.argv[1]; OX,OY=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (512,392); XR=int(sys.argv[4]) if len(sys.argv)>4 else 830; base=Image.open(os.path.join(d,'00-base.png')).convert('RGB')
W,H=base.size
own=None
def cls(n):
    im=Image.open(os.path.join(d,n+'.png')).convert('RGB')
    df=ImageChops.difference(im,base).convert('L').point(lambda v:255 if v>40 else 0)
    px=df.load(); xs=[];ys=[]
    for y in range(OY-150,OY+210):
        for x in range(OX-316,min(XR,OX+318)):
            if OX-42<=x<=OX+48 and OY-42<=y<=OY+28: continue   # own player
            if OX-42<=x<=OX+28 and OY-107<=y<=OY-42: continue   # block NPC + counter
            if px[x,y]: xs.append(x); ys.append(y)
    if len(xs)<150: return 'none',len(xs),None,None
    xs.sort(); ys.sort(); cx=xs[len(xs)//2]; cy=ys[len(ys)//2]
    tx=30+(cx-OX)/16; ty=30+(cy-OY)/16
    v='x36' if 33<=tx<=39 else ('x26' if 23<=tx<=29 else 'other')
    return v,len(xs),round(tx,1),round(ty,1)
names=sorted(f[:-4] for f in os.listdir(d) if f.endswith('.png') and (f.startswith('p') or f.startswith('ctl')))
for n in names:
    print(n,*cls(n),sep='\t')
