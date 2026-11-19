#!/usr/bin/env python3
"""ncprobe: lab-only zlib-only proxy for the NPC-Control (NC) socket.

NC framing (protocol/npc-control.md): login is type 3 + an 8-byte token + a ``str``
account + a ``str`` password, with **no** key byte; after login every frame is
``u16be length + zlib body``, with **no** type byte and **no** cipher, both
directions, for the whole session. The token is build-dependent: the standalone
NPCControl tools (nc7132001 and the 2001 builds) send ``NCL15031`` [lab]; the NC
socket embedded in RC 2002/01/11 sends ``NCL11012``. This proxy passes the login
frame through untouched, so it does not care which. Message bodies are classic Graal text lines
(``GCHAR id`` + payload + ``\\n``), G-integers biased ``+0x20``; batches flush at
0x1000 bytes. Id 50 (PLI_RAWDATA, C>S) / id 100 (PLO_RAWDATA, S>C) announce a raw
block of ``GINT3`` length that must not be line-split.

Because there is no cipher and no compression-type byte, this is a much simpler
cousin of ``gen5probe.py``: every frame is an independent, complete zlib stream.

Sits between a real NC client (``nc7132001`` and the other standalone NPCControl
builds, or RC in NC mode) and our own lab npcserver, inside a private network namespace with loopback
only. It is never pointed at a public server, and nothing here helps reach one.

Control is a unix socket (``tcp:PORT`` on Windows, which has no AF_UNIX in Python):
one command per line, one reply line per command. See probectl.py and README.md.

  s2c SPEC   inject an NC-server->client packet (PLO ids 16/33/80/157-164/167/188)
  c2s SPEC   inject a client->NC packet (PLI ids 103-119/150/151)
  after s2c|c2s ID SPEC   add SPEC right after the next packet with that id
  drop s2c|c2s ID         withhold packets with that id (whole lines only)
  seen s2c|c2s ID         count of packets with that id so far
  mark TEXT / status

SPEC is a packet id followed by typed fields, for example ``158 i3:7 c:50 str:bob``
(NC_NPCADD, NPC id 7, prop 50 = name "bob"). Field types:
  c:N  GCHAR (N+32)        s:N  GSHORT (2 x 7 bits)   i3/i4/i5:N  3/4/5 x 7 bits
  b:N  one raw byte        t:TEXT raw text            str:TEXT GCHAR length + text
  hex:HEX raw bytes        rep:N:TEXT TEXT repeated N times
Quote text with spaces: t:"two words". The trailing newline is added.

Usage: ncprobe.py LISTEN_HOST PORT UP_HOST UP_PORT LOGFILE LABEL CTLSOCK
"""
import os, select, shlex, socket, sys, threading, time, zlib

FULLHEX = {int(x) for x in os.environ.get('PROBE_FULLHEX', '').split(',') if x.strip()}


def gnum(n, width):
    """Graal 7-bit big-endian number of WIDTH bytes, each byte + 32."""
    return bytes((((n >> (7 * k)) & 0x7f) + 32) for k in range(width - 1, -1, -1))


def gint3(b):
    return ((b[0] - 32) << 14) | ((b[1] - 32) << 7) | (b[2] - 32)


def encode(spec):
    """'158 i3:7 c:50 str:bob' -> bytes of one packet including the trailing newline."""
    toks = shlex.split(spec)
    if not toks:
        raise ValueError('empty spec')
    out = bytearray([int(toks[0], 0) + 32])
    for t in toks[1:]:
        kind, _, v = t.partition(':')
        if kind == 'c':
            out.append((int(v, 0) + 32) & 0xff)
        elif kind == 'b':
            out.append(int(v, 0) & 0xff)
        elif kind == 's':
            out += gnum(int(v, 0), 2)
        elif kind in ('i3', 'i4', 'i5'):
            out += gnum(int(v, 0), int(kind[1]))
        elif kind == 't':
            out += v.encode('latin1')
        elif kind == 'str':
            out.append((len(v.encode('latin1')) + 32) & 0xff); out += v.encode('latin1')
        elif kind == 'hex':
            out += bytes.fromhex(v)
        elif kind == 'rep':  # rep:COUNT:TEXT, TEXT repeated COUNT times (for size tests)
            n, _, txt = v.partition(':'); out += txt.encode('latin1') * int(n)
        else:
            raise ValueError('unknown field %r' % t)
    return bytes(out) + b'\n'


def show(b, n=160):
    s = ''.join(chr(c) if 32 <= c < 127 else '.' for c in b[:n])
    return s + ('...' if len(b) > n else '')


# Ids whose GINT3 length announces a following raw (non-line-split) block.
RAW_ID = {'C>S': 50, 'S>C': 100}


class Dir:
    """One direction of one connection: frame buffer, packet splitter, counters."""
    def __init__(self, name):
        self.name = name; self.buf = b''; self.stream = b''; self.raw = None
        self.seen = {}; self.queue = []; self.after = []; self.drop = set()

    def clean(self):
        return self.raw is None and not self.stream


