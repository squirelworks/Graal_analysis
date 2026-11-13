#!/usr/bin/env python3
"""List jump-table switches in a 32-bit BE PPC Mach-O (gcc PIC style).
usage: ppcswitch.py BIN [minbound]  -> one line per switch: bctr addr, bound, base offset, case ids (non-default)"""
import sys, struct
from capstone import Cs, CS_ARCH_PPC, CS_MODE_32, CS_MODE_BIG_ENDIAN
data=open(sys.argv[1],'rb').read(); minb=int(sys.argv[2]) if len(sys.argv)>2 else 100
ncmds=struct.unpack_from('>I',data,16)[0]; off=28; secs=[]
for _ in range(ncmds):
    cmd,sz=struct.unpack_from('>II',data,off)
    if cmd==1:
        n=struct.unpack_from('>I',data,off+48)[0]; s=off+56
        for _ in range(n):
            sect=data[s:s+16].rstrip(b'\0').decode(); a,size,fo=struct.unpack_from('>III',data,s+32); secs.append((sect,a,size,fo)); s+=68
    off+=sz
def rd(v):
    for sect,a,size,fo in secs:
        if fo and a<=v<a+size: return struct.unpack_from('>i',data,fo+v-a)[0]
    return None
t=[x for x in secs if x[0]=='__text'][0]
md=Cs(CS_ARCH_PPC,CS_MODE_32|CS_MODE_BIG_ENDIAN)
_,ta,tsize,tfo=t
ins=[]
# decode word by word so data islands don't stop us
for i in range(0,tsize,4):
    w=data[tfo+i:tfo+i+4]; d=list(md.disasm(w,ta+i))
    ins.append((ta+i, d[0].mnemonic if d else '.word', d[0].op_str if d else ''))
def num(x):
    try: return int(x,0)
    except: return None
pic={}
for k,(a,m,o) in enumerate(ins):
    ops=[s.strip() for s in o.split(',')]
    if m in ('bcl','bdnzl','bl') and ops and num(ops[-1])==a+4:
        for a9,m9,o9 in ins[k+1:k+10]:
            if m9=='mflr': pic[o9.strip()]=a+4; break
    if m!='bctr': continue
    win=ins[max(0,k-24):k]
    bound=None; cmpreg=None; dflt=None; tbl=None; base=0
    for j,(a2,m2,o2) in enumerate(win):
        p=[s.strip() for s in o2.split(',')]
        if m2=='cmplwi':
            bound=num(p[-1]); cmpreg=p[-2]; dflt=None
            for a3,m3,o3 in win[j+1:j+3]:
                if m3.startswith('bgt'): dflt=num(o3.split(',')[-1])
        if m2=='addis' and len(p)==3 and p[1] in pic:
            hi=num(p[2]); tb=pic[p[1]]+(hi<<16)
            for a3,m3,o3 in win[j+1:]:
                q=[s.strip() for s in o3.split(',')]
                if m3=='addi' and q[1]==p[0]: tbl=tb+num(q[2]); break
    if bound is None or tbl is None or bound<minb: continue
    # case base: addi cmpreg, X, -N earlier
    for a2,m2,o2 in win:
        p=[s.strip() for s in o2.split(',')]
        if m2=='addi' and p[0]==cmpreg and num(p[2]) is not None and num(p[2])<0: base=-num(p[2])
    tg=[tbl+rd(tbl+4*i) for i in range(bound+1)]
    if dflt is None:
        from collections import Counter; dflt=Counter(tg).most_common(1)[0][0]
    cases=[i+base for i,x in enumerate(tg) if x!=dflt]
    print(f'bctr {a:#x} bound {bound} base {base} table {tbl:#x} default {dflt:#x} ncases {len(cases)}')
    print('  ids', ' '.join(map(str,cases)))
