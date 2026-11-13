import re,sys
src=open(sys.argv[1]).read()
chain=src[src.index('pub const CHAIN'):src.index('const fn resolve_chain')]
s=set(range(0,30))|set(range(31,35))|{100}
def ids(x): return [int(v) for v in re.findall(r'\d+',x)] if x else []
def rng(x): return [(int(a),int(b)) for a,b in re.findall(r'\((\d+),\s*(\d+)\)',x or '')]
out={}
for blk in re.split(r'\n    Step \{',chain)[1:]:
    tok=re.search(r'token: "(\w+)"',blk).group(1)
    m=re.search(r'\bplo: (IdDelta[^\n]*)',blk)
    if m:
        d=m.group(1)
        if d.startswith('IdDelta::plus_minus'):
            a,b=re.match(r'IdDelta::plus_minus\(&\[([^\]]*)\],\s*&\[([^\]]*)\]\)',d).groups(); s|=set(ids(a)); s-=set(ids(b))
        elif d.startswith('IdDelta::plus('):
            s|=set(ids(re.match(r'IdDelta::plus\(&\[([^\]]*)\]',d).group(1)))
        elif d.startswith('IdDelta {'):
            p=re.search(r'plus: &\[([^\]]*)\]',d); pr=re.search(r'plus_ranges: &\[(.*?)\],',d)
            if p: s|=set(ids(p.group(1)))
            for a,b in rng(pr.group(1) if pr else ''): s|=set(range(a,b+1))
            mi=re.search(r'minus: &\[([^\]]*)\]',d)
            if mi: s-=set(ids(mi.group(1)))
    out.setdefault(tok,sorted(s))
for t in sys.argv[2:]: print(t,len(out[t]),' '.join(map(str,out[t])))
