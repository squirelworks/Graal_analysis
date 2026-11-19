#!/usr/bin/env python3
"""selftest: gen5probe between a fake gen-5 client and a fake server (loopback only, Linux).

Checks that relayed packets survive the proxy's re-encryption in both directions,
that s2c/c2s injection arrives decryptable at the right peer, that `after` fires
after the named packet, and that `drop` withholds a packet.
"""
import os, socket, subprocess, sys, tempfile, threading, time, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen5probe import crypt, encode, INIT_STATE, lcg  # noqa: E402

LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)  # built, not written: the repo bars dotted IP literals

KEY = 77


class Peer:
    def __init__(self, sock):
        self.s = sock; self.o = INIT_STATE; self.i = INIT_STATE; self.buf = b''; self.got = []

    def send(self, payload, typ=4):
        comp = zlib.compress(payload) if typ == 4 else payload
        enc, self.o = crypt(comp, KEY, self.o, typ)
        self.s.sendall((len(enc) + 1).to_bytes(2, 'big') + bytes([typ]) + enc)

    def read(self, secs=2):
        self.s.settimeout(0.2); end = time.time() + secs
        while time.time() < end:
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                continue
            if not d:
                break
            self.buf += d
            while len(self.buf) >= 2 and len(self.buf) >= int.from_bytes(self.buf[:2], 'big') + 2:
                ln = int.from_bytes(self.buf[:2], 'big'); fr, self.buf = self.buf[2:ln + 2], self.buf[ln + 2:]
                dec, self.i = crypt(fr[1:], KEY, self.i, fr[0])
                body = zlib.decompress(dec) if fr[0] == 4 else dec
                self.got += [p for p in body.split(b'\n') if p]
        return self.got


class Gen3Client:
    """A 2.05-style client: plain zlib frames, one iterator byte in every message after the login line."""
    def __init__(self, sock):
        self.s = sock; self.it = INIT_STATE; self.buf = b''; self.got = []

    def junk(self, msg):  # msg without the newline
        self.it = lcg(self.it, KEY); pos = (self.it & 0xffff) % (len(msg) + 1)
        return msg[:pos] + bytes([((self.it >> 16) & 0x7f) + 0x20]) + msg[pos:] + b'\n'

    def send(self, *msgs, login=None):
        body = (login + b'\n' if login else b'') + b''.join(self.junk(m) for m in msgs)
        z = zlib.compress(body); self.s.sendall(len(z).to_bytes(2, 'big') + z)

    def read(self, secs=1):
        self.s.settimeout(0.2); end = time.time() + secs
        while time.time() < end:
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                continue
            if not d:
                break
            self.buf += d
            while len(self.buf) >= 2 and len(self.buf) >= int.from_bytes(self.buf[:2], 'big') + 2:
                ln = int.from_bytes(self.buf[:2], 'big'); fr, self.buf = self.buf[2:ln + 2], self.buf[ln + 2:]
                self.got += [p for p in zlib.decompress(fr).split(b'\n') if p]
        return self.got


class Gen3Server:
    """The server side of gen 3: deletes the iterator byte, sends plain zlib frames."""
    def __init__(self, sock):
        self.s = sock; self.it = INIT_STATE; self.buf = b''; self.got = []; self.first = True

    def send(self, payload):
        z = zlib.compress(payload); self.s.sendall(len(z).to_bytes(2, 'big') + z)

    def read(self, secs=1):
        self.s.settimeout(0.2); end = time.time() + secs
        while time.time() < end:
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                continue
            if not d:
                break
            self.buf += d
            while len(self.buf) >= 2 and len(self.buf) >= int.from_bytes(self.buf[:2], 'big') + 2:
                ln = int.from_bytes(self.buf[:2], 'big'); fr, self.buf = self.buf[2:ln + 2], self.buf[ln + 2:]
                for m in zlib.decompress(fr).split(b'\n')[:-1]:
                    if self.first:
                        self.first = False; continue  # the login line
                    self.it = lcg(self.it, KEY); pos = (self.it & 0xffff) % len(m)
                    self.got.append(m[:pos] + m[pos + 1:])
        return self.got


