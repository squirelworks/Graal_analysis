#!/usr/bin/env python3
"""Reference server for the February 2000 Graal3D client (GR3DV002).

Written from graal3d/protocol.md and the 2026-10-30 lab captures of the
original GServer.exe. It is meant to show that the notes are complete enough
to host the real client; it is not a copy of the original server.

    python3 g3dserver.py [--port 14901] [--levels DIR] [--accounts FILE]

Accounts are a JSON file: {"name": {"password": "...", "level": 0..3,
"loadonly": false, "disabled": false}}. Without one, any name logs in with
any password as a load-only account. Levels are DirectX .x text files.
"""
import argparse, json, os, socket, selectors, struct, zlib

# ---------------------------------------------------------------- codec

def c(v): return bytes([v + 32])

def sN(v, n):
    out = bytearray()
    for _ in range(n):
        out.append((v & 0x7f) + 32); v >>= 7
    return bytes(reversed(out))

def rN(b, i, n):
    v = 0
    for k in range(n): v = (v << 7) | (b[i + k] - 32)
    return v

def st(s):
    if isinstance(s, str): s = s.encode('latin1')
    return c(len(s)) + s

# Prop value kinds, by prop id. Width in bytes, or 'str'.
#  0 id  1-3 xyz  4 angle  5 anim  6-9 look strings  10/11/17 colours
#  12 nick  13 chat  14 level  15 UDP port  16 IPv4  50 in-level  51 left
KIND = {0: 1, 1: 2, 2: 2, 3: 2, 4: 1, 5: 2, 6: 'str', 7: 'str', 8: 'str', 9: 'str',
        10: 'col', 11: 'col', 12: 'str', 13: 'str', 14: 'str', 15: 3, 16: 'ip', 17: 'col',
        50: 1, 51: 0}
UDP_PROPS = (1, 2, 3, 4, 5, 13)    # left out of TCP relay when both ends have UDP
FULL_PROPS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
OWN_PROPS = (0, 1, 2, 3, 4, 5)      # packet 3 on login
SAVED_PROPS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17)

def enc_value(pid, v):
    k = KIND[pid]
    if k == 'str': return st(v[:200] if pid in (12, 13) else v)
    if k == 'col': return bytes(((v >> s) & 63) + 32 for s in (18, 12, 6, 0))
    if k == 'ip':  # dotted quad as the little-endian in_addr word: 4 bits + 4 x 7 bits
        a = sum(int(p) << (8 * i) for i, p in enumerate(v.split('.')))
        return bytes([((a >> 28) & 15) + 32] + [((a >> s) & 127) + 32 for s in (21, 14, 7, 0)])
    if k == 0: return b''
    return sN(v, k) if k > 1 else c(v)

def parse_props(b):
    out, i = [], 0
    while i < len(b):
        pid = b[i] - 32; i += 1
        k = KIND.get(pid)
        if k is None: break                       # unknown prop: stop, as the originals do
        if k == 'str': n = b[i] - 32; out.append((pid, b[i+1:i+1+n].decode('latin1'))); i += 1 + n
        elif k == 'col':
            v = 0
            for j in range(4): v = (v << 6) | (b[i + j] - 32)
            out.append((pid, v)); i += 4
        elif k == 'ip':
            a = (b[i]-32) << 28 | rN(b, i + 1, 4); i += 5
            out.append((pid, '.'.join(str((a >> s) & 255) for s in (0, 8, 16, 24))))
        elif k == 0: out.append((pid, None))
        elif k == 1: out.append((pid, b[i] - 32)); i += 1
        else: out.append((pid, rN(b, i, k))); i += k
    return out

# ---------------------------------------------------------------- state

DEFAULTS = {1: 8000, 2: 8000, 3: 8000, 4: 135, 5: 0, 6: 'body.x', 7: 'head.x', 8: 'body.bmp',
            9: 'man.bmp', 10: 0xFF0000, 11: 0x800000, 12: '', 13: '', 14: 'startlevel.x',
            15: 0, 16: '0.0.0.0', 17: 0xFDCC47}

