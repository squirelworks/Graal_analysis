import sys,struct
data=open(sys.argv[1],'rb').read(); tgt=int(sys.argv[2],16)
ncmds=struct.unpack_from('>I',data,16)[0]; off=28
for _ in range(ncmds):
    cmd,sz=struct.unpack_from('>II',data,off)
    if cmd==1:
        n=struct.unpack_from('>I',data,off+48)[0]; s=off+56
        for _ in range(n):
            sect=data[s:s+16].rstrip(b'\0').decode(); a,size,fo=struct.unpack_from('>III',data,s+32)
            if sect=='__text': ta,ts,tf=a,size,fo
            s+=68
    off+=sz
for i in range(0,ts,4):
    w=struct.unpack_from('>I',data,tf+i)[0]
    if w>>26==18:
        li=w&67108860
        if li&33554432: li-=67108864
        t=li if w&2 else ta+i+li
        if t==tgt: print(hex(ta+i), 'bl' if w&1 else 'b')
