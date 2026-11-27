"""Checks g3dmini against the published wire vectors (torque/udp-session.md
sections 3 and 8, torque/terrain-512.md) and runs one loopback login.

    python3 -m pytest graal3d/examples/g3dmini -q
"""
import os
import socket
import sys
import threading
import time
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3dmini as g  # noqa: E402

CONNECT_REQUEST = bytes.fromhex(
    "2000040000000102030405060708090a0b0c0d0e0f1d6213fd6a4af4185809000000e0ffffffff41ac650e47670c"
    "0000000c00008008d1e976dc8548169b000000c082de7f0300")
FULL_ACCEPT = bytes.fromhex(
    "24000400000100001aac96e82d0340006470ae5022c6b196ad05000168e15ca1448c632d5bebfa7a304e500b0003d0c2b94289184fe7acbfebebc138"
    "412d00104085d844bfe26ef1180240011c984e2a01c0000e4c3d058003c8b07eb3648a188a270100012a3838e12d62289e048004a8b039997a92e77e"
    "860100002322b8774ec8d5664f93b8f404032000464470ef9c90534883b8f4040340005aaca6448f81955cdf5af61f979e60000c408bd8591b748e22"
    "2b6dc5dde231c4a527180004d0c1ed610ac6d4c7a52718000550a2eb91c2afa6082585b8f40403c0004a747d64f3dfa0eb8766884b4f30000e60c4fa"
    "cd9269b5d9d3242e3dc10040801aeb374ba6ae8f6cfe1bc8b10e09dfe2d213c000000000")
GAMEOBJECT = bytes.fromhex(
    "6d887574de1b5979938ddce9c2c81df6bb2f1d431300000000000000000000f00700000000000000000000f00700000000e8c0c8ddffffff7f2400")
SUN = bytes.fromhex(
    "1d987ab2699ef8b1699ef8b1699ef86d6666fa696666fa696666fa010000fcd1ccccf4d1ccccf4999999f5010000fc01")
SKY = bytes.fromhex(
    "1d984e2a0100f4874c69938a6cb368b749456610ed36a9c8769368b7494536b668b74945e6eb68b7494516080000e0473333e3a79999e90700000020"
    "00a09999d9473333e3c7ccccec0700000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000")
FIRST_CLIENT_PACKET = bytes.fromhex("0500000441b800000000000000000000000000")


def bits_of(obj, mask=None):
    w = g.BitWriter()
    obj.write(w, obj.full_mask() if mask is None else mask)
    return w


def test_connect_request_decodes():
    req = g.read_connect_request(CONNECT_REQUEST)
    assert req["sequence"] == 0x400
    assert req["digest"] == list(g.struct.unpack("<4I", bytes(range(16))))
    assert req["class"] == b"GameConnection" and req["game"] == b"Graal3D"
    assert req["group"] == 0 and req["crc"] == 0xFFFFFFFF
    assert (req["protocol"], req["min_protocol"]) == (24, 24)
    assert req["args"] == [b"guest", b""]


def test_full_accept_matches_vector():
    assert g.connect_accept(0x400) == FULL_ACCEPT
    assert len(FULL_ACCEPT) == 276


def test_gameobject_create_matches_vector():
    o = g.GameObject("G3DPlayer_lab", "labcube.3ds", (0, 0, 1))
    o.nickname, o.flags = "lab", g.SOLID | g.COLLISION
    w = bits_of(o)
    assert len(w) == 471 and w.bytes() == GAMEOBJECT
    assert len(bits_of(g.GameObject(""), 0)) == 13  # the empty update


def test_sun_matches_vector():
    w = bits_of(g.Sun())
    assert len(w) == 379 and w.bytes() == SUN


def test_sky_matches_vector():
    w = bits_of(g.Sky("sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn"))
    assert len(w) == 956 and w.bytes() == SKY


def test_gameobject_reads_back():
    o = g.GameObject("Thing", "a.dts", (1.5, -2, 3), (0, 0, 1), 0.5)
    o.chat, o.nickname, o.flags = "hi", "nick", g.SOLID
    o.attr[2] = "x"
    back = g.GameObject("")
    m = back.read(g.BitReader(bits_of(o).bytes()))
    assert m == o.full_mask()
    assert (back.name, back.shape, back.chat, back.nickname) == ("Thing", "a.dts", "hi", "nick")
    assert back.position == (1.5, -2.0, 3.0) and abs(back.angle - 0.5) < 1e-6 and back.attr[2] == "x"


def test_link_reads_first_client_packet():
    link = g.Link(0x400)
    ptype, notes, body = link.receive(FIRST_CLIENT_PACKET)
    assert ptype == g.DATA and notes == [] and body is not None
    assert link.last_seq_received == 1
    # Our next data packet acks it: seq 1, highest received 1, one ack byte with bit 0.
    w = link.header(g.DATA)
    r = g.BitReader(w.bytes())
    assert r.flag() == 1 and r.int(1) == 0 and r.int(9) == 1 and r.int(9) == 1
    assert r.int(2) == g.DATA and r.int(3) == 1 and r.int(8) == 1


def test_remote_command_round_trip():
    w = g.remote_command("MissionStartPhase1Ack", 7, -300)
    assert g.read_remote_command(g.BitReader(w.bytes()), {}) == [b"MissionStartPhase1Ack", 7, -300]


def test_crc_and_stamp():
    check = int("cbf43926", 16)  # the standard CRC-32 check value of "123456789"
    assert zlib.crc32(b"123456789") == check
    assert g.stamp(b"123456789") == check ^ 0xFFFFFFFF