class Session:
    def __init__(self, n, c, u, rec):
        self.n = n; self.c = c; self.u = u; self.rec = rec; self.ready = False
        self.cs, self.sc = Dir('C>S'), Dir('S>C'); self.lock = threading.Lock(); self.alive = True


class Probe:
    def __init__(self, rec):
        self.rec = rec; self.sessions = []; self.lock = threading.Lock()

    def current(self):
        with self.lock:
            live = [s for s in self.sessions if s.alive and s.ready]
        return live[-1] if live else None

    def command(self, line):
        parts = line.strip().split(None, 1)
        if not parts:
            return 'err empty'
        cmd, rest = parts[0], (parts[1] if len(parts) > 1 else '')
        if cmd == 'mark':
            self.rec('MARK', rest); return 'ok'
        if cmd == 'status':
            s = self.current()
            if not s:
                return 'ok no-session'
            return 'ok session=%d s2c=%s c2s=%s' % (s.n, sum(s.sc.seen.values()), sum(s.cs.seen.values()))
        s = self.current()
        if not s:
            return 'err no live session'
        if cmd == 'seen':  # seen s2c|c2s ID -> count of packets with that id so far
            d, pid = rest.split()
            dd = s.sc if d == 's2c' else s.cs
            return 'ok %d' % dd.seen.get(int(pid), 0)
        if cmd in ('s2c', 'c2s'):  # several specs joined by ' | ' share one frame
            pkts = [encode(x) for x in rest.split(' | ')]
            dd = s.sc if cmd == 's2c' else s.cs
            with s.lock:
                dd.queue.extend(pkts)
            for pkt in pkts:
                self.rec('QUEUE', cmd, 'id=%d' % (pkt[0] - 32), 'len=%d' % (len(pkt) - 1), '|', show(pkt[1:-1]), '| hex=' + pkt[1:-1][:64].hex())
            return 'ok queued %d bytes' % sum(len(p) for p in pkts)
        if cmd == 'after':  # after s2c|c2s ID SPEC : add SPEC right after the next packet with that id
            d, pid, spec = rest.split(None, 2)
            dd = s.sc if d == 's2c' else s.cs
            pkt = encode(spec)
            with s.lock:
                dd.after.append((int(pid), pkt))
            self.rec('ARM', d, 'after id=%s' % pid, '|', show(pkt[1:-1]))
            return 'ok armed'
        if cmd in ('drop', 'undrop'):  # drop s2c|c2s ID : withhold packets with that id
            d, pid = rest.split()
            dd = s.sc if d == 's2c' else s.cs
            (dd.drop.add if cmd == 'drop' else dd.drop.discard)(int(pid))
            self.rec(cmd.upper(), d, pid); return 'ok'
        return 'err unknown command'


def split_packets(d, body, rec, keep):
    """Split one decompressed bundle into packets (tracking RAWDATA lengths); log each.
    Returns the bundle to forward: packets whose id is in d.drop are removed (whole lines only)."""
    d.stream += body; out = bytearray(); dropped = False
    raw_id = RAW_ID[d.name]
    while d.stream:
        if d.raw is not None:
            if len(d.stream) < d.raw:
                out += d.stream; d.raw -= len(d.stream); d.stream = b''; break
            p, d.stream = d.stream[:d.raw], d.stream[d.raw:]; d.raw = None
            out += p; log_raw(d, p, rec); continue
        i = d.stream.find(b'\n')
        if i < 0:
            out += d.stream; d.stream = b''; break
        p, d.stream = d.stream[:i], d.stream[i + 1:]
        if not p:
            out += b'\n'; continue
        pid = p[0] - 32
        if pid in d.drop:
            rec(d.name, 'DROPPED id=%d len=%d' % (pid, len(p))); dropped = True; continue
        out += p + b'\n'
        if pid == raw_id and len(p) >= 4:
            d.raw = gint3(p[1:4])
        log_packet(d, p, rec)
        for aid, pkt in list(d.after):
            if aid == pid:
                keep.append(pkt); d.after.remove((aid, pkt)); break
    return bytes(out) if dropped else body


def log_packet(d, p, rec):
    pid = p[0] - 32; body = p[1:]
    d.seen[pid] = d.seen.get(pid, 0) + 1
    n = len(body) if pid in FULLHEX else 48
    rec(d.name, 'id=%d' % pid, 'len=%d' % len(p), '|', show(body), '| hex=' + body[:n].hex())


def log_raw(d, p, rec):
    rec(d.name, 'RAW', 'len=%d' % len(p), '|', show(p), '| hex=' + p[:48].hex())


def frame(payload):
    """One NC frame: u16be length + zlib body. Each frame is an independent zlib stream."""
    enc = zlib.compress(payload, 9)
    return len(enc).to_bytes(2, 'big') + enc


def flush(s, d):
    """Send queued injected packets for direction d as their own frame, at a packet boundary.
    Only the session's own thread calls this, so there is a single writer per socket."""
    with s.lock:
        if not d.queue or not d.clean() or not s.ready:
            return
        pkts, d.queue = d.queue, []
        data = frame(b''.join(pkts))
        sock = s.c if d.name == 'S>C' else s.u
        try:
            sock.sendall(data)
        except OSError as e:
            s.rec('INJECT-ERROR', d.name, repr(e)); return
    for p in pkts:
        s.rec('INJECT', d.name, 'id=%d' % (p[0] - 32), 'len=%d' % (len(p) - 1), '|', show(p[1:-1]), '| hex=' + p[1:-1][:64].hex())


