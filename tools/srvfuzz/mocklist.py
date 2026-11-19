#!/usr/bin/env python3
"""A tiny pre-2.2 listserver for self-testing srvfuzz on cloud loopback.

Imitates the client<->listserver pre-2.2 link (../../protocol/listserver.md): u16be+zlib
framing, id 0 V1VER + id 1 SERVERLIST login, and a reply of id 0 SVRLIST (one fake
server entry) then id 2 status. It is not a real listserver and holds no real hosts:
the single advertised entry uses the loopback address, built not written.

Exits (simulated crash) on a GRSECURELOGIN (id 223) whose body contains 'CRASHME'.
Loopback only. Usage: mocklist.py [HOST] [PORT]   (prints 'listening PORT').
"""
import os, socket, sys, threading, zlib

LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)
INFLATE_CAP = 64 << 20


def frame(body):
    z = zlib.compress(body, 9)
    return len(z).to_bytes(2, 'big') + z


def gstr(s):
    b = s.encode('latin1')
    return bytes([(len(b) + 32) & 0xff]) + b


def svrlist_reply():
    # id 0: count=1, then field count 8 and 8 GSTRING fields. Host is loopback (built).
    entry = bytes([32 + 8]) + b''.join(gstr(x) for x in (
        'Lab World', 'English', 'a lab server', 'http://localhost/', '2.37', '1', LOOPBACK, '14804'))
    p0 = bytes([0 + 32]) + bytes([32 + 1]) + entry
    p2 = bytes([2 + 32]) + b'welcome'
    return frame(p0 + b'\n' + p2 + b'\n')


def serve_one(c):
    buf = b''; replied = False
    c.settimeout(5.0)
    try:
        while True:
            try:
                d = c.recv(65536)
            except socket.timeout:
                return
            if not d:
                return
            buf += d
            while len(buf) >= 2:
                ln = int.from_bytes(buf[:2], 'big')
                if len(buf) < ln + 2:
                    break
                fr, buf = buf[2:ln + 2], buf[ln + 2:]
                try:
                    dco = zlib.decompressobj()
                    body = dco.decompress(fr, INFLATE_CAP)
                except Exception:
                    continue
                for line in body.split(b'\n'):
                    if not line:
                        continue
                    pid = line[0] - 32
                    if pid == 223 and b'CRASHME' in line:
                        os._exit(1)
                    if pid in (0, 1) and not replied:
                        # the real server answers the list once it has the login frame.
                        replied = True
                        c.sendall(svrlist_reply())
    finally:
        c.close()


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else LOOPBACK
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    L = socket.socket(); L.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    L.bind((host, port)); L.listen(16)
    print('listening %d' % L.getsockname()[1], flush=True)
    while True:
        c, _ = L.accept()
        threading.Thread(target=serve_one, args=(c,), daemon=True).start()


if __name__ == '__main__':
    main()
