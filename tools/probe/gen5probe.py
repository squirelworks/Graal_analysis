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
  hex:HEX raw bytes
Quote text with spaces: t:"two words". The trailing newline is added.

Usage: gen5probe.py LISTEN_HOST PORT UP_HOST UP_PORT LOGFILE LABEL CTLSOCK
"""
import bz2, os, select, shlex, socket, sys, threading, time, zlib

INIT_STATE = 0x04a80b38


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
            out.append(len(v.encode('latin1')) + 32); out += v.encode('latin1')
        elif kind == 'hex':
            out += bytes.fromhex(v)
        else:
            raise ValueError('unknown field %r' % t)
    return bytes(out) + b'\n'


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


class Probe:
    def __init__(self, rec):
        self.rec = rec; self.sessions = []; self.lock = threading.Lock()

    def current(self):
        with self.lock:
            live = [s for s in self.sessions if s.alive and s.key is not None]
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
        if cmd in ('s2c', 'c2s'):
            pkt = encode(rest)
            dd = s.sc if cmd == 's2c' else s.cs
            with s.lock:
                dd.queue.append(pkt)
            self.rec('QUEUE', cmd, 'id=%d' % (pkt[0] - 32), 'len=%d' % (len(pkt) - 1), '|', show(pkt[1:-1]), '| hex=' + pkt[1:-1][:64].hex())
            return 'ok queued %d bytes' % len(pkt)
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
    rec(d.name, 'id=%d' % pid, 'len=%d' % len(p), '|', show(body), '| hex=' + body[:48].hex())


def frame(d, key, payload):
    comp = payload if d.typ == 2 else zlib.compress(payload, 9) if d.typ == 4 else bz2.compress(payload)
    enc, d.ostate = crypt(comp, key, d.ostate, d.typ)
    return (len(enc) + 1).to_bytes(2, 'big') + bytes([d.typ]) + enc


def flush(s, d):
    """Send queued injected packets for direction d as their own frame, if the stream is at a packet boundary.
    Only the session's own thread calls this, so the outgoing cipher state has one writer."""
    with s.lock:
        if not d.queue or not d.clean() or s.key is None:
            return
        pkts, d.queue = d.queue, []
        data = frame(d, s.key, b''.join(pkts))
        sock = s.c if d.name == 'S>C' else s.u
        try:
            sock.sendall(data)
        except OSError as e:
            s.rec('INJECT-ERROR', d.name, repr(e)); return
    for p in pkts:
        s.rec('INJECT', d.name, 'id=%d' % (p[0] - 32), 'len=%d' % (len(p) - 1), '|', show(p[1:-1]), '| hex=' + p[1:-1][:64].hex())


def pump(s, d, data):
    """Decrypt frames from one side, log, re-encrypt with our state, and return bytes for the other side."""
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
    u = socket.create_connection((uh, up)); s = Session(n, c, u, rec)
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
                        if len(pre) >= 2 and len(pre) >= int.from_bytes(pre[:2], 'big') + 2:
                            ln = int.from_bytes(pre[:2], 'big'); first, rest = pre[:ln + 2], pre[ln + 2:]
                            lg = zlib.decompress(first[2:])
                            s.key = lg[1] - 32; al = lg[10] - 32
                            rec('C>S LOGIN type=%d key=%d ver=%s account=%s password=<pw>' % (
                                lg[0] - 32, s.key, lg[2:10].decode('latin1'), lg[11:11 + al].decode('latin1')))
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
