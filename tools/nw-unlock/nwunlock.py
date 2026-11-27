#!/usr/bin/env python3
"""nwunlock.py: unlock the dormant New World body colours and shield frames in the
2.1x to 2.3x Windows clients (2.17.1, 2.22, 2.31).

Background: ../../client-internals/newworld-mode-2x.md.

These clients already switch into New World mode when the server sends id 177, and in
that mode they read eight COLORS values instead of five. The routine that recolours a
body still writes only the five classic palette slots, and every SHIELD sprite rect is
rescaled against a built-in 38x20 sheet. This tool adds a small code section that, only
while New World mode is on:

  --colours  recolours a body the way the NewWorld betas do: eight colour slots, each
             written to three palette entries (slot, slot+9, slot+18) with a highlight,
             mid and shadow shade. Classic bodies are untouched while the mode is off.
  --shield   draws SHIELD sprites with the GANI's own rect (no 38x20 rescale), so the
             wider New World shield sheets line up.

Everything is found by byte pattern, so the tool needs no per-build table. It refuses a
file in which any pattern is missing or ambiguous.

    python3 nwunlock.py scan  Graal.exe
    python3 nwunlock.py patch Graal.exe Graal-nw.exe [--colours] [--shield] [--bodycolors FILE]

With neither --colours nor --shield, both are applied. --bodycolors takes the
57-line bodycolors.txt that ships with the NewWorld betas (19 colours x 3 shades, in the
order mid, shadow, highlight); without it the shades are made from the client's own
colour table (highlight 1.0, mid 0.9, shadow 0.8).

A patched exe has a different code checksum, so its tamper-check value (PLI 39) changes.
Use it only on your own lab server. Pure Python 3, no dependencies.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys

NEW_SECTION = b'.nwu\x00\x00\x00\x00'
# PE section flags
SCN_CODE, SCN_EXEC, SCN_READ = 1 << 5, 1 << 29, 1 << 30
SCN_TEXT = SCN_CODE | SCN_EXEC | SCN_READ


# ---------------------------------------------------------------- PE helpers
class PE:
    def __init__(self, data: bytes):
        self.data = bytearray(data)
        if self.data[:2] != b'MZ':
            raise SystemExit('not an MZ file')
        self.pe = struct.unpack_from('<I', self.data, 0x3C)[0]
        if self.data[self.pe:self.pe + 4] != b'PE\x00\x00':
            raise SystemExit('not a PE file')
        self.nsec = struct.unpack_from('<H', self.data, self.pe + 6)[0]
        self.opt = self.pe + 24
        self.optsize = struct.unpack_from('<H', self.data, self.pe + 20)[0]
        self.base = struct.unpack_from('<I', self.data, self.opt + 28)[0]
        self.salign = struct.unpack_from('<I', self.data, self.opt + 32)[0]
        self.falign = struct.unpack_from('<I', self.data, self.opt + 36)[0]
        self.hdrsize = struct.unpack_from('<I', self.data, self.opt + 60)[0]
        self.sectab = self.opt + self.optsize
        self.sections = []
        for i in range(self.nsec):
            o = self.sectab + 40 * i
            name = bytes(self.data[o:o + 8])
            vsize, va, rsize, roff = struct.unpack_from('<IIII', self.data, o + 8)
            chars = struct.unpack_from('<I', self.data, o + 36)[0]
            self.sections.append((name, va, vsize, roff, rsize, chars))

    def image(self) -> bytes:
        """The memory image (headers plus sections at their RVAs)."""
        end = max(va + max(vs, rs) for _, va, vs, _, rs, _ in self.sections)
        img = bytearray(end)
        img[:self.hdrsize] = self.data[:self.hdrsize]
        for _, va, vs, ro, rs, _ in self.sections:
            n = min(vs, rs) if vs else rs
            img[va:va + n] = self.data[ro:ro + n]
        return bytes(img)

    def code(self):
        for s in self.sections:
            if s[5] & SCN_EXEC:
                return s
        raise SystemExit('no executable section')

    def va_to_off(self, va: int) -> int:
        rva = va - self.base
        for _, sva, vs, ro, rs, _ in self.sections:
            if sva <= rva < sva + max(vs, rs):
                return ro + (rva - sva)
        raise ValueError('address outside every section')

    def add_section(self, payload: bytes) -> int:
        """Append an executable, readable section; return its virtual address."""
        if any(s[0] == NEW_SECTION for s in self.sections):
            raise SystemExit('already patched (.nwu section present)')
        o = self.sectab + 40 * self.nsec
        # The slot past the last declared header is ignored by the loader; some unpacked
        # builds keep a stale entry there, which is safe to overwrite. The first section's
        # data must still start after the new header.
        first_raw = min(s[3] for s in self.sections if s[4])
        if o + 40 > min(self.hdrsize, first_raw):
            raise SystemExit('no room for another section header')
        last = max(self.sections, key=lambda s: s[1])
        va = align(last[1] + max(last[2], last[4]), self.salign)
        roff = align(len(self.data), self.falign)
        rsize = align(len(payload), self.falign)
        self.data.extend(b'\x00' * (roff - len(self.data)))
        self.data.extend(payload + b'\x00' * (rsize - len(payload)))
        struct.pack_into('<8sIIIIIIHHI', self.data, o, NEW_SECTION, len(payload), va, rsize, roff,
                         0, 0, 0, 0, SCN_TEXT)
        self.nsec += 1
        struct.pack_into('<H', self.data, self.pe + 6, self.nsec)
        struct.pack_into('<I', self.data, self.opt + 56, align(va + len(payload), self.salign))
        struct.pack_into('<I', self.data, self.opt + 64, 0)  # checksum: not checked for exes
        self.sections.append((NEW_SECTION, va, len(payload), roff, rsize, SCN_TEXT))
        return self.base + va


def align(v: int, a: int) -> int:
    return (v + a - 1) // a * a


def pat(spec: str) -> re.Pattern:
    """'c7 45 f4 05 ?? (..)' -> regex; '??' is any byte, '(' ')' group around bytes."""
    out = b''
    for tok in spec.split():
        if tok == '??':
            out += b'.'
        elif tok == '(':
            out += b'('
        elif tok == ')':
            out += b')'
        else:
            out += re.escape(bytes([int(tok, 16)]))
    return re.compile(out, re.S)


def u32(b: bytes) -> int:
    return struct.unpack('<I', b)[0]


def p32(v: int) -> bytes:
    return struct.pack('<I', v & 0xFFFFFFFF)


def rel32(src_next: int, dst: int) -> bytes:
    return struct.pack('<i', dst - src_next)


# ---------------------------------------------------------------- anchors
# COLORS prop writer: <form pointer> <getter> ... 8 if New World else 5.
P_GATE = pat('a1 ( ?? ?? ?? ?? ) 8b 00 e8 ( ?? ?? ?? ?? ) 84 c0 74 07 b8 08 00 00 00 eb 05 b8 05 00 00 00')
# Body recolour: count 5, colour buffer, palette-slot table, loop over esi's palette.
P_RECOLOUR = pat('( c7 45 f4 05 00 00 00 b8 ( ?? ?? ?? ?? ) ba ( ?? ?? ?? ?? ) ) 8b 0a 8d 0c 49 8b 18 8d 1c 5b'
                 ' 8d bc 0e ( ?? ?? ?? ?? ) 66 8b 8b ( ?? ?? ?? ?? ) 66 89 0f 8a 8b ?? ?? ?? ?? 88 4f 02'
                 ' 83 c2 04 83 c0 04 ff 4d f4 75 d1 ( 8b c6 )')
# SHIELD sprite: compare the sprite name with "SHIELD", jne past the 38x20 rescale.
P_SHIELD = pat('ba ( ?? ?? ?? ?? ) e8 ?? ?? ?? ?? ( 0f 85 ( ?? ?? ?? ?? ) ) 8b c3 e8 ?? ?? ?? ?? 85 c0'
               ' 0f 84 ?? ?? ?? ?? 8b c3 e8 ?? ?? ?? ?? 83 78 24 26')


def find_anchors(pe: PE) -> dict:
    img = pe.image()
    _, cva, cvs, _, _, _ = pe.code()
    code = img[cva:cva + cvs]
    base = pe.base + cva
    a = {}
    gates = list(P_GATE.finditer(code))
    forms = {(u32(m.group(1)), base + m.start(2) + 4 + struct.unpack('<i', m.group(2))[0]) for m in gates}
    if len(forms) != 1:
        raise SystemExit(f'New World mode getter: expected one, found {len(forms)} ({len(gates)} gates)')
    a['form_ptr'], a['getter'] = forms.pop()
    anyg = re.compile(re.escape(b'\xa1' + p32(a['form_ptr']) + b'\x8b\x00\xe8') + b'(....)\x84\xc0\x74.'
                      b'(?:[\xb8-\xbf]|\xc7\x45.)\x08\x00\x00\x00\xeb.(?:[\xb8-\xbf]|\xc7\x45.)\x05\x00\x00\x00', re.S)
    a['colour_gates'] = sum(1 for m in anyg.finditer(code)
                            if base + m.start(1) + 4 + struct.unpack('<i', m.group(1))[0] == a['getter'])
    rc = list(P_RECOLOUR.finditer(code))
    if len(rc) != 1:
        raise SystemExit(f'body recolour loop: expected one, found {len(rc)}')
    m = rc[0]
    a['rc_site'] = base + m.start(1)
    a['rc_len'] = m.end(1) - m.start(1)
    a['rc_loop'] = base + m.end(1)
    a['rc_after'] = base + m.start(6)
    a['colbuf'] = u32(m.group(2))
    a['slots'] = u32(m.group(3))
    a['paloff'] = u32(m.group(4))
    a['coltab'] = u32(m.group(5))
    sh = [m for m in P_SHIELD.finditer(code)
          if img[u32(m.group(1)) - pe.base:u32(m.group(1)) - pe.base + 7] == b'SHIELD\x00']
    if len(sh) != 1:
        raise SystemExit(f'SHIELD rescale: expected one, found {len(sh)}')
    m = sh[0]
    a['sh_site'] = base + m.start(2)
    a['sh_back'] = base + m.end(2)
    a['sh_skip'] = a['sh_back'] + struct.unpack('<i', m.group(3))[0]
    # sanity: the slot table must be the classic 5, 6, 4, 3, 1
    s = a['slots'] - pe.base
    if struct.unpack_from('<5i', img, s) != (5, 6, 4, 3, 1):
        raise SystemExit('palette-slot table is not 5, 6, 4, 3, 1')
    a['img'] = img
    a['base'] = pe.base
    return a


# ---------------------------------------------------------------- shades
def shade_table(a: dict, bodycolors: str | None) -> bytes:
    """3 tables x 20 colours x RGB, laid out shade-major like the NewWorld betas."""
    img = a['img']
    t = a['coltab'] - a['base']
    base = [tuple(img[t + 3 * i:t + 3 * i + 3]) for i in range(20)]
    tab = [[base[i] for i in range(20)] for _ in range(3)]
    if bodycolors:
        rows = [tuple(int(x) for x in ln.split(',')[:3])
                for ln in open(bodycolors, encoding='latin-1') if ln.strip()]
        if len(rows) < 57:
            raise SystemExit('bodycolors.txt needs 57 lines (19 colours x 3)')
        for n in range(57):
            tab[n % 3][n // 3] = rows[n]
    else:
        for i in range(19):
            r, g, b = base[i]
            tab[0][i] = tuple(min(255, round(v * 0.9)) for v in (r, g, b))
            tab[1][i] = tuple(min(255, round(v * 0.8)) for v in (r, g, b))
            tab[2][i] = (r, g, b)
    return b''.join(bytes(c) for s in tab for c in s)


# ---------------------------------------------------------------- stubs
def build(pe: PE, a: dict, colours: bool, shield: bool, bodycolors: str | None) -> list:
    """Return (payload, patches) with stubs laid out from the new section's address."""
    last = max(pe.sections, key=lambda s: s[1])
    sva = pe.base + align(last[1] + max(last[2], last[4]), pe.salign)
    out = bytearray()
    patches = []

    def here():
        return sva + len(out)

    def emit(b):
        out.extend(b)

    def call_getter():
        # push ecx; push edx; mov eax,[form]; mov eax,[eax]; call getter; pop edx; pop ecx; test al,al
        emit(b'\x51\x52\xa1' + p32(a['form_ptr']) + b'\x8b\x00\xe8')
        emit(rel32(here() + 4, a['getter']))
        emit(b'\x5a\x59\x84\xc0')

    if colours:
        shades = here()
        emit(shade_table(a, bodycolors))
        while len(out) % 16:
            emit(b'\xcc')
        stub = here()
        call_getter()
        emit(b'\x0f\x85'); jnz_at = len(out); emit(b'\x00' * 4)       # jnz new_world
        emit(b'\xc7\x45\xf4\x05\x00\x00\x00')                         # mov [ebp-0xc],5
        emit(b'\xb8' + p32(a['colbuf']) + b'\xba' + p32(a['slots']))  # mov eax,buf; mov edx,slots
        emit(b'\xe9'); emit(rel32(here() + 4, a['rc_loop']))           # jmp classic loop
        nw = here()
        out[jnz_at:jnz_at + 4] = rel32(sva + jnz_at + 4, nw)
        emit(b'\x31\xff')                                              # xor edi,edi (slot)
        l1 = here()
        emit(b'\x8b\x04\xbd' + p32(a['colbuf']))                       # mov eax,[buf+edi*4]
        emit(b'\x83\xf8\x13\x76\x02\x31\xc0')                          # cmp eax,19; jbe +2; xor eax,eax
        emit(b'\x8d\x04\x40\x31\xc9')                                  # lea eax,[eax*3]; xor ecx,ecx
        l2 = here()
        emit(b'\x6b\xd1\x3c\x01\xc2')                                  # imul edx,ecx,60; add edx,eax
        emit(b'\x8d\x1c\xc9\x01\xfb\x8d\x1c\x5b')                      # ebx=(ecx*9+edi)*3
        emit(b'\x50')                                                  # push eax
        emit(b'\x66\x8b\x82' + p32(shades))                            # mov ax,[edx+shades]
        emit(b'\x66\x89\x84\x1e' + p32(a['paloff']))                   # mov [esi+ebx+pal],ax
        emit(b'\x8a\x82' + p32(shades + 2))                            # mov al,[edx+shades+2]
        emit(b'\x88\x84\x1e' + p32(a['paloff'] + 2))                   # mov [esi+ebx+pal+2],al
        emit(b'\x58\x41\x83\xf9\x03\x75')                              # pop eax; inc ecx; cmp ecx,3; jne l2
        emit(struct.pack('<b', l2 - (here() + 1)))
        emit(b'\x47\x83\xff\x08\x75')                                  # inc edi; cmp edi,8; jne l1
        emit(struct.pack('<b', l1 - (here() + 1)))
        emit(b'\xe9'); emit(rel32(here() + 4, a['rc_after']))          # jmp after the loop
        site = a['rc_site']
        patches.append((site, b'\xe9' + rel32(site + 5, stub) + b'\x90' * (a['rc_len'] - 5)))

    if shield:
        while len(out) % 16:
            emit(b'\xcc')
        stub = here()
        emit(b'\x0f\x85'); emit(rel32(here() + 4, a['sh_skip']))      # not SHIELD: as before
        call_getter()
        emit(b'\x0f\x85'); emit(rel32(here() + 4, a['sh_skip']))      # New World: skip the rescale
        emit(b'\xe9'); emit(rel32(here() + 4, a['sh_back']))          # classic: rescale as before
        site = a['sh_site']
        patches.append((site, b'\xe9' + rel32(site + 5, stub) + b'\x90'))
    return bytes(out), patches, sva


