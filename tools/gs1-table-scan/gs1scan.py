"""Read the GS1 command list out of a Graal client binary.

    python -I gs1scan.py <mode> <binary>        -> JSON {"count": n, "commands": [...]}

Modes (pick by client family, see README.md):

  table   Delphi clients 2nd Graal .. 2.1 tests / NewWorld betas. The executor
          matches commands against one static array: plain pointers (1998 betas
          to 1.1.9) or fixed-size records whose first field points at the name
          (1.21 onwards). Found from the record that points at "say".
  init    Delphi clients 2.17 .. 2.31. The list is built at start-up by one
          routine that creates a command object per name (name loaded into ECX).
  x86     C++ engine on x86 (Linux 3.04 ELF, GraalEngine.dll 4.x/5.x). The
          engine registers every GS1 keyword by straight-line code; the command
          part is the run before the first expression function.
  ppc     The same engine built for Mac OS X PowerPC (3.153, 4.20).

Only names are printed: no addresses. Needs pefile, capstone and pyelftools
(pip install pefile capstone pyelftools). Run it only on copies of the client
binaries kept outside the repo; it never executes them.
"""
from __future__ import annotations

import json
import re
import struct
import sys

# Things the tables carry after the command list, or around it, that are not commands.
TABLE_STOP = {'gotrupees', 'graysoldier', 'up', 'left', 'down', 'right', '*=', ':=',
              'nwweek', 'nwmonth', 'nwmin'}
# Node kinds the compiler registers next to the commands but scripts never write.
INTERNAL = {'assign', 'endif', 'callfunction', 'jump'}
# How far around the "say " reference the x86 scan disassembles (bytes).
WINDOW_BEFORE, WINDOW_AFTER = 192 * 1024, 384 * 1024
NAME = re.compile(r'[a-z][a-z0-9]*( )?')


class Image:
    """Virtual-address view of a PE, ELF or 32-bit big-endian Mach-O file."""

    def __init__(self, path: str):
        self.d = open(path, 'rb').read()
        self.segs: list[tuple[int, int, int]] = []
        self.text = None
        d = self.d
        if d[:2] == b'MZ':
            import pefile
            pe = pefile.PE(path, fast_load=True)
            base = pe.OPTIONAL_HEADER.ImageBase
            self.base = base
            for s in pe.sections:
                self.segs.append((base + s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData))
            self.endian = '<'
        elif d[:4] == b'\x7fELF':
            from elftools.elf.elffile import ELFFile
            for s in ELFFile(open(path, 'rb')).iter_segments():
                if s['p_type'] == 'PT_LOAD':
                    self.segs.append((s['p_vaddr'], s['p_offset'], s['p_filesz']))
            self.endian = '<'
        elif d[:4] == bytes.fromhex('feedface'):
            self.endian = '>'
            ncmds = struct.unpack_from('>I', d, 16)[0]
            o = 28
            for _ in range(ncmds):
                cmd, size = struct.unpack_from('>II', d, o)
                if cmd == 1:  # LC_SEGMENT
                    vmaddr, _vmsize, fileoff, filesize = struct.unpack_from('>IIII', d, o + 24)
                    self.segs.append((vmaddr, fileoff, filesize))
                    nsect = struct.unpack_from('>I', d, o + 48)[0]
                    so = o + 56
                    for _ in range(nsect):
                        if d[so:so + 16].rstrip(b'\0') == b'__text':
                            taddr, tsize, toff = struct.unpack_from('>III', d, so + 32)
                            self.text = (taddr, toff, tsize)
                        so += 68
                o += size
        else:
            raise SystemExit('unknown file format')

    def off(self, va: int):
        for v, o, s in self.segs:
            if s and v <= va < v + s:
                return o + va - v
        return None

    def va(self, off: int):
        for v, o, s in self.segs:
            if o <= off < o + s:
                return v + off - o
        return None

    def cstr(self, va: int, pattern=rb'[\x21-\x7e][\x20-\x7e]*'):
        o = self.off(va)
        if o is None:
            return None
        e = self.d.find(b'\0', o, o + 64)
        if e <= o:
            return None
        s = self.d[o:e]
        return s.decode('latin1') if re.fullmatch(pattern, s) else None


def scan_table(img: Image) -> list[str]:
    d = img.d
    name_re = rb'[a-z0-9_ ]+|[*:=+\-]+'
    best = None
    for m in re.finditer(rb'(?<=\0)say ?\0', d):
        va = img.va(m.start())
        if va is None:
            continue
        for r in re.finditer(re.escape(struct.pack('<I', va)), d):
            for stride in (4, 8, 12, 16, 20, 24):
                names, o = [], r.start()
                while o + 4 <= len(d):
                    s = img.cstr(struct.unpack_from('<I', d, o)[0], name_re)
                    if s is None:
                        break
                    names.append(s)
                    o += stride
                # A plain pointer array also matches every larger stride with
                # every other entry, so it wins once it is clearly a table.
                score = len(names) * (1000 if stride == 4 and len(names) >= 8 else 1)
                if best is None or score > best[0]:
                    best = (score, names)
    if best is None:
        return []
    out = []
    for n in best[1]:
        if n.strip() in TABLE_STOP:
            break
        out.append(n)
    return out


def _x86():
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.skipdata = True
    return md


