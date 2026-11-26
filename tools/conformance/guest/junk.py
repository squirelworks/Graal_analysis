#!/usr/bin/env python3
"""junk.py HOST PORT PIDFILE [flood] : (server VM, lab only) send junk at
the gserver's 3D ports and report whether it is still running (T3D-142,
T3D-144). With `flood`, instead 2000 datagrams a second for 10 seconds at
the 3D port (T3D-143: far past seihai-gserver-v2's per-address budget).

UDP datagrams to PORT + 1 (the 3D link): empty, one byte, truncated
headers, random bytes of up to 1400, an oversized 8000-byte one, and a
burst of 500 at full rate. TCP to PORT: connections that send random
bytes, a bad first line, or nothing and close. Each line printed is one
fact the case's `inject` checks match."""
import os
import random
import socket
import sys
import time

host, port, pidfile = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rng = random.Random(1126)


def alive() -> bool:
    try:
        os.kill(int(open(pidfile).read().strip()), 0)
        return True
    except (OSError, ValueError):
        return False


u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if sys.argv[4:] == ["flood"]:
    sent = 0
    end = time.time() + 10
    while time.time() < end:
        t = time.time()
        for _ in range(200):
            try:
                u.sendto(rng.randbytes(rng.randrange(1, 200)), (host, port + 1))
                sent += 1
            except OSError:
                pass
        time.sleep(max(0.0, 0.1 - (time.time() - t)))
    print(f"udp sent {sent}")
    time.sleep(5)
    print("gserver alive" if alive() else "gserver gone")
    sys.exit(0)
shapes = [b"", b"\x00", b"\xff" * 3, bytes(8), bytes([0x80]) + bytes(5)]
shapes += [rng.randbytes(rng.randrange(1, 1400)) for _ in range(200)]
shapes += [rng.randbytes(8000)]
sent = 0
for d in shapes:
    try:
        u.sendto(d, (host, port + 1))
        sent += 1
    except OSError as e:
        print(f"udp send failed: {e}")
for _ in range(500):
    try:
        u.sendto(rng.randbytes(64), (host, port + 1))
        sent += 1
    except OSError:
        pass
print(f"udp sent {sent}")
tcp = 0
for body in [b"", b"GRAAL junk\n", rng.randbytes(256), rng.randbytes(4096), b"\x00\x05" + rng.randbytes(5)]:
    try:
        with socket.create_connection((host, port), timeout=3) as t:
            t.sendall(body)
            time.sleep(0.2)
            tcp += 1
    except OSError as e:
        print(f"tcp failed: {e}")
print(f"tcp sent {tcp}")
time.sleep(5)
print("gserver alive" if alive() else "gserver gone")
