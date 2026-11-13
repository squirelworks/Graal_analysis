# g3dref.py: static G3D token read for PE engine DLLs (4.x/5.x) and 32-bit ELF.
# Validated on Windows 4.04r2 and 4.20r8 GraalEngine.dll (G3D17026, G3D20126) and 5.12
# Graal3DEngine.dll (G3D14097). Run it on the engine DLL, not on the Delphi launcher.
# Static G3D token reader for PE and 32-bit ELF game engines (3.x-6.01).
# The token is built at run time from one-character strings; code references each by
# absolute 32-bit address. Map one-char strings in data sections, collect 32-bit values in
# code that point at them, group into runs, and spell G3D + DDMMY.
import sys,re,struct
TOK=re.compile(rb'G3D[0-9]{4}[0-9A-F]')
SCN_MEM_EXECUTE=1<<29  # PE section flag: the section holds code
def sections(p,b):
    if b[:2]==b'MZ':
        import pefile
        pe=pefile.PE(data=b); base=pe.OPTIONAL_HEADER.ImageBase
        return [(base+s.VirtualAddress,s.get_data(),bool(s.Characteristics&SCN_MEM_EXECUTE)) for s in pe.sections]
    if b[:4]==b'\x7fELF' and b[4]==1:
        shoff,=struct.unpack_from('<I',b,0x20); shentsize,shnum=struct.unpack_from('<HH',b,0x2e)
        out=[]
        for k in range(shnum):
            name,typ,flags,addr,off,size=struct.unpack_from('<IIIIII',b,shoff+k*shentsize)
            if typ==8 or not (flags&2) or size==0: continue  # NOBITS or not ALLOC
            out.append((addr,b[off:off+size],bool(flags&4)))
        return out
    raise SystemExit('not PE or ELF32: '+p)
ALL='--all-sections' in sys.argv
for p in [a for a in sys.argv[1:] if not a.startswith('--')]:
    b=open(p,'rb').read(); secs=sections(p,b); ch={}
    for va,d,x in secs:
        if x and not ALL: continue
        for i in range(len(d)-1):
            if 0x30<=d[i]<=0x5A and d[i+1]==0 and (i==0 or d[i-1]==0): ch[va+i]=d[i]
    found=set()
    # Unpacked Themida dumps (5.30r3, 6.00r2/r4) flag their real code section as data:
    # pass --all-sections to map strings and search code references in every section.
    for va,d,x in secs:
        if not x and not ALL: continue
        refs=[(i,ch[v]) for i in range(len(d)-3) for v in [struct.unpack_from('<I',d,i)[0]] if v in ch]
        for gap in (24,64,200):
            run=[];last=-10**9
            for r in refs+[(10**12,0)]:
                if r[0]-last>gap:
                    for m in TOK.finditer(bytes(c for _,c in run)): found.add(m.group().decode())
                    run=[]
                run.append(r); last=r[0]
    print(p, sorted(found) or '-')
