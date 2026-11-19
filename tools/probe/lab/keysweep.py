#!/usr/bin/env python3
"""keysweep.py: press every key (and mouse action) of a key list on a running Graal client, one at
a time, and record what each one does. Run by keysweep.sh as the `sh` step of a probe plan, while
gen5probe sits between the client and the lab world.

  keysweep.py --disp N --sock CTLSOCK --proxylog LOG --out DIR --keys FILE [--start I]
              [--targets 'player=X,Y ground=X,Y npc=X,Y hud=X,Y'] [--label NAME] [--bytecode HEXFILE]

For each entry: windows + screen before, mark in the proxy log, send it to the game window, wait,
windows + screen after, pixel difference (count and bounding box), alive/connected, the C>S packets
between the marks (decoded: id, name, player props), then reset (close new windows with Escape,
then 'n'; press toggles again) and check again. Rows go to DIR/rows.tsv (appended). When the client
died, lost its session or kept a window open, it writes the next index to DIR/next.txt and exits 3,
so keysweep.sh starts the client again and carries on. Exit 0 when the list is done.

Key list lines (tab separated): NAME  ACTION  [RESET]
  ACTION  key KEYS...        xdotool key (e.g. F1, ctrl+a, alt+Return)
          hold KEY SECS      keydown, wait, keyup
          click B TARGET     B = 1 left, 2 middle, 3 right; TARGET from --targets
          dclick B TARGET    double click
          wheel up|down TARGET
  RESET   again (press the same thing again), undo ACTION (e.g. undo hold Left 0.4), none
          default: again only if a large part of the screen still differs
Screens are grabbed with xwd (no PIL or ImageMagick needed); PNGs are written only when they differ.
"""
import argparse, json, os, re, socket, struct, subprocess, sys, time, zlib

WAIT = 1.5
BIG = 0.02          # share of the screen that counts as a large lasting change
PIXTOL = 24         # per-channel difference below this is not a change (dithering, fades)
QUIET = 15          # no C>S packet for this long (seconds) = the client hung: restart it
RELEASE = ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down',
           'space', 'Return', 'Tab'] + ['KP_%d' % d for d in range(10)] + ['KP_Up', 'KP_Down', 'KP_Left', 'KP_Right',
           'KP_Home', 'KP_End', 'KP_Prior', 'KP_Next', 'KP_Insert', 'KP_Delete', 'KP_Begin', 'KP_Enter', 'KP_Add',
           'KP_Subtract', 'KP_Multiply', 'KP_Divide', 'KP_Decimal']

C2S = {0: 'LEVELWARP', 1: 'BOARDMODIFY', 2: 'PLAYERPROPS', 3: 'NPCPROPS', 4: 'BOMBADD', 5: 'BOMBDEL',
       6: 'TOALL', 7: 'HORSEADD', 8: 'HORSEDEL', 9: 'ARROWADD', 10: 'FIRESPY', 11: 'THROWCARRIED',
       12: 'ITEMADD', 13: 'ITEMDEL', 14: 'CLAIMPKER', 15: 'BADDYPROPS', 16: 'BADDYHURT', 17: 'BADDYADD',
       18: 'FLAGSET', 19: 'FLAGDEL', 20: 'OPENCHEST', 21: 'PUTNPC', 22: 'NPCDEL', 23: 'WANTFILE',
       24: 'SHOWIMG', 26: 'HURTPLAYER', 27: 'EXPLOSION', 28: 'PRIVATEMESSAGE', 29: 'NPCWEAPONDEL',
       30: 'LEVELWARPMOD', 31: 'PACKETCOUNT', 32: 'ITEMTAKE', 33: 'WEAPONADD', 34: 'UPDATEFILE',
       35: 'ADJACENTLEVEL', 36: 'HITOBJECTS', 37: 'LANGUAGE', 38: 'TRIGGERACTION', 39: 'MAPINFO',
       40: 'SHOOT', 41: 'SERVERWARP', 48: 'SHOOT2', 50: 'RAWDATA', 157: 'UPDATEGANI', 158: 'UPDATESCRIPT',
       159: 'UPDATEPACKAGEREQUESTFILE'}

