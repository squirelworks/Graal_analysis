# Torque (TGE 1.x) BitStream reader/writer with the stock Huffman string coder.
# The character-frequency table is stock Torque's (from the MIT-licensed Torque3D source, core/stream/bitStream.cpp).
# Bits are packed LSB first. Strings: flag(huffman) + U8 len + codes, or flag 0 + U8 len + raw bytes.
import struct,sys
FREQS=[0,0,0,0,0,0,0,0,0,329,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2809,68,0,27,0,58,3,62,4,7,0,0,15,65,554,3,394,404,189,117,30,51,27,15,34,32,80,1,142,3,142,39,0,144,125,44,122,275,70,135,61,127,8,12,113,246,122,36,185,1,149,309,335,12,11,14,54,151,0,0,2,0,0,211,0,2090,344,736,993,2872,701,605,646,1552,328,305,1240,735,1533,1713,562,3,1775,1149,1469,979,407,553,59,279,31,0,0,0,68,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
def _build():
    leaves=[[f+1,i] for i,f in enumerate(FREQS)]; nodes=[None]
    wraps=[('L',i) for i in range(256)]
    pop=lambda w: leaves[w[1]][0] if w[0]=='L' else nodes[w[1]][0]
    idx=lambda w: -(w[1]+1) if w[0]=='L' else w[1]
    while len(wraps)!=1:
        m1,m2,i1,i2=0xfffffffe,0xffffffff,-1,-1
        for i,w in enumerate(wraps):
            p=pop(w)
            if p<m1: m2,i2,m1,i1=m1,i1,p,i
            elif p<m2: m2,i2=p,i
        nodes.append([pop(wraps[i1])+pop(wraps[i2]),idx(wraps[i1]),idx(wraps[i2])])
        mi,ni=min(i1,i2),max(i1,i2); wraps[mi]=('N',len(nodes)-1)
        if i2!=len(wraps)-1: wraps[ni]=wraps[-1]
        wraps.pop()
    nodes[0]=list(nodes[wraps[0][1]])
    codes={}
    def gen(i,code):
        if i<0: codes[-(i+1)]=code; return
        gen(nodes[i][1],code+[0]); gen(nodes[i][2],code+[1])
    gen(0,[]); return nodes,codes
NODES,CODES=_build()
class R:
    def __init__(s,d,pos=0): s.d=d; s.p=pos
    def flag(s):
        if s.p>=len(s.d)*8: raise EOFError
        b=(s.d[s.p>>3]>>(s.p&7))&1; s.p+=1; return b
    def int(s,n): return sum(s.flag()<<i for i in range(n))
    def u8(s): return s.int(8)
    def u32(s): return s.int(32)
    def str(s):
        if s.flag():
            out=[]
            for _ in range(s.u8()):
                i=0
                while i>=0: i=NODES[i][2] if s.flag() else NODES[i][1]
                out.append(-(i+1))
            return bytes(out).decode('latin1')
        return bytes(s.u8() for _ in range(s.u8())).decode('latin1')
    def left(s): return len(s.d)*8-s.p
class W:
    def __init__(s): s.bits=[]
    def flag(s,b): s.bits.append(1 if b else 0); return b
    def int(s,v,n): [s.bits.append((v>>i)&1) for i in range(n)]
    def u8(s,v): s.int(v,8)
    def u32(s,v): s.int(v&0xffffffff,32)
    def str(s,t):
        t=t.encode('latin1')[:255]; nb=sum(len(CODES[c]) for c in t)
        if nb<len(t)*8:
            s.flag(1); s.u8(len(t)); [s.bits.extend(CODES[c]) for c in t]
        else:
            s.flag(0); s.u8(len(t)); [s.u8(c) for c in t]
    def bytes(s):
        b=bytearray((len(s.bits)+7)//8)
        for i,x in enumerate(s.bits): b[i>>3]|=x<<(i&7)
        return bytes(b)
def connect_request(d):
    r=R(d); t=r.u8(); seq=r.u32(); dig=[r.u32() for _ in range(4)]
    o=dict(type=hex(t),seq=hex(seq),digest=[hex(x) for x in dig],cls=r.str(),group=r.u32(),crc=hex(r.u32()),
           game=r.str(),cur=r.u32(),min=r.u32(),password=r.str())
    n=r.u32(); o['argv']=[r.str() for _ in range(min(n,16))]; o['bits_left']=r.left(); return o
if __name__=='__main__':
    print(connect_request(bytes.fromhex(sys.argv[1])))
