#!/usr/bin/env python3
"""Mac v3.04 PowerPC client, inner-record layer only.

Teardown: ../teardown/. The real process also wraps a flush in a
big-endian length and an LCG (framing.md). This process speaks the
newline records unless --framed is set, and it never dials a host
unless --host or --stub is passed.
"""

from __future__ import annotations

import argparse
import socket
import threading
from pathlib import Path

# framing.md — 62-character board alphabet at file offset 5536006.
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BOARD = 64


def gchar_byte(value: int) -> bytes:
    """framing.md — one small value is value + 0x20."""
    return bytes([(value + 0x20) & 0xFF])


def gchar_string(text: str) -> bytes:
    """framing.md — short string if len < 0xE0, else 0xFF and 0xDF bytes."""
    raw = text.encode("latin1", "replace")
    if len(raw) < 0xE0:
        return gchar_byte(len(raw)) + raw
    return bytes([0xFF]) + raw[:0xDF]


def record(packet_id: int, payload: bytes, *, first: bool, extra: int = 0) -> bytes:
    """framing.md a client routine — id+0x20, optional extra byte, payload, newline."""
    head = gchar_byte(packet_id)
    if first:
        head += gchar_byte(extra)
    return head + payload + b"\n"


def packet_login(account: str, second: str, *, first: bool = True, extra: int = 0) -> bytes:
    """login.md — id 5, G3D28015, then two short strings. a client routine."""
    payload = b"G3D28015" + gchar_string(account) + gchar_string(second)
    return record(5, payload, first=first, extra=extra)


def packet_login_follow(text: str) -> bytes:
    """login.md — id 37, the string at a client global. Contents are unknown."""
    return record(0x25, text.encode("latin1", "replace"), first=False)


def packet_lister_hello(*, first: bool = True, extra: int = 0) -> bytes:
    """token.md — id 7 on the lister connection. a client routine."""
    return record(7, b"G3D30123newmain", first=first, extra=extra)


def packet_lister_login(first_string: str, second: str) -> bytes:
    """login.md — id 1, string C then string B. a client routine."""
    payload = gchar_string(first_string) + gchar_string(second)
    return record(1, payload, first=False)


def packet_file_ask(name: str) -> bytes:
    """packets.md — id 23 (0x17). a client routine. Names ending in .gft are not sent."""
    if name.endswith(".gft"):
        raise ValueError("a client routine skips .gft")
    return record(0x17, name.encode("latin1", "replace"), first=False)


def parse_player_buffer(buf: bytes) -> list[tuple[int, bytes]]:
    """packets.md a client routine — ids 0..10. Any other id stops the buffer."""
    out = []
    i = 0
    while i + 1 < len(buf):
        kind = buf[i] - 0x20
        if not 0 <= kind <= 10:
            break
        if kind in (8, 9, 10):
            if i + 1 >= len(buf):
                break
            length = buf[i + 1] - 0x20
            end = i + 2 + length
            if end > len(buf) or length < 0:
                break
            out.append((kind, buf[i + 2:end]))
            i = end
            continue
        # ids 0..7 in the recovered function each take one more byte.
        # id 4 may continue into a string. Keep the one-byte form here.
        if i + 1 >= len(buf):
            break
        out.append((kind, bytes([buf[i + 1] - 0x20])))
        i += 2
    return out


class Board:
    """assets.md a client routine — 64 by 64, two alphabet characters per tile."""

    def __init__(self) -> None:
        self.tiles = [0] * (BOARD * BOARD)
        self.magic = ""
        self.sections: list[str] = []

    def load(self, path: Path) -> None:
        text = path.read_text("latin1")
        header = text[:8]
        self.magic = header
        if header not in ("GLEVNW01", "GR-V1.00", "GR-V1.01", "GR-V1.02", "GR-V1.03"):
            raise ValueError("header %r is not a magic a client routine accepts" % header)
        for line in text.splitlines():
            parts = line.split()
            if not parts:
                continue
            self.sections.append(parts[0])
            if parts[0] != "BOARD" or len(parts) < 6:
                continue
            x, y, width = int(parts[1]), int(parts[2]), int(parts[3])
            data = parts[5]
            self._place(x, y, width, data)

    def _place(self, x: int, y: int, width: int, data: str) -> None:
        # assets.md — x < 64, 0 <= y < 64, x + width <= 64.
        if not (x < BOARD and 0 <= y < BOARD and width > 0 and x + width <= BOARD):
            return
        if len(data) < width * 2:
            return
        base = (y * BOARD + x) * 1
        for n in range(width):
            a = ALPHABET.find(data[n * 2])
            b = ALPHABET.find(data[n * 2 + 1])
            if a < 0 or b < 0:
                break
            self.tiles[base + n] = (a << 6) + b

    def tile(self, x: int, y: int) -> int | None:
        if 0 <= x < BOARD and 0 <= y < BOARD:
            return self.tiles[y * BOARD + x]
        return None