# player props: (name, kind); kind: n = n-byte number, s = 1-byte length + string, special handled below
PROPS = {0: ('nick', 's'), 1: ('maxhp', 1), 2: ('hp', 1), 3: ('rupees', 3), 4: ('arrows', 1),
         5: ('bombs', 1), 6: ('glove', 1), 7: ('bombpow', 1), 8: ('sword', 'sword'), 9: ('shield', 'shield'),
         10: ('gani', 's'), 11: ('head', 'head'), 12: ('chat', 's'), 13: ('colors', 5), 14: ('id', 2),
         15: ('x', 1), 16: ('y', 1), 17: ('sprite', 1), 18: ('status', 1), 19: ('carry', 1),
         20: ('level', 's'), 21: ('horse', 's'), 22: ('horsebush', 1), 23: ('effcol', 'eff'),
         24: ('carrynpc', 3), 25: ('ap', 2), 26: ('mp', 1), 27: ('kills', 3), 28: ('deaths', 3),
         29: ('online', 3), 30: ('ip', 5), 31: ('udp', 3), 32: ('align', 1), 33: ('flags', 1),
         34: ('account', 's'), 35: ('body', 's'), 36: ('rating', 3), 37: ('ga1', 's'), 38: ('ga2', 's'),
         39: ('ga3', 's'), 40: ('ga4', 's'), 41: ('ga5', 's'), 42: ('attach', 4), 43: ('gmapx', 1),
         44: ('gmapy', 1), 45: ('z', 1), 46: ('ga6', 's'), 47: ('ga7', 's'), 48: ('ga8', 's'),
         49: ('ga9', 's'), 50: ('ga10', 's'), 78: ('x2', 2), 79: ('y2', 2), 80: ('z2', 2)}
PROPS.update({i: ('ga%d' % (i - 44), 's') for i in range(55, 75)})


def gnum(b):
    v = 0
    for c in b:
        v = (v << 7) | ((c - 32) & 0x7f)
    return v


def decode_props(b):
    """best effort walk of a PLI_PLAYERPROPS body; stops at the first prop it does not know"""
    out, i = [], 0
    while i < len(b):
        pid = b[i] - 32; i += 1
        if pid not in PROPS:
            out.append('p%d?' % pid); break
        name, kind = PROPS[pid]
        try:
            if kind == 's':
                n = b[i] - 32; v = b[i + 1:i + 1 + n].decode('latin1'); i += 1 + n; v = repr(v)
            elif kind in ('sword', 'shield'):
                p = b[i] - 32; i += 1
                lim = 4 if kind == 'sword' else 3
                if p > lim:
                    n = b[i] - 32; v = '%d:%s' % (p, b[i + 1:i + 1 + n].decode('latin1')); i += 1 + n
                else:
                    v = str(p)
            elif kind == 'head':
                n = b[i] - 32; i += 1
                if n >= 100:
                    v = repr(b[i:i + n - 100].decode('latin1')); i += n - 100
                else:
                    v = str(n)
            elif kind == 'eff':
                n = b[i] - 32; i += 1
                if n:
                    i += 4
                v = str(n)
            else:
                raw = b[i:i + kind]; i += kind
                v = gnum(raw)
                if name in ('x2', 'y2', 'z2'):  # low bit = sign, value in pixels
                    v = ('-' if v & 1 else '') + '%g' % ((v >> 1) / 16)
                elif name in ('x', 'y'):
                    v = '%g' % (v / 2)
                v = str(v)
        except (IndexError, UnicodeDecodeError):
            out.append(name + '=<cut>'); break
        out.append('%s=%s' % (name, v))
    return ' '.join(out)


LINE = re.compile(r'^\s*([\d.]+) (\S+) (?:c\d+ )?(C>S|S>C|MARK) ?(.*)$')


