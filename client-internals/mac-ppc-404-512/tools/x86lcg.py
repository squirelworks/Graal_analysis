#!/usr/bin/env python3
import sys, pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
p=pefile.PE(sys.argv[1]); base=p.OPTIONAL_HEADER.ImageBase
img=p.get_memory_mapped_image()
pat=bytes.fromhex('05840808')
i=img.find(pat); hits=[]
while i!=-1:
    hits.append(i); i=img.find(pat,i+1)
md=Cs(CS_ARCH_X86,CS_MODE_32)
for h in hits:
    print('const at',hex(base+h))
if len(sys.argv)>2:
    a=int(sys.argv[2],16); n=int(sys.argv[3])
    for ins in md.disasm(img[a-base:a-base+n], a): print(hex(ins.address), ins.mnemonic, ins.op_str)
