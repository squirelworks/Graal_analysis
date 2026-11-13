#!/usr/bin/env python3
"""Decode or encode the GANIs that Android Graal Classic 1.8 ships encrypted.

usage: classicgani.py decode|encode FILE [-o OUT] [--name NAME]

The 1.8 package's GANIs are the 1.7 plain text run through the client's resource
cipher. The key depends only on the file's base name:

- start from the fixed eight bytes in SEED;
- lower-case the base name; for step i from 0 to len-1, take character i-1
  (step 0 takes a zero byte, because the client's string type counts from 1)
  and XOR byte (i mod 8) of the key with (char - 97*i) mod 256;
- run DES-ECB with that key over every whole 8-byte block. The DES is the
  2.05 one in graaldes.py (each key byte bit-reversed). A tail shorter than
  eight bytes is left as it is, so the file keeps its length.

The client applies this to any `.gani` it loads as a resource. Round trip:
all 47 GANIs that 1.7 and 1.8 share decode to the 1.7 bytes, and the 1.7
bytes encode back to the 1.8 bytes. See client-internals/android-classic.md.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graaldes import GraalDES

SEED = bytes([0x45, 0xCE, 0x4A, 0x0C, 0x24, 0x89, 0x1B, 0x07])


def file_key(name):
    """The 8-byte key for one file, before graaldes reverses its bits."""
    base = name.replace('\\', '/').rsplit('/', 1)[-1].lower().encode('latin1')
    key = bytearray(SEED)
    for i in range(len(base)):
        c = base[i - 1] if i > 0 else 0
        key[i & 7] ^= (c - 97 * i) & 0xFF
    return bytes(key)


def _run(name, data, encrypt):
    des = GraalDES(file_key(name))
    whole = len(data) & ~7
    head = des.encrypt(data[:whole]) if encrypt else des.decrypt(data[:whole])
    return head + data[whole:]


def decode(name, data):
    return _run(name, bytes(data), False)


def encode(name, data):
    return _run(name, bytes(data), True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('mode', choices=['decode', 'encode'])
    ap.add_argument('file')
    ap.add_argument('-o', '--out', help='output file (default: stdout)')
    ap.add_argument('--name', help='name the key is made from (default: the file name)')
    a = ap.parse_args(argv)
    data = open(a.file, 'rb').read()
    name = a.name or os.path.basename(a.file)
    out = (decode if a.mode == 'decode' else encode)(name, data)
    if a.out:
        open(a.out, 'wb').write(out)
    else:
        sys.stdout.buffer.write(out)


if __name__ == '__main__':
    main()
