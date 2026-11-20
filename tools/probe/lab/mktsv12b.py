#!/usr/bin/env python3
"""mktsv2: probe-results.tsv rows for the 2026-11-20 follow-up (run from labs/fz12/vm-backup)."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, "..")); import fuzz12  # noqa: E402

DATE = '2026-11-20'
T = '\t'
A = 'fz12/out/'; B = 'fz12b/out/'


def rows():
    out = []
    # gen-2 row set on 1.21
    fuzz12.OUT.clear(); fuzz12.read(2, A + 'c121-1')
    for n, sp, c, post, alive, rep, v, rr in fuzz12.OUT:
        t = sp.split(' | ')[0].split(); pk = 'raw' if t[0] == 'raw' else t[0]
        pr = t[1][2:] if pk == '9' and len(t) > 1 and t[1].startswith('c:') else '-'
        out.append([DATE, 'win-1.21 (gen 2, GSERV007)', 's2c', pk, pr, sp, 'yes' if c == 'landed' else 'no', alive,
                    rep or 'none', 'same as 1.28b2-1.39 (see early-clients note) [%s]' % v, 'w121-row', n])
    # width sweep on 1.21
    fuzz12.OUT.clear(); fuzz12.read(3, A + 's121b-1')
    got = {}
    for r in fuzz12.OUT:
        got.setdefault(int(r[0][1:3]), []).append((r[0][4:], r[2]))
    for p in sorted(got):
        landed = [w for w, c in got[p] if c == 'landed']
        unclear = all(c == 'unclear' for w, c in got[p])
        obs = ('own prop %d read as %s' % (p, '/'.join(landed)) if landed else
               'own prop %d: unreadable (a small X/Y scrolls the HUD over bright tiles)' % p if unclear else
               'own prop %d: no simple layout or past the last prop (message ends)' % p)
        out.append([DATE, 'win-1.21 (gen 2, GSERV007)', 's2c', '9', str(p), 'width sweep c/s/i3/i5/str/cstr + bombs canary',
                    'yes' if landed else 'no', 'yes', 'none', obs, 'w121-sweep', 'w%02d' % p])
    # compound rows
    for b, run, label in [('121', 'k121b-1', '1.21'), ('128', 'k128-2', '1.28b2'), ('13', 'k13-1', '1.3test'), ('132', 'k132-1', '1.32'),
                          ('135', 'k135-1', '1.35'), ('136', 'k136-1', '1.36'), ('139', 'k139-1', '1.39')]:
        fuzz12.OUT.clear(); fuzz12.read(5, A + run)
        extra = A + 'kk%s-1' % b
        if os.path.isdir(extra):
            fuzz12.read(5, extra)
        for n, sp, c, post, alive, rep, v, rr in fuzz12.OUT:
            out.append([DATE, 'win-%s (gen 2)' % label, 's2c', '9', sp.split()[1][2:], sp, 'yes' if c == 'landed' else 'no', alive,
                        rep or 'none', 'compound layout row: canary %s' % c, 'w%s-compound' % b, n])
    # PLO 8 with the level
    drawn = {('128', '1'): 'no', ('128', '2'): 'no', ('128', 'l'): 'no', ('135', '1'): 'yes', ('135', '2'): 'no', ('135', 'l'): 'no',
             ('136', '1'): 'no', ('136', '2'): 'yes', ('136', 'l'): 'yes', ('139', '1'): 'no', ('139', '2'): 'yes', ('139', 'l'): 'yes'}
    specs = {'1': ('pl8-1byte-lvl', '8 c:7 c:0 str:one c:20 str:<own level> c:15 c:52 c:16 c:60 c:17 c:2 c:13 (5) c:11 c:3'),
             '2': ('pl8-2byte-lvl', '8 s:9 c:0 str:two c:20 str:<own level> c:15 c:70 c:16 c:60 c:17 c:2 c:13 (5) c:11 c:3'),
             'l': ('pl8-lvl-first', '8 s:11 c:20 str:<own level> c:0 str:three c:15 c:60 c:16 c:56 c:17 c:2')}
    for b, label in [('128', '1.28b2'), ('135', '1.35'), ('136', '1.36'), ('139', '1.39')]:
        for k, (n, sp) in specs.items():
            out.append([DATE, 'win-%s (gen 2)' % label, 's2c', '8', '-', sp, '-', 'yes', 'none',
                        'other player drawn: %s' % drawn[(b, k)], 'w%s-pl8' % b, n])
    # gen-1 rows on the alphas and the 9th re-run
    for b, runs, label in [('5thalpha', ['f5thalpha-1'], '5th Graal alpha'), ('9thalpha', ['g9thalpha-1', 'g9thalpha-2'], '9th Graal alpha'),
                           ('9th', ['g9th-1'], '9th Graal')]:
        fuzz12.OUT.clear()
        for r in runs:
            fuzz12.read(1, B + r)
        for n, sp, c, post, alive, rep, v, rr in fuzz12.OUT:
            pk = 'D' + sp[3] if sp.startswith('D') and len(sp) > 3 else (sp[:1] or 'LF')
            if sp.startswith('-0000'):
                sp = '`-` + id %d as 8 digits' % int(sp[1:])
            out.append([DATE, 'win-%s (gen 1 relay)' % label, 's2c', pk, '-', sp, '-', alive, rep or 'none',
                        'no reply; both relay connections kept [%s]' % v if v == 'alive' else v, 'w%s-row' % b, n])
    # gen-1 lobby probes on the alphas and the 9th
    for b, run, label in [('5thalpha', 'm5thalpha-1', '5th Graal alpha'), ('9thalpha', 'n9thalpha-1', '9th Graal alpha'), ('9th', 'n9th-1', '9th Graal')]:
        o = subprocess.run([sys.executable, os.path.join(here, "..", "g1obs.py"), B + run], capture_output=True, text=True).stdout
        lines = {n: l[0] for n, l in fuzz12.rows4()}
        for line in o.splitlines():
            f = line.split(T)
            if f[1] in ('pre', 'baseline'):
                continue
            sent = lines[f[1]]
            sp = '`-` + id %d as 8 digits' % int(sent[1:]) if sent.startswith('-0000') else sent
            out.append([DATE, 'win-%s (gen 1 relay)' % label, 's2c', 'lobby', '-', sp, '-', 'yes', (f[3] or 'nothing')[:80],
                        'own sender ids seen %s' % f[2][5:], 'w%s-lobby' % b, f[1]])
    # 1.1.9 fake-peer timing
    for run, how, res in [('y119-2', '+ 2 s after the join', 'no P, no push'), ('y119-5', '+ 5 s after the join', 'no P, no push'),
                          ('y119-10', '+ 10 s after the join', 'no P, no push'), ('z119-c0', 'C then + at the join', 'P on the level connection, no push'),
                          ('z119-c3', 'C then + 3 s after the join', 'no P, no push')]:
        out.append([DATE, 'win-1.1.9 (gen 1 relay)', 's2c', 'lobby', '-', 'fake peer: ' + how, '-', 'yes', res,
                    'answers a peer only right after it joins a room; no state push to a fake peer in any form', 'w119-lobby', run])
    out.append([DATE, 'win-15th Graal (gen 1 relay)', 's2c', 'lobby', '-', 'fake peer: + 5 s after the join', '-', 'yes',
                'P on both connections, then the state push', 'control for the 1.1.9 timing rows', 'w15th-lobby', 'y15th-5'])
    return out


if __name__ == '__main__':
    for r in rows():
        print(T.join(str(x).replace(T, ' ').replace('\n', ' ') for x in r))
