"""Inner records and the outer flush.

Inner layout: v3-python-repro/teardown/framing.md a client routine
and login.md a client routine.
Outer layout: framing.md a client routine. The decompiled body is
the source of the group counts, the backward key walk, and the 1000-byte
slices. a client routine and a client routine are still unrecovered.
"""

from __future__ import annotations

import ctypes
import time
from pathlib import Path

import bz2

# Word at a client global is 6934480. The uint32 at that address is
# 1000000 (1000000). a client routine uses it as the zlib destLen.
COPY_CAP = 1000000
SLICE = 1000
# a client routine stores this constant at connection+0x8.
LCG_STATE = 0x04A80B38

_ZLIB113 = None


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
    """a client routine — id+0x20, optional extra byte, payload, newline."""
    head = gchar_byte(packet_id)
    if first:
        head += gchar_byte(extra)
    return head + payload + b"\n"


def packet_login(account: str, second: str, *, first: bool = True, extra: int = 0) -> bytes:
    """login.md — id 5, G3D28015, then two short strings. a client routine."""
    payload = b"G3D28015" + gchar_string(account) + gchar_string(second)
    return record(5, payload, first=first, extra=extra)


def packet_login_follow(text: str, *, first: bool = False, extra: int = 0) -> bytes:
    """login.md — id 37, the string at a client global. Contents are unknown."""
    return record(0x25, text.encode("latin1", "replace"), first=first, extra=extra)


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
        if i + 1 >= len(buf):
            break
        out.append((kind, bytes([buf[i + 1] - 0x20])))
        i += 2
    return out


def parse_server_list(payload: bytes) -> list[list[str]]:
    """List-connection id 0, a client routine.

    One gchar count, then that many rows. Each row is a gchar field count
    and that many short fields: a length byte, then (byte-0x20) characters.
    Field uses come from the dialog, not from names in this function:
    0 name, 1 language, 2 description, 3 homepage, 4 version,
    5 the number a client routine parses, 6 host, 7 port.
    """
    rows: list[list[str]] = []
    if not payload:
        return rows
    count = payload[0] - 0x20
    i = 1
    for _ in range(max(count, 0)):
        if i >= len(payload):
            break
        fields_n = payload[i] - 0x20
        i += 1
        fields: list[str] = []
        for _field in range(max(fields_n, 0)):
            if i >= len(payload):
                break
            length = payload[i] - 0x20
            if length < 0 or i + 1 + length > len(payload):
                return rows
            fields.append(payload[i + 1:i + 1 + length].decode("latin1"))
            i += 1 + length
        rows.append(fields)
    return rows


def server_category(name: str) -> int:
    """a client routine. The button strings name these prefixes.

    ``U `` is -1 and the dialog does not keep the row.
    ``H `` is 2 and keeps the two-character prefix.
    """
    if name.startswith("3 "):
        return 1
    if name.startswith("P "):
        return 0
    if name.startswith("U "):
        return -1
    if name.startswith("H "):
        return 2
    return 3


def parse_number(text: str) -> int:
    """a client routine. Empty is an address. ``true`` is 1 and ``false`` is 0.

    A ``0x`` prefix is hex of the rest. Anything else is atoi. A zero result
    is kept for ``0`` and ``0x0`` only.
    """
    if text == "":
        return 0xFFFFFFFF
    if text == "true":
        return 1
    if text == "false":
        return 0
    if text.startswith("0x"):
        rest = text[2:]
        try:
            value = int(rest, 16) if rest else 0
        except ValueError:
            value = 0
    else:
        sign = 1
        i = 0
        if text[:1] == "-":
            sign = -1
            i = 1
        end = i
        while end < len(text) and text[end].isdigit():
            end += 1
        value = sign * int(text[i:end] or "0")
    value &= 0xFFFFFFFF
    if value == 0 and text not in ("0", "0x0"):
        return 0xFFFFFFFF
    return value


def server_line(fields: list[str]) -> str | None:
    """a client routine draws a row when the field count is above 5.

    Field 0 is the name. Field 5 is parsed by a client routine and appended
    after a tab. Category 2 keeps the prefix. Every other category drops
    the first two characters.
    """
    if len(fields) <= 5:
        return None
    name = fields[0]
    if server_category(name) < 0:
        return None
    if server_category(name) != 2 and len(name) >= 2:
        name = name[2:]
    return name + "\t" + str(parse_number(fields[5]))