class Walker:
    """movement.md — the only spatial rule recovered is the 64-bound."""

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.facing = "down"

    def step(self, way: str, board: Board | None) -> str:
        delta = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        if way not in delta:
            return "unknown direction %s" % way
        dx, dy = delta[way]
        nx, ny = self.x + dx, self.y + dy
        self.facing = way
        if not (0 <= nx < BOARD and 0 <= ny < BOARD):
            return "blocked by the 64-bound at %d,%d" % (nx, ny)
        self.x, self.y = nx, ny
        tile = board.tile(nx, ny) if board else None
        return "walk %s to %d,%d tile %s anim %s" % (way, nx, ny, tile, "walk")


def _read_line(sock: socket.socket) -> bytes:
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf.split(b"\n", 1)[0]


def serve_stub(ready: threading.Event, holder: dict) -> None:
    """Local stand-in. Speaks one newline reply. Does not open any other host."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("localhost", 0))
    srv.listen(1)
    holder["port"] = srv.getsockname()[1]
    ready.set()
    conn, _addr = srv.accept()
    with conn:
        conn.settimeout(2)
        blob = b""
        while blob.count(b"\n") < 2:
            blob += conn.recv(1024)
        login_line, follow, _rest = blob.split(b"\n", 2)
        print("stub login id=%s follow id=%s" % (login_line[:1], follow[:1]))
        # packets.md id 0 — one small byte. Not a recovered login-accept.
        conn.sendall(gchar_byte(0) + gchar_byte(1) + b"\n")
    srv.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Mac v3 inner-record client")
    parser.add_argument("--host", default="", help="game host. Omit to stay offline")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--stub", action="store_true", help="talk to a local stub instead of --host")
    parser.add_argument("--nw", default="", help="local GLEVNW01 file")
    parser.add_argument("--account", default="guest")
    parser.add_argument("--second", default="", help="login string B, name unknown")
    parser.add_argument("--follow", default="", help="id 37 payload, name unknown")
    parser.add_argument("moves", nargs="*", help="up down left right")
    args = parser.parse_args()

    board = None
    if args.nw:
        board = Board()
        board.load(Path(args.nw))
        print("loaded %s magic %s sections %s" % (args.nw, board.magic, board.sections[:8]))
    walker = Walker()
    for way in args.moves:
        print(walker.step(way, board))

    login = packet_login(args.account, args.second)
    follow = packet_login_follow(args.follow)
    print("login record %d bytes %s" % (len(login), login))
    print("follow record %d bytes %s" % (len(follow), follow))

    if not args.stub and not args.host:
        print("offline. Pass --stub or --host to open a socket.")
        return

    if args.stub:
        ready = threading.Event()
        holder: dict = {}
        thread = threading.Thread(target=serve_stub, args=(ready, holder), daemon=True)
        thread.start()
        ready.wait(2)
        host, port = "localhost", holder["port"]
    else:
        host, port = args.host, args.port
        thread = None

    print("connect %s:%d" % (host, port))
    sock = socket.create_connection((host, port), timeout=3)
    with sock:
        sock.sendall(login)
        sock.sendall(follow)
        reply = _read_line(sock)
    print("reply %s parsed %s" % (reply, parse_player_buffer(reply)))
    if thread is not None:
        thread.join(2)


if __name__ == "__main__":
    main()
