#!/usr/bin/env python3
"""ncstub: a minimal cipher-free NPC-Control backend for lab fuzz runs.

Stands in for a real NPC server on the NC socket when the goal is to fuzz the NC
*client's* receive handlers: the malformed packets come from the proxy's `s2c`
injection, so the backend only has to complete the login and hold the socket open
so the client stays connected. It accepts the NC login frame (type 3 + any token +
account + password, no key byte), logs every packet id both ways, and sends nothing.

Framing is the NC socket's own (protocol/npc-control.md): `u16be length + zlib body`,
no type byte, no cipher, each frame an independent zlib stream.

Two uses:
  - direct backend for ncprobe.py (standalone NPCControl runs): point ncprobe's
    upstream at this.
  - fallback upstream for the RC-embedded NC run: if the real gserver drops the
    RC's NCL session, point the RC proxy's upstream here instead for the NC run.

Usage: ncstub.py LISTEN_HOST PORT LOGFILE [LABEL]
"""
import os, select, socket, sys, threading, time, zlib

FULLHEX = {int(x) for x in os.environ.get('PROBE_FULLHEX', '').split(',') if x.strip()}


def show(b, n=160):
    s = ''.join(chr(c) if 32 <= c < 127 else '.' for c in b[:n])
    return s + ('...' if len(b) > n else '')


def handle(c, rec, n):
    rec('conn', n, 'open')
    buf = b''; first = True
    try:
        while True:
            r, _, _ = select.select([c], [], [], 0.5)
            if not r:
                continue
            data = c.recv(65536)
            if not data:
                rec('conn', n, 'closed'); return
            buf += data
            while len(buf) >= 2:
                ln = int.from_bytes(buf[:2], 'big')
                if len(buf) < ln + 2:
                    break
                fr, buf = buf[2:ln + 2], buf[ln + 2:]
                try:
                    body = zlib.decompress(fr)
                except Exception as e:
                    rec('c%d' % n, 'frame-decode-error', repr(e)); continue
                if first:  # the login frame: type 3 + token + str account + str password
                    first = False
                    typ = body[0] - 32 if body else -1
                    token = body[1:9]
                    rec('c%d LOGIN type=%d token=%s | %s' % (n, typ, show(token), show(body)))
                    continue
                # classic Graal lines: GCHAR id + payload + \n
                for p in body.split(b'\n'):
                    if not p:
                        continue
                    pid = p[0] - 32
                    m = len(p) if pid in FULLHEX else 48
                    rec('c%d C>S id=%d len=%d | %s | hex=%s' % (n, pid, len(p), show(p[1:]), p[1:m].hex()))
    except Exception as e:
        rec('conn', n, 'error', repr(e))
    finally:
        c.close()


def main():
    lh, lp, logf = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'ncstub'
    log = open(logf, 'a', buffering=1); t0 = time.monotonic(); lk = threading.Lock()

    def rec(*a):
        with lk:
            log.write('%9.3f %s %s\n' % (time.monotonic() - t0, label, ' '.join(str(x) for x in a)))
    L = socket.socket(); L.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); L.bind((lh, lp)); L.listen(4)
    rec('listening', lh, lp)
    k = 0
    while True:
        c, _ = L.accept(); k += 1
        threading.Thread(target=handle, args=(c, rec, k), daemon=True).start()


if __name__ == '__main__':
    main()