class Player:
    def __init__(self, srv, sock, addr):
        self.srv, self.sock, self.addr = srv, sock, addr
        self.rbuf, self.out = b'', []
        self.id = 0; self.admin = False; self.account = None
        self.props = dict(DEFAULTS); self.props[16] = addr[0]
        self.level_sent = set(); self.room = None

    def enc(self, ids):
        return b''.join(c(p) + enc_value(p, self.id if p == 0 else self.props[p]) for p in ids)

    def queue(self, pid, payload=b''):
        self.out.append(c(pid) + payload)

    def flush(self):
        if not self.out: return
        raw = b''.join(l + b'\n' for l in self.out); self.out = []
        z = zlib.compress(raw)
        try: self.sock.sendall(struct.pack('>H', len(z)) + z)
        except OSError: self.srv.drop(self)

class Server:
    def __init__(self, port, levels, accounts):
        self.levels, self.accounts_file = levels, accounts
        self.accounts = json.load(open(accounts)) if accounts and os.path.exists(accounts) else None
        self.players = {}           # id -> Player (logged-in players)
        self.admins, self.conns = [], []
        self.sel = selectors.DefaultSelector()
        self.ls = socket.socket(); self.ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ls.bind(('0.0.0.0', port)); self.ls.listen(16); self.ls.setblocking(False)
        self.sel.register(self.ls, selectors.EVENT_READ)
        print('Graal3D reference server on port', port)

    def level_text(self, name):
        path = os.path.join(self.levels, os.path.basename(name))
        if not os.path.exists(path): return None
        return open(path, 'rb').read().replace(b'\r', b'').replace(b'\n', b'\xa7')

    def same_level(self, p):
        # level membership, not prop 14: a client-sent prop 14 is relayed but does not move anyone
        return [q for q in self.players.values() if q is not p and q.room == p.room]

    # -- login
    def login(self, p, admin, b):
        ver = b[0:8]; i = 8
        acc = b[i+1:i+1+b[i]-32].decode('latin1'); i += 1 + b[i] - 32
        pw = b[i+1:i+1+b[i]-32].decode('latin1')
        if ver == b'GR3DV001':
            return self.reject(p, 'You need at least Graal3D beta2 to play on this server.')
        if ver != b'GR3DV002': return self.reject(p, 'Wrong client version.')
        rec = self.accounts.get(acc) if self.accounts is not None else {'password': pw, 'loadonly': True}
        if not rec or rec.get('password') != pw:
            return self.reject(p, "An account with the name and password you typed in doesn't exist.")
        if rec.get('disabled'): return self.reject(p, 'This account is disabled.')
        if not rec.get('loadonly') and any(q.account == acc for q in self.players.values()):
            return self.reject(p, 'The account is already in use.')
        p.account, p.level = acc, rec.get('level', 0)
        if admin:
            if p.level < 1: return self.reject(p, 'You have no admin rights.')
            p.admin = True; self.admins.append(p)
            for name, r in (self.accounts or {}).items():
                cat = (0 if r.get('loadonly') else 1) + 4 * r.get('level', 0)
                p.queue(50, sN(0, 4) + c(cat) + name.encode('latin1'))
            for q in self.players.values(): p.queue(55, c(q.id) + st(q.account) + q.enc([14]))
            return
        p.id = next(n for n in range(1, 201) if n not in self.players)
        saved = {int(k): v for k, v in rec.get('props', {}).items()}
        p.props.update(saved)
        if saved.get(12):                     # the original relays the saved nickname first
            for q in self.players.values(): q.queue(2, c(p.id) + p.enc([12]))
        p.queue(3, p.enc(OWN_PROPS))
        for q in self.players.values():       # everyone learns about everyone
            p.queue(2, c(q.id) + q.enc(FULL_PROPS))
            q.queue(2, c(p.id) + p.enc(FULL_PROPS))
        self.players[p.id] = p
        self.enter_level(p, p.props[14])
        for a in self.admins: a.queue(55, c(p.id) + st(p.account) + p.enc([14]))

    def reject(self, p, text):
        p.queue(5, text.encode('latin1')); p.flush(); self.drop(p)

    def enter_level(self, p, name):
        p.props[14] = p.room = name
        text = self.level_text(name)
        p.queue(1, name.encode('latin1'))
        if text is None: p.queue(7, name.encode('latin1')); return
        p.queue(0, b'' if name in p.level_sent else text); p.level_sent.add(name)
        others = self.same_level(p)
        for q in others:
            p.queue(2, c(q.id) + c(50) + c(1))
            q.queue(2, c(p.id) + c(50) + c(1))
        if not others: p.queue(4)

    # -- props from a client
    def on_props(self, p, b):
        changed = []
        for pid, v in parse_props(b):
            if pid in (0, 16, 50, 51): continue          # server-owned
            if pid == 12:
                nick, guild = v, None
                if '(' in v and v.endswith(')'):
                    nick, guild = v[:v.index('(')].rstrip(), v[v.index('(')+1:-1]
                    gf = os.path.join(self.levels, '..', 'guilds', 'guild%s.txt' % guild)
                    ok = os.path.exists(gf) and p.account in open(gf).read().split()
                    v = '%s (%s)' % (nick, guild) if ok else nick
                p.props[12] = v
                if guild is not None: p.queue(3, p.enc([12]))
                for q in self.players.values():
                    if q is not p: q.queue(2, c(p.id) + p.enc([12]))
            elif pid == 15:
                p.props[15] = v
                for q in self.players.values():
                    if q is not p: q.queue(2, c(p.id) + p.enc([15]))
            else:
                p.props[pid] = v
            if pid not in changed: changed.append(pid)
        if not changed: return
        full = p.enc(changed)
        tcp_only = p.enc([x for x in changed if x not in UDP_PROPS])
        for q in self.same_level(p):
            if p.props[15] > 0 and q.props[15] > 0:
                if tcp_only: q.queue(2, c(p.id) + tcp_only)
            else:
                q.queue(2, c(p.id) + full)

    # -- admin commands (subset)
    def on_admin(self, p, pid, b):
        if pid == 63:
            for q in self.players.values(): q.queue(8, b'Administrator %s:\xa7' % p.account.encode() + b)
        elif pid == 64 and (b[0] - 32) in self.players:
            self.players[b[0] - 32].queue(8, b'Administrator %s:\xa7' % p.account.encode() + b[1:])
        elif pid == 61 and (b[0] - 32) in self.players:
            self.reject(self.players[b[0] - 32], 'The server administrator has disconnected you.')

    def on_line(self, p, line):
        pid, b = line[0] - 32, line[1:]
        if p.account is None:
            if pid in (0, 1): self.login(p, pid == 1, b)
            return
        if p.admin: self.on_admin(p, pid, b)
        elif pid == 1: self.on_props(p, b)

    def drop(self, p):
        if p not in self.conns: return
        self.conns.remove(p)
        try: self.sel.unregister(p.sock)
        except (KeyError, ValueError): pass
        p.sock.close()
        if p in self.admins: self.admins.remove(p)
        if self.players.get(p.id) is p:
            del self.players[p.id]
            if self.accounts is not None and p.account in self.accounts and not self.accounts[p.account].get('loadonly'):
                self.accounts[p.account]['props'] = {k: p.props[k] for k in SAVED_PROPS}
                json.dump(self.accounts, open(self.accounts_file, 'w'), indent=1)
            for q in self.players.values():
                q.queue(2, c(p.id) + c(51))
            for a in self.admins: a.queue(56, c(p.id))

    def run(self):
        while True:
            for key, _ in self.sel.select(0.05):
                if key.fileobj is self.ls:
                    s, addr = self.ls.accept(); s.setblocking(True)
                    p = Player(self, s, addr); self.conns.append(p)
                    self.sel.register(s, selectors.EVENT_READ, p)
                    p.queue(6, c(0)); p.flush()
                    continue
                p = key.data
                try: d = p.sock.recv(65536)
                except OSError: d = b''
                if not d: self.drop(p); continue
                p.rbuf += d
                while len(p.rbuf) >= 2:
                    n = struct.unpack('>H', p.rbuf[:2])[0]
                    if len(p.rbuf) < 2 + n: break
                    raw = zlib.decompress(p.rbuf[2:2+n]); p.rbuf = p.rbuf[2+n:]
                    for line in raw.split(b'\n')[:-1]:
                        if not line: continue
                        try: self.on_line(p, line)
                        except (IndexError, ValueError) as e:
                            print('bad line from %s: %r (%s)' % (p.addr, line[:80], e)); self.drop(p); break
            for p in list(self.conns): p.flush()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=14901)
    ap.add_argument('--levels', default='levels')
    ap.add_argument('--accounts')
    a = ap.parse_args()
    Server(a.port, a.levels, a.accounts).run()