def test_chunk_round_trip_and_settling():
    flat = [[800] * 16 for _ in range(16)]
    mats = [[(x // 4) % 3 for x in range(16)] for _ in range(16)]
    h, m = g.decode_chunk(g.encode_chunk(flat, mats))
    assert h == flat and m == mats
    # A gentle slope survives exactly.
    slope = [[400 + 3 * x + 2 * y for x in range(16)] for y in range(16)]
    assert g.decode_chunk(g.encode_chunk(slope, mats))[0] == slope
    # A cliff does not, but the settled form is a fixed point of the client's re-encode.
    cliff = [[0 if x < 8 else 4000 for x in range(16)] for _ in range(16)]
    data = g.settle_chunk(cliff, mats)
    assert g.encode_chunk(*g.decode_chunk(data)) == data
    assert len(zlib.compress(data, 9)) <= 1023


def test_demo_terrain(tmp_path):
    g.make_demo_terrain(str(tmp_path))
    chunks = g.load_terrain(str(tmp_path))
    assert len(chunks) == 256
    names = (tmp_path / "heights.info").read_text().split()
    assert names == ["g3d_water.png", "g3d_sand.png", "g3d_grass.png", "g3d_rock.png"]


# --- a loopback login with a small scripted client --------------------------

class ScriptedClient:
    """Plays the 5.12's part far enough to reach login step 6: handshake,
    acks, the two mission phases, a terrain request with empty stamps."""

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.2)
        self.addr = ("localhost", port)
        self.link = g.Link(0x400)
        self.events = g.Events()
        self.ghosts = {}
        self.commands = []
        self.chunks = 0
        self.control = self.camera = None

    def handshake(self):
        self.sock.sendto(bytes([0x1A, 0, 4, 0, 0]), self.addr)
        data, _ = self.sock.recvfrom(2048)
        assert data[0] == 0x1E
        digest = list(g.struct.unpack("<4I", data[5:21]))
        w = g.BitWriter()
        w.u8(0x20); w.u32(0x400)
        for d in digest:
            w.u32(d)
        w.string("GameConnection"); w.u32(0); w.u32(0xFFFFFFFF); w.string("Graal3D")
        w.u32(24); w.u32(24); w.string("pw"); w.u32(2); w.string("tester"); w.string("Tester")
        self.sock.sendto(w.bytes(), self.addr)
        data, _ = self.sock.recvfrom(2048)
        assert data == g.connect_accept(0x400)

    def send(self):
        w = self.link.header(g.DATA)
        w.flag(0)
        for _ in range(3):
            w.f32(0)
        w.flag(0); w.flag(0); w.flag(0)
        self.events.write(w, self.link.last_send_seq, 3000)
        self.sock.sendto(w.bytes(), self.addr)

    def read(self, data):
        ptype, notes, r = self.link.receive(data)
        for seq, ok in notes:
            self.events.notify(seq, ok)
        if r is None:
            return
        if r.flag():  # server game section
            if r.flag():
                r.u32()
                self.control = r.int(12)
                g.GameObject("").read(r)
            if r.flag():
                self.camera = r.int(12)
                r.flag()
            if r.flag():
                r.int(8)
        for name, er, end in self.events.read(r):
            if name == "RemoteCommandEvent":
                cmd = g.read_remote_command(er, self.events.tags)[0]
                self.commands.append(cmd)
                if cmd == b"MissionStartPhase1":
                    self.events.send("TerrainRequestUpdatesEvent", self.zero_stamps())
                self.events.send("RemoteCommandEvent", g.remote_command(cmd.decode() + "Ack"))
            elif name == "TerrainChunkEvent":
                self.chunks += 1
        if r.flag():  # ghosts
            width = r.int(4)
            while r.flag():
                idx = r.int(width)
                if r.flag():
                    self.ghosts.pop(idx, None)
                    continue
                cls, length = r.int(12), r.int(14)
                self.ghosts[idx] = g.OBJECT_CLASSES[cls]
                r.pos += length

    @staticmethod
    def zero_stamps():
        w = g.BitWriter()
        for _ in range(256):
            w.u32(0)
        return w

    def step(self):
        try:
            while True:
                data, _ = self.sock.recvfrom(4096)
                self.read(data)
        except socket.timeout:
            pass
        self.send()


def test_loopback_login(tmp_path):
    folder = tmp_path / "terrain"
    g.make_demo_terrain(str(folder))
    world_file = tmp_path / "world.txt"
    world_file.write_text("sun 0.5 0.5 -0.7 0.9 0.9 0.8 1 0.3 0.3 0.35 1\n"
                          "sky sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn 600\n"
                          "terrain terrain 8\nspawn 0 0 40\nobject Tower tower.dts 10 10 30 0 0 1 0.785398\n")
    world = g.World.load(str(world_file))
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    probe.bind(("localhost", 0))
    port = probe.getsockname()[1]
    probe.close()
    server = g.Server(world, port)
    t = threading.Thread(target=server.serve, args=(20,), daemon=True)
    t.start()
    c = ScriptedClient(port)
    c.handshake()
    end = time.monotonic() + 15
    while time.monotonic() < end and not (c.control is not None and c.camera is not None
                                           and b"MissionStartPhase2" in c.commands):
        c.step()
    assert c.commands[:2] == [b"MissionStartPhase1", b"MissionStartPhase2"]
    assert c.chunks == 256
    assert sorted(c.ghosts.values()) == sorted(
        ["TerrainBlock", "GameObject", "Camera", "Sun", "Sky", "GameObject"])
    assert c.ghosts[c.control] == "GameObject" and c.ghosts[c.camera] == "Camera"