def apply_board(tiles: list[int], payload: bytes, width: int = 64) -> int:
    """Game-connection id 0, a client routine then a client routine.

    Each run is x, y, width, height as byte-0x20, then width*height tiles.
    A tile is two bytes, (first-0x20)*0x80 + (second-0x20), stored at
    (y * 64 + x). A run longer than the buffer stops the packet.
    a client routine looks this level up in a 3 by 3 table and returns -1, -1
    when the table does not hold it. a client routine then blits the cells that
    sit inside the camera. Neither call changes the stored tiles.
    """
    i = 0
    runs = 0
    while len(payload) - i > 3:
        x = payload[i] - 0x20
        y = payload[i + 1] - 0x20
        w = payload[i + 2] - 0x20
        h = payload[i + 3] - 0x20
        if w < 0 or h < 0:
            break
        need = w * h * 2 + 4
        if len(payload) - i < need:
            break
        p = i + 4
        for row in range(h):
            for col in range(w):
                tile = (payload[p] - 0x20) * 0x80 + (payload[p + 1] - 0x20)
                p += 2
                tx, ty = x + col, y + row
                if 0 <= tx < width and 0 <= ty < width:
                    tiles[ty * width + tx] = tile & 0xFFFF
        i += need
        runs += 1
    return runs


def _coord(raw: int) -> float:
    """a client routine cases 1 and 2. (byte-0x20) * 0.5, clamped to 0..63."""
    value = raw * 0.5
    if value < 0.0:
        return 0.0
    if value > 63.0:
        return 63.0
    return value


def parse_remote_player(payload: bytes) -> dict | None:
    """Game-connection id 2, a client routine, then a client routine.

    The first byte minus 0x20 selects the player (+0x40). The same bytes are
    the property stream. Field 1 is x and field 2 is y. Field 0 replaces the
    stored id. Field 3 is the unnamed byte at +0x3a. Field 7 splits into
    (byte-0x20)>>2 and (byte-0x20)&3. No field is named direction.
    """
    if not payload:
        return None
    player: dict = {"lookup": payload[0] - 0x20, "id": payload[0] - 0x20}
    i = 0
    while i + 1 < len(payload):
        kind = payload[i] - 0x20
        if not 0 <= kind <= 10:
            break
        if kind in (8, 9, 10):
            length = payload[i + 1] - 0x20
            end = i + 2 + length
            if length < 0 or end > len(payload):
                break
            i = end
            continue
        value = payload[i + 1] - 0x20
        if kind == 0:
            player["id"] = value
        elif kind == 1:
            player["x"] = _coord(value)
        elif kind == 2:
            player["y"] = _coord(value)
        elif kind == 3:
            player["field_3"] = value
        elif kind == 7:
            player["field_7_hi"] = value >> 2
            player["field_7_lo"] = value & 3
        # Field 4's optional string is still unread. One following byte is consumed.
        i += 2
    return player


def file_extension(name: str) -> str:
    """a client routine. a client routine walks backward, so this is the last '.' onward."""
    dot = name.rfind(".")
    if dot < 0:
        return ""
    return name[dot:]


def file_ask_payload(name: str) -> bytes | None:
    """a client routine. Id 0x17 carries the filename bytes, not a length prefix.

    The extension is compared with ``.gft``. A match is not asked.
    a client routine's five-gchar prefix on id 0x22 is a separate list.
    """
    if file_extension(name) == ".gft":
        return None
    return name.encode("latin1", "replace")


def parse_file_body(payload: bytes) -> tuple[str, bytes] | None:
    """Game id 0x84. A short name, then the remaining bytes.

    a client routine hands those bytes to the object whose name already matches.
    """
    if not payload:
        return None
    length = payload[0] - 0x20
    if length < 0 or 1 + length > len(payload):
        return None
    name = payload[1:1 + length].decode("latin1")
    return name, payload[1 + length:]


def chat_datagram(payload: bytes, prefix: int, key_a: int, key_b: int) -> bytes:
    """a client routine. One prefix byte, then the payload, each byte XORed.

    The prefix is the byte at player+0x1cf. The key is the low byte of
    player+0x1ec XORed with the low byte of the object at a client global,
    field +0x1ec. Those three values are unread, so this is not called
    from setChat. a client routine then sendto's the result to the four address
    bytes at player+0x314 and the port at player+0x31a.
    """
    key = (key_a ^ key_b) & 0xFF
    data = bytes([prefix & 0xFF]) + payload
    return bytes(byte ^ key for byte in data)


def chat_bytes(text: str) -> bytes:
    """a client routine truncates to 0xdc, then a client routine sends id 0x16.

    The bytes here are gchar(0x16) plus the text. a client routine wraps them
    before a client routine. That datagram is not built.
    """
    raw = text.encode("latin1", "replace")[:0xDC]
    return bytes([0x16 + 0x20]) + raw


