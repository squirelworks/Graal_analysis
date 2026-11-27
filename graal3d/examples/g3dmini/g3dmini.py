#!/usr/bin/env python3
"""g3dmini: a small Graal 3D server for the Torque-era clients (protocol 24).

This is the UDP half of a Graal 3D server, written for the community guide
(graal3d/community-guide.md, part 6) so you can read a whole working 3D side
in one file. It speaks the Torque protocol 24 link that the 4.20r8, 5.00r7 and
5.12 clients open on the listed TCP port + 1:

  * the challenge and connect handshake, with Graal's class-name table;
  * the notify link (sequence numbers, acks, lost-packet notification);
  * guaranteed events (mission start commands, terrain chunks);
  * ghosts: Sun, Sky, TerrainBlock, GameObjects and a Camera per client;
  * the mission start (phase 1, phase 2 held until the terrain is in, then
    the control object);
  * the client's own position in every packet, relayed to other players.

What it does NOT do: the TCP side. A real client also logs in over TCP on the
listed port, asks for every shape and texture over TCP, and waits for
PLO_SERVERLISTCONNECTED before it shows the 3D view. Pair this with a gserver
that does those things (see the guide, part 6.2), or read seihai-gserver's
src/graal3d/ for a complete server. Here the account named in the connect
request is trusted; a real server must tie it to a TCP login from the same
address.

Standard library only. Everything is written from the behaviour notes in
Graal_analysis (torque/udp-session.md, torque/terrain-512.md and the board).
The Huffman character table is stock Torque's, from the MIT-licensed Torque3D
source (core/stream/bitStream.cpp), as in torque/tools/tbits.py.

Run it:
  python3 g3dmini.py --port 14901 --world world.txt
  python3 g3dmini.py --make-terrain hills        # writes a demo terrain folder
"""

import argparse
import hashlib
import hmac
import math
import os
import socket
import struct
import sys
import time
import zlib

# ---------------------------------------------------------------------------
# 1. Bit streams (udp-session.md section 2)
# ---------------------------------------------------------------------------

FREQS = [0] * 9 + [329, 21] + [0] * 21 + [
    2809, 68, 0, 27, 0, 58, 3, 62, 4, 7, 0, 0, 15, 65, 554, 3, 394, 404, 189, 117, 30, 51, 27, 15, 34, 32,
    80, 1, 142, 3, 142, 39, 0, 144, 125, 44, 122, 275, 70, 135, 61, 127, 8, 12, 113, 246, 122, 36, 185, 1,
    149, 309, 335, 12, 11, 14, 54, 151, 0, 0, 2, 0, 0, 211, 0, 2090, 344, 736, 993, 2872, 701, 605, 646,
    1552, 328, 305, 1240, 735, 1533, 1713, 562, 3, 1775, 1149, 1469, 979, 407, 553, 59, 279, 31, 0, 0, 0,
    68] + [0] * 129


def _build_huffman():
    """Torque's fixed Huffman tree. Same construction (and tie-breaks) as stock."""
    leaves = [f + 1 for f in FREQS]
    nodes = [None]
    wraps = [("L", i) for i in range(256)]

    def pop(w):
        return leaves[w[1]] if w[0] == "L" else nodes[w[1]][0]

    def idx(w):
        return -(w[1] + 1) if w[0] == "L" else w[1]

    while len(wraps) != 1:
        m1, m2, i1, i2 = 0xFFFFFFFE, 0xFFFFFFFF, -1, -1
        for i, w in enumerate(wraps):
            p = pop(w)
            if p < m1:
                m2, i2, m1, i1 = m1, i1, p, i
            elif p < m2:
                m2, i2 = p, i
        nodes.append([pop(wraps[i1]) + pop(wraps[i2]), idx(wraps[i1]), idx(wraps[i2])])
        lo, hi = min(i1, i2), max(i1, i2)
        wraps[lo] = ("N", len(nodes) - 1)
        if i2 != len(wraps) - 1:
            wraps[hi] = wraps[-1]
        wraps.pop()
    nodes[0] = list(nodes[wraps[0][1]])
    codes = {}

    def walk(i, code):
        if i < 0:
            codes[-(i + 1)] = code
            return
        walk(nodes[i][1], code + [0])
        walk(nodes[i][2], code + [1])

    walk(0, [])
    return nodes, codes


assert len(FREQS) == 256
HUFF_NODES, HUFF_CODES = _build_huffman()


class OutOfBits(Exception):
    pass


