import sys
B='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
g=[[2047]*64 for _ in range(64)]
def obj(x,y,t):  # t = top-left id of 2x2 block
    g[y][x]=t; g[y][x+1]=t+1; g[y+1][x]=t+16; g[y+1][x+1]=t+17
# row of objects at y=26, player at (30,30)
for i,t in enumerate([2,512,684,34,990,420,2,2]):
    obj(20+i*3,26,t)
for i in range(6): obj(20+i*3,33,2)   # more bushes below
out=['GLEVNW01']
for y in range(64):
    out.append('BOARD 0 %d 64 0 %s'%(y,''.join(B[v>>6]+B[v&63] for v in g[y])))
open(sys.argv[1],'w').write('\n'.join(out)+'\n')
