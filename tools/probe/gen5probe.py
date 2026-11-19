#!/usr/bin/env python3
"""gen5probe: lab-only gen-5 proxy that injects chosen packets into a live session.

Sits between a real client and our own lab gserver (never a public server). Both
directions are decrypted, logged, and re-encrypted with the proxy's own cipher state,
so the proxy can add packets in either direction at a frame boundary:

  s2c SPEC   add a server->client packet (PLO) for the real client
  c2s SPEC   add a client->server packet (PLI) for our gserver

Control is a unix socket (it crosses the lab's private network namespace):
one command per line, one reply line per command. See probectl.py and README.md.

SPEC is a packet id followed by typed fields, for example `9 c:83 i5:1234`
(PLO_PLAYERPROPS, prop 83, a 5-byte number). Field types:
  c:N  GCHAR (N+32)        s:N  GSHORT (2 x 7 bits)   i3/i4/i5:N  3/4/5 x 7 bits
  b:N  one raw byte        t:TEXT raw text            str:TEXT GCHAR length + text
  hex:HEX raw bytes          rep:N:TEXT TEXT repeated N times
Quote text with spaces: t:"two words". The trailing newline is added.
A spec starting with `raw` (`raw hex:0a`) is sent as exactly its fields: no id byte, no newline.

Usage: gen5probe.py LISTEN_HOST PORT UP_HOST UP_PORT LOGFILE LABEL CTLSOCK   (CTLSOCK = a unix socket path, or tcp:PORT)
"""
import bz2, os, select, shlex, socket, sys, threading, time, zlib

INIT_STATE = 0x04a80b38
FULLHEX = {int(x) for x in os.environ.get('PROBE_FULLHEX', '').split(',') if x.strip()}


