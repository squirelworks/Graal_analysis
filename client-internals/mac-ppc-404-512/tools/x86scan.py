import sys, pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
p=pefile.PE(sys.argv[1]); base=p.OPTIONAL_HEADER.ImageBase; img=p.get_memory_mapped_image()
md=Cs(CS_ARCH_X86,CS_MODE_32)
i=img.find(bytes.fromhex('05840808'))
while i!=-1:
    found=False
    for back in range(0x90,0x10,-1):
        s=i-back; txt=[(x.address,x.mnemonic,x.op_str) for x in md.disasm(img[s:i+8],base+s)]
        if txt and txt[-1][0]<=base+i<=txt[-1][0]+8 or any(a<=base+i<a+8 for a,_,_ in txt[-3:]):
            ops=' ; '.join(f'{m} {o}' for a,m,o in txt)
            if ('0xc' in ops) and (', 2' in ops):
                print(hex(base+i), 'CANDIDATE'); found=True
            break
    i=img.find(bytes.fromhex('05840808'),i+1)