def step_record() -> None:
    """The walk flag is copied and then consumed locally.

    a client routine stores it. a client routine copies the eleven flags onto the
    player. a client routine calls a client routine, which calls a client routine.
    That path does not call a client routine or a client routine.
    """
    return None


def parse_record(line: bytes) -> tuple[int, bytes]:
    """First byte is id+0x20. A following 0x20 on ids 5, 7, and 1 is the extra byte."""
    if not line:
        return -1, b""
    kind = line[0] - 0x20
    rest = line[1:]
    if rest.startswith(b" ") and kind in (5, 7, 1):
        rest = rest[1:]
    return kind, rest


def lcg_xor(body: bytes, mode: int, state: int, word: int) -> tuple[bytes, int]:
    """a client routine modes 2, 4, and 6.

    Each group does state = state * 0x8088405 + word, stored at connection+0x8.
    The four key bytes are the new state, walked backward from connection+0x0B,
    which is the low byte of that big-endian word first.
    Mode 2 uses at most 12 groups, rounded up. Modes 4 and 6 use at most 4,
    rounded down.
    """
    data = bytearray(body)
    size = len(data)
    if mode == 2:
        groups = min(12, (size + 3) >> 2)
    elif mode in (4, 6):
        groups = min(4, size >> 2)
    else:
        return bytes(data), state & 0xFFFFFFFF
    point = 0
    state &= 0xFFFFFFFF
    word &= 0xFFFFFFFF
    for group in range(groups):
        state = (state * 0x8088405 + word) & 0xFFFFFFFF
        remain = size - group * 4
        nbytes = 4 if group * 4 + 4 <= size else remain
        key = (
            state & 0xFF,
            (state >> 8) & 0xFF,
            (state >> 16) & 0xFF,
            (state >> 24) & 0xFF,
        )
        for k in range(nbytes):
            data[point] ^= key[k]
            point += 1
    return bytes(data), state


def _zlib113() -> ctypes.CDLL:
    """a client routine is zlib 1.1.3 compress (deflateInit_ level -1, version "1.1.3")."""
    global _ZLIB113
    if _ZLIB113 is None:
        lib = ctypes.CDLL(str(Path(__file__).with_name("libz113.so")))
        lib.compress.argtypes = [
            ctypes.c_char_p, ctypes.POINTER(ctypes.c_ulong), ctypes.c_char_p, ctypes.c_ulong,
        ]
        lib.compress.restype = ctypes.c_int
        _ZLIB113 = lib
    return _ZLIB113


