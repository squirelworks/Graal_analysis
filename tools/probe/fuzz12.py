#!/usr/bin/env python3
"""fuzz12: S->C row set for the early (gen 1 / gen 2) clients, plan writer and result reader.

  fuzz12.py rows GEN                    list the row names
  fuzz12.py plan GEN FIRST [LAST]       write a probectl plan for rows FIRST..LAST (names or numbers)
  fuzz12.py read GEN RUNDIR...          classify each row from the runs' shots, marks and proxy logs
  fuzz12.py tsv GEN CLIENT DATE RUNDIR... the same as protocol/probe-results.tsv rows
  fuzz12.py next GEN RUNDIR FIRST       the row a campaign resumes at after that run (crash -> the next row)

Gen 2 (1.21-1.39, GSERV/GNW tokens): the canary is the HUD bomb count. Each row resets it to 1,
sends the row with bombs=99 behind it (in the same message, or as its own message in the same
frame), takes a shot, then sends bombs=99 again in a frame of its own and takes a "post" shot.
  row landed              -> ok: the row was read with the expected width, and the rest too
  row lost, post landed   -> ignored-rest: the client dropped the rest of that message or frame
  both lost, alive        -> desync-or-hang
  CLIENT-GONE             -> crash (the game window went away)
Gen 1 (1998 relay, text lines): relay98 --fakepeer pairs the client with a fake partner (id 9900)
as it joins its level room; the D rows carry that partner's id. These clients send nothing unprompted
and do not redraw while idle under Wine, so there is no in-band canary: a row is `crash` (window
gone), `conn-closed` (the client dropped a relay connection) or `alive`.
"""
import os, re, sys

CAN = 'c:5 c:99'


def rows2():
    r = []
    own = lambda n, s: r.append((n, '9 %s %s' % (s, CAN)))           # canary inside the same message
    sep = lambda n, s: r.append((n, '%s | 9 %s' % (s, CAN)))          # canary as its own message, same frame
    own('p3-i3', 'c:3 i3:4321')
    own('p4-c', 'c:4 c:7')
    own('p0-str', 'c:0 str:probe')
    own('p12-str', 'c:12 str:hi')
    own('p40-c1', 'c:40 c:1')
    own('p50-c1', 'c:50 c:1')
    own('p83-i5', 'c:83 i5:1234')
    own('p90-i3', 'c:90 i3:300000')
    for pid in (42, 60, 110):
        sep('plo%d-empty' % pid, '%d' % pid)
        sep('plo%d-c1' % pid, '%d c:1' % pid)
        sep('plo%d-text' % pid, '%d t:"probe body 0123456789"' % pid)
        sep('plo%d-bin' % pid, '%d hex:ff00ff00' % pid)
    sep('plo30-empty', '30')
    own('nul-nick', 'c:0 hex:23610062')
    own('high-nick', 'c:0 hex:2361ff62')
    own('nul-chat', 'c:12 hex:2100')
    sep('raw0-bombs', '9 c:5 b:0')
    own('high-rupees', 'c:3 hex:ffffff')
    sep('id00', '-32 t:junk')
    sep('id1f', '-1 t:junk')
    sep('id7f', '95 t:junk')
    sep('idff', '223 t:junk')
    sep('emptyline', 'raw hex:0a')
    sep('cr-in-props', '9 c:4 c:7 hex:0d')
    own('nick-223', 'c:0 b:255 rep:223:A')
    sep('trunc-prop', '9 c:3')
    return r


# Values chosen so that any misread puts unknown prop 90 (0x7a) or 65/66 next, which ends the
# message in every 1.x build, so only the right layout lets the canary land. Every layout has its
# own length (1, 2, 3, 5, 7 and 8 bytes), so a string is never taken for a number of the same width.
WIDTHS = [('c', 'c:3'), ('s', 's:90'), ('i3', 'i3:11610'), ('i5', 'i5:190229850'), ('str', 'str:abcdef'), ('cstr', 'c:1 str:abcdef')]


def rows3():
    """Gen-2 own-prop sweep: props 0-40, each with five layouts, the bomb canary behind it.
    The layout whose canary lands is the one the build reads; none landing = longer/compound or
    the end of the build's prop table (it stops reading the message there)."""
    r = []
    for p in range(0, 41):
        if p == 5:
            continue  # the canary prop itself
        for wn, val in WIDTHS:
            r.append(('w%02d-%s' % (p, wn), '9 c:%d %s %s' % (p, val, CAN)))
    return r


