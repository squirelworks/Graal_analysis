# boardscan.py <pid> : find 64x64 board arrays (i16 or i32) containing our row-26 pattern
import sys, struct, re
pid=int(sys.argv[1]); mem=open(f'/proc/{pid}/mem','rb')
row=[2,3,2047,512,513,2047,684,685]
pats={'i16':struct.pack('<8h',*row),'i32':struct.pack('<8i',*row)}
for line in open(f'/proc/{pid}/maps'):
    a,perm=line.split()[:2]
    if 'rw' not in perm: continue
    lo,hi=(int(v,16) for v in a.split('-'))
    if hi>0xffffffff or hi-lo>256<<20: continue
    try: mem.seek(lo); buf=mem.read(hi-lo)
    except Exception: continue
    for k,p in pats.items():
        for m in re.finditer(re.escape(p),buf):
            print(k,hex(lo+m.start()))