def quiet_for(log, mark):
    """seconds between the last C>S packet and the given mark (a hung client sends nothing at all;
    a live one has a periodic packet every few seconds)"""
    last_cs, tmark = None, None
    try:
        for ln in open(log, encoding='latin1'):
            m = LINE.match(ln)
            if not m:
                continue
            if m.group(3) == 'C>S':
                last_cs = float(m.group(1))
            elif m.group(3) == 'MARK' and m.group(4).strip() == mark:
                tmark = float(m.group(1))
    except OSError:
        return 0
    if tmark is None or last_cs is None:
        return 0
    return tmark - last_cs


def packets(log, k0, k1):
    """C>S packets of the world connection between the two marks; plus S>C ids (counts)"""
    cs, sc, inside = [], {}, False
    try:
        lines = open(log, encoding='latin1').read().splitlines()
    except OSError:
        return [], {}
    for ln in lines:
        m = LINE.match(ln)
        if not m:
            continue
        what, rest = m.group(3), m.group(4)
        if what == 'MARK':
            if rest.strip() == k0:
                inside, cs, sc = True, [], {}
            elif rest.strip() == k1 and inside:
                break
            continue
        if not inside:
            continue
        mm = re.match(r'id=(\d+) len=(\d+) \| (.*) \| hex=([0-9a-f]*)', rest)
        if not mm:
            continue
        pid = int(mm.group(1))
        if what == 'S>C':
            sc[pid] = sc.get(pid, 0) + 1
            continue
        body = bytes.fromhex(mm.group(4))
        d = C2S.get(pid, '?')
        if pid == 2:
            d += '{' + decode_props(body) + '}'
        elif pid == 6:
            d += '{' + repr(body.decode('latin1')) + '}'
        else:
            d += '{' + mm.group(3)[:40] + '}'
        cs.append('%d:%s' % (pid, d))
    return cs, sc


class Screen:
    def __init__(self, disp):
        self.env = dict(os.environ, DISPLAY=':%s' % disp)

    def run(self, *a, timeout=8):
        try:
            return subprocess.run(a, env=self.env, capture_output=True, timeout=timeout).stdout.decode('latin1')
        except subprocess.TimeoutExpired:
            return ''

    def windows(self):
        out = []
        for w in self.run('xdotool', 'search', '--onlyvisible', '--name', '.').split():
            g = self.run('xdotool', 'getwindowgeometry', '--shell', w)
            d = dict(l.split('=', 1) for l in g.split() if '=' in l)
            if not d:
                continue
            name = self.run('xdotool', 'getwindowname', w).strip()
            out.append((int(w), name, int(d['X']), int(d['Y']), int(d['WIDTH']), int(d['HEIGHT'])))
        return out

    def grab(self):
        try:
            r = subprocess.run(['xwd', '-root', '-silent'], env=self.env, capture_output=True, timeout=20)
        except subprocess.TimeoutExpired:
            self.err = 'xwd timeout'; return None
        d = r.stdout
        if len(d) < 100:
            self.err = 'xwd: %r' % r.stderr[:200]; return None
        h = struct.unpack('>25I', d[:100])
        hsize, w, ht, bpp, bpl, nc = h[0], h[4], h[5], h[11], h[12], h[19]
        off = hsize + nc * 12
        if bpp == 24:  # Xvfb hands out packed 24-bit dumps while a GL client runs: widen to 32 bits
            px = bytearray(w * 4 * ht)
            for y in range(ht):
                r = d[off + y * bpl:off + y * bpl + w * 3]; o = y * w * 4
                px[o:o + w * 4:4] = r[0::3]; px[o + 1:o + w * 4:4] = r[1::3]; px[o + 2:o + w * 4:4] = r[2::3]
            return (w, ht, w * 4, bytes(px))
        if bpp != 32:
            self.err = 'bpp %d len %d' % (bpp, len(d)); return None
        return (w, ht, bpl, d[off:off + bpl * ht])

    @staticmethod
    def diff(a, b, tol=PIXTOL):
        """changed pixel count and bounding box (x0,y0,x1,y1) between two grabs"""
        if not a or not b or a[:3] != b[:3]:
            return -1, None
        w, ht, bpl, pa = a; pb = b[3]
        n, x0, y0, x1, y1 = 0, w, ht, -1, -1
        for y in range(ht):
            ra = pa[y * bpl:y * bpl + w * 4]; rb = pb[y * bpl:y * bpl + w * 4]
            if ra == rb:
                continue
            ia = memoryview(ra).cast('I'); ib = memoryview(rb).cast('I')
            for x, (u, v) in enumerate(zip(ia, ib)):
                if (u ^ v) & 0xffffff == 0:
                    continue
                if max(abs((u & 255) - (v & 255)), abs(((u >> 8) & 255) - ((v >> 8) & 255)),
                       abs(((u >> 16) & 255) - ((v >> 16) & 255))) < tol:
                    continue
                n += 1
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
        return n, ((x0, y0, x1, y1) if n else None)

    @staticmethod
    def png(g, path):
        w, ht, bpl, px = g
        rows = []
        for y in range(ht):
            r = px[y * bpl:y * bpl + w * 4]; o = bytearray(w * 3)
            o[0::3] = r[2::4]; o[1::3] = r[1::4]; o[2::3] = r[0::4]
            rows.append(b'\0' + bytes(o))
        def chunk(t, b): return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)
        open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, ht, 8, 2, 0, 0, 0))
                               + chunk(b'IDAT', zlib.compress(b''.join(rows), 6)) + chunk(b'IEND', b''))


