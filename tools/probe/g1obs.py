#!/usr/bin/env python3
"""g1obs: per row, what the gen-1 client sent back (line kinds, the sender id inside its D lines),
and connection events, from a fuzz12 gen-1 run's proxy.log.

  g1obs.py RUNDIR...
"""
import re, sys
from collections import OrderedDict


def sid(b):
    return (b[0] - 32) * 128 + (b[1] - 32) if len(b) >= 2 else None


def run(d):
    rows = OrderedDict(); cur = 'pre'; rows[cur] = {'lines': [], 'sids': OrderedDict(), 'ev': []}
    for line in open(d + '/proxy.log', encoding='latin1'):
        m = re.search(r'MARK plan: mark row (\S+)', line)
        if m:
            cur = m.group(1); rows[cur] = {'lines': [], 'sids': OrderedDict(), 'ev': []}; continue
        m = re.search(r' (c\d) (C>S|S>C) line len=(\d+) \| .* \| hex=([0-9a-f]*)', line)
        if m:
            conn, dr, ln, hx = m.groups(); b = bytes.fromhex(hx)
            if dr == 'C>S':
                if b[:1] == b'D' and len(b) >= 4:
                    s = sid(b[1:3]); rows[cur]['sids'][s] = rows[cur]['sids'].get(s, 0) + 1
                    rows[cur]['lines'].append(conn + ':D' + chr(b[3]))
                else:
                    rows[cur]['lines'].append(conn + ':' + b.decode('latin1')[:16])
            elif not hx.startswith('6d4c') and b[:1] not in (b'D',):
                rows[cur]['lines'].append(conn + '<' + b.decode('latin1')[:12])
            continue
        m = re.search(r' (c\d) conn \d+ (closed by \w+|error .*)', line)
        if m:
            rows[cur]['ev'].append(m.group(1) + ' ' + m.group(2)[:40])
    for n, r in rows.items():
        kinds = OrderedDict()
        for x in r['lines']:
            kinds[x] = kinds.get(x, 0) + 1
        ks = ' '.join('%s%s' % (k, '' if v == 1 else 'x%d' % v) for k, v in kinds.items())
        print('%s\t%s\tsids=%s\t%s\t%s' % (d.rstrip('/').split('/')[-1], n, dict(r['sids']), ks[:200], '; '.join(r['ev'])))


for d in sys.argv[1:]:
    run(d)
