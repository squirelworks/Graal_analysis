#!/usr/bin/env python3
"""Conformance lobby (lab only): answer each gen-5 client login on PORT with
one PLO_SERVERWARP to the lab gserver, then hold the link 20 s so the client
acts on the warp before it sees a close (a client-side race, seihai-gserver
docs/GRAAL3D.md lab 2026-11-19).

    lobby.py PORT "NAME,HOST,GSPORT"

NAME is the server name the client sees: with a leading "3 " a 3D-capable
client enters 3D (T3D-059), without it the same server plays 2D.
Python 3 standard library only.
"""
import socket
import struct
import sys
import threading
import time
import zlib


def enc(key, b, limit=12):
    """The gen-5 partial XOR stream (the first `limit` words of a frame)."""
    it = 0x04A80B38
    b = bytearray(b)
    for j in range(min((len(b) + 3) // 4, limit)):
        it = (it * 0x08088405 + key) & 0xFFFFFFFF
        ks = struct.pack("<I", it)
        for q in range(4):
            if 4 * j + q < len(b):
                b[4 * j + q] ^= ks[q]
    return bytes(b)


def serve(c, warp):
    try:
        n = struct.unpack(">H", c.recv(2))[0]
        body = b""
        while len(body) < n:
            part = c.recv(n - len(body))
            if not part:
                return
            body += part
        d = zlib.decompress(body)
        key = d[1] - 32
        print("login", d[2:10], flush=True)
        out = bytes([2]) + enc(key, bytes([178 + 32]) + warp.encode() + b"\n")
        c.sendall(struct.pack(">H", len(out)) + out)
        print("sent warp", warp, flush=True)
        c.settimeout(1)
        t = time.time()
        while time.time() - t < 20:
            try:
                if c.recv(4096) == b"":
                    break
            except socket.timeout:
                pass
    except Exception as e:  # a lab helper: log and carry on
        print("lobby error", e, flush=True)
    finally:
        c.close()


def main():
    port, warp = int(sys.argv[1]), sys.argv[2]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", port))
    s.listen(4)
    while True:
        c, _ = s.accept()
        threading.Thread(target=serve, args=(c, "0," + warp), daemon=True).start()


if __name__ == "__main__":
    main()
