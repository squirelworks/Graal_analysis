# machotok.py: static login-token read for Graal Mac OS X clients (Mach-O, thin or universal).
# Method (same as conntok.py for ELF): the game-connection connect routine references the string
# "Connecting to the game server"; right after it the token is appended one character at a time
# from one-character NUL-terminated strings. The script finds code that materialises the string's
# address, then lists the next one-character strings referenced in the following 3000 bytes.
#   PPC: linear symbolic scan of lis/addis/addi/ori, the bcl 20,31 + mflr PIC base, mr, and lwz
#        through globals (pointer-to-string). Every computed value is tested.
#   i386: absolute 32-bit operands (PIC builds give no hit). x86_64: RIP-relative lea.
#   If no 8-char result, it also tries the 6.03 scramble (NOT b, -10-n, ror 2, -i; g3d0511c is 50 1d 54 21 09 15 11 44).
# Take the first 8 characters of the result.
# Validated against wire-captured Mac tokens: 4.04r2 PPC -> G3D18026, 5.12 PPC -> G3D15097,
# the 2006-09-19 PPC build (archive label "4.20r6") -> G3D27076.
# Limits: on the 6.x universal binaries the PPC slice reads out of order (same characters) and the
# i386 slice gives nothing; use the x86_64 slice.
import sys, struct, re

NEEDLE = b'Connecting to the game server'
M32 = (1 << 32) - 1
BL_MASK = (0x3F << 26) | 3          # opcode bits and AA/LK of a branch
BL_LINK = (18 << 26) | 1            # "bl" (branch and link)
BCL_20_31 = (16 << 26) | (20 << 21) | (31 << 16) | 5   # bcl 20,31,$+4


def slices(d):
    if d[:4] == b'\xca\xfe\xba\xbe':
        n, = struct.unpack('>I', d[4:8]); out = []
        for i in range(n):
            ct, cs, off, size, al = struct.unpack('>iiIII', d[8 + 20 * i:28 + 20 * i])
            out.append((ct, d[off:off + size]))
        return out
    return [(None, d)]


def parse(b):
    mg = b[:4]
    if mg == b'\xfe\xed\xfa\xce': e, bits = '>', 32
    elif mg == b'\xce\xfa\xed\xfe': e, bits = '<', 32
    elif mg == b'\xcf\xfa\xed\xfe': e, bits = '<', 64
    else: return None
    cpu, = struct.unpack(e + 'i', b[4:8]); ncmds, = struct.unpack(e + 'I', b[16:20])
    o = 28 if bits == 32 else 32; segs = []
    for _ in range(ncmds):
        cmd, sz = struct.unpack(e + 'II', b[o:o + 8])
        if cmd == 1:
            va, vs, fo, fs = struct.unpack(e + 'IIII', b[o + 24:o + 40]); segs.append((va, fo, fs))
        elif cmd == 25:
            va, vs, fo, fs = struct.unpack(e + 'QQQQ', b[o + 24:o + 56]); segs.append((va, fo, fs))
        o += sz
    return e, bits, cpu, segs


def v2o(segs, va):
    for v, o, s in segs:
        if s and v <= va < v + s: return o + va - v
    return None


def o2v(segs, off):
    for v, o, s in segs:
        if s and o <= off < o + s: return v + off - o
    return None


def onechar(b, segs, va):
    o = v2o(segs, va)
    if o is None or o + 2 > len(b): return None
    return chr(b[o]) if b[o + 1] == 0 and 0x20 < b[o] < 0x7f else None


def sext16(x): return x - 0x10000 if x & 0x8000 else x