# ---------------------------------------------------------------- main
def cmd_scan(args):
    pe = PE(open(args.exe, 'rb').read())
    a = find_anchors(pe)
    print(f'{args.exe}: all anchors found')
    print(f'  COLORS 8-or-5 gates: {a["colour_gates"]} (prop writer, own, other-player and NPC readers)')
    print('  body recolour loop: found, writes 5 palette slots (5, 6, 4, 3, 1)')
    print('  SHIELD 38x20 rescale: found')


def cmd_patch(args):
    pe = PE(open(args.exe, 'rb').read())
    if any(s[0] == NEW_SECTION for s in pe.sections):
        raise SystemExit('already patched (.nwu section present)')
    a = find_anchors(pe)
    colours = args.colours or not (args.colours or args.shield)
    shield = args.shield or not (args.colours or args.shield)
    payload, patches, sva = build(pe, a, colours, shield, args.bodycolors)
    got = pe.add_section(payload)
    if got != sva:
        raise SystemExit('section layout changed under us')
    for va, b in patches:
        o = pe.va_to_off(va)
        pe.data[o:o + len(b)] = b
    open(args.out, 'wb').write(pe.data)
    what = ', '.join(x for x, on in (('8-colour New World bodies', colours), ('New World shield rects', shield)) if on)
    print(f'wrote {args.out}: {what} (active only after the server sends id 177)')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('scan'); s.add_argument('exe'); s.set_defaults(fn=cmd_scan)
    p = sub.add_parser('patch'); p.add_argument('exe'); p.add_argument('out')
    p.add_argument('--colours', action='store_true'); p.add_argument('--shield', action='store_true')
    p.add_argument('--bodycolors'); p.set_defaults(fn=cmd_patch)
    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
