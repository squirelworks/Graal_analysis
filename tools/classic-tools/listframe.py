"""Frames for the classic listserver (the ELF `serverlist3`).

Static read of that image: a frame is a big-endian length and a zlib body.
Inside the body, each line ends with a newline. The first byte of a line is
a message id stored as that id plus 32. A length-prefixed string is the same
idea: one length byte (count plus 32) and then that many bytes.

Nothing here opens a socket. See `serverlist3.md`.
"""

import struct
import zlib

GLSER_001 = b'GLSER001'
GLSER_002 = b'GLSER002'
GSERVER_TOKENS = (GLSER_001, GLSER_002)


def _id_byte(msg_id):
    if not 0 <= msg_id <= 223:
        raise ValueError('message id out of range')
    return bytes([msg_id + 32])


def gstr(text):
    """Length-prefixed string. `text` is bytes."""
    if isinstance(text, str):
        text = text.encode('latin1')
    if not 0 <= len(text) <= 223:
        raise ValueError('string longer than a length byte can hold')
    return bytes([len(text) + 32]) + text


def take_gstr(buf, index=0):
    if index >= len(buf):
        raise ValueError('truncated string')
    count = buf[index] - 32
    if count < 0 or index + 1 + count > len(buf):
        raise ValueError('bad string length')
    start = index + 1
    return buf[start:start + count], start + count


def line(msg_id, payload=b''):
    if isinstance(payload, str):
        payload = payload.encode('latin1')
    if b'\n' in payload:
        raise ValueError('a line payload cannot contain a newline')
    return _id_byte(msg_id) + payload


def pack_frame(lines):
    """One frame holding several newline-terminated lines."""
    body = b''.join(line + b'\n' for line in lines)
    compressed = zlib.compress(body)
    if len(compressed) > 65535:
        raise ValueError('compressed frame too long')
    return struct.pack('>H', len(compressed)) + compressed


def unpack_frames(buf):
    """Yield every line in `buf`. `buf` may hold more than one frame."""
    index = 0
    while index < len(buf):
        if index + 2 > len(buf):
            raise ValueError('truncated length')
        size = struct.unpack_from('>H', buf, index)[0]
        index += 2
        if size < 0 or index + size > len(buf):
            raise ValueError('truncated zlib body')
        body = zlib.decompress(buf[index:index + size])
        index += size
        if not body.endswith(b'\n'):
            raise ValueError('frame does not end on a newline')
        for raw in body.split(b'\n')[:-1]:
            if not raw:
                continue
            yield raw


def client_lines(edition, account, password):
    """What a classic client sends: id 0 edition, then id 1 account and password."""
    return [
        line(0, edition),
        line(1, gstr(account) + gstr(password)),
    ]


def parse_client_line(raw):
    msg_id = raw[0] - 32
    rest = raw[1:]
    if msg_id == 0:
        return {'id': 0, 'edition': rest}
    if msg_id == 1:
        account, index = take_gstr(rest, 0)
        password, index = take_gstr(rest, index)
        if index != len(rest):
            raise ValueError('trailing bytes after the password')
        return {'id': 1, 'account': account, 'password': password}
    return {'id': msg_id, 'rest': rest}


def gserver_login_line(kind, token, world):
    """First line from a game server. `kind` is 0 or 1. `token` is 8 bytes."""
    if kind not in (0, 1):
        raise ValueError('login kind must be 0 or 1')
    if isinstance(token, str):
        token = token.encode('ascii')
    if isinstance(world, str):
        world = world.encode('latin1')
    if token not in GSERVER_TOKENS:
        raise ValueError('token must be GLSER001 or GLSER002')
    if b'\n' in world:
        raise ValueError('world name cannot contain a newline')
    return bytes([kind + 32]) + token + world


def parse_gserver_login(raw):
    kind = raw[0] - 32
    if kind not in (0, 1):
        raise ValueError('rejected login kind')
    token = raw[1:9]
    if token not in GSERVER_TOKENS:
        raise ValueError('rejected token')
    return {'kind': kind, 'token': token, 'world': raw[9:]}