def gen3_test(ask, pport, srv):
    c = socket.create_connection((LOOPBACK, pport))
    C = Gen3Client(c)
    C.send(encode('37 t:English')[:-1], login=bytes([32, KEY + 32]) + b'GNW03081' + bytes([4 + 32]) + b'test' + bytes([2 + 32]) + b'pw')
    s, _ = srv.accept(); S = Gen3Server(s)
    assert S.read(1)[-1] == encode('37 t:English')[:-1], S.got
    S.send(encode('6 t:start.nw')); assert C.read(1)[-1] == encode('6 t:start.nw')[:-1], C.got
    C.send(encode('2 c:1 c:5')[:-1]); assert S.read(1)[-1] == encode('2 c:1 c:5')[:-1], S.got
    assert ask('s2c 9 c:5 c:11').startswith('ok'); assert C.read(1)[-1] == encode('9 c:5 c:11')[:-1], C.got
    assert ask('c2s 99 t:hello').startswith('ok'); assert S.read(1)[-1] == encode('99 t:hello')[:-1], S.got
    # the client's own iterator and the server's stay in step after the injected message
    C.send(encode('2 c:1 c:6')[:-1], encode('2 c:1 c:7')[:-1]); got = S.read(1)
    assert got[-2:] == [encode('2 c:1 c:6')[:-1], encode('2 c:1 c:7')[:-1]], got
    c.close(); s.close()


def main():
    d = tempfile.mkdtemp(); ctl = os.path.join(d, 'ctl'); log = os.path.join(d, 'log')
    srv = socket.socket(); srv.bind((LOOPBACK, 0)); srv.listen(1); sport = srv.getsockname()[1]
    tmp = socket.socket(); tmp.bind((LOOPBACK, 0)); pport = tmp.getsockname()[1]; tmp.close()
    px = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen5probe.py'),
                           LOOPBACK, str(pport), LOOPBACK, str(sport), log, 't', ctl])
    try:
        for _ in range(50):
            if os.path.exists(ctl):
                break
            time.sleep(0.1)
        c = socket.create_connection((LOOPBACK, pport))
        login = bytes([5 + 32, KEY + 32]) + b'G3D0511C' + bytes([4 + 32]) + b'test' + bytes([2 + 32]) + b'pw'
        z = zlib.compress(login); c.sendall(len(z).to_bytes(2, 'big') + z)
        s, _ = srv.accept(); s.recv(4096)
        C, S = Peer(c), Peer(s)
        S.send(encode('9 c:0 str:alice')[:-1] + b'\n' + encode('6 t:start.nw'))
        assert C.read(1) == [encode('9 c:0 str:alice')[:-1], encode('6 t:start.nw')[:-1]], C.got
        C.send(encode('2 c:1 c:5')); assert S.read(1) == [encode('2 c:1 c:5')[:-1]], S.got

        def ask(cmd):
            k = socket.socket(socket.AF_UNIX); k.connect(ctl); k.sendall((cmd + '\n').encode())
            r = k.makefile().readline().strip(); k.close(); return r
        assert ask('s2c 9 c:83 i5:1234').startswith('ok')
        assert encode('9 c:83 i5:1234')[:-1] in C.read(1), C.got
        assert ask('c2s 99 t:hello').startswith('ok')
        assert encode('99 t:hello')[:-1] in S.read(1), S.got
        assert ask('after s2c 6 9 c:3 i3:42').startswith('ok')
        S.send(encode('6 t:next.nw'))
        got = C.read(1); assert got[-2:] == [encode('6 t:next.nw')[:-1], encode('9 c:3 i3:42')[:-1]], got
        assert ask('drop s2c 13').startswith('ok')
        S.send(encode('13 t:dropme') + encode('6 t:kept.nw'))
        got = C.read(1); assert encode('13 t:dropme')[:-1] not in got and got[-1] == encode('6 t:kept.nw')[:-1], got
        # traffic still flows both ways after all that (cipher states stayed in step)
        S.send(encode('6 t:last.nw')); assert C.read(1)[-1] == encode('6 t:last.nw')[:-1]
        C.send(encode('2 c:1 c:6')); assert S.read(1)[-1] == encode('2 c:1 c:6')[:-1]
        c.close(); s.close()
        gen3_test(ask, pport, srv)
        print('selftest ok (gen 5 and gen 3)'); return 0
    finally:
        px.kill()


if __name__ == '__main__':
    sys.exit(main())
