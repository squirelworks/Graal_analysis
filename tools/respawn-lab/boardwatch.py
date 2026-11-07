# boardwatch.py <pid> <secs> <out> <base>... : poll 64x64 i16 boards, log every changed tile with time
import sys, struct, time, json
pid=int(sys.argv[1]); secs=float(sys.argv[2]); out=open(sys.argv[3],'w'); bases=[int(a,16) for a in sys.argv[4:]]
mem=open(f'/proc/{pid}/mem','rb')
def rd(b): mem.seek(b); return struct.unpack('<4096h',mem.read(8192))
prev={b:rd(b) for b in bases}; t0=time.time()
while time.time()-t0<secs:
    for b in bases:
        try: cur=rd(b)
        except Exception: sys.exit()
        if cur!=prev[b]:
            ch=[(i%64,i//64,prev[b][i],cur[i]) for i in range(4096) if cur[i]!=prev[b][i]]
            out.write(json.dumps({'t':round(time.time()-t0,3),'base':hex(b),'ch':ch})+'\n'); out.flush()
            prev[b]=cur
    time.sleep(0.01)
