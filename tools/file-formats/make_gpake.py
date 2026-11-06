#!/usr/bin/env python3
"""Build an encrypted Graal .gpake package and the PLO 104 packet that carries its key.

Format (read from the 4.20r8 and 6.03r7 clients; see formats/gpak.md):
  * the ZIP itself is plain; only each entry's *uncompressed* contents are encrypted
  * DES-ECB with an 8-byte key, full 8-byte blocks only
  * a tail shorter than 8 bytes stays plaintext, no padding (ZIP size == real size)
The client decrypts with its own build of libtomcrypt DES, which is NOT textbook DES:
it reads every key byte with its bits reversed (bit 0 <-> bit 7, and so on). Found by
running the 6.03r7 client's own DES routines in an emulator: it equals standard DES with
each key byte bit-reversed (200/200 random key/block pairs). So the key sent in PLO 104
is the "Graal key"; the standard-DES key we encrypt with is graal_des_key(that key).

Usage:
  make_gpake.py --sample OUTDIR [--key HEX16]
        writes sample.gpake, plo104_sample.gpake.bin and plo104_sample.gpake.hex
  make_gpake.py OUT.gpake --key HEX16 FILE[=NAME_IN_PACKAGE] ...
  make_gpake.py --decrypt IN.gpake --key HEX16 OUTDIR     (round-trip helper)
  make_gpake.py --selftest

Needs pycryptodome (pip install pycryptodome).
"""
import os, sys, struct, zipfile

from Crypto.Cipher import DES

import make_gpak  # same folder: limits and the two sample files

SAMPLE_KEY = bytes.fromhex("133457799BBCDFF1")   # the textbook DES test key


# ---------------------------------------------------------------- DES layer
def graal_des_key(key):
    """Standard-DES key equivalent to the client's DES with this PLO 104 key."""
    return bytes(int(f"{b:08b}"[::-1], 2) for b in key)


def _blocks(data, key, encrypt):
    n = len(data) & ~7                       # full blocks only
    c = DES.new(graal_des_key(key), DES.MODE_ECB)
    body = (c.encrypt if encrypt else c.decrypt)(data[:n])
    return body + data[n:]                   # short tail left as is


def encrypt_entry(data, key):
    return _blocks(data, key, True)


def decrypt_entry(data, key):
    return _blocks(data, key, False)


# ---------------------------------------------------------------- package
def build(out, entries, key):
    if len(key) != 8:
        raise SystemExit("key must be 8 bytes (16 hex digits)")
    enc = [(name, encrypt_entry(data, key)) for name, data in entries]
    make_gpak.build(out, enc)                # same plain ZIP writer as .gpak


def unpack(path, key):
    with zipfile.ZipFile(path) as z:
        return [(i.filename, decrypt_entry(z.read(i), key)) for i in z.infolist()]


# ---------------------------------------------------------------- PLO 104
def gint5(v):
    v &= 0xFFFFFFFF
    return bytes(((v >> s) & 0x7F) + 32 for s in (28, 21, 14, 7, 0))


def plo104(filename, key, a=1):
    """{GCHAR 104}{GSTRING filename}{GCHAR a}{GINT5 lo}{GINT5 hi}, without the line end."""
    name = os.path.basename(filename).lower().encode("latin-1")
    if len(name) > 223:
        raise SystemExit("file name too long for a GSTRING")
    lo, hi = struct.unpack("<II", key)
    return bytes([104 + 32, len(name) + 32]) + name + bytes([a + 32]) + gint5(lo) + gint5(hi)


def parse_plo104(pkt):
    """Inverse of plo104(), the way the client reads it. Returns (name, a, key)."""
    assert pkt[0] == 104 + 32
    n = pkt[1] - 32
    name = pkt[2:2 + n].decode("latin-1")
    p = 2 + n
    a = pkt[p] - 32
    def g5(b):
        v = 0
        for c in b:
            v = (v << 7) | (c - 32)
        return v & 0xFFFFFFFF
    lo, hi = g5(pkt[p + 1:p + 6]), g5(pkt[p + 6:p + 11])
    return name, a, struct.pack("<II", lo, hi)


def hexdump(b):
    out = []
    for off in range(0, len(b), 16):
        row = b[off:off + 16]
        out.append(f"{off:08x}  {row.hex(' '):<47}  "
                   + "".join(chr(c) if 32 <= c < 127 else "." for c in row))
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- tests
def selftest():
    # FIPS 46 / Stallings worked example
    k = bytes.fromhex("133457799BBCDFF1")
    ct = DES.new(k, DES.MODE_ECB).encrypt(bytes.fromhex("0123456789ABCDEF"))
    assert ct.hex().upper() == "85E813540F0AB405", ct.hex()
    print("DES test vector 133457799BBCDFF1 / 0123456789ABCDEF -> 85E813540F0AB405: OK")
    # Graal DES: same vector as computed by the 6.03r7 client's own routine (emulated)
    assert encrypt_entry(bytes.fromhex("0123456789ABCDEF"), k).hex().upper() == "CEE55ACD2386B23F"
    assert encrypt_entry(bytes.fromhex("0123456789ABCDEF"), bytes(8)).hex().upper() == "617B3A0CE8F07100"
    print("Graal DES (bit-reversed key bytes) matches the 6.03r7 client's output: OK")
    # tail handling: lengths 0..17 round-trip, tail stays plaintext
    for n in range(18):
        d = bytes(range(n))
        e = encrypt_entry(d, k)
        assert len(e) == n and decrypt_entry(e, k) == d
        assert e[n & ~7:] == d[n & ~7:]
    print("tail handling (0..17 bytes): OK")
    # GINT5 / PLO 104 round trip
    for key in (k, b"\x00" * 8, b"\xff" * 8):
        assert parse_plo104(plo104("X.gpake", key))[2] == key
    print("PLO 104 encode/decode: OK")


def main(argv):
    key = SAMPLE_KEY
    if "--key" in argv:
        i = argv.index("--key")
        key = bytes.fromhex(argv[i + 1])
        del argv[i:i + 2]
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) == 3 and argv[0] == "--decrypt":
        os.makedirs(argv[2], exist_ok=True)
        for name, data in unpack(argv[1], key):
            p = os.path.join(argv[2], name)
            os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
            open(p, "wb").write(data)
            print(f"{name}: {len(data)} bytes")
        return
    if len(argv) == 2 and argv[0] == "--sample":
        d = argv[1]
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, "sample.gpake")
        entries = make_gpak.sample_entries()
        build(out, entries, key)
        assert unpack(out, key) == [(n.lower(), b) for n, b in entries], "round trip failed"
        pkt = plo104("sample.gpake", key)
        assert parse_plo104(pkt) == ("sample.gpake", 1, key)
        open(os.path.join(d, "plo104_sample.gpake.bin"), "wb").write(pkt + b"\n")
        with open(os.path.join(d, "plo104_sample.gpake.hex"), "w") as f:
            lo, hi = struct.unpack("<II", key)
            f.write(f"# PLO 104 for sample.gpake, key {key.hex().upper()}, a=1\n"
                    f"# lo=0x{lo:08X} hi=0x{hi:08X}; .bin adds the trailing 0x0a line end\n")
            f.write(hexdump(pkt + b"\n"))
        print(f"wrote {out} with key {key.hex().upper()}; round trip OK")
        return
    if len(argv) < 2:
        raise SystemExit(__doc__)
    entries = []
    for spec in argv[1:]:
        path, _, name = spec.partition("=")
        entries.append((name or os.path.basename(path), open(path, "rb").read()))
    build(argv[0], entries, key)


if __name__ == "__main__":
    main(sys.argv[1:])