def scan_init(img: Image) -> list[str]:
    """Delphi 2.17+: names are AnsiString literals passed in ECX."""
    d, md = img.d, _x86()

    def lit(va):
        o = img.off(va)
        if o is None or o < 8 or d[o - 8:o - 4] != b'\xff' * 4:
            return None
        n = struct.unpack_from('<I', d, o - 4)[0]
        return d[o:o + n].decode('latin1') if n <= 64 else None

    for m in re.finditer(rb'\xff\xff\xff\xff\x04\x00\x00\x00say \x00', d):
        va = img.va(m.start() + 8)
        for r in re.finditer(re.escape(b'\xb9' + struct.pack('<I', va)), d):
            names = []
            for ins in md.disasm(d[r.start():r.start() + 400000], img.va(r.start())):
                if ins.mnemonic == 'ret':
                    break
                mm = re.fullmatch(r'ecx, 0x([0-9a-f]+)', ins.op_str) if ins.mnemonic == 'mov' else None
                if mm:
                    s = lit(int(mm.group(1), 16))
                    if s is not None:
                        names.append(s)
            # The same routine goes on to register internal nodes, flags and
            # functions; the commands are everything before the first internal node.
            if 'callfunction' in names:
                names = names[:names.index('callfunction')]
            return _dedupe(names)
    return []


def _cluster(hits, gap):
    idx = [i for i, h in enumerate(hits) if h[1] == 'say ']
    if not idx:
        return []
    a = b = idx[0]
    while a > 0 and hits[a][0] - hits[a - 1][0] < gap:
        a -= 1
    while b + 1 < len(hits) and hits[b + 1][0] - hits[b][0] < gap:
        b += 1
    return [h[1] for h in hits[a:b + 1]]


def scan_x86(img: Image) -> list[str]:
    d, md = img.d, _x86()
    for m in re.finditer(rb'(?<=\0)say \0', d):
        va = img.va(m.start())
        for r in re.finditer(re.escape(struct.pack('<I', va)), d):
            seg = [s for s in img.segs if s[1] <= r.start() < s[1] + s[2]]
            if not seg:
                continue
            lo = max(seg[0][1], r.start() - WINDOW_BEFORE)
            hi = min(seg[0][1] + seg[0][2], r.start() + WINDOW_AFTER)
            hits = []
            for ins in md.disasm(d[lo:hi], img.va(lo)):
                for mm in re.finditer(r'0x([0-9a-f]{6,8})', ins.op_str):
                    s = img.cstr(int(mm.group(1), 16))
                    if s is not None:
                        hits.append((ins.address, s))
            run = _cluster(hits, 400)
            if run:
                return engine_commands(run, sig_after=False)
    return []


def scan_ppc(img: Image) -> list[str]:
    d = img.d
    addr, off, size = img.text
    bcl_next = int('429f0005', 16)        # bcl 20,31,$+4: loads the PIC base into LR
    mflr_mask, mflr = int('fc1fffff', 16), int('7c0802a6', 16)
    reg: dict[int, int] = {}
    lr = None
    hits = []
    for i in range(0, size, 4):
        w = struct.unpack_from('>I', d, off + i)[0]
        op, rd, ra, imm = w >> 26, (w >> 21) & 31, (w >> 16) & 31, w & 0xffff
        simm = imm - 0x10000 if imm & 0x8000 else imm
        if w == bcl_next:
            lr = addr + i + 4
        elif (w & mflr_mask) == mflr:
            if lr is None:
                reg.pop(rd, None)
            else:
                reg[rd] = lr
        elif op == 31 and ((w >> 1) & 0x3ff) == 444 and rd == (w >> 11) & 31:  # mr
            if rd in reg:
                reg[ra] = reg[rd]
            else:
                reg.pop(ra, None)
        elif op == 15:  # addis / lis
            if ra == 0 or ra in reg:
                reg[rd] = ((reg[ra] if ra else 0) + (simm << 16)) & 0xffffffff
            else:
                reg.pop(rd, None)
        elif op == 14:  # addi / li
            if ra and ra in reg:
                v = (reg[ra] + simm) & 0xffffffff
                s = img.cstr(v)
                if s is not None:
                    hits.append((addr + i, s))
                reg[rd] = v
            else:
                reg.pop(rd, None)
        elif op == 24 and rd in reg:  # ori
            reg[ra] = reg[rd] | imm
    return engine_commands(_cluster(hits, 600), sig_after=True)


def engine_commands(run: list[str], sig_after: bool) -> list[str]:
    """Keep the command names of a registration run.

    Each keyword is registered with its argument signature: upper-case letters
    for commands (pushed before the name on x86, loaded after it on PPC), and
    "(...)" or "[...]" for expression functions. The command part ends at the
    first function.
    """
    items = [x for x in run if not x.endswith('.cpp') and x != 'Q=']
    out = []
    for i, x in enumerate(items):
        if not NAME.fullmatch(x):
            continue
        if sig_after:
            sig = items[i + 1] if i + 1 < len(items) else ''
        else:
            sig = items[i - 1] if i else ''
        if sig[:1] in ('(', '['):
            break
        if x.strip() not in INTERNAL:
            out.append(x)
    return _dedupe(out)


def _dedupe(names):
    out = []
    for n in names:
        if n not in out:
            out.append(n)
    return out


def main(argv):
    if len(argv) != 3 or argv[1] not in ('table', 'init', 'x86', 'ppc'):
        raise SystemExit(__doc__)
    img = Image(argv[2])
    cmds = {'table': scan_table, 'init': scan_init, 'x86': scan_x86, 'ppc': scan_ppc}[argv[1]](img)
    print(json.dumps({'count': len(cmds), 'commands': cmds}))


if __name__ == '__main__':
    main(sys.argv)
