#!/usr/bin/env python3
"""mktsv12: probe-results.tsv rows for the 2026-11-19 early-client campaign, with a protocol reading
per row. Run from the lab results folder (labs/fz12). Prints TSV rows on stdout."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); import fuzz12  # noqa: E402

DATE = '2026-11-19'
G2 = [('128', 'c128-2', 'win-1.28b2 (gen 2, GSERV013)'), ('13', 'c13-1', 'win-1.3test (gen 2, GSERV014)'),
      ('131', 'c131-1', 'win-1.31 (gen 2, GSERV016)'), ('132', 'c132-1', 'win-1.32 (gen 2, GSERV018)'),
      ('133', 'c133-1', 'win-1.33 (gen 2, GNW20020)'), ('134', 'c134-1', 'win-1.34 (gen 2, GNW22030)'),
      ('135', 'c135-1', 'win-1.35 (gen 2, GNW13040)'), ('136', 'c136-1', 'win-1.36 (gen 2, GNW10050)'),
      ('137', 'c137-1', 'win-1.37 (gen 2, GNW21050)'), ('138', 'c138-1', 'win-1.38 (gen 2, GNW22060)'),
      ('139', 'c139-1', 'win-1.39 (gen 2, GNW07080)')]

OBS2 = {
    'p3-i3': 'prop 3 (rupees) read as GINT3; next prop read',
    'p4-c': 'prop 4 (arrows) read as one byte',
    'p0-str': 'prop 0 (nickname) read as length-prefixed string',
    'p12-str': 'prop 12 (chat) read as length-prefixed string',
    'p40-c1': 'unknown own prop 40: client stops reading the message (no one-byte skip as in 4.x-6.x)',
    'p50-c1': 'unknown own prop 50: rest of message not read',
    'p83-i5': 'unknown own prop 83: rest of message not read',
    'p90-i3': 'unknown own prop 90: rest of message not read',
    'plo30-empty': 'PLO 30 with empty body: no effect, next message in frame read',
    'nul-nick': 'NUL inside a string prop: rest of frame dropped (NUL ends the frame)',
    'high-nick': 'byte 0xFF inside a string: read as data',
    'nul-chat': 'NUL as the only chat byte: rest of frame dropped',
    'raw0-bombs': 'raw 0x00 as a prop value: rest of frame dropped',
    'high-rupees': 'all-0xFF GINT3: decoded without error, next prop read',
    'id00': 'id byte 0x00 (id -32): rest of frame dropped',
    'id1f': 'id byte 0x1F (id -1) with text: line ignored, next message read',
    'id7f': 'id byte 0x7F (id 95) with text: line ignored',
    'idff': 'id byte 0xFF (id 223) with text: line ignored',
    'emptyline': 'a lone LF (empty message): rest of frame dropped',
    'cr-in-props': 'CR after the last prop: ignored',
    'nick-223': '223-byte nickname (length byte 0xFF) read whole',
    'trunc-prop': 'prop id with no value at message end: no effect on the next message',
}
for pid in (42, 60, 110):
    OBS2['plo%d-empty' % pid] = 'unknown PLO %d, empty: ignored, next message read' % pid
    OBS2['plo%d-c1' % pid] = 'unknown PLO %d, one byte: ignored' % pid
    OBS2['plo%d-text' % pid] = 'unknown PLO %d, text body: ignored' % pid
    OBS2['plo%d-bin' % pid] = 'unknown PLO %d with ff 00 ff 00: rest of frame dropped (the NUL)' % pid

G1 = [('1st', '1st Graal'), ('2nd', '2nd Graal'), ('3rd', '3rd Graal'), ('4th', '4th Graal'), ('4thalpha', '4th Graal alpha'),
      ('5th', '5th Graal'), ('6th', '6th Graal'), ('7th', '7th Graal'), ('8th', '8th Graal'), ('9th', '9th Graal'),
      ('10th', '10th Graal'), ('11th', '11th Graal'), ('12th', '12th Graal'), ('13th', '13th Graal'), ('14th', '14th Graal'),
      ('15th', '15th Graal'), ('11', '1.1'), ('119', '1.1.9')]
RESET1K = {'10th', '11th', '12th', '13th', '14th', '15th', '11'}

OBS1 = {  # what the row is; gen 1 has no in-band canary, so a D row shows only reply / connection / alive
    'lobby-I-short': '`I` with 2 digits',
    'lobby-I-long': '`I` + 40 digits',
    'lobby-plus-empty': '`+` with no id',
    'lobby-plus-long': '`+` with a 300-char id, while partnered',
    'lobby-P-unknown': '`P` for an id never announced',
    'lobby-C-empty': 'bare `C`',
    'lobby-minus-unknown': '`-` for an unknown id',
    'lobby-unknown-cmd': 'unknown command letter `Z`',
    'lobby-NR': '`NR` mid-session',
    'lobby-NX': '`NX` (unknown N sub-command)',
    'd-empty': '`D` with no sid', 'd-sid-only': '`D` + partner sid, no type', 'd-type-unknown': 'D type `~`',
    'd-chat': 'D type C (chat)', 'd-chat-high': 'D type C with bytes 0x80-0xFF', 'd-nick-long': 'D type N, 600 bytes',
    'd-pos-short': 'D type P, no coordinates', 'd-pos-high': 'D type P, 0xFF coordinates', 'd-board-short': 'D type B, truncated header',
    'd-board-big': 'D type B announcing more tiles than sent', 'd-baddy-M-short': 'D type M, partial record',
    'd-colours-many': 'D type S, count 0xDF', 'd-time-short': 'D type T, 1 of 10 chars', 'd-carry-npc-short': 'D type 3, no payload',
    'd-dead-list': 'D type D, 30 high-byte ids', 'd-unknown-sid': 'D from a sid that is no partner',
    'line-nul': 'NUL inside a D line', 'line-cr': 'CR before LF', 'emptyline': 'empty line',
}
SENDS_D = {'10th', '11th', '12th', '13th', '14th', '15th', '11'}   # send arrow D lines on their start level


def g2rows():
    for b, run, client in G2:
        fuzz12.OUT.clear(); fuzz12.read(2, run)
        for r in fuzz12.OUT:
            n, sp, c, post, alive, rep, v, rr = r
            t = sp.split(' | ')[0].split(); pk = 'raw' if t[0] == 'raw' else t[0]
            pr = t[1][2:] if pk == '9' and len(t) > 1 and t[1].startswith('c:') else '-'
            obs = OBS2.get(n, '') + ' [' + v + ']'
            yield [DATE, client, 's2c', pk, pr, sp, 'yes' if c == 'landed' else 'no', alive, rep or 'none', obs, 'w%s-row' % b, n]


def g1rows():
    for b, label in G1:
        run = {'9th': 'e9th-1'}.get(b, 'd%s-1' % b)
        runs = [run] + (['d%s-2' % b] if os.path.isdir('g1all/d%s-2' % b) and b != '9th' else [])
        fuzz12.OUT.clear()
        for d in runs:
            fuzz12.read(1, 'g1all/' + d)
        for r in fuzz12.OUT:
            n, sp, c, post, alive, rep, v, rr = r
            obs = OBS1.get(n, '') + ': no reply, both relay connections kept'
            if n == 'd-chat-1100':
                obs = ('1104-byte D line: client resets the level connection (longer than its ~1 KB read buffer)'
                       if b in RESET1K else '1104-byte D line: connection kept')
                v = 'conn-reset' if b in RESET1K else v
            if n == 'lobby-I-long' and b in SENDS_D:
                obs = '`I` + 40 digits: own sid in later D lines = low 14 bits of the first 8 digits (99999999)'
            if n == 'lobby-I-short' and b in SENDS_D:
                obs = '`I` with 2 digits: own sid unchanged'
            if sp.startswith('-0000'):
                sp = '`-` + id %d as 8 digits' % int(sp[1:])
            pk = 'D' + sp[3] if sp.startswith('D') and len(sp) > 3 else (sp[:1] or 'LF')
            yield [DATE, 'win-%s (gen 1 relay)' % label, 's2c', pk, '-', sp, '-', alive, rep or 'none', obs + ' [' + v + ']', 'w%s-row' % b, n]


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


def sweep():
    for b, _, client in G2:
        fuzz12.OUT[:] = merged(b)
        got = {}
        for r in fuzz12.OUT:
            p, w = int(r[0][1:3]), r[0][4:]
            got.setdefault(p, []).append((w, r[2]))
        for p in sorted(got):
            landed = [w for w, c in got[p] if c == 'landed']
            unclear = [w for w, c in got[p] if c == 'unclear']
            if landed:
                obs = 'own prop %d read as %s' % (p, '/'.join(landed))
            elif len(unclear) == len(got[p]):
                obs = 'own prop %d: unreadable (HUD hidden)' % p
            else:
                obs = 'own prop %d: none of 1/2/3/5-byte number, string, byte+string; compound or not read (message ends)' % p
            yield [DATE, client, 's2c', '9', str(p), 'width sweep c/s/i3/i5/str/cstr + bombs canary', 'yes' if landed else 'no',
                   'yes', 'none', obs, 'w%s-sweep' % b, 'w%02d' % p]


LOBBY = {
    'I-8digits': 'own id set to 12345678; sender id in later D lines = 8526 (id mod 16384)',
    'I-9digits': 'no change (first 8 digits same as before)',
    'I-7digits': 'ignored (fewer than 8 digits)',
    'I-nondigit': 'client stops sending its arrow D lines',
    'I-junk-after': 'not observable (no D lines since the previous row)',
    'I-empty': 'not observable (no D lines)',
    'I-reset': 'id back to 1 (seen in the next push)',
    'C-partner': 'no reply',
    'P-partner-again': 'no reply, no push (already partnered)',
    'plus-partner-again': 'no reply (already partnered)',
    'minus-partner': 'no reply; the client is now unpartnered',
    'plus-new-peer': 'client answers P with the new id (it had no partner)',
    'P-new-peer': 'client pushes its state to the new partner',
    'NL-alone': 'no reply',
    'NR-alone': 'no reply',
}


def lobby():
    lines = {n: l[0] for n, l in fuzz12.rows4()}
    for b, label in [('15th', '15th Graal'), ('11', '1.1'), ('10th', '10th Graal'), ('5th', '5th Graal'), ('1st', '1st Graal'), ('119', '1.1.9')]:
        out = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'g1obs.py'), 'g1all/l%s-1' % b],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            f = line.split('	')
            if f[1] in ('pre', 'baseline'):
                continue
            sent = lines[f[1]]
            sp = '`-` + id %d as 8 digits' % int(sent[1:]) if sent.startswith('-0000') else sent
            seen = (f[3] or 'nothing').replace('c1:', '').replace('c2:', 'fixed:')
            mean = LOBBY.get(f[1], '')
            if b == '119' or (f[1].startswith('I-') and b in ('5th', '1st')):
                mean = 'no visible reaction (this build sends no D lines here)' if f[1].startswith('I-') or b == '119' else mean
            ev = '' if f[1] == 'NR-alone' else ('; ' + f[4] if f[4] else '')
            yield [DATE, 'win-%s (gen 1 relay)' % label, 's2c', 'lobby', '-', sp, '-', 'yes', seen[:80],
                   '%s; own sender ids seen %s%s' % (mean, f[2][5:], ev), 'w%s-lobby' % b, f[1]]

if __name__ == '__main__':
    for gen in (g2rows, g1rows, sweep, lobby):
        for row in gen():
            print('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in row))
