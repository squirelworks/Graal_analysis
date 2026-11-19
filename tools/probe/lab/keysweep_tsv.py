#!/usr/bin/env python3
"""keysweep_tsv.py: turn keysweep.py's raw rows (DIR/rows.tsv, JSON lines) into the derived table.

  keysweep_tsv.py CLIENT ROWS[,ROWS...] [--clean ROWS2[,...]] [--targets 'player=X,Y hud=X,Y ...'] > client.tsv

Columns: client, key, effect, c2s, script_event, notes.
- effect: new windows (title, size), screen change (pixels, box, near what), chat/state change,
  disconnect or crash.
- c2s: the client->server packets between the key's marks, minus the key logger's own chat props,
  grouped by id (WANTFILE file names folded into one list).
- script_event: what the key logger saw: onKeyPressed(code, char, scan) for GS2 clients, keypressed
  #p(0..2) for GS1 clients, and keydown(0..10) bit changes (D values).
--clean: rows of a run without the key logger; its screen/window effect replaces the logged one (the
logger's chat bubble is then not mixed in), packets are taken from the logged run minus logger chat.
"""
import argparse, json, re, sys
from collections import OrderedDict


def load(paths):
    """rows by key name; a later row for the same key (a later run, or a later file) wins"""
    rows = OrderedDict()
    for path in paths.split(','):
        for ln in open(path):
            r = json.loads(ln)
            if r.get('skipped'):
                rows.setdefault('#%d' % r['i'], {'i': r['i'], 'skipped': True})
                continue
            rows[r['key']] = r
    return rows


def near(box, tg, org=(0, 0)):
    """box in screen coordinates; reported relative to the game window (org = its top left)"""
    if not box:
        return ''
    x0, y0, x1, y1 = box[0] - org[0], box[1] - org[1], box[2] - org[0], box[3] - org[1]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    best, bd = '', 1e9
    for k, (x, y) in tg.items():
        d = ((cx - x) ** 2 + (cy - y) ** 2) ** 0.5
        if d < bd:
            best, bd = k, d
    w, h = x1 - x0 + 1, y1 - y0 + 1
    where = 'near %s' % best if bd < 120 else 'centre %d,%d' % (cx, cy)
    return '%dx%d box %d,%d-%d,%d (%s)' % (w, h, x0, y0, x1, y1, where)


def script_of(c2s):
    ev, rest = [], []
    for c in c2s:
        m = re.match(r"2:PLAYERPROPS\{(.*)\}$", c)
        if m:
            props = m.group(1)
            ch = re.search(r"chat='([KD][^']*)'", props)
            if ch:
                v = ch.group(1)
                if v[0] == 'K':
                    p = v[1:].split('_')
                    ev.append('key(%s)' % ','.join(p))
                elif v != 'D0' or not ev or ev[-1] != 'keydown=0':
                    ev.append('keydown=%s' % v[1:])
                props = re.sub(r" ?chat='[KD][^']*'", '', props).strip()
                if not props:
                    continue
                c = '2:PLAYERPROPS{%s}' % props
        rest.append(c)
    return ev, rest


def fold(c2s):
    files, out, last = [], [], None
    for c in c2s:
        m = re.match(r'23:WANTFILE\{(.*)\}$', c)
        if m:
            files.append(m.group(1)); continue
        if c == last:
            continue
        out.append(c); last = c
    # collapse runs of position-only props into first..last
    res, run = [], []
    def flush():
        if len(run) > 2:
            res.append('%s ..(%d).. %s' % (run[0], len(run) - 2, run[-1]))
        else:
            res.extend(run)
        run.clear()
    for c in out:
        if re.match(r'2:PLAYERPROPS\{(x2|y2|x|y)=[^ ]*\}$', c):
            run.append(c)
        else:
            flush(); res.append(c)
    flush()
    if files:
        res.append('23:WANTFILE{%s}' % ','.join(sorted(set(files))))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('client'); ap.add_argument('rows'); ap.add_argument('--clean')
    ap.add_argument('--targets', default='')
    ap.add_argument('--origin', default='0,0', help='game window top left on the screen, for rows without game_xy')
    a = ap.parse_args()
    tg = {}
    for t in a.targets.split():
        k, v = t.split('='); x, y = v.split(','); tg[k] = (int(x), int(y))
    rows = load(a.rows); clean = load(a.clean) if a.clean else {}
    print('\t'.join(['client', 'key', 'effect', 'c2s', 'script_event', 'notes']))
    for i, r in rows.items():
        if r.get('skipped'):
            print('\t'.join([a.client, '#%d' % r['i'], 'not tested (client did not come up three times)', '', '', ''])); continue
        v = clean.get(i) if clean.get(i) and not clean[i].get('skipped') else r
        eff, notes = [], []
        if v['new_windows']:
            eff.append('opens window: ' + '; '.join(v['new_windows']))
        if v['diff_px'] and v['diff_px'] > 0:
            org = v.get('game_xy') or [int(x) for x in a.origin.split(',')]
            eff.append('screen %d px %s' % (v['diff_px'], near(v['diff_box'], tg, org)))
        if not r['alive'] or not r['alive_after']:
            eff.append('CLIENT GONE (crash or quit)')
        elif not r['connected'] or not r['connected_after']:
            eff.append('DISCONNECTED')
        if v['windows_left']:
            notes.append('window would not close: ' + ', '.join(v['windows_left']))
        if v['reset']:
            notes.append('reset: ' + ', '.join(v['reset']))
        if v.get('after_reset_px', 0) and v['after_reset_px'] > 20000:
            notes.append('screen still differs after reset (%d px)' % v['after_reset_px'])
        ev, rest = script_of(r['c2s'])
        f = fold(rest)
        props = [c for c in f if c.startswith('2:')]
        if any('chat=' in c for c in props):
            eff.append('chat prop sent')
        if v is not r:
            notes.append('effect from the run without the key logger')
        print('\t'.join([a.client, r['key'], '; '.join(eff) or 'nothing seen', ' | '.join(f) or '-',
                         ' '.join(ev) or '-', '; '.join(notes)]))


if __name__ == '__main__':
    sys.exit(main())