def pump(s, d, data):
    """Decompress frames from one side, log, re-compress if changed, return bytes for the other side."""
    d.buf += data; out = b''
    while len(d.buf) >= 2:
        ln = int.from_bytes(d.buf[:2], 'big')
        if len(d.buf) < ln + 2:
            break
        fr, d.buf = d.buf[2:ln + 2], d.buf[ln + 2:]
        try:
            body = zlib.decompress(fr)
        except Exception as e:
            s.rec(d.name, 'frame-decode-error', repr(e))
            out += ln.to_bytes(2, 'big') + fr; continue
        extra = []
        nb = split_packets(d, body, s.rec, extra)
        if nb:
            out += frame(nb) if nb != body else (ln.to_bytes(2, 'big') + fr)
        if extra:
            with s.lock:
                d.queue.extend(extra)
    return out


def parse_login(fr, rec):
    """Log the NC login line from the first client frame. Pass-through only; never modified."""
    try:
        lg = zlib.decompress(fr[2:])
    except Exception as e:
        rec('C>S LOGIN frame-decode-error', repr(e)); return
    typ = lg[0] - 32
    token = lg[1:9]
    rest = lg[9:]
    acct = pw = b''
    if rest:
        al = rest[0] - 32
        acct = rest[1:1 + al]
        rest2 = rest[1 + al:]
        if rest2:
            pl = rest2[0] - 32
            pw = rest2[1:1 + pl]
    rec('C>S LOGIN type=%d token=%s account=%s password=<pw len=%d>' % (
        typ, show(token), show(acct), len(pw)))


def handle(probe, c, uh, up, rec, n):
    u = socket.create_connection((uh, up))
    crec = lambda *a, _r=rec: _r('c%d' % n, *a)  # every line of this connection carries its number
    s = Session(n, c, u, crec); rec = crec
    with probe.lock:
        probe.sessions.append(s)
    rec('conn', n, 'open')
    pre = b''
    try:
        while True:
            r, _, _ = select.select([c, u], [], [], 0.2)
            for sock in r:
                data = sock.recv(65536)
                if not data:
                    rec('conn', n, 'closed by', 'client' if sock is c else 'server'); return
                if sock is c:
                    if not s.ready:  # the login frame goes through untouched
                        pre += data
                        if len(pre) >= 2 and len(pre) >= int.from_bytes(pre[:2], 'big') + 2:
                            ln = int.from_bytes(pre[:2], 'big'); first, extra = pre[:ln + 2], pre[ln + 2:]
                            parse_login(first, rec)
                            with s.lock:
                                u.sendall(first)
                            s.ready = True
                            if extra:
                                o = pump(s, s.cs, extra)
                                if o:
                                    with s.lock:
                                        u.sendall(o)
                    else:
                        o = pump(s, s.cs, data)
                        if o:
                            with s.lock:
                                u.sendall(o)
                else:
                    if not s.ready:
                        with s.lock:
                            c.sendall(data)
                    else:
                        o = pump(s, s.sc, data)
                        if o:
                            with s.lock:
                                c.sendall(o)
            if s.ready:
                flush(s, s.sc); flush(s, s.cs)
    except Exception as e:
        rec('conn', n, 'error', repr(e))
    finally:
        s.alive = False; c.close(); u.close()


def control(probe, path, rec):
    if path.startswith('tcp:'):  # Windows has no AF_UNIX in Python: a loopback TCP port instead
        L = socket.socket(); L.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        L.bind(('%d.%d.%d.%d' % (127, 0, 0, 1), int(path[4:]))); L.listen(4)
    else:
        if os.path.exists(path):
            os.unlink(path)
        L = socket.socket(socket.AF_UNIX); L.bind(path); L.listen(4)
    while True:
        c, _ = L.accept(); f = c.makefile('rwb')
        for line in f:
            try:
                reply = probe.command(line.decode('latin1'))
            except Exception as e:
                reply = 'err %r' % e
            f.write((reply + '\n').encode()); f.flush()
        c.close()


def main():
    lh, lp, uh, up, logf, label, ctl = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
    log = open(logf, 'a', buffering=1); t0 = time.monotonic(); lk = threading.Lock()

    def rec(*a):
        with lk:
            log.write('%9.3f %s %s\n' % (time.monotonic() - t0, label, ' '.join(str(x) for x in a)))
    probe = Probe(rec)
    threading.Thread(target=control, args=(probe, ctl, rec), daemon=True).start()
    L = socket.socket(); L.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); L.bind((lh, lp)); L.listen(4)
    rec('listening', lh, lp, '->', uh, up, 'ctl', ctl)
    k = 0
    while True:
        c, _ = L.accept(); k += 1
        threading.Thread(target=handle, args=(probe, c, uh, up, rec, k), daemon=True).start()


if __name__ == '__main__':
    main()
