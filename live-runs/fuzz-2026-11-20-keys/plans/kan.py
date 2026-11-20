#!/usr/bin/env python3
# kan.py proxy.log : per plan mark, C>S packets with a printable body (non-printables as .), ids 3/24 skipped
import sys,re
cur=None; order=[]; out={}
def pr(h):
    b=bytes.fromhex(h); return ''.join(chr(c) if 32<=c<127 else '.' for c in b)
for l in open(sys.argv[1],errors='replace'):
    m=re.search(r'MARK plan: mark (.*)',l)
    if m: cur=m.group(1).strip(); order.append(cur); out[cur]=[]; continue
    if cur is None: continue
    m=re.search(r'^\s*([\d.]+) \S+ (c\d+) C>S id=(\d+) len=(\d+) \| (.*?) \| hex=(\S*)',l)
    if m and m.group(3) not in ('3','24'):
        out[cur].append(f"{m.group(3)}:{pr(m.group(6))}")
for k in order:
    xs=out[k]
    # collapse runs
    s=[]; 
    for x in xs:
        if s and s[-1][0]==x: s[-1][1]+=1
        else: s.append([x,1])
    print(f"## {k}: "+' | '.join(a if c==1 else f"{a} x{c}" for a,c in s)[:1500])
