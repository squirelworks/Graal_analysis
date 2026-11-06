#!/usr/bin/env python3
"""Build a plain (unencrypted) Graal .gpak package.

A .gpak is an ordinary ZIP archive (stored or deflate entries, no ZIP password),
as read by the 4.20r8 and 6.03r7 clients through minizip. See formats/gpak.md.

Usage: make_gpak.py OUT.gpak FILE[=NAME_IN_PACKAGE] ...
       make_gpak.py --sample OUTDIR      (writes sample.gpak and sample.zip with two test files)
"""
import sys, os, zipfile, zlib, struct

MAX_ENTRIES = 10000          # client reads at most 10000 entries
MAX_ENTRY_SIZE = 20 * 1024 * 1024  # entries over 20 MiB (uncompressed) are skipped
MAX_NAME = 255               # client's entry-name buffer is 256 bytes


def build(out, entries):
    if len(entries) > MAX_ENTRIES:
        raise SystemExit("too many entries for the client")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries:
            name = name.replace("\\", "/").lower()
            if len(name.encode()) > MAX_NAME or len(data) > MAX_ENTRY_SIZE:
                raise SystemExit(f"{name}: too long a name or too big for the client")
            z.writestr(name, data)


def tiny_png(w=16, h=16):
    rows = b"".join(b"\x00" + b"".join(bytes((x * 16, y * 16, 160, 255)) for x in range(w))
                    for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def sample_entries():
    txt = (b"This file came out of sample.gpak.\r\n"
           b"If the client can read it, the package was opened.\r\n")
    return [("gpaksample_note.txt", txt), ("gpaksample_tile.png", tiny_png())]


def main(argv):
    if len(argv) == 2 and argv[0] == "--sample":
        os.makedirs(argv[1], exist_ok=True)
        e = sample_entries()
        build(os.path.join(argv[1], "sample.gpak"), e)
        build(os.path.join(argv[1], "sample.zip"), e)   # same bytes; 4.20r8 takes .zip
        return
    if len(argv) < 2:
        raise SystemExit(__doc__)
    entries = []
    for spec in argv[1:]:
        path, _, name = spec.partition("=")
        entries.append((name or os.path.basename(path), open(path, "rb").read()))
    build(argv[0], entries)


if __name__ == "__main__":
    main(sys.argv[1:])