def plan2(rows, post=True):
    out = ['# fuzz12 gen-2 rows (generated)', 'waitsession 240', 'wait s2c 9 90', 'sleep 10',
           's2c 9 c:5 c:1', 'sleep 1.5', 'shot ref-01', 's2c 9 %s' % CAN, 'sleep 1.5', 'shot ref-99']
    for n, spec in rows:
        out += ['mark row %s' % n, 's2c 9 c:5 c:1', 'sleep 0.8', 's2c %s' % spec, 'sleep 1.3', 'shot %s' % n]
        if post:
            out += ['s2c 9 %s' % CAN, 'sleep 1.5', 'shot %s-post' % n]
    out += ['sleep 2', 'shot final']
    return out


PEER = 9900                                            # the fake partner the D rows speak for
SID = chr(PEER // 128 + 32) + chr(PEER % 128 + 32)     # its id as two base-128 characters


def rows1():
    """Gen 1 relay rows: each is a list of S->C lines (text, no LF)."""
    D = lambda t, payload='': 'D' + SID + t + payload
    return [
        ('lobby-I-short', ['I12']),
        ('lobby-I-long', ['I' + '9' * 40]),
        ('lobby-plus-empty', ['+']),
        ('lobby-plus-long', ['+' + 'A' * 300]),
        ('lobby-P-unknown', ['P00009999']),
        ('lobby-C-empty', ['C']),
        ('lobby-minus-unknown', ['-' + '%08d' % 7777]),
        ('lobby-unknown-cmd', ['Zprobe']),
        ('lobby-NR', ['NR']),
        ('lobby-NX', ['NX']),
        ('d-empty', ['D']),
        ('d-sid-only', ['D' + SID]),
        ('d-type-unknown', [D('~', 'probe')]),
        ('d-chat', [D('C', 'probe chat')]),
        ('d-chat-high', [D('C', '\xff\xfe\x80')]),
        ('d-chat-1100', [D('C', 'x' * 1100)]),
        ('d-nick-long', [D('N', 'n' * 600)]),
        ('d-pos-short', [D('P')]),
        ('d-pos-high', [D('P', '\xff\xff\xff')]),
        ('d-board-short', [D('B', '!!')]),
        ('d-board-big', [D('B', '  \xff' + '!' * 40)]),
        ('d-baddy-M-short', [D('M', '!')]),
        ('d-colours-many', [D('S', '\xff' + '!' * 20)]),
        ('d-time-short', [D('T', '!')]),
        ('d-carry-npc-short', [D('3')]),
        ('d-dead-list', [D('D', '\xff' * 30)]),
        ('d-unknown-sid', ['D\xff\xffCfrom nobody']),
        ('line-nul', [D('C', 'a\x00b')]),
        ('line-cr', [D('C', 'ab\r')]),
        ('emptyline', ['']),
    ]


def rows4():
    """Gen-1 lobby semantics probes. Read with g1obs.py: the sender id inside the client's own D
    lines shows its current id; whether D lines keep flowing shows whether it still has a partner."""
    peer = '0000%04d' % PEER
    return [
        ('I-8digits', ['I12345678']),
        ('I-9digits', ['I123456789']),
        ('I-7digits', ['I1234567']),
        ('I-nondigit', ['I1234567x']),
        ('I-junk-after', ['I00000005junk']),
        ('I-empty', ['I']),
        ('I-reset', ['I00000001']),
        ('C-partner', ['C' + peer]),
        ('P-partner-again', ['P' + peer]),
        ('plus-partner-again', ['+' + peer + 'def']),
        ('minus-partner', ['-' + peer]),
        ('plus-new-peer', ['+00009800def']),
        ('P-new-peer', ['P00009800']),
        ('NL-alone', ['NL']),
        ('NR-alone', ['NR']),
    ]


def hexline(l):
    return 's2c raw hex:' + (l.encode('latin1') + b'\n').hex()


def plan4(rows, conn=1):
    out = ['# fuzz12 gen-1 lobby probes (generated)', 'waitsession 240', 'sleep 10', 'use %d' % conn, 'mark row baseline', 'sleep 6']
    for n, lines in rows:
        out += ['mark row %s' % n] + [hexline(l) for l in lines] + ['sleep 6', 'shot %s' % n]
    return out + ['shot final']


def plan1(rows, conn=1):
    """The relay (relay98 --fakepeer=9900) has already paired the client with the fake partner
    whose sid the D rows carry. After each row: a shot (window alive?) and the proxy's record of
    whether the client closed either relay connection."""
    out = ['# fuzz12 gen-1 rows (generated)', 'waitsession 240', 'sleep 10', 'use %d' % conn, 'shot ref']
    for n, lines in rows:
        out += ['mark row %s' % n] + [hexline(l) for l in lines] + ['sleep 2.5', 'shot %s' % n]
    out += ['sleep 3', 'shot final']
    return out


def pick(rows, a, b):
    names = [n for n, _ in rows]
    ix = lambda x: int(x) if x.isdigit() else names.index(x)
    lo = ix(a); hi = ix(b) if b else len(rows) - 1
    return rows[lo:hi + 1]


# ---- reading results --------------------------------------------------------------------------

def pixels(im):
    return list(im.get_flattened_data()) if hasattr(im, 'get_flattened_data') else list(im.getdata())


def autobox(d):
    """Bounding box of the pixels that differ between ref-01 and ref-99 (the bomb count)."""
    from PIL import Image, ImageChops
    a = Image.open(os.path.join(d, 'ref-01.png')).convert('L'); b = Image.open(os.path.join(d, 'ref-99.png')).convert('L')
    return ImageChops.difference(a, b).point(lambda v: 255 if v > 40 else 0).getbbox()


def white(im, box):
    """The HUD digits are white: compare only near-white pixels, so a changed background does not count."""
    return [255 if min(p) > 200 else 0 for p in pixels(im.convert('RGB').crop(box))]


def boxv(d, name, box, rl, rd):
    from PIL import Image
    f = os.path.join(d, name + '.png')
    if not os.path.exists(f):
        return None
    x = white(Image.open(f), box)
    dl = sum(abs(p - q) for p, q in zip(x, rl)) / len(x); dd = sum(abs(p - q) for p, q in zip(x, rd)) / len(x)
    return 'landed' if dd < dl * 0.5 else 'lost' if dl < dd * 0.5 else 'unclear'


def replies(d, gen):
    """Per row: C>S ids (gen 2); for gen 1 the line kinds sent after the row, and 'push' when the
    client pushed its state (a `D..N` line) after the row's canary pair."""
    out = {}; cur = None; can = False
    for line in open(os.path.join(d, 'proxy.log'), encoding='latin1'):
        m = re.search(r'MARK plan: mark row (\S+)', line)
        if m:
            cur = m.group(1); out.setdefault(cur, []); can = False; continue
        if 'MARK plan: mark canary' in line:
            can = True; continue
        if cur and gen == 1 and 'closed by client' in line:
            out[cur].append('closed'); continue
        if not cur or ' C>S ' not in line:
            continue
        if gen in (2, 3):
            m = re.search(r'C>S id=(-?\d+)', line)
            if m:
                out[cur].append(m.group(1))
        else:
            m = re.search(r'C>S line len=\d+ \| (\S*)', line)
            if not m:
                continue
            t = m.group(1)
            if can and t[:1] == 'D' and t[3:4] == 'N':
                out[cur].append('push')
            elif not can:
                out[cur].append(t[:1] + (t[3:4] if t[:1] == 'D' else ''))
    return out


OUT = []
WORDS = {'ok': 'canary landed', 'ignored-rest': 'rest of message/frame dropped; separate canary afterwards landed',
         'desync-or-hang': 'canary and separate post-canary both lost: stream desynchronised or game loop stalled',
         'crash': 'client window gone', 'crash-late': 'client window gone before the post-canary',
         'conn-closed': 'client closed a relay connection',
         'alive': 'client window and both relay connections still up (gen 1 has no in-band canary)'}


def tsvrow(gen, client, date, r):
    n, sp, c, post, alive, rep, v, run = r
    if gen in (2, 3):
        t = sp.split(' | ')[0].split(); pk = t[0] if t[0] != 'raw' else 'raw'
        pr = t[1][2:] if pk == '9' and len(t) > 1 and t[1].startswith('c:') else '-'
    else:
        pk = sp[:1] if not sp.startswith('D') or len(sp) < 4 else 'D' + sp[3]
        pr = '-'
    obs = WORDS.get(v.split('+')[0], v) + (' (Wine crash dialog)' if '+errdlg' in v else '')
    return chr(9).join([date, client, 's2c', pk, pr, sp, 'yes' if c == 'landed' else 'no' if c == 'lost' else '-',
                      alive, rep, obs + ' [' + v + ']', run, n])


def read(gen, d):
    marks = {}
    for line in open(os.path.join(d, 'marks.txt'), encoding='latin1'):
        p = line.split()
        if len(p) == 2:
            marks[p[0]] = p[1]
    rep = replies(d, gen)
    rows = rows2() if gen == 2 else rows3() if gen == 3 else rows1()
    if gen in (2, 3):
        from PIL import Image
        box = autobox(d)
        if not box:
            print('# %s: no bomb-count difference between ref-01 and ref-99: canary unusable' % d); return
        rl = white(Image.open(os.path.join(d, 'ref-01.png')), box)
        rd = white(Image.open(os.path.join(d, 'ref-99.png')), box)
    for n, spec in rows:
        if n not in marks:
            continue
        st = marks[n]; alive = st.startswith('alive')
        if gen in (2, 3):
            c = boxv(d, n, box, rl, rd) if alive else '-'
            ps = marks.get(n + '-post', '')
            post = boxv(d, n + '-post', box, rl, rd) if ps.startswith('alive') else '-'
            v = ('crash' if not alive else 'ok' if c == 'landed' else 'ignored-rest' if post == 'landed'
                 else 'crash-late' if post == '-' else 'desync-or-hang')
            r = ','.join(sorted(set(x for x in rep.get(n, []) if x not in ('2', '31'))))
            sp = spec
        else:
            got = rep.get(n, []); c = '-'; post = '-'
            v = 'crash' if not alive else 'conn-closed' if 'closed' in got else 'alive'
            r = ','.join(sorted(set(x for x in got if x not in ('DA', 'DP', 'closed'))))
            sp = ' / '.join(ascii(x)[1:-1] if len(x) < 48 else ascii(x[:24])[1:-1] + '...(%d bytes)' % len(x) for x in spec)
        if 'ERRDLG' in st:
            v += '+errdlg'
        OUT.append([n, sp, c or '-', post or '-', 'yes' if alive else 'no', r or 'none', v, os.path.basename(os.path.normpath(d))])


def main():
    a = sys.argv[1:]
    gen = int(a[1])
    rows = rows2() if gen == 2 else rows3() if gen == 3 else rows4() if gen == 4 else rows1()
    if a[0] == 'rows':
        for i, (n, _) in enumerate(rows):
            print(i, n)
    elif a[0] == 'plan':
        sel = pick(rows, a[2], a[3] if len(a) > 3 else None)
        print('\n'.join(plan2(sel) if gen == 2 else plan2(sel, post=False) if gen == 3 else plan4(sel) if gen == 4 else plan1(sel)))
    elif a[0] == 'read':
        for d in a[2:]:
            read(gen, d)
        for r in OUT:
            print(chr(9).join(r))
    elif a[0] == 'tsv':  # tsv GEN CLIENT DATE RUNDIR... : probe-results.tsv rows
        for d in a[4:]:
            read(gen, d)
        for r in OUT:
            print(tsvrow(gen, a[2], a[3], r))
    elif a[0] == 'next':  # next GEN RUNDIR FIRST: where a campaign resumes after this part
        marks = {}
        for line in open(os.path.join(a[2], 'marks.txt'), encoding='latin1'):
            p = line.split()
            if len(p) == 2:
                marks[p[0]] = p[1]
        names = [n for n, _ in rows]
        for i in range(int(a[3]), len(names)):
            n = names[i]
            if n not in marks:
                print(i); return
            if not marks[n].startswith('alive') or not marks.get(n + '-post', 'alive').startswith('alive'):
                print(i + 1); return
        print(len(names))


if __name__ == '__main__':
    main()
