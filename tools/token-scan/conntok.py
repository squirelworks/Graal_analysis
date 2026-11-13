# conntok.py: static login-token read for Graal Linux clients 3.x to 6.01 (ELF32 and ELF64, non-PIE).
# Method: the token is built in the game-connection connect routine, which references the string
# "Connecting to the game server...". From each code reference to that string it reads the next
# 3000 bytes and collects, in order, every 4-byte absolute immediate (and on x64 every RIP-relative
# lea) that points at a one-character NUL-terminated string. The first 8 characters are the token
# (the routine appends "G","3","D",digits one string at a time). Both reference sites normally give
# the same 8 characters; anything after the 8th is unrelated.
# Validated against wire-captured tokens: Linux 4.04r2 -> G3D19026, 4.20r6 -> G3D22126,
# 4.20r8 (2007-01-17) -> G3D22126, 6.01r1 x86 -> G3D0108A, 6.01r1 x64 -> G3D0108A;
# and against listed tokens 3.0 -> G3D16053, 3.01 -> G3D27063 (UPX-packed 3.x: run upx -d first).
# Does not cover 6.03+ (one scrambled string; see the decode in login-tokens-3x-7x.md) or PE files.
import sys, struct, re

def load(p):
    d = open(p, 'rb').read()
    if d[:4] != b'\x7fELF': return d, None
    cls = d[4]; segs = []
    if cls == 1:
        phoff, = struct.unpack('<I', d[28:32]); phentsize, phnum = struct.unpack('<HH', d[42:46])
        for i in range(phnum):
            o = phoff + i * phentsize
            t, off, va, pa, fsz, msz = struct.unpack('<IIIIII', d[o:o + 24])
            if t == 1: segs.append((va, off, fsz))
    else:
        phoff, = struct.unpack('<Q', d[32:40]); phentsize, phnum = struct.unpack('<HH', d[54:58])
        for i in range(phnum):
            o = phoff + i * phentsize
            t, fl, off, va, pa, fsz, msz = struct.unpack('<IIQQQQQ', d[o:o + 48])
            if t == 1: segs.append((va, off, fsz))
    return d, (cls, segs)

def v2o(segs, va):
    for v, o, s in segs:
        if v <= va < v + s: return o + va - v
    return None

def o2v(segs, off):
    for v, o, s in segs:
        if o <= off < o + s: return v + off - o
    return None

def onechar(d, segs, va):
    o = v2o(segs, va)
    if o is None or o + 2 > len(d): return None
    if d[o + 1] == 0 and 0x20 < d[o] < 0x7f: return chr(d[o])
    return None

def run(p):
    d, info = load(p)
    if not info: return 'not ELF'
    cls, segs = info
    res = []
    for m in re.finditer(re.escape(b'Connecting to the game server'), d):
        va = o2v(segs, m.start())
        if va is None: continue
        refs = [x.start() for x in re.finditer(re.escape(struct.pack('<I', va)), d)]
        if cls == 2:
            for x in re.finditer(rb'\x48\x8d[\x05\x0d\x15\x1d\x35\x3d]|\x4c\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]', d):
                off = x.start(); disp, = struct.unpack('<i', d[off + 3:off + 7])
                ip = o2v(segs, off + 7)
                if ip is not None and ip + disp == va: refs.append(off)
        for r in refs:
            win = d[r:r + 3000]; chars = []
            for k in range(len(win) - 4):
                val, = struct.unpack('<I', win[k:k + 4])
                c = onechar(d, segs, val)
                if c: chars.append((k, c))
            if cls == 2:
                for k in range(len(win) - 7):
                    if win[k] in (0x48, 0x4c) and win[k + 1] == 0x8d and (win[k + 2] & 0xc7) == 0x05:
                        disp, = struct.unpack('<i', win[k + 3:k + 7])
                        ip = o2v(segs, r + k + 7)
                        if ip is None: continue
                        c = onechar(d, segs, ip + disp)
                        if c: chars.append((k, c))
            chars.sort()
            res.append((hex(r), ''.join(c for _, c in chars[:12])))
    return res

for p in sys.argv[1:]:
    print(p, run(p))
