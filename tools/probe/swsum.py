#!/usr/bin/env python3
"""swsum: per prop, the layouts whose canary landed in a fuzz12 gen-3 width sweep.  swsum.py RUNDIR..."""
import os, subprocess, sys
from collections import OrderedDict
here = os.path.dirname(os.path.abspath(__file__))
for d in sys.argv[1:]:
    out = subprocess.run([sys.executable, os.path.join(here, 'fuzz12.py'), 'read', '3', d], capture_output=True, text=True).stdout
    t = OrderedDict()
    for l in out.splitlines():
        if l.startswith('#'):
            print(l); continue
        f = l.split('\t'); p, w = f[0][1:3], f[0][4:]
        t.setdefault(p, []).append(w if f[2] == 'landed' else ('?' + w if f[2] == 'unclear' else ''))
    print(os.path.basename(d.rstrip('/')), ' '.join('%s:%s' % (p, '/'.join(x for x in v if x) or '-') for p, v in t.items()))
