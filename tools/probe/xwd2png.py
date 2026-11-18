#!/usr/bin/env python3
"""Convert an xwd dump (ZPixmap, 24/32 bpp TrueColor, as written by `xwd -silent`) to PNG. No scaling."""
import struct, sys, zlib
d = open(sys.argv[1], 'rb').read()
h = struct.unpack('>25I', d[:100])
hsize, ver, fmt, depth, w, ht = h[0], h[1], h[2], h[3], h[4], h[5]
order, bpp, bpl, ncolors = h[7], h[11], h[12], h[19]
rmask, gmask, bmask = h[14], h[15], h[16]
off = hsize + ncolors * 12
px = d[off:off + bpl * ht]
assert bpp == 32, bpp
rows = []
for y in range(ht):
    row = px[y * bpl: y * bpl + w * 4]
    out = bytearray(b'\0')
    for x in range(w):
        v = struct.unpack('<I' if order == 0 else '>I', row[4 * x:4 * x + 4])[0]
        out += bytes(((v & rmask) >> 16, (v & gmask) >> 8, v & bmask))
    rows.append(bytes(out))
def chunk(t, b): return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, ht, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b'')
open(sys.argv[2], 'wb').write(png)
print(w, ht)