class Ctl:
    def __init__(self, path):
        self.path = path

    def __call__(self, line):
        try:
            s = socket.socket(socket.AF_UNIX); s.settimeout(5); s.connect(self.path)
            f = s.makefile('rwb'); f.write((line + '\n').encode('latin1')); f.flush()
            r = f.readline().decode('latin1').strip(); s.close(); return r
        except OSError as e:
            return 'err ' + str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--disp', required=True); ap.add_argument('--sock', required=True)
    ap.add_argument('--proxylog', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--keys', required=True); ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--targets', default=''); ap.add_argument('--label', default='')
    ap.add_argument('--settle', type=float, default=0)
    ap.add_argument('--bytecode', default='', help='hex file of GS2 bytecode for the keylog.png stub NPC')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); shots = os.path.join(a.out, 'shots'); os.makedirs(shots, exist_ok=True)
    keys = []
    for ln in open(a.keys):
        if ln.strip() and not ln.startswith('#'):
            p = ln.rstrip('\n').split('\t')
            keys.append((p[0], p[1], p[2] if len(p) > 2 else ''))
    tg = {}
    for t in a.targets.split():
        k, v = t.split('='); x, y = v.split(','); tg[k] = (int(x), int(y))
    sc = Screen(a.disp); ctl = Ctl(a.sock)
    rows = open(os.path.join(a.out, 'rows.tsv'), 'a')
    log = open(os.path.join(a.out, 'sweep.log'), 'a')

    def say(*m):
        log.write('%s %s\n' % (time.strftime('%H:%M:%S'), ' '.join(str(x) for x in m))); log.flush()

    if a.settle:
        time.sleep(a.settle)
    wins0 = sc.windows()
    if not wins0:
        say('no window at start'); open(os.path.join(a.out, 'next.txt'), 'w').write('%d\n' % a.start); return 3
    game = max(wins0, key=lambda w: w[4] * w[5])
    st0 = ctl('status'); m = re.search(r'session=(\d+)', st0); sess = m.group(1) if m else None
    say('start', a.label, 'index', a.start, 'game', game, 'status', st0)
    if a.bytecode:
        # replace the script of the stub NPC (image keylog.png) with our GS2 bytecode: PLO_RAWDATA + PLO_NPCBYTECODE
        code = ''.join(l.strip() for l in open(a.bytecode) if not l.startswith('#'))
        npc = None
        for ln in open(a.proxylog, encoding='latin1'):
            m = re.search(r'S>C id=3 len=\d+ \| .*keylog\.png.* \| hex=([0-9a-f]{6})', ln)
            if m:
                b = bytes.fromhex(m.group(1)); npc = ((b[0] - 32) << 14) | ((b[1] - 32) << 7) | (b[2] - 32)
        if npc is None:
            say('bytecode: no keylog.png NPC seen in the proxy log')
        else:
            n = 1 + 3 + len(code) // 2 + 1
            r = ctl('s2c 100 i3:%d | 131 i3:%d hex:%s' % (n, npc, code))
            time.sleep(3)
            say('bytecode for NPC %d: %s' % (npc, r))
    base = sc.grab()
    if not base:
        say('no grab', getattr(sc, 'err', ''))
    if base:
        Screen.png(base, os.path.join(shots, 'start-%03d.png' % a.start))
        time.sleep(WAIT); n2 = sc.grab(); nz = Screen.diff(base, n2)
        say('idle noise over %.1fs: %s' % (WAIT, nz))

    def gamewin():
        ws = sc.windows()
        g = [w for w in ws if w[0] == game[0]]
        return ws, (g[0] if g else None)

    def focus():
        sc.run('xdotool', 'windowfocus', str(game[0]))

    def do(action):
        p = action.split()
        if not p:
            return
        _, gw = gamewin(); gx, gy = (gw[2], gw[3]) if gw else (game[2], game[3])
        if p[0] == 'key':
            focus(); sc.run('xdotool', 'key', '--delay', '60', *p[1:])
        elif p[0] == 'hold':
            focus(); sc.run('xdotool', 'keydown', p[1]); time.sleep(float(p[2])); sc.run('xdotool', 'keyup', p[1])
        elif p[0] in ('click', 'dclick', 'wheel'):
            t = p[2]
            if t not in tg:
                say('no target', t); return
            x, y = tg[t]
            sc.run('xdotool', 'mousemove', str(gx + x), str(gy + y)); time.sleep(0.2)
            if p[0] == 'click':
                sc.run('xdotool', 'click', p[1])
            elif p[0] == 'dclick':
                sc.run('xdotool', 'click', '--repeat', '2', '--delay', '120', p[1])
            else:
                sc.run('xdotool', 'click', '4' if p[1] == 'up' else '5')
            time.sleep(0.2); sc.run('xdotool', 'mousemove', str(gx + 2), str(gy + 2))

    def connected():
        r = ctl('status'); m = re.search(r'session=(\d+)', r)
        return bool(m and m.group(1) == sess), r

    W, H = (base[0], base[1]) if base else (1024, 768)
    for i in range(a.start, len(keys)):
        name, action, reset = keys[i]
        ws0, gw = gamewin()
        if not gw:
            say('game window gone before', name); open(os.path.join(a.out, 'next.txt'), 'w').write('%d\n' % i); return 3
        pre = sc.grab()
        if not pre:
            say('no grab', getattr(sc, 'err', ''))
        k0, k1 = 'KEY %d %s' % (i, name), 'END %d %s' % (i, name)
        ctl('mark ' + k0)
        do(action)
        time.sleep(WAIT)
        ctl('mark ' + k1)
        ws1, gw1 = gamewin(); post = sc.grab()
        n, bb = Screen.diff(pre, post)
        new = [w for w in ws1 if w[0] not in {x[0] for x in ws0}]
        gone = [w for w in ws0 if w[0] not in {x[0] for x in ws1}]
        alive = gw1 is not None
        conn, st = connected()
        cs, s2c = packets(a.proxylog, k0, k1)
        tag = '%03d' % i
        if n and post:
            Screen.png(post, os.path.join(shots, '%s-after.png' % tag))
        # reset
        rnote = []
        for w in new:
            sc.run('xdotool', 'windowfocus', str(w[0])); sc.run('xdotool', 'key', 'Escape'); time.sleep(0.8)
        ws2, _ = gamewin()
        left = [w for w in new if w[0] in {x[0] for x in ws2}]
        for w in left:
            sc.run('xdotool', 'windowfocus', str(w[0])); sc.run('xdotool', 'key', 'n'); time.sleep(0.8)
        if new:
            ws2, _ = gamewin(); left = [w for w in new if w[0] in {x[0] for x in ws2}]
            for w in left:  # last resort: Alt+F4, only while that window (not the game) has the focus
                if w[0] == game[0]:
                    continue
                sc.run('xdotool', 'windowfocus', str(w[0])); time.sleep(0.3)
                if sc.run('xdotool', 'getwindowfocus').strip() == str(w[0]):
                    sc.run('xdotool', 'key', 'alt+F4'); time.sleep(0.8)
            ws2, _ = gamewin(); left = [w for w in new if w[0] in {x[0] for x in ws2}]
            rnote.append('closed %d/%d new windows' % (len(new) - len(left), len(new)))
        else:
            left = []
        if reset.startswith('undo '):
            do(reset[5:]); time.sleep(0.6); rnote.append('undo')
        elif reset == 'again':
            do(action); time.sleep(WAIT); rnote.append('again')
        elif reset != 'none' and alive and not new and n > BIG * W * H:  # an in-game GUI, not a new window
            g2 = sc.grab(); n2, _ = Screen.diff(pre, g2)
            if n2 > BIG * W * H:
                do(action); time.sleep(WAIT); rnote.append('again(auto)')
                g3 = sc.grab(); n3, _ = Screen.diff(pre, g3)
                if n3 > BIG * W * H and not action.startswith('hold') and 'Escape' not in action:
                    do('key Escape'); time.sleep(1); rnote.append('escape')  # an in-game GUI that took the keys
        # release everything a combination or a lock-key change may have left down (stuck arrows/keypad)
        sc.run('xdotool', 'keyup', *RELEASE); time.sleep(0.2)
        ws3, gw3 = gamewin(); fin = sc.grab(); nf, bbf = Screen.diff(pre, fin)
        if nf and fin and nf > BIG * W * H:
            Screen.png(fin, os.path.join(shots, '%s-reset.png' % tag))
        conn2, st2 = connected()
        alive2 = gw3 is not None
        row = {'i': i, 'key': name, 'action': action, 'game_xy': [gw[2], gw[3]], 'diff_px': n, 'diff_box': bb,
               'new_windows': ['%s %dx%d@%d,%d' % (w[1], w[4], w[5], w[2], w[3]) for w in new],
               'gone_windows': [w[1] for w in gone], 'alive': alive, 'connected': conn,
               'c2s': cs, 's2c_ids': s2c, 'reset': rnote, 'after_reset_px': nf, 'after_reset_box': bbf,
               'alive_after': alive2, 'connected_after': conn2, 'windows_left': [w[1] for w in left]}
        quiet = quiet_for(a.proxylog, k1); hung = quiet > QUIET
        row['quiet_s'] = round(quiet, 1); row['hung'] = hung
        rows.write(json.dumps(row) + '\n'); rows.flush()
        say(i, name, 'diff', n, bb, 'new', len(new), 'c2s', len(cs), 'alive', alive2, 'conn', conn2, 'quiet', round(quiet, 1))
        if hung:
            say('no C>S packet for %.0f s: client hung' % quiet)
        if hung:  # the last few keys may have gone to a hung client: press them again after the restart
            say('restart needed after', name, st2)
            open(os.path.join(a.out, 'next.txt'), 'w').write('%d' % max(a.start + 1, i - 3) + chr(10)); return 3
        if not alive2 or not conn2 or left or hung:
            say('restart needed after', name, st2)
            open(os.path.join(a.out, 'next.txt'), 'w').write('%d\n' % (i + 1)); return 3
    open(os.path.join(a.out, 'next.txt'), 'w').write('%d\n' % len(keys))
    say('done'); return 0


if __name__ == '__main__':
    sys.exit(main())
