import sys, time, json, random; sys.path.insert(0,'/root/lab/tools')
from g2cli import Cli
def gs(v): return bytes([(v>>7)+32,(v&0x7f)+32])
def bm(x,y,w,h,tiles): return bytes([x+32,y+32,w+32,h+32])+b''.join(gs(t) for t in tiles)
A=Cli('guest','guest'); B=Cli('guest','guest')
A.recv(2); B.recv(2); A.recv(0.5)
log=open(sys.argv[1],'w')
def note(**k): k['t']=round(time.time(),3); log.write(json.dumps(k)+'\n'); log.flush()
sent={}
# shapes test first
tests=[(2,2),(1,1),(2,1),(1,2),(4,4),(3,3),(2,2)]
pos=[(2+i*5,2) for i in range(len(tests))]
for (w,h),(x,y) in zip(tests,pos):
    A.send(1,bm(x,y,w,h,[677+i%2+16*(i//2) for i in range(w*h)])); sent[(x,y)]=time.time(); note(ev='send',x=x,y=y,w=w,h=h)
# timing samples: N 2x2 changes spread over rows 10..60, spaced 0.37 s apart
N=int(sys.argv[2])
pts=[(2+(i%15)*4, 10+(i//15)*3) for i in range(N)]
for (x,y) in pts:
    A.send(1,bm(x,y,2,2,[677,678,693,694])); sent[(x,y)]=time.time(); note(ev='send',x=x,y=y,w=2,h=2)
    for c,nm in ((A,'A'),(B,'B')):
        for mid,d in c.recv(0.01):
            if mid==7: note(ev='recv',who=nm,x=d[0]-32,y=d[1]-32,w=d[2]-32,h=d[3]-32,first=(d[4]-32)*128+d[5]-32)
    time.sleep(0.37)
end=time.time()+20
while time.time()<end:
    for c,nm in ((A,'A'),(B,'B')):
        for mid,d in c.recv(0.05):
            if mid==7: note(ev='recv',who=nm,x=d[0]-32,y=d[1]-32,w=d[2]-32,h=d[3]-32,first=(d[4]-32)*128+d[5]-32)