def transform_bde98(pending: bytes) -> bytes:
    """a client routine calls a client routine, zlib 1.1.3 compress into a client global.

    Returns the compressed size, or empty when compress fails, the size is 0,
    or the size exceeds the cap at a client global.
    """
    if not pending:
        return b""
    lib = _zlib113()
    bound = ctypes.c_ulong(min(COPY_CAP, len(pending) + len(pending) // 10 + 64))
    dest = ctypes.create_string_buffer(bound.value)
    src = ctypes.create_string_buffer(pending)
    rc = lib.compress(dest, ctypes.byref(bound), src, len(pending))
    if rc != 0 or bound.value == 0 or bound.value > COPY_CAP:
        return b""
    return dest.raw[:bound.value]


def transform_be17c(pending: bytes) -> bytes:
    """a client routine calls a client routine, bzip2 1.0.2 BZ2_bzBuffToBuffCompress.

    blockSize100k is 5, verbosity is 0, workFactor 0 becomes 30.
    A negative return, a zero size, or a size past the cap becomes empty.
    """
    if not pending:
        return b""
    try:
        out = bz2.compress(pending, 5)
    except OSError:
        return b""
    if not out or len(out) > COPY_CAP:
        return b""
    return out


class GraalLink:
    """One connection object. a client routine sets the fields below.

    +0x8 is the constant 0x04a80b38. +0x10 is time() masked with 0x7f
. +0x14 starts at 3, so the first flush is zlib and is
    not XORed. a client routine then stores 0 back into +0x14.
    a client routine sets +0x18 before the TCP open. +0x13 is left 0.
    """

    def __init__(self) -> None:
        self.flag_18 = 1
        self.byte_13 = 0
        self.codec = 3
        self.state = LCG_STATE
        self.word = int(time.time()) & 0x7F
        self.pending = bytearray()
        self.stubs: list[str] = []

    def append(self, packet_id: int, payload: bytes) -> bytes:
        first = self.flag_18 != 0
        self.pending += record(packet_id, payload, first=first, extra=self.byte_13)
        if first:
            self.flag_18 = 0
        if len(self.pending) >= 0x1000:
            return self.flush()
        return b""

    def login(self, account: str, second: str, follow: str, files: list[str] | None = None) -> list[bytes]:
        """a client routine. Id 5 is the first flush. Id 37, then up to four
        id 0x17 names from a client routine, is the second flush.
        """
        frames = []
        self.append(5, b"G3D28015" + gchar_string(account) + gchar_string(second))
        frames.append(self.flush())
        self.append(0x25, follow.encode("latin1", "replace"))
        sent = 0
        for name in files or []:
            payload = file_ask_payload(name)
            if payload is None:
                continue
            if sent >= 4:
                break
            self.append(0x17, payload)
            sent += 1
        frames.append(self.flush())
        return frames

    def flush(self) -> bytes:
        """a client routine. Returns the bytes a client routine would write."""
        if len(self.pending) < 1:
            return b""
        mode = self.codec
        if mode == 0:
            if len(self.pending) < 0x30:
                mode = 2
            elif len(self.pending) < 0x1000:
                mode = 4
            else:
                mode = 6
        raw = bytes(self.pending)
        self.pending.clear()
        if mode in (1, 2):
            body = raw[:COPY_CAP]
        elif mode in (3, 4):
            body = transform_bde98(raw)
        elif mode in (5, 6):
            body = transform_be17c(raw)
        else:
            body = raw
        if mode in (2, 4, 6):
            body, self.state = lcg_xor(body, mode, self.state, self.word)
        if not (1 <= len(body) <= 0xFFFE):
            if self.codec == 3:
                self.codec = 0
            return b""
        declared = len(body) + (1 if self.codec == 0 else 0)
        header = bytes([(declared >> 8) & 0xFF, declared & 0xFF])
        if self.codec == 0:
            header += bytes([mode & 0xFF])
        out = bytearray()
        offset = 0
        header_left = header
        while offset < len(body):
            room = SLICE
            chunk = bytearray()
            if header_left:
                chunk += header_left
                room -= len(chunk)
                header_left = b""
            take = min(room, len(body) - offset)
            chunk += body[offset:offset + take]
            offset += take
            out += chunk
        if self.codec == 3:
            self.codec = 0
        return bytes(out)


def unframe(blob: bytes, state: int = 0, word: int = 0, *, codec: int = 0) -> tuple[int, bytes, int]:
    """Inverse of one flush.

    codec 3 is the constructor's first packet: a 2-byte length and a zlib
    body, with no mode byte and no XOR. codec 0 includes the mode byte.
    """
    if len(blob) < 2:
        raise ValueError("frame shorter than a length")
    declared = (blob[0] << 8) | blob[1]
    if codec == 3:
        body = blob[2:2 + declared]
        if len(body) != declared:
            raise ValueError("frame truncated")
        return 3, transform_bde98_open(body), state
    if len(blob) < 3:
        raise ValueError("frame shorter than a codec-0 header")
    mode = blob[2]
    body = blob[3:3 + (declared - 1)]
    if len(body) != declared - 1:
        raise ValueError("frame truncated: declared %d got %d" % (declared, len(body) + 1))
    plain, state = lcg_xor(body, mode, state, word)
    if mode in (4, 6):
        plain = transform_bde98_open(plain) if mode == 4 else bz2.decompress(plain)
    return mode, plain, state


def transform_bde98_open(body: bytes) -> bytes:
    """Inflate a buffer that a client routine produced. zlib 1.1.3 wrapper."""
    lib = _zlib113()
    # uncompress(dest, destLen, source, sourceLen)
    if not hasattr(lib, "uncompress"):
        raise OSError("zlib 1.1.3 uncompress missing")
    lib.uncompress.argtypes = [
        ctypes.c_char_p, ctypes.POINTER(ctypes.c_ulong), ctypes.c_char_p, ctypes.c_ulong,
    ]
    lib.uncompress.restype = ctypes.c_int
    bound = ctypes.c_ulong(max(len(body) * 8, 64))
    for _ in range(6):
        dest = ctypes.create_string_buffer(bound.value)
        rc = lib.uncompress(dest, ctypes.byref(bound), body, len(body))
        if rc == 0:
            return dest.raw[:bound.value]
        if rc != -5:  # Z_BUF_ERROR
            raise OSError("zlib 1.1.3 uncompress %d" % rc)
        bound = ctypes.c_ulong(bound.value * 2)
    raise OSError("zlib 1.1.3 uncompress grew past the cap")