def ppc_values(b, segs, start, end):
    reg = {}; out = []; lastbcl = None
    for off in range(start, min(end, len(b) - 3), 4):
        w, = struct.unpack('>I', b[off:off + 4]); op = w >> 26
        rd = (w >> 21) & 31; ra = (w >> 16) & 31; imm = w & 0xffff
        pc = o2v(segs, off)
        if w & BL_MASK == BL_LINK and (w & (M32 >> 6) & ~3) == 4:
            lastbcl = pc + 4; continue
        if w == BCL_20_31: lastbcl = pc + 4; continue
        if op == 31 and ((w >> 1) & 0x3ff) == 339 and ((w >> 11) & 0x3ff) == 0x100:
            if lastbcl is not None: reg[rd] = lastbcl
            continue
        if op == 15:
            base = 0 if ra == 0 else reg.get(ra)
            if base is None: reg.pop(rd, None); continue
            reg[rd] = (base + (imm << 16)) & M32; continue
        if op == 14:
            base = 0 if ra == 0 else reg.get(ra)
            if base is None: reg.pop(rd, None); continue
            v = (base + sext16(imm)) & M32; reg[rd] = v; out.append((off, v)); continue
        if op == 24:
            if rd in reg: v = reg[rd] | imm; reg[ra] = v; out.append((off, v))
            continue
        if op == 32:
            if ra in reg:
                a = (reg[ra] + sext16(imm)) & M32; out.append((off, a))
                o = v2o(segs, a)
                if o is not None and o + 4 <= len(b):
                    reg[rd], = struct.unpack('>I', b[o:o + 4]); out.append((off, reg[rd]))
                else: reg.pop(rd, None)
            else: reg.pop(rd, None)
            continue
        if op == 18 and (w & 1): lastbcl = None
        if op == 31 and ((w >> 1) & 0x3ff) == 444 and rd == (w >> 11) & 31:
            if rd in reg: reg[ra] = reg[rd]
    return out


def scan_ppc(b, segs):
    res = []
    for m in re.finditer(re.escape(NEEDLE), b):
        tgt = o2v(segs, m.start())
        vals = ppc_values(b, segs, 0, len(b))
        for r in [off for off, v in vals if v == tgt]:
            seq = [c for c in (onechar(b, segs, v) for off, v in vals if r <= off < r + 3000) if c]
            res.append((hex(r), ''.join(seq[:12])))
    return res


def scan_x86(b, segs, bits):
    res = []
    for m in re.finditer(re.escape(NEEDLE), b):
        va = o2v(segs, m.start())
        if va is None: continue
        refs = [x.start() for x in re.finditer(re.escape(struct.pack('<I', va & M32)), b)]
        if bits == 64:
            for x in re.finditer(rb'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]', b):
                off = x.start(); disp, = struct.unpack('<i', b[off + 3:off + 7]); ip = o2v(segs, off + 7)
                if ip is not None and ip + disp == va: refs.append(off)
        for r in refs:
            win = b[r:r + 3000]; ch = []
            for k in range(len(win) - 4):
                v, = struct.unpack('<I', win[k:k + 4]); c = onechar(b, segs, v)
                if c: ch.append((k, c))
            if bits == 64:
                for k in range(len(win) - 7):
                    if win[k] in (0x48, 0x4c) and win[k + 1] == 0x8d and (win[k + 2] & 0xc7) == 0x05:
                        disp, = struct.unpack('<i', win[k + 3:k + 7]); ip = o2v(segs, r + k + 7)
                        if ip is None: continue
                        c = onechar(b, segs, ip + disp)
                        if c: ch.append((k, c))
            ch.sort(); res.append((hex(r), ''.join(c for _, c in ch[:12])))
    return res


def rotr2(x): return ((x >> 2) | (x << 6)) & 0xff


def dec603(bs):
    n = len(bs); out = []
    for i, b in enumerate(bs):
        c = ((~b) - 10 - n) & 0xff; c = rotr2(c); out.append((c - i) & 0xff)
    return bytes(out)


def scramble(b):
    hits = set()
    for k in range(len(b) - 8):
        if b[k] in (0x50, 0xd0):
            t = dec603(b[k:k + 8]).lower()
            if re.match(rb'^g3d[0-9a-f]{5}$', t): hits.add((t.decode().upper(), hex(k)))
    return sorted(hits)


for p in sys.argv[1:]:
    d = open(p, 'rb').read()
    for ct, b in slices(d):
        info = parse(b)
        if not info: print(p, ct, 'not mach-o'); continue
        e, bits, cpu, segs = info
        if cpu == 18: r = scan_ppc(b, segs); arch = 'ppc'
        else: r = scan_x86(b, segs, bits); arch = 'x86_64' if bits == 64 else 'i386'
        s = scramble(b) if not any(len(x[1]) >= 8 for x in r) else []
        print(p, arch, r, s[:4])
