"""NetConnection that speaks the v3 inner records.

Torque methods connect, connectLocal, getAddress come from a client routine
. The bytes on the socket are not those methods. They are the
newline records in the v3 teardown framing.md and the
player parser a client routine.

transmitPaths, clearPaths, setSimulatedNetParams, getPing, getPacketLoss,
and checkMaxRate are stubbed. used.md marks them as Torque stats.
"""

from __future__ import annotations

import socket
import threading


def gchar(value: int) -> bytes:
    return bytes([(value + 0x20) & 0xFF])


class NetConnection:
    def __init__(self) -> None:
        self.address = ""
        self.ping = 0
        self.packet_loss = 0
        self.log: list[str] = []

    def connect(self, address: str) -> None:
        self.address = address
        self.log.append("connect %s" % address)

    def connectLocal(self) -> None:
        self.address = "local"
        self.log.append("connectLocal")

    def getAddress(self) -> str:
        return self.address

    def getPing(self) -> int:
        return self.ping

    def getPacketLoss(self) -> int:
        return self.packet_loss

    def setSimulatedNetParams(self, *_args: str) -> None:
        return None

    def transmitPaths(self) -> None:
        return None

    def clearPaths(self) -> None:
        return None

    def checkMaxRate(self) -> bool:
        return True


def parse_record(line: bytes) -> tuple[int, bytes]:
    """First byte is id+0x20. A following 0x20 is the first-record extra."""
    if not line:
        return -1, b""
    kind = line[0] - 0x20
    rest = line[1:]
    if rest.startswith(b" ") and kind in (5, 7, 1):
        rest = rest[1:]
    return kind, rest


class LineHost:
    """Accepts the Python v3 client and answers inbound id 0.

    The other client sends id 5 (byte 0x25) then id 37 (byte 0x45) and
    reads one newline. There is no recovered login-accept opcode, so the
    reply is player-buffer id 0, which a client routine does accept.
    """

    def __init__(self) -> None:
        self.events: list[str] = []

    def serve(self, port: int, ready: threading.Event | None = None) -> None:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("localhost", port))
        srv.listen(1)
        if ready is not None:
            ready.set()
        conn, _addr = srv.accept()
        with conn:
            conn.settimeout(3)
            blob = b""
            while blob.count(b"\n") < 2:
                blob += conn.recv(1024)
            first, second, _rest = blob.split(b"\n", 2)
            k1, body1 = parse_record(first)
            k2, body2 = parse_record(second)
            self.events.append("id %d %r" % (k1, body1[:40]))
            self.events.append("id %d %r" % (k2, body2[:40]))
            print("net id %d payload %r" % (k1, body1))
            print("net id %d payload %r" % (k2, body2))
            conn.sendall(gchar(0) + gchar(1) + b"\n")
        srv.close()
