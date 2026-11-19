#!/usr/bin/env python3
"""widthmd: markdown rows of the own-prop width table from the sweeps (run from labs/fz12)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); import fuzz12  # noqa: E402

NAMES = {'c': '1', 's': 'GSHORT', 'i3': 'GINT3', 'i5': '5 bytes', 'str': 'string', 'cstr': 'byte + string'}
COLS = [('128',), ('13',), ('131',), ('132',), ('133',), ('134', '135'), ('136', '137', '138'), ('139',)]


def merged(b):
    """Sweep rows for build b: first pass for props 0-2, re-runs (fresh logins) for 3-16 and 17-40."""
    parts = [('s', None, 'w03'), ('t', 'w03', 'w17'), ('u', 'w17', None)]
    have = [p for p in parts if os.path.isdir('sw/%s%s-1' % (p[0], b))]
    rows = []
    for i, (k, lo, hi) in enumerate(have):
        nxt = have[i + 1][1] if i + 1 < len(have) else None
        fuzz12.OUT.clear(); fuzz12.read(3, 'sw/%s%s-1' % (k, b))
        rows += [r for r in fuzz12.OUT if (lo is None or r[0] >= lo) and (nxt is None or r[0] < nxt)]
    return rows


def table(b):
    rows = merged(b)
    t = {}
    for r in rows:
        p, w = int(r[0][1:3]), r[0][4:]
        t.setdefault(p, {'landed': [], 'unclear': [], 'n': 0})
        t[p]['n'] += 1
        if r[2] == 'landed':
            t[p]['landed'].append(w)
        elif r[2] == 'unclear':
            t[p]['unclear'].append(w)
    out = {}
    for p, v in t.items():
        if len(v['landed']) == 1:
            out[p] = NAMES[v['landed'][0]]
        elif len(v['landed']) > 1:
            out[p] = NAMES[v['landed'][0]] + '?'   # more than one landed: the first (shortest) is the likely one
        elif len(v['unclear']) == v['n']:
            out[p] = 'n/a'
        else:
            out[p] = '—'
    return out


def main():
    tabs = {b: table(b) for col in COLS for b in col}
    diff = []
    for col in COLS:
        if len(col) > 1:
            for p in range(41):
                vals = {tabs[b].get(p) for b in col}
                if len(vals) > 1:
                    diff.append((col, p, {b: tabs[b].get(p) for b in col}))
    for p in range(41):
        if p == 5:
            continue
        cells = [tabs[col[0]].get(p, '') for col in COLS]
        print('| %d | %s |' % (p, ' | '.join(cells)))
    for d in diff:
        print('# differs inside merged column', d, file=sys.stderr)


if __name__ == '__main__':
    main()
