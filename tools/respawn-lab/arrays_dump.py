import sys,struct
def parse(b,o):
    h=struct.unpack_from('>I',b,o)[0]; o+=4; kind,n=h>>16,h&0xffff
    if kind==0:
        v=list(struct.unpack_from('>%di'%n,b,o)); return v,o+4*n
    out=[]
    for i in range(n):
        x,o=parse(b,o); out.append(x)
    return out,o
b=open(sys.argv[1],'rb').read(); o=0; arrs=[]
while o<len(b):
    a,o=parse(b,o); arrs.append(a)
print(sys.argv[1],len(arrs),'arrays')
for i in (9,10,11,12,16):
    if i<len(arrs): print(i,arrs[i])
