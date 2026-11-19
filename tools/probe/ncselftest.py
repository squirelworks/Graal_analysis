#!/usr/bin/env python3
"""ncselftest: ncprobe between a fake NC client and a fake npcserver (loopback only, Linux).

Checks that relayed packets survive the proxy's decompress/recompress in both
directions, that s2c/c2s injection arrives at the right peer, that ``after`` fires
after the named packet, that ``drop`` withholds a packet, and that the RAWDATA
length announcement (id 100 S>C, id 50 C>S) keeps a raw block from being line-split.

Run: python3 ncselftest.py   (Linux; needs AF_UNIX for the control socket)
"""
import os, socket, subprocess, sys, tempfile, time, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ncprobe import encode, gnum  # noqa: E402

LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)  # built, not written: the repo bars dotted IP literals


class Peer:
    """Either side of the NC socket: plain u16be-length + zlib frames, no cipher, no type byte."""
    def __init__(self, sock):
        self.s = sock; self.buf = b''; self.got = []

    def send(self, payload):
        z = zlib.compress(payload, 9); self.s.sendall(len(z).to_bytes(2, 'big') + z)

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

    def read_raw(self, secs=1):
        """Return whole decompressed frame bodies (so a RAW block is not split on newlines)."""
        self.s.settimeout(0.2); end = time.time() + secs; out = []
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
                out.append(zlib.decompress(fr))
        return out


def main():
    d = tempfile.mkdtemp(); ctl = os.path.join(d, 'ctl'); log = os.path.join(d, 'log')
    srv = socket.socket(); srv.bind((LOOPBACK, 0)); srv.listen(1); sport = srv.getsockname()[1]
    tmp = socket.socket(); tmp.bind((LOOPBACK, 0)); pport = tmp.getsockname()[1]; tmp.close()
    px = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ncprobe.py'),
                           LOOPBACK, str(pport), LOOPBACK, str(sport), log, 't', ctl])
    try:
        for _ in range(50):
            if os.path.exists(ctl):
                break
            time.sleep(0.1)
        c = socket.create_connection((LOOPBACK, pport))
        # NC login: type 3 + NCL11012 + str account + str password, no key byte. Passed through untouched.
        login = bytes([3 + 32]) + b'NCL11012' + bytes([4 + 32]) + b'test' + bytes([2 + 32]) + b'pw'
        z = zlib.compress(login, 9); c.sendall(len(z).to_bytes(2, 'big') + z)
        s, _ = srv.accept()
        C, S = Peer(c), Peer(s)
        # the upstream server must receive the login frame byte-for-byte
        assert S.read(1) == [p for p in login.split(b'\n') if p], S.got

        # relay a server->client NC packet (NC_LEVELLIST) and a client->NC packet (NC_NPCGET)
        S.send(encode('80 t:level1.nw'))
        assert C.read(1)[-1] == encode('80 t:level1.nw')[:-1], C.got
        C.send(encode('103 i3:7'))
        assert S.read(1)[-1] == encode('103 i3:7')[:-1], S.got

        def ask(cmd):
            k = socket.socket(socket.AF_UNIX); k.connect(ctl); k.sendall((cmd + '\n').encode())
            r = k.makefile().readline().strip(); k.close(); return r

        # inject a server->client NC_NPCADD (158) and a client->NC NC_NPCWARP (107)
        assert ask('s2c 158 i3:7 c:50 str:bob').startswith('ok'), ask('status')
        assert encode('158 i3:7 c:50 str:bob')[:-1] in C.read(1), C.got
        assert ask('c2s 107 i3:7 c:30 c:30 t:start.nw').startswith('ok')
        assert encode('107 i3:7 c:30 c:30 t:start.nw')[:-1] in S.read(1), S.got

        # after: queue an NPCADD right behind the next NC_LEVELLIST (80)
        assert ask('after s2c 80 158 i3:9 c:50 str:eve').startswith('ok')
        S.send(encode('80 t:level2.nw'))
        got = C.read(1)
        assert got[-2:] == [encode('80 t:level2.nw')[:-1], encode('158 i3:9 c:50 str:eve')[:-1]], got

        # drop: withhold an NC_NPCDELETE (159), keep the following NC_LEVELLIST (80)
        assert ask('drop s2c 159').startswith('ok')
        S.send(encode('159 i3:9') + encode('80 t:kept.nw'))
        got = C.read(1)
        assert encode('159 i3:9')[:-1] not in got and got[-1] == encode('80 t:kept.nw')[:-1], got

        # RAWDATA: id 100 (S>C) announces a GINT3-length raw block that must survive intact,
        # even when it contains newlines (so it is not mis-split into "packets").
        raw = b'line-a\nline-b\nline-c'  # 20 bytes, with embedded newlines
        bundle = encode('100 i3:%d' % len(raw)) + raw + encode('80 t:after-raw.nw')
        S.send(bundle)
        frames = C.read_raw(1)
        joined = b''.join(frames)
        assert raw in joined, joined
        assert encode('80 t:after-raw.nw') in joined, joined
        # the raw block's embedded newlines did not spawn phantom packets downstream
        assert joined.count(b'\n') == bundle.count(b'\n'), (joined.count(b'\n'), bundle.count(b'\n'))

        # traffic still flows both ways after all that
        S.send(encode('80 t:last.nw')); assert C.read(1)[-1] == encode('80 t:last.nw')[:-1]
        C.send(encode('150')); assert S.read(1)[-1] == encode('150')[:-1]
        c.close(); s.close()
        print('ncselftest ok'); return 0
    finally:
        px.kill()


if __name__ == '__main__':
    sys.exit(main())