def crypt(data, key, state, typ):
    """gen-5 stream cipher: XOR the first 12 (none) or 4 (zlib/bz2) words of a frame."""
    out = bytearray(data)
    groups = min((len(data) + 3) // 4, 12) if typ == 2 else min(len(data) // 4, 4)
    for g in range(groups):
        state = (state * 0x08088405 + key) & 0xffffffff
        m = state.to_bytes(4, 'little'); p = 4 * g
        for j in range(min(4, len(data) - p)):
            out[p + j] ^= m[j]
    return bytes(out), state


def gnum(n, width):
    """Graal 7-bit big-endian number of WIDTH bytes, each byte + 32."""
    return bytes((((n >> (7 * k)) & 0x7f) + 32) for k in range(width - 1, -1, -1))


def gint3(b):
    return ((b[0] - 32) << 14) | ((b[1] - 32) << 7) | (b[2] - 32)


def encode(spec):
    """'9 c:83 i5:1234' -> bytes of one packet including the trailing newline."""
    toks = shlex.split(spec)
    if not toks:
        raise ValueError('empty spec')
    raw = toks[0] == 'raw'  # 'raw FIELDS': exactly these bytes, no id byte and no newline (wire-level tests)
    out = bytearray() if raw else bytearray([(int(toks[0], 0) + 32) & 0xff])
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
            out.append(len(v.encode('latin1')) + 32); out += v.encode('latin1')
        elif kind == 'hex':
            out += bytes.fromhex(v)
        elif kind == 'rep':  # rep:COUNT:TEXT, TEXT repeated COUNT times (for size tests)
            n, _, txt = v.partition(':'); out += txt.encode('latin1') * int(n)
        else:
            raise ValueError('unknown field %r' % t)
    return bytes(out) if raw else bytes(out) + b'\n'


def show(b, n=160):
    s = ''.join(chr(c) if 32 <= c < 127 else '.' for c in b[:n])
    return s + ('...' if len(b) > n else '')


class Dir:
    """One direction of one connection: cipher states, packet splitter, counters."""
    def __init__(self, name):
        self.name = name; self.buf = b''; self.state = INIT_STATE; self.ostate = INIT_STATE
        self.raw = None; self.stream = b''; self.typ = 4
        self.seen = {}; self.queue = []; self.after = []; self.drop = set()

    def clean(self):
        return self.raw is None and not self.stream


class Session:
    def __init__(self, n, c, u, rec):
        self.n = n; self.c = c; self.u = u; self.rec = rec; self.key = None
        self.cs, self.sc = Dir('C>S'), Dir('S>C'); self.lock = threading.Lock(); self.alive = True
        self.gen = 5  # set from the login line: 2 or 3 (type 0), 4 (type 4), 5 (type 5 and 6); 1 for a relay join line


class Probe:
    def __init__(self, rec):
        self.rec = rec; self.sessions = []; self.lock = threading.Lock(); self.use = 0

    def current(self):
        with self.lock:
            live = [s for s in self.sessions if s.alive and s.key is not None]
        if self.use:  # `use N`: aim at connection N while it lives (a gen-1 client keeps two)
            pick = [s for s in live if s.n == self.use]
            return pick[0] if pick else None
        return live[-1] if live else None

    def command(self, line):
        parts = line.strip().split(None, 1)
        if not parts:
            return 'err empty'
        cmd, rest = parts[0], (parts[1] if len(parts) > 1 else '')
        if cmd == 'mark':
            self.rec('MARK', rest); return 'ok'
        if cmd == 'use':  # use N : send to connection N (0 = the newest live one)
            self.use = int(rest or 0); self.rec('USE', self.use); return 'ok'
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
        if cmd in ('s2c', 'c2s'):  # several specs joined by ' | ' are queued at once and so share one frame
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
    """Split one decompressed bundle into packets (tracking PLO_RAWDATA lengths); log each.
    Returns the bundle to forward: packets whose id is in d.drop are removed (whole lines only)."""
    d.stream += body; out = bytearray(); dropped = False
    while d.stream:
        if d.raw is not None:
            if len(d.stream) < d.raw:
                out += d.stream; d.stream = b''; break
            p, d.stream = d.stream[:d.raw], d.stream[d.raw:]; d.raw = None
            out += p; p = p[:-1] if p.endswith(b'\n') else p
            log_packet(d, p, rec); continue
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
        if d.name == 'S>C' and pid == 100 and len(p) >= 4:
            d.raw = gint3(p[1:4])
        log_packet(d, p, rec)
        for aid, pkt in list(d.after):
            if aid == pid:
                keep.append(pkt); d.after.remove((aid, pkt)); break
    # a stream left mid-packet is still forwarded byte for byte; dropping only applies to whole lines
    return bytes(out) if dropped else body


def log_packet(d, p, rec):
    pid = p[0] - 32; body = p[1:]
    d.seen[pid] = d.seen.get(pid, 0) + 1
    n = len(body) if pid in FULLHEX else 48  # PROBE_FULLHEX=8,9 logs those ids' whole bodies
    rec(d.name, 'id=%d' % pid, 'len=%d' % len(p), '|', show(body), '| hex=' + body[:n].hex())


def lcg(state, key):
    return (state * 0x08088405 + key) & 0xffffffff


def junk_out(d, key, body):
    """Gen 3, client to server: insert the iterator byte into every message, as the client does."""
    out = bytearray()
    for m in body.split(b'\n')[:-1]:
        d.ostate = lcg(d.ostate, key); it = d.ostate
        pos = (it & 0xffff) % (len(m) + 1)
        out += m[:pos] + bytes([((it >> 16) & 0x7f) + 0x20]) + m[pos:] + b'\n'
    return bytes(out)


def junk_in(d, key, body):
    """Gen 3, client to server: remove the iterator byte from every message, as the server does."""
    out = bytearray()
    for m in body.split(b'\n')[:-1]:
        d.state = lcg(d.state, key); it = d.state
        pos = (it & 0xffff) % len(m) if m else 0
        out += m[:pos] + m[pos + 1:] + b'\n'
    return bytes(out)


def frame(s, d, key, payload):
    if s.gen == 1:  # 1998 relay: the lines go out as they are
        return payload
    if s.gen == 5:
        typ = 4 if d.typ == 2 and len(payload) > 60000 else d.typ  # an uncompressed frame cannot exceed the u16 length
        comp = payload if typ == 2 else zlib.compress(payload, 9) if typ == 4 else bz2.compress(payload)
        enc, d.ostate = crypt(comp, key, d.ostate, typ)
        return (len(enc) + 1).to_bytes(2, 'big') + bytes([typ]) + enc
    if s.gen == 3 and d.name == 'C>S':
        payload = junk_out(d, key, payload)
    if s.gen == 4:  # bz2 body, then the partial XOR (unverified: no gen-4 client is held)
        enc, d.ostate = crypt(bz2.compress(payload), key, d.ostate, 6)
    else:
        enc = zlib.compress(payload, 9)
    return len(enc).to_bytes(2, 'big') + enc


def flush(s, d):
    """Send queued injected packets for direction d as their own frame, if the stream is at a packet boundary.
    Only the session's own thread calls this, so the outgoing cipher state has one writer."""
    with s.lock:
        if not d.queue or not d.clean() or s.key is None:
            return
        pkts, d.queue = d.queue, []
        data = frame(s, d, s.key, b''.join(pkts))
        sock = s.c if d.name == 'S>C' else s.u
        try:
            sock.sendall(data)
        except OSError as e:
            s.rec('INJECT-ERROR', d.name, repr(e)); return
    for p in pkts:
        s.rec('INJECT', d.name, 'id=%d' % (p[0] - 32), 'len=%d' % (len(p) - 1), '|', show(p[1:-1]), '| hex=' + p[1:-1][:64].hex())


def pump_old(s, d, data):
    """Gens 2, 3 and 4: u16 length + zlib body (bz2 + partial XOR in gen 4), no compression byte.
    Gen 3 client frames carry one iterator byte per message; it is removed for logging and
    re-inserted with the proxy's own iterator, so injected messages keep the server in step."""
    d.buf += data; out = b''
    while len(d.buf) >= 2:
        ln = int.from_bytes(d.buf[:2], 'big')
        if len(d.buf) < ln + 2:
            break
        fr, d.buf = d.buf[2:ln + 2], d.buf[ln + 2:]
        try:
            if s.gen == 4:
                dec, d.state = crypt(fr, s.key, d.state, 6); body = bz2.decompress(dec)
            else:
                body = zlib.decompress(fr)
        except Exception as e:
            s.rec(d.name, 'frame-decode-error gen', s.gen, e)
            out += ln.to_bytes(2, 'big') + fr; continue
        if s.gen == 3 and d.name == 'C>S':
            body = junk_in(d, s.key, body)
        extra = []
        nb = split_packets(d, body, s.rec, extra)
        if nb:
            out += frame(s, d, s.key, nb)
        if extra:
            with s.lock:
                d.queue.extend(extra)
    return out


def pump_lines(s, d, data):
    """Gen 1 (1st Graal to 1.1.9, the relay lobby): LF-terminated text lines, no length, no
    compression, no cipher. The first character is the command (`N`, `I`, `+`, `P`, `D` ...);
    `seen` counts lines by that character's code. A partial line is held until its LF arrives,
    so an injected line always lands between two whole lines."""
    d.buf += data; out = bytearray()
    while b'\n' in d.buf:
        ln, d.buf = d.buf.split(b'\n', 1)
        k = ln[0] if ln else 10
        if k in d.drop:
            s.rec(d.name, 'DROPPED line', chr(k)); continue
        out += ln + b'\n'
        d.seen[k] = d.seen.get(k, 0) + 1
        s.rec(d.name, 'line', 'len=%d' % len(ln), '|', show(ln), '| hex=' + ln[:48].hex())
        for aid, pkt in list(d.after):
            if aid == k:
                d.queue.append(pkt); d.after.remove((aid, pkt)); break
    return bytes(out)


def pump(s, d, data):
    """Decrypt frames from one side, log, re-encrypt with our state, and return bytes for the other side."""
    if s.gen == 1:
        return pump_lines(s, d, data)
    if s.gen != 5:
        return pump_old(s, d, data)
    d.buf += data; out = b''
    while len(d.buf) >= 2:
        ln = int.from_bytes(d.buf[:2], 'big')
        if len(d.buf) < ln + 2:
            break
        fr, d.buf = d.buf[2:ln + 2], d.buf[ln + 2:]
        typ = fr[0]; dec, d.state = crypt(fr[1:], s.key, d.state, typ)
        try:
            body = dec if typ == 2 else zlib.decompress(dec) if typ == 4 else bz2.decompress(dec) if typ == 6 else None
        except Exception as e:
            s.rec(d.name, 'frame-decode-error', typ, e); body = None
        if body is None:
            enc, d.ostate = crypt(dec, s.key, d.ostate, typ)
            out += (len(enc) + 1).to_bytes(2, 'big') + bytes([typ]) + enc; continue
        d.typ = typ; extra = []
        nb = split_packets(d, body, s.rec, extra)
        if nb != body:
            comp = nb if typ == 2 else zlib.compress(nb, 9) if typ == 4 else bz2.compress(nb)
        else:
            comp = dec
        if nb:
            enc, d.ostate = crypt(comp, s.key, d.ostate, typ)
            out += (len(enc) + 1).to_bytes(2, 'big') + bytes([typ]) + enc
        if extra:
            with s.lock:
                d.queue.extend(extra)
    return out


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
                    if s.key is None:  # the login frame goes through untouched
                        pre += data
                        if pre[:1] in (b'N', b'O', b'S', b'V'):  # gen 1: a lobby join line, not a u16 length
                            if b'\n' not in pre:
                                continue
                            s.gen, s.key = 1, 0
                            rec('C>S GEN1 relay session (plain lines), first line:', show(pre.split(b'\n')[0]))
                            o = pump(s, s.cs, pre)
                            with s.lock:
                                u.sendall(o)
                            continue
                        if len(pre) >= 2 and len(pre) >= int.from_bytes(pre[:2], 'big') + 2:
                            ln = int.from_bytes(pre[:2], 'big'); first, rest = pre[:ln + 2], pre[ln + 2:]
                            lg = zlib.decompress(first[2:]); typ = lg[0] - 32
                            line, _, more = lg.partition(b'\n')
                            if typ == 0 and lg[1:4] in (b'GNW', b'GNP', b'G3D', b'GSE'):
                                s.gen, s.key, off = 2, 0, 1  # a known token right after the type: no key, no cipher
                            elif typ in (1, 3) and (lg[1:6] in (b'GSERV', b'G2NRC') or lg[1:4] == b'NCL'):
                                # staff login (pre-2002 RC id 1, NewWorld RC id 1, NC id 3): a token right after
                                # the id, then plain u16be+zlib with no cipher, no type byte and no key byte for the
                                # whole session. gen 2 is the proxy's plain-zlib path, so it fits these unchanged.
                                s.gen, s.key, off = 2, 0, 1
                            else:
                                s.gen = 3 if typ == 0 else 4 if typ == 4 else 5
                                s.key, off = lg[1] - 32, 2
                            al = lg[off + 8] - 32
                            rec('C>S LOGIN type=%d gen=%d key=%d ver=%s account=%s password=<pw>' % (
                                typ, s.gen, s.key, lg[off:off + 8].decode('latin1'), lg[off + 9:off + 9 + al].decode('latin1')))
                            if s.gen == 3 and more:  # the rest of the first frame already carries iterator bytes
                                clean = junk_in(s.cs, s.key, more)
                                for m in clean.split(b'\n')[:-1]:
                                    s.cs.ostate = lcg(s.cs.ostate, s.key)  # the server steps for these too
                                split_packets(s.cs, clean, rec, [])
                            with s.lock:
                                u.sendall(first)
                            o = pump(s, s.cs, rest)
                            if o:
                                with s.lock:
                                    u.sendall(o)
                    else:
                        o = pump(s, s.cs, data)
                        if o:
                            with s.lock:
                                u.sendall(o)
                else:
                    if s.key is None:
                        with s.lock:
                            c.sendall(data)
                    else:
                        o = pump(s, s.sc, data)
                        if o:
                            with s.lock:
                                c.sendall(o)
            if s.key is not None:
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
    def serve(c):  # one thread per connection, so an observer can talk to the proxy while a plan runs
        f = c.makefile('rwb')
        for line in f:
            try:
                reply = probe.command(line.decode('latin1'))
            except Exception as e:
                reply = 'err %r' % e
            f.write((reply + '\n').encode()); f.flush()
        c.close()
    while True:
        c, _ = L.accept()
        threading.Thread(target=serve, args=(c,), daemon=True).start()


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
