#!/usr/bin/env python3
# find PPC sites building 0x08088405 / 0x04A80B38 and the funcs (prev mflr/stwu) containing them
import os, sys, struct
sys.path.insert(0, os.environ.get('PPC_HELPERS_DIR', '.'))  # dir holding the PPC disassembly helpers
from capstone import Cs, CS_ARCH_PPC, CS_MODE_32, CS_MODE_BIG_ENDIAN
data=open(sys.argv[1],'rb').read()
ncmds=struct.unpack_from('>I',data,16)[0]; off=28; secs=[]
for _ in range(ncmds):
    cmd,sz=struct.unpack_from('>II',data,off)
    if cmd==1:
        n=struct.unpack_from('>I',data,off+48)[0]; s=off+56
        for _ in range(n):
            sect=data[s:s+16].rstrip(b'\0').decode(); a,size,fo=struct.unpack_from('>III',data,s+32); secs.append((sect,a,size,fo)); s+=68
    off+=sz
t=[x for x in secs if x[0]=='__text'][0]
_,a,size,fo=t
# raw word scan: lis rX,0x808 => opcode 15, rA=0, imm 0x0808 ; also 0x04a8
for i in range(0,size,4):
    w=struct.unpack_from('>I',data,fo+i)[0]
    op=w>>26; imm=w&0xffff; ra=(w>>16)&31
    if op==15 and ra==0 and imm in (0x0808,0x04a8):
        print(hex(a+i), 'lis', imm)
