"""NetConnection and the two listeners.

Torque methods are a client routine. GameConnection methods are
a client routine. The socket bytes are protocol.GraalLink, not
these Torque calls.
"""

from __future__ import annotations

import socket
import threading

from protocol import LCG_STATE, GraalLink, gchar_byte, lcg_xor, parse_record, unframe
from simobject import SimObject


class NetConnection(SimObject):
    def __init__(self, name: str = "NetConnection") -> None:
        super().__init__(name, "NetConnection")
        self.address = ""
        self.ping = 0
        self.packet_loss = 0
        self.link = GraalLink()

    def connect(self, address: str) -> None:
        """a client routine. Records the address. Does not write Graal bytes."""
        self.address = address
        self.record("connect", (address,))

    def connectLocal(self) -> None:
        self.address = "local"
        self.record("connectLocal", ())

    def getAddress(self) -> str:
        return self.address

    def getPing(self) -> int:
        return self.ping

    def getPacketLoss(self) -> int:
        return self.packet_loss

    def setSimulatedNetParams(self, *args: str) -> str:
        return self.record("setSimulatedNetParams", args)

    def transmitPaths(self) -> str:
        return self.record("transmitPaths", ())

    def clearPaths(self) -> str:
        return self.record("clearPaths", ())

    def checkMaxRate(self) -> bool:
        return True


class GameConnection(NetConnection):
    """a client routine. Methods record the call. Ghosting and demos are not run."""

    def __init__(self, name: str = "GameConnection") -> None:
        super().__init__(name)
        self.class_name = "GameConnection"
        self.control: SimObject | None = None
        self.fov = ""
        self.blackout = False

    def activateGhosting(self) -> str:
        return self.record("activateGhosting", ())

    def resetGhosting(self) -> str:
        return self.record("resetGhosting", ())

    def setControlObject(self, obj: str) -> str:
        self.fields["control"] = str(obj)
        return self.record("setControlObject", (obj,))

    def getControlObject(self) -> str:
        return self.fields.get("control", "")

    def isAIControlled(self) -> str:
        return "0"

    def play2D(self, *args: str) -> str:
        return self.record("play2D", args)

    def play3D(self, *args: str) -> str:
        return self.record("play3D", args)

    def chaseCam(self, *args: str) -> str:
        return self.record("chaseCam", args)

    def setControlCameraFov(self, value: str) -> str:
        self.fov = str(value)
        return self.fov

    def getControlCameraFov(self) -> str:
        return self.fov

    def setBlackOut(self, flag: str) -> str:
        self.blackout = str(flag) not in ("0", "false", "")
        return str(flag)

    def startRecording(self, *args: str) -> str:
        return self.record("startRecording", args)

    def stopRecording(self) -> str:
        return self.record("stopRecording", ())

    def playDemo(self, *args: str) -> str:
        return self.record("playDemo", args)

    def isDemoPlaying(self) -> str:
        return "0"

    def isDemoRecording(self) -> str:
        return "0"


class LineHost:
    """Inner-record host. The Python v3 client sends id 5 then id 37.

    There is no recovered login-accept opcode. The reply is player-buffer
    id 0, which a client routine accepts.
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
                chunk = conn.recv(1024)
                if not chunk:
                    break
                blob += chunk
            first, second, _rest = blob.split(b"\n", 2)
            k1, body1 = parse_record(first)
            k2, body2 = parse_record(second)
            self.events.append("id %d %r" % (k1, body1[:40]))
            self.events.append("id %d %r" % (k2, body2[:40]))
            print("net id %d payload %r" % (k1, body1))
            print("net id %d payload %r" % (k2, body2))
            conn.sendall(gchar_byte(0) + gchar_byte(1) + b"\n")
        srv.close()


def _recvn(conn: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf


class FramedHost:
    """Reads one codec-0 flush and answers with a framed id 0 record.

    The reply link starts with flag +0x18 already clear so the body matches
    a client routine, which treats byte 0 as the id. No login-accept opcode exists.
    """

    def __init__(self) -> None:
        self.mode = -1
        self.body = b""
        self.stubs: list[str] = []

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
            head = _recvn(conn, 2)
            if len(head) < 2:
                print("framed short header %r" % head)
                return
            declared = (head[0] << 8) | head[1]
            rest = _recvn(conn, declared)
            mode, body, _state = unframe(head + rest, codec=3)
            self.mode = mode
            self.body = body
            print("framed mode %d body %r" % (mode, body))
            for line in body.split(b"\n"):
                if line:
                    kind, payload = parse_record(line)
                    print("framed id %d payload %r" % (kind, payload))
            # Second flush is codec 0. The addend is time() & 0x7f, so 128 candidates.
            head2 = _recvn(conn, 2)
            if len(head2) == 2:
                declared2 = (head2[0] << 8) | head2[1]
                tail = _recvn(conn, declared2)
                blob = head2 + tail
                found = None
                for word in range(128):
                    try:
                        mode2, plain, _st = unframe(blob, LCG_STATE, word, codec=0)
                    except (ValueError, OSError):
                        continue
                    if plain[:1] == b"E":
                        found = (word, mode2, plain)
                        break
                if found is None:
                    print("framed follow undecoded")
                else:
                    word, mode2, plain = found
                    print("framed follow mode %d word %d body %r" % (mode2, word, plain))
            reply = GraalLink()
            reply.flag_18 = 0
            reply.codec = 3
            reply.append(0, gchar_byte(1))
            conn.sendall(reply.flush())
        srv.close()