class BitWriter:
    """Bits packed least significant first, bytes in order."""

    def __init__(self):
        self.bits = []

    def __len__(self):
        return len(self.bits)

    def flag(self, b):
        self.bits.append(1 if b else 0)
        return bool(b)

    def int(self, v, n):
        v = int(v)
        self.bits.extend((v >> i) & 1 for i in range(n))

    def u8(self, v):
        self.int(v & 0xFF, 8)

    def u32(self, v):
        self.int(v & 0xFFFFFFFF, 32)

    def f32(self, v):
        self.u32(struct.unpack("<I", struct.pack("<f", float(v)))[0])

    def raw(self, data):
        for b in data:
            self.u8(b)

    def string(self, text):
        """An out-of-band string: Huffman when shorter, else raw (as stock)."""
        data = text.encode("latin1")[:255] if isinstance(text, str) else bytes(text)[:255]
        coded = sum(len(HUFF_CODES[c]) for c in data)
        if coded < len(data) * 8:
            self.flag(1)
            self.u8(len(data))
            for c in data:
                self.bits.extend(HUFF_CODES[c])
        else:
            self.flag(0)
            self.u8(len(data))
            self.raw(data)

    def pstring(self, text):
        """A string inside a data packet: the 'shares a prefix' flag (always 0 here)."""
        self.flag(0)
        self.string(text)

    def append(self, other):
        self.bits.extend(other.bits)

    def bytes(self):
        out = bytearray((len(self.bits) + 7) // 8)
        for i, b in enumerate(self.bits):
            out[i >> 3] |= b << (i & 7)
        return bytes(out)


class BitReader:
    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos
        self.prev = b""  # the per-packet previous-string buffer for pstrings

    def left(self):
        return len(self.data) * 8 - self.pos

    def flag(self):
        if self.pos >= len(self.data) * 8:
            raise OutOfBits()
        b = (self.data[self.pos >> 3] >> (self.pos & 7)) & 1
        self.pos += 1
        return b

    def int(self, n):
        v = 0
        for i in range(n):
            v |= self.flag() << i
        return v

    def u8(self):
        return self.int(8)

    def u32(self):
        return self.int(32)

    def f32(self):
        return struct.unpack("<f", struct.pack("<I", self.u32()))[0]

    def raw(self, n):
        return bytes(self.u8() for _ in range(n))

    def string(self):
        if self.flag():
            out = bytearray()
            for _ in range(self.u8()):
                i = 0
                while i >= 0:
                    i = HUFF_NODES[i][2] if self.flag() else HUFF_NODES[i][1]
                out.append(-(i + 1))
            return bytes(out)
        return self.raw(self.u8())

    def pstring(self):
        if self.flag():  # reuse the first <int8> characters of the previous string
            keep = self.u8()
            s = self.prev[:keep] + self.string()
        else:
            s = self.string()
        self.prev = s
        return s


# ---------------------------------------------------------------------------
# 2. Handshake (udp-session.md section 3)
# ---------------------------------------------------------------------------

CHALLENGE_REQUEST, CHALLENGE_RESPONSE = 0x1A, 0x1E
CONNECT_REQUEST, CONNECT_REJECT, CONNECT_ACCEPT, DISCONNECT = 0x20, 0x22, 0x24, 0x26

PROTOCOL = 24
# The server chooses class ids; the client maps them by name. Objects are
# type 0 and events type 1 on protocols 21 and 24.
OBJECT_CLASSES = ["Camera", "DynamicGrass", "DynamicGrassReplicator", "DynamicShapeReplicator",
                  "GameObject", "Sky", "Sun", "TerrainBlock", "WaterBlock", "fxSunLight"]
EVENT_CLASSES = ["BigDataChunkEvent", "BigDataStartEvent", "ConnectionMessageEvent",
                 "GhostAlwaysObjectEvent", "NetStringEvent", "RemoteCommandEvent",
                 "RequestReloadEvent", "TerrainChunkEvent", "TerrainRequestUpdatesEvent"]
OBJ_ID = {n: i for i, n in enumerate(OBJECT_CLASSES)}
EVT_ID = {n: i for i, n in enumerate(EVENT_CLASSES)}


def challenge_response(sequence, digest):
    w = BitWriter()
    w.u8(CHALLENGE_RESPONSE)
    w.u32(sequence)
    for d in digest:
        w.u32(d)
    return w.bytes()


def read_connect_request(packet):
    r = BitReader(packet)
    if r.u8() != CONNECT_REQUEST:
        return None
    req = {"sequence": r.u32(), "digest": [r.u32() for _ in range(4)],
           "class": r.string(), "group": r.u32(), "crc": r.u32(), "game": r.string(),
           "protocol": r.u32(), "min_protocol": r.u32(), "password": r.string()}
    argc = r.u32()
    req["args"] = [r.string() for _ in range(min(argc, 16))]
    return req


def connect_accept(sequence):
    w = BitWriter()
    w.u8(CONNECT_ACCEPT)
    w.u32(sequence)
    for ctype, names in ((0, OBJECT_CLASSES), (1, EVENT_CLASSES)):
        for i, name in enumerate(names):
            w.flag(1)
            w.int(ctype, 12)
            w.int(i, 12)
            w.string(name)
    w.flag(0)
    w.u32(PROTOCOL)
    return w.bytes()


def connect_reject(sequence, reason):
    w = BitWriter()
    w.u8(CONNECT_REJECT)
    w.u32(sequence)
    w.string(reason)
    return w.bytes()


def disconnect_packet(sequence, reason):
    w = BitWriter()
    w.u8(DISCONNECT)
    w.u32(sequence)
    w.string(reason)
    return w.bytes()


# ---------------------------------------------------------------------------
# 3. The notify link (udp-session.md section 4)
# ---------------------------------------------------------------------------

DATA, PING, ACK = 0, 1, 2
WINDOW = 30


class Link:
    """Packet numbering and acks. Every data packet we send is later reported
    delivered or lost, in order; that is the only delivery signal."""

    def __init__(self, connect_sequence):
        self.connect_bit = connect_sequence & 1
        self.last_seq_received = 0
        self.highest_acked = 0
        self.last_send_seq = 0
        self.ack_mask = 0
        self.last_ack_acked = 0
        self.received_at_send = [0] * 32

    def window_full(self):
        return self.last_send_seq - self.highest_acked >= WINDOW

    def header(self, ptype):
        ack_bytes = min(4, (self.last_seq_received - self.last_ack_acked + 7) >> 3)
        if ptype == DATA:
            self.last_send_seq += 1
        w = BitWriter()
        w.flag(1)
        w.int(self.connect_bit, 1)
        w.int(self.last_send_seq & 0x1FF, 9)
        w.int(self.last_seq_received & 0x1FF, 9)
        w.int(ptype, 2)
        w.int(ack_bytes, 3)
        w.int(self.ack_mask & ((1 << (ack_bytes * 8)) - 1), ack_bytes * 8)
        if ptype == DATA:
            self.received_at_send[self.last_send_seq & 31] = self.last_seq_received
            w.flag(0)  # current rate unchanged
            w.flag(0)  # max rate unchanged
        return w

    def receive(self, packet):
        """Returns (type, [(seq, delivered)], reader or None). Raises ValueError to drop."""
        r = BitReader(packet)
        if not r.flag():
            raise ValueError("out of band")
        bit, seq, highest = r.int(1), r.int(9), r.int(9)
        ptype, ack_bytes = r.int(2), r.int(3)
        if bit != self.connect_bit or ptype > 2 or ack_bytes > 4:
            raise ValueError("bad header or another link")
        their_mask = r.int(ack_bytes * 8)
        seq |= self.last_seq_received & ~0x1FF
        if seq < self.last_seq_received:
            seq += 0x200
        if seq > self.last_seq_received + 31:
            raise ValueError("outside the receive window")
        highest |= self.highest_acked & ~0x1FF
        if highest < self.highest_acked:
            highest += 0x200
        if highest > self.last_send_seq:
            raise ValueError("acks a packet we never sent")
        shift = seq - self.last_seq_received
        self.ack_mask = 0 if shift >= 32 else (self.ack_mask << shift) & 0xFFFFFFFF
        if ptype == DATA:
            self.ack_mask |= 1
        notes = []
        for s in range(self.highest_acked + 1, highest + 1):
            back = highest - s
            delivered = back < 32 and (their_mask >> back) & 1 == 1
            notes.append((s, delivered))
            if delivered:
                self.last_ack_acked = self.received_at_send[s & 31]
        if seq - self.last_ack_acked > 32:
            self.last_ack_acked = seq - 32
        self.highest_acked = highest
        body = None
        if self.last_seq_received != seq:
            self.last_seq_received = seq
            if ptype == DATA:
                for _ in range(2):  # current and max rate: flag, then 10 + 10 bits
                    if r.flag():
                        r.int(10)
                        r.int(10)
                body = r
        return ptype, notes, body


# ---------------------------------------------------------------------------
# 4. Events (udp-session.md section 5)
# ---------------------------------------------------------------------------

def remote_command(*args):
    """A RemoteCommandEvent payload. Strings go as plain text (code 1); the
    5.12 accepts that for the mission commands, and answers the same way."""
    w = BitWriter()
    w.int(len(args), 5)
    for a in args:
        if isinstance(a, int):
            w.int(3, 2)
            w.flag(a < 0)
            m = min(abs(a), (1 << 31) - 1)
            if w.flag(m < 1 << 7):
                w.int(m, 7)
            elif w.flag(m < 1 << 15):
                w.int(m, 15)
            else:
                w.int(m, 31)
        else:
            w.int(1, 2)
            w.pstring(a)
    return w


def read_remote_command(r, tags):
    args = []
    for _ in range(r.int(5)):
        code = r.int(2)
        if code == 0:
            args.append(b"")
        elif code == 1:
            args.append(r.pstring())
        elif code == 2:
            args.append(tags.get(r.int(5), b""))
        else:
            neg = r.flag()
            v = r.int(7) if r.flag() else (r.int(15) if r.flag() else r.int(31))
            args.append(-v if neg else v)
    return args


def bigdata_events(transfer, weapon, kind, option, text):
    """Graal's text channel: a BigDataStartEvent, then chunks of up to 191 bytes."""
    data = text.encode("latin1")
    start = BitWriter()
    start.int(transfer, 16)
    start.pstring(weapon)
    start.pstring(kind)
    start.pstring(option)
    start.int(len(data), 24)
    start.int(0, 3)  # no compression
    out = [("BigDataStartEvent", start)]
    for i in range(0, len(data), 191):
        c = BitWriter()
        c.int(transfer, 16)
        c.int(len(data[i:i + 191]), 8)
        c.raw(data[i:i + 191])
        out.append(("BigDataChunkEvent", c))
    return out


class Events:
    """Guaranteed, ordered events in both directions."""

    def __init__(self):
        self.next_send = 0
        self.acked_below = 0
        self.to_send = []        # [(seq, class name, payload)]
        self.in_flight = {}      # packet seq -> [(seq, name, payload)]
        self.delivered = set()
        self.next_receive = 0
        self.waiting = {}
        self.tags = {}

    def send(self, name, payload):
        seq = self.next_send
        self.next_send += 1
        self.to_send.append((seq, name, payload))
        return seq

    def is_delivered(self, seq):
        return seq < self.acked_below or seq in self.delivered

    def write(self, w, packet, max_bits):
        w.flag(0)  # no unguaranteed events
        prev, sent = None, []
        while self.to_send:
            seq, name, payload = self.to_send[0]
            if seq > self.acked_below + 125:
                break
            in_order = prev is not None and prev + 1 == seq
            size = 2 + (0 if in_order else 7) + 12 + 14 + len(payload) + 1
            if sent and len(w) + size > max_bits:
                break
            w.flag(1)
            if not w.flag(in_order):
                w.int(seq & 0x7F, 7)
            w.int(EVT_ID[name], 12)
            w.int(len(payload), 14)
            w.append(payload)
            prev = seq
            sent.append(self.to_send.pop(0))
        w.flag(0)
        if sent:
            self.in_flight[packet] = sent

    def notify(self, packet, delivered):
        sent = self.in_flight.pop(packet, None)
        if not sent:
            return
        if delivered:
            for seq, _, _ in sent:
                self.delivered.add(seq)
            while self.acked_below in self.delivered:
                self.delivered.discard(self.acked_below)
                self.acked_below += 1
        else:  # put them back, in order, ahead of anything newer
            self.to_send = sorted(self.to_send + sent, key=lambda e: e[0])

    def read(self, r):
        """Reads both lists; returns [(class name, reader at payload, end bit)] in order."""
        out = []
        while r.flag():  # unguaranteed
            out.append(self._read_one(r))
        prev = None
        while r.flag():  # guaranteed
            if r.flag():
                seq7 = ((prev + 1) & 0x7F) if prev is not None else 0x7F
            else:
                seq7 = r.int(7)
            prev = seq7
            ev = self._read_one(r)
            seq = seq7 | (self.next_receive & ~0x7F)
            if seq < self.next_receive:
                seq += 128
            self.waiting.setdefault(seq, ev)
        while self.next_receive in self.waiting:
            out.append(self.waiting.pop(self.next_receive))
            self.next_receive += 1
        return out

    @staticmethod
    def _read_one(r):
        class_id, length = r.int(12), r.int(14)
        start = r.pos
        r.pos += length  # skip by length whatever the class
        name = EVENT_CLASSES[class_id] if class_id < len(EVENT_CLASSES) else None
        return name, BitReader(r.data, start), start + length


# ---------------------------------------------------------------------------
# 5. Ghost classes (udp-session.md section 8, terrain-512.md section 1)
# ---------------------------------------------------------------------------

# GameObject sections, as bits of a change mask.
NAME, SCALE, SHAPE, SKIN, TRANSFORM, MOVETYPE, MOVEDATA, SHAPEDATA, CHAT, CLASSES, ATTRS, NICK, FLAGS = \
    (1 << i for i in range(13))
ALL = (1 << 13) - 1
SOLID, SHADOW, COLLISION = 0x08, 0x10, 0x40


def facing(position, target):
    """A transform at `position` whose forward axis (+y) looks at `target`.
    The clients turn the opposite way from the right-hand rule, so the angle
    is negated (lab, 5.12 and 4.20r6)."""
    d = [t - p for t, p in zip(target, position)]
    flat = math.hypot(d[0], d[1])
    if flat == 0 and d[2] == 0:
        return (position, (0.0, 0.0, 1.0), 0.0)
    yaw = 0.0 if flat == 0 else math.atan2(-d[0], d[1])
    pitch = math.atan2(d[2], flat)
    sz, cz = math.sin(yaw / 2), math.cos(yaw / 2)
    sx, cx = math.sin(pitch / 2), math.cos(pitch / 2)
    qw, v = cz * cx, (cz * sx, sz * sx, sz * cx)
    n = math.sqrt(sum(c * c for c in v))
    if n < 1e-6:
        return (position, (0.0, 0.0, 1.0), 0.0)
    return (position, tuple(c / n for c in v), -2 * math.atan2(n, qw))


class GameObject:
    cls = "GameObject"

    def __init__(self, name, shape="", position=(0, 0, 0), axis=(0, 0, 1), angle=0.0):
        self.name, self.shape, self.skin, self.chat = name, shape, "", ""
        self.scale = (0.0, 0.0, 0.0)          # (0,0,0) means "normal size"
        self.position, self.axis, self.angle = tuple(position), tuple(axis), float(angle)
        self.attr = [""] * 8
        self.nickname, self.nick_color = "", (255, 255, 255, 255)
        self.flags = 0

    def full_mask(self):
        m = NAME | SHAPE | TRANSFORM | FLAGS
        if self.scale != (0.0, 0.0, 0.0):
            m |= SCALE
        if self.skin:
            m |= SKIN
        if self.chat:
            m |= CHAT
        if any(self.attr):
            m |= ATTRS
        if self.nickname:
            m |= NICK
        return m

    def write(self, w, mask):
        if w.flag(mask & NAME):
            w.pstring(self.name)
        if w.flag(mask & SCALE):
            for v in self.scale:
                w.f32(v)
        if w.flag(mask & SHAPE):
            w.pstring(self.shape)
        if w.flag(mask & SKIN):
            w.pstring(self.skin)
        if w.flag(mask & TRANSFORM):
            for v in self.position + self.axis + (self.angle,):
                w.f32(v)
        w.flag(0)  # 6 movetype: none, so section 7 never follows
        w.flag(0)  # 7 movement data
        w.flag(0)  # 8 shape data (animation threads)
        if w.flag(mask & CHAT):
            w.pstring(self.chat)
        w.flag(0)  # 10 script classes
        if w.flag(mask & ATTRS):
            for a in self.attr:
                if w.flag(a):
                    w.pstring(a)
        if w.flag(mask & NICK):
            w.pstring(self.nickname)
            for c in self.nick_color:
                w.u8(c)
        if w.flag(mask & FLAGS):
            w.int(self.flags, 16)

    def read(self, r):
        """Reads a client's update of its own object. Returns the changed mask."""
        m = 0
        if r.flag():
            self.name = r.pstring().decode("latin1"); m |= NAME
        if r.flag():
            self.scale = (r.f32(), r.f32(), r.f32()); m |= SCALE
        if r.flag():
            self.shape = r.pstring().decode("latin1"); m |= SHAPE
        if r.flag():
            self.skin = r.pstring().decode("latin1"); m |= SKIN
        if r.flag():
            self.position = (r.f32(), r.f32(), r.f32())
            self.axis = (r.f32(), r.f32(), r.f32())
            self.angle = r.f32(); m |= TRANSFORM
        if r.flag():
            r.pstring()  # a movetype from the client; this server never sends one
        if r.flag():
            raise OutOfBits("movement data without a movetype is not handled here")
        if r.flag():
            r.pos += r.int(14)  # shape data, skipped by its length
        if r.flag():
            self.chat = r.pstring().decode("latin1"); m |= CHAT
        if r.flag():
            r.pstring()
        if r.flag():
            for i in range(8):
                if r.flag():
                    self.attr[i] = r.pstring().decode("latin1")
            m |= ATTRS
        if r.flag():
            self.nickname = r.pstring().decode("latin1")
            self.nick_color = tuple(r.u8() for _ in range(4)); m |= NICK
        if r.flag():
            self.flags = r.int(16); m |= FLAGS
        return m


class Camera(GameObject):
    cls = "Camera"

    def write(self, w, mask):
        super().write(w, mask)
        w.flag(0)  # camera mode: left to the client's scripts
        w.flag(0)  # followed object: none


class Sun:
    cls = "Sun"

    def __init__(self, direction=(0.57735, 0.57735, -0.57735), color=(0.8, 0.8, 0.8, 1.0),
                 ambient=(0.3, 0.3, 0.35, 1.0)):
        self.direction, self.color, self.ambient = direction, color, ambient

    def full_mask(self):
        return 1

    def write(self, w, mask):
        w.flag(1)  # always the whole Sun
        w.pstring("Sun")
        for v in tuple(self.direction) + tuple(self.color) + tuple(self.ambient):
            w.f32(v)


class Sky:
    cls = "Sky"

    def __init__(self, textures="", distance=500.0, fog=(0.5, 0.6, 0.8), options=(1, 0, 0),
                 solid=(0.4, 0.6, 0.9)):
        self.textures, self.distance, self.fog = textures, distance, fog
        self.options, self.solid = options, solid

    def full_mask(self):
        return 1

    def write(self, w, mask):
        w.flag(1)
        w.pstring("Sky")
        w.flag(1)  # material list
        w.f32(self.distance)
        w.pstring(self.textures)  # six faces, comma separated
        for v in self.fog:
            w.f32(v)
        w.u32(0)  # no fog volumes
        w.u8(self.options[0])  # 1: draw the sky textures (else the solid colour)
        w.u8(self.options[1])  # 1: draw the bottom face
        for v in self.solid:
            w.f32(v)
        w.u8(self.options[2])  # no visible effect found
        w.flag(0)
        for _ in range(3):  # no cloud layers
            w.pstring("")
            w.f32(0)
            w.f32(0)
        for _ in range(3):  # wind
            w.f32(0)
        w.u32(0)
        w.flag(0)  # no storm fog
        for b in (0, 0, 1, 0, 0, 0, 0):  # the trailing guarded sections, as the stock writer leaves them
            w.flag(b)


class TerrainBlock:
    cls = "TerrainBlock"

    def __init__(self, square_size=8, repeat=False):
        self.square_size, self.repeat = square_size, repeat

    def full_mask(self):
        return 1

    def write(self, w, mask):
        w.flag(1)
        w.pstring("Terrain")
        w.u32(0)
        w.pstring("")
        w.pstring("")
        w.f32(1.0)
        w.f32(0.01)
        w.u32(8)
        w.u32(self.square_size)  # metres a square; the 256 x 256 grid is centred on 0,0
        w.u8(1 if self.repeat else 0)


# ---------------------------------------------------------------------------
# 6. Terrain chunks (terrain-512.md sections 2 and 3)
# ---------------------------------------------------------------------------

def _half(v):
    return int(v / 2)  # C division: truncates toward zero


class _Bits:
    def __init__(self):
        self.w = BitWriter()

    def int(self, v, n):
        self.w.int(v, n)


def encode_chunk(heights, materials):
    """One 16 x 16 chunk in the client's own (canonical) encoding.

    heights[y][x] are wire units (8 to a world unit); materials[y][x] are
    indices into heights.info. The client re-encodes every chunk it gets and
    stamps that, so a server that sends this form gets matching stamps back.
    """
    d = [[0] * 16 for _ in range(16)]
    for x in range(1, 16):
        d[0][x] = max(-127, min(127, heights[0][x] - heights[0][x - 1]))
    for y in range(1, 16):
        d[y][0] = max(-127, min(127, heights[y][0] - heights[y - 1][0]))
        for x in range(1, 16):
            pred = (heights[y - 1][x] + heights[y][x - 1]) // 2
            d[y][x] = max(-127, min(127, heights[y][x] - pred))
    for y in range(15, 0, -1):
        for x in range(15, 0, -1):
            d[y][x] = max(-127, min(127, d[y][x] - _half(d[y - 1][x] + d[y][x - 1])))
    b = _Bits()
    b.int(2, 8)                 # mode 2: hole flags at the end
    b.int(heights[0][0], 16)
    for row in d:
        for v in row:
            b.int(v & 0xFF, 8)
    ids = sorted({m & 31 for row in materials for m in row})
    b.int(len(ids), 6)
    for m in ids:
        b.int(m, 5)
    if len(ids) > 1:
        width = (len(ids) - 1).bit_length()
        for row in materials:
            for m in row:
                b.int(0, 1)  # no blend
                b.int(ids.index(m & 31), width)
    for _ in range(256):
        b.int(0, 1)  # no holes
    return b.w.bytes()


def decode_chunk(data):
    """Decodes chunk data exactly as the client does. Returns (heights, materials)."""
    r = BitReader(data + b"\0" * 8)
    r.int(8)
    base = r.int(16)
    d = [[struct.unpack("b", bytes([r.int(8)]))[0] for _ in range(16)] for _ in range(16)]
    h = [[0] * 16 for _ in range(16)]
    h[0][0] = base
    for x in range(1, 16):
        h[0][x] = (h[0][x - 1] + d[0][x]) & 0xFFFF
    for y in range(1, 16):
        h[y][0] = (h[y - 1][0] + d[y][0]) & 0xFFFF
        for x in range(1, 16):
            v = d[y][x] + _half(d[y - 1][x] + d[y][x - 1])
            d[y][x] = ((v + 128) & 0xFF) - 128
            h[y][x] = ((h[y - 1][x] + h[y][x - 1]) // 2 + d[y][x]) & 0xFFFF
    n = r.int(6)
    ids = [r.int(5) for _ in range(n)]
    mats = [[ids[0] if ids else 0] * 16 for _ in range(16)]
    if n > 1:
        width = (n - 1).bit_length()
        for y in range(16):
            for x in range(16):
                blend = r.flag()
                p = r.int(width)
                if blend:
                    r.int(width)
                    r.int(4)
                mats[y][x] = ids[p] if p < n else 0
    return h, mats


def settle_chunk(heights, materials):
    """Encodes, then re-encodes what the client would decode until it no
    longer changes: large steps are lossy, and the client stamps its own form."""
    data = encode_chunk(heights, materials)
    for _ in range(16):
        again = encode_chunk(*decode_chunk(data))
        if again == data:
            break
        data = again
    return data


def stamp(chunk_data):
    """The client's chunk stamp: CRC-32 with no final inversion."""
    return zlib.crc32(chunk_data) ^ 0xFFFFFFFF


def terrain_chunk_event(x, y, zdata, chunk_stamp):
    w = BitWriter()
    w.int(x, 4)
    w.int(y, 4)
    w.u32(chunk_stamp)
    w.int(len(zdata), 10)
    w.raw(zdata)
    return w


def make_demo_terrain(folder, square=8):
    """Rolling hills with a sea, as 256 chunk files plus heights.info."""
    os.makedirs(folder, exist_ok=True)
    for cy in range(16):
        for cx in range(16):
            hs, ms = [], []
            for y in range(16):
                hrow, mrow = [], []
                for x in range(16):
                    gx, gy = cx * 16 + x, cy * 16 + y
                    wx, wy = (gx - 128) * square, (gy - 128) * square
                    hill = 30 + 18 * math.sin(wx / 160) * math.cos(wy / 190) - wx * wy / 400000
                    z = max(0.0, hill)
                    hrow.append(int(z * 8))  # 8 wire units a world unit
                    mrow.append(0 if z < 6 else (1 if z < 9 else (2 if z < 40 else 3)))
                hs.append(hrow)
                ms.append(mrow)
            data = settle_chunk(hs, ms)
            with open(os.path.join(folder, "heights%d-%d.dat" % (cx, cy)), "wb") as f:
                f.write(zlib.compress(data, 9))
    with open(os.path.join(folder, "heights.info"), "w") as f:
        f.write("g3d_water.png\ng3d_sand.png\ng3d_grass.png\ng3d_rock.png\n")


def load_terrain(folder):
    """heights<x>-<y>.dat files -> {(x, y): (zlib bytes, stamp)}."""
    chunks = {}
    for y in range(16):
        for x in range(16):
            p = os.path.join(folder, "heights%d-%d.dat" % (x, y))
            if os.path.exists(p):
                z = open(p, "rb").read()
                if 0 < len(z) <= 1023:
                    chunks[(x, y)] = (z, stamp(zlib.decompress(z)))
    return chunks


# ---------------------------------------------------------------------------
# 7. The world file (a subset of seihai-gserver's graal3dworld.txt)
# ---------------------------------------------------------------------------

class World:
    def __init__(self):
        self.objects, self.sun, self.sky = [], None, None
        self.spawn, self.camera = (0.0, 0.0, 1.0), None
        self.playershape, self.terrain, self.terrain_block = "", {}, None

    @classmethod
    def load(cls, path):
        wd = cls()
        base = os.path.dirname(os.path.abspath(path))
        for n, line in enumerate(open(path, encoding="latin1"), 1):
            p = line.split("#", 1)[0].split()
            if not p:
                continue
            k, a = p[0], p[1:]
            try:
                if k == "object":
                    f = [float(v) for v in a[2:]]
                    o = GameObject(a[0], a[1], f[0:3], f[3:6] if len(f) >= 7 else (0, 0, 1),
                                   f[6] if len(f) >= 7 else 0.0)
                    o.flags = SOLID | COLLISION
                    wd.objects.append(o)
                elif k == "sun":
                    f = [float(v) for v in a]
                    wd.sun = Sun(tuple(f[0:3]), tuple(f[3:7]), tuple(f[7:11]))
                elif k == "sky":
                    s = Sky(a[0])
                    if len(a) > 1:
                        s.distance = float(a[1])
                    if len(a) > 4:
                        s.fog = tuple(float(v) for v in a[2:5])
                    wd.sky = s
                elif k == "spawn":
                    wd.spawn = tuple(float(v) for v in a[:3])
                elif k == "camera":
                    wd.camera = [float(v) for v in a]
                elif k == "playershape":
                    wd.playershape = a[0]
                elif k == "terrain":
                    wd.terrain = load_terrain(os.path.join(base, a[0]))
                    wd.terrain_block = TerrainBlock(int(a[1]) if len(a) > 1 else 8, "repeat" in a)
                else:
                    raise ValueError("unknown keyword")
            except (ValueError, IndexError) as e:
                print("world line %d not understood (%s): %s" % (n, e, line.strip()))
        return wd


# ---------------------------------------------------------------------------
# 8. One client's 3D link
# ---------------------------------------------------------------------------

PACKET_BITS = 400 * 8  # stay under the client's 450-byte packets
SEND_MS = 50


class Slot:
    def __init__(self, index, obj):
        self.index, self.obj = index, obj
        self.created = False      # the client has acked the create
        self.need_create = True
        self.dirty = 0
        self.kill = False


class Client:
    def __init__(self, server, addr, request):
        self.server, self.addr = server, addr
        self.sequence = request["sequence"]
        self.account = request["args"][0].decode("latin1")
        self.link = Link(self.sequence)
        self.events = Events()
        self.slots, self.by_obj, self.free = {}, {}, list(range(4095, -1, -1))
        self.packet_notes = {}
        self.last_heard = self.last_sent = time.monotonic()
        self.started = False          # the client's first data packet arrived
        self.phase = 0                # 1: phase 1 sent, 2: phase 1 acked, 3: phase 2 sent, 4: phase 2 acked
        self.phase1_acked_at = None
        self.terrain_answer = None    # event seqs of the chunks sent for the terrain request
        self.control_state = "none"   # none -> pending -> in flight -> delivered
        self.sky_resent = False

        w = server.world
        self.player = GameObject("G3DPlayer_" + self.account, w.playershape, w.spawn)
        self.player.nickname, self.player.flags = self.account, SOLID | COLLISION
        cx, cy, cz = (w.camera[:3] if w.camera else (0.0, -5.0, 2.0))
        at = (w.spawn[0] + cx, w.spawn[1] + cy, w.spawn[2] + cz)
        if w.camera and len(w.camera) >= 7:
            pose = (at, tuple(w.camera[3:6]), w.camera[6])
        else:
            pose = facing(at, w.spawn)
        self.camera = Camera("G3DCamera_" + self.account, "", *pose)

        # Ghost order matters on a big world: the client's own things first.
        if w.terrain_block:
            self.ghost(w.terrain_block)
        self.player_slot = self.ghost(self.player)
        self.camera_slot = self.ghost(self.camera)
        for o in (w.sun, w.sky):
            if o:
                self.ghost(o)
        for other in server.clients.values():
            if other is not self:
                self.ghost(other.player)
        for o in w.objects:
            self.ghost(o)

    # --- ghosts ---------------------------------------------------------
    def ghost(self, obj):
        if obj in self.by_obj or not self.free:
            return self.by_obj.get(obj)
        s = Slot(self.free.pop(), obj)
        self.slots[s.index] = s
        self.by_obj[obj] = s
        return s

    def unghost(self, obj):
        s = self.by_obj.pop(obj, None)
        if s:
            s.kill = True

    def mark(self, obj, mask):
        s = self.by_obj.get(obj)
        if s and not s.kill:
            s.dirty |= mask

    def write_ghosts(self, w, note):
        deletes = [s for s in self.slots.values() if s.kill]
        creates = [s for s in self.slots.values() if not s.kill and s.need_create]
        updates = [s for s in self.slots.values() if not s.kill and not s.need_create and s.created and s.dirty]
        picked, bits = [], len(w) + 1 + 4 + 1
        for kind, group in (("delete", deletes), ("create", creates), ("update", updates)):
            for s in sorted(group, key=lambda s: s.index):
                body = BitWriter()
                mask = ALL if kind == "create" else s.dirty
                if kind != "delete":
                    s.obj.write(body, s.obj.full_mask() if kind == "create" else mask)
                size = 2 + 12 + 1 + (0 if kind == "delete" else 26 + len(body))
                if picked and bits + size > PACKET_BITS:
                    break
                picked.append((kind, s, mask, body))
                bits += size
        if not w.flag(picked):
            return
        width = max(1, max(s.index for _, s, _, _ in picked).bit_length())
        w.int(width, 4)
        for kind, s, mask, body in picked:
            w.flag(1)
            w.int(s.index, width)
            if w.flag(kind == "delete"):
                note.append(("delete", s, 0))
                continue
            w.int(OBJ_ID[s.obj.cls], 12)
            w.int(len(body), 14)
            w.append(body)
            if kind == "create":
                s.need_create = False
                note.append(("create", s, 0))
            else:
                note.append(("update", s, s.dirty))
                s.dirty = 0
        w.flag(0)

    # --- receiving ------------------------------------------------------
    def receive(self, packet, now):
        try:
            ptype, notes, r = self.link.receive(packet)
        except ValueError:
            return
        self.last_heard = now
        for seq, delivered in notes:
            self.notify(seq, delivered)
        if ptype == PING:
            self.server.send(self.link.header(ACK).bytes(), self.addr)
        if r is None:
            return
        try:
            self.read_game_section(r)
            for name, er, end in self.events.read(r):
                self.on_event(name, er)
        except OutOfBits:
            print("%s: could not read a packet to its end" % self.account)
        if not self.started:
            self.started = True
            self.events.send("RemoteCommandEvent", remote_command("MissionStartPhase1"))
            self.phase = 1
            print("%s: MissionStartPhase1" % self.account)

    def read_game_section(self, r):
        r.flag()                                    # first person
        position = (r.f32(), r.f32(), r.f32())      # the control object's position
        if r.flag():
            r.int(12)                               # its ghost index
        changed = 0
        if r.flag():                                # the client's update of its own object
            mine = GameObject(self.player.name)
            mine.__dict__.update({k: v for k, v in self.player.__dict__.items()})
            changed = mine.read(r)
            if self.control_state == "delivered" and changed:
                for k in ("position", "axis", "angle", "chat", "shape", "nickname", "nick_color", "attr"):
                    setattr(self.player, k, getattr(mine, k))
        if r.flag():
            r.int(8)                                # field of view
        if self.control_state == "delivered":
            if position != (0.0, 0.0, 0.0) and position != self.player.position:
                self.player.position = position
                changed |= TRANSFORM
            if changed:
                self.server.relay(self, changed & (TRANSFORM | CHAT | SHAPE | NICK | ATTRS))

    def on_event(self, name, r):
        if name == "RemoteCommandEvent":
            args = read_remote_command(r, self.events.tags)
            cmd = args[0] if args else b""
            if cmd == b"MissionStartPhase1Ack" and self.phase == 1:
                self.phase, self.phase1_acked_at = 2, time.monotonic()
            elif cmd == b"MissionStartPhase2Ack" and self.phase == 3:
                self.phase = 4
                self.control_state = "pending"
            print("%s: %s" % (self.account, cmd.decode("latin1")))
        elif name == "NetStringEvent":
            self.events.tags[r.int(5)] = r.pstring()
        elif name == "TerrainRequestUpdatesEvent":
            have = [r.u32() for _ in range(256)]
            seqs = []
            for (x, y), (z, st) in sorted(self.server.world.terrain.items(), key=lambda e: (e[0][1], e[0][0])):
                if have[y * 16 + x] != st:
                    seqs.append(self.events.send("TerrainChunkEvent", terrain_chunk_event(x, y, z, st)))
            self.terrain_answer = seqs
            print("%s: terrain request, %d chunks to send" % (self.account, len(seqs)))
        elif name == "BigDataStartEvent":
            r.int(16)
            print("%s: text from the client (%s)" % (self.account, r.pstring().decode("latin1")))

    def notify(self, seq, delivered):
        self.events.notify(seq, delivered)
        for kind, s, mask in self.packet_notes.pop(seq, []):
            if kind == "control":
                self.control_state = "delivered" if delivered else "pending"
                if delivered:
                    print("%s: control object delivered (login step 5)" % self.account)
            elif delivered:
                if kind == "create":
                    s.created = True
                elif kind == "delete":
                    self.slots.pop(s.index, None)
                    self.free.append(s.index)
            elif kind == "create":
                s.need_create = True
            elif kind == "update":
                s.dirty |= mask

    # --- sending --------------------------------------------------------
    def lighting_ready(self):
        """Phase 2 lights the mission from what the client has by then, so hold
        it until the terrain, Sun and Sky creates and every terrain chunk are in."""
        lit = [s for s in self.slots.values() if s.obj.cls in ("TerrainBlock", "Sun", "Sky", "WaterBlock")]
        if not all(s.created for s in lit):
            return False
        if self.server.world.terrain_block:
            if self.terrain_answer is None:
                return False
            if not all(self.events.is_delivered(q) for q in self.terrain_answer):
                return False
        return True

    def tick(self, now):
        if self.phase == 2 and (self.lighting_ready() or now - self.phase1_acked_at > 15):
            self.events.send("RemoteCommandEvent", remote_command("MissionStartPhase2"))
            self.phase = 3
            print("%s: MissionStartPhase2" % self.account)
        if self.control_state == "delivered" and not self.sky_resent:
            # The client loads Sky textures only when it unpacks the Sky; by now they are downloaded.
            for s in self.slots.values():
                if s.obj.cls == "Sky":
                    s.dirty |= 1
            self.sky_resent = True
        busy = (self.events.to_send or self.control_state == "pending"
                or any(s.kill or s.need_create or (s.created and s.dirty) for s in self.slots.values()))
        due = now - self.last_sent >= (SEND_MS / 1000 if busy else 1.0)
        if not due or not self.started or self.link.window_full():
            return
        w = self.link.header(DATA)
        seq, note = self.link.last_send_seq, []
        # Server game section: the control object (once), then the camera.
        w.flag(1)
        if w.flag(self.control_state == "pending" and self.player_slot.created):
            w.u32(int((now - self.server.started) * 1000))
            w.int(self.player_slot.index, 12)
            GameObject("").write(w, 0)  # no sections: the ghost carries the state
            self.control_state = "in flight"
            note.append(("control", None, 0))
        if w.flag(self.camera_slot.created):
            w.int(self.camera_slot.index, 12)  # draw the view through this Camera
            w.flag(0)
        w.flag(0)  # field of view unchanged
        self.events.write(w, seq, PACKET_BITS - 16)  # a lone event may go over; the client takes it
        self.write_ghosts(w, note)
        self.packet_notes[seq] = note
        self.server.send(w.bytes(), self.addr)
        self.last_sent = now


# ---------------------------------------------------------------------------
# 9. The server: one UDP socket, many clients
# ---------------------------------------------------------------------------

class Server:
    def __init__(self, world, port, host="localhost"):
        self.world = world
        self.secret = os.urandom(16)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.clients = {}
        self.started = time.monotonic()

    def digest(self, addr):
        h = hmac.new(self.secret, ("%s:%d" % addr).encode(), hashlib.sha256).digest()
        return list(struct.unpack("<4I", h[:16]))

    def send(self, data, addr):
        self.sock.sendto(data, addr)

    def relay(self, sender, mask):
        for c in self.clients.values():
            if c is not sender:
                c.mark(sender.player, mask)

    def drop(self, addr, why):
        c = self.clients.pop(addr, None)
        if c:
            print("%s: link closed (%s)" % (c.account, why))
            for other in self.clients.values():
                other.unghost(c.player)

    def datagram(self, data, addr, now):
        if not data:
            return
        if data[0] & 1:  # a data-link packet
            c = self.clients.get(addr)
            if c:
                c.receive(data, now)
            return
        kind = data[0]
        if kind == CHALLENGE_REQUEST and len(data) >= 5:
            seq = struct.unpack("<I", data[1:5])[0]
            self.send(challenge_response(seq, self.digest(addr)), addr)
        elif kind == CONNECT_REQUEST:
            try:
                req = read_connect_request(data)
            except OutOfBits:
                return
            if not req or req["digest"] != self.digest(addr):
                return  # no work for an address that did not take a challenge
            c = self.clients.get(addr)
            if c and c.sequence == req["sequence"]:
                self.send(connect_accept(req["sequence"]), addr)  # our accept was lost
                return
            reason = None
            if req["class"] != b"GameConnection":
                reason = "CHR_INVALID"
            elif req["game"] != b"Graal3D":
                reason = "CHR_GAME"
            elif req["protocol"] != PROTOCOL:
                reason = "CHR_PROTOCOL"
            elif not req["args"] or not req["args"][0]:
                reason = "CR_INVALID_ARGS"
            if reason:
                self.send(connect_reject(req["sequence"], reason), addr)
                return
            self.drop(addr, "relinked")
            c = Client(self, addr, req)
            self.clients[addr] = c
            for other in self.clients.values():
                if other is not c:
                    other.ghost(c.player)
            self.send(connect_accept(req["sequence"]), addr)
            print("%s: linked from %s:%d (protocol 24)" % (c.account, addr[0], addr[1]))
        elif kind == DISCONNECT:
            self.drop(addr, "the client disconnected")

    def serve(self, seconds=None):
        end = None if seconds is None else time.monotonic() + seconds
        while end is None or time.monotonic() < end:
            now = time.monotonic()
            try:
                while True:
                    data, addr = self.sock.recvfrom(65536)
                    self.datagram(data, addr, now)
            except BlockingIOError:
                pass
            for addr, c in list(self.clients.items()):
                if now - c.last_heard > 30:
                    self.drop(addr, "timed out")
                else:
                    c.tick(now)
            time.sleep(0.005)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=14901, help="UDP port: the listed TCP port + 1")
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--world", help="a graal3dworld.txt-style file")
    ap.add_argument("--seconds", type=float, help="stop after this long")
    ap.add_argument("--make-terrain", metavar="DIR", help="write a demo terrain folder and exit")
    a = ap.parse_args(argv)
    if a.make_terrain:
        make_demo_terrain(a.make_terrain)
        print("wrote 256 chunks and heights.info to %s" % a.make_terrain)
        return 0
    world = World.load(a.world) if a.world else World()
    if not a.world:
        world.sun = Sun()
        world.sky = Sky("sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn")
        world.objects.append(GameObject("Cube", "redcube.3ds", (0, 4, 1)))
    print("g3dmini: UDP %s:%d, %d objects, %d terrain chunks"
          % (a.host, a.port, len(world.objects), len(world.terrain)))
    Server(world, a.port, a.host).serve(a.seconds)
    return 0


if __name__ == "__main__":
    sys.exit(main())
