#!/usr/bin/env python3
"""A tiny, faithful-enough gen-2 gserver for self-testing srvfuzz on cloud loopback.

It is NOT GServer13; it imitates just enough of the gen-2 contract to exercise the
fuzzer end to end without the real binary: u16be+zlib framing, a gen-2 login line
(type 0, GSERVnnn token, account, password), and a login reply that opens with id 9
(own props) then id 6 (level name), matching ../../protocol/gserv-1999.md. Unknown
client ids are ignored. Inflate is capped, so a decompression-ratio case cannot take
the mock down -- a real server is exactly what we are testing for that.

To let the self-test prove the canary actually detects a dead server, the mock exits
(simulating a crash) when it receives a WANTFILE (id 23) whose name contains the
sentinel 'CRASHME'. Nothing in the real case list contains that sentinel.

Loopback only. Usage: mockgen2.py [HOST] [PORT]   (prints 'listening PORT' on stdout)
"""
import os, socket, sys, threading, zlib

LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)
INFLATE_CAP = 64 << 20


def frame(body):
    z = zlib.compress(body, 9)
    return len(z).to_bytes(2, 'big') + z


def login_reply():
    # id 9 own-props (a couple of bytes), then id 6 level name.
    p9 = bytes([9 + 32]) + bytes([32 + 5, 32 + 3])
    p6 = bytes([6 + 32]) + b'level13.graal'
    return frame(p9 + b'\n' + p6 + b'\n')


def serve_one(c):
    buf = b''; logged_in = False
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
                    continue  # a real server may error or drop; the mock just ignores the frame
                for line in body.split(b'\n'):
                    if not line:
                        continue
                    pid = line[0] - 32
                    if not logged_in:
                        # expect a login: type 0, then an 8-byte GSERV token.
                        if pid == 0 and line[1:6] == b'GSERV':
                            logged_in = True
                            c.sendall(login_reply())
                        else:
                            return  # bad first packet -> drop the connection (like the real refusal path)
                        continue
                    if pid == 23 and b'CRASHME' in line:  # self-test crash sentinel
                        os._exit(1)
                    # everything else: ignored, no reply (matches "unknown id, no handler")
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
