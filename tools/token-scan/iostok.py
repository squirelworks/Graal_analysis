#!/usr/bin/env python3
"""Read the login token from a 32-bit ARM iPhone Graal client (Mach-O).

The iPhone clients share the desktop engine's connect routine: log
"Connecting to the game server...", connect, log "Done.", then append eight
one-character C strings. This follows the routine in ARM mode, tracking the
literal-pool + PC-relative string addresses and the stack slots the compiler
uses for repeated characters, and prints the characters passed to the
append calls after "Done.".

Works only on decrypted executables (LC_ENCRYPTION_INFO cryptid 0); an App
Store-encrypted one is reported and skipped. Needs `capstone`.

Usage: python3 -I iostok.py <Payload/App.app/App> ...
"""
import struct
import sys
from collections import Counter

import capstone as cs
from capstone import arm

FAT_MAGIC = bytes.fromhex('cafe' 'babe')  # universal header, big-endian
MH_MAGIC_LE = bytes.fromhex('cefa' 'edfe')  # 32-bit Mach-O, little-endian


def parse(raw):
    if raw[:4] == FAT_MAGIC:
        n = struct.unpack('>I', raw[4:8])[0]
        for k in range(n):
            ct, _, off, size, _ = struct.unpack('>5I', raw[8 + 20 * k:28 + 20 * k])
            if ct == 12:
                return parse_thin(raw, off)
        raise SystemExit('no ARM slice')
    return parse_thin(raw, 0)


def parse_thin(raw, base):
    ct, _, _, ncmds, _, _ = struct.unpack('<6I', raw[base + 4:base + 28])
    if raw[base:base + 4] != MH_MAGIC_LE or ct != 12:
        raise SystemExit('not a 32-bit ARM Mach-O')
    p = base + 28
    sects, cryptid = {}, None
    for _ in range(ncmds):
        cmd, size = struct.unpack('<2I', raw[p:p + 8])
        if cmd == 0x1:  # LC_SEGMENT
            nsects = struct.unpack('<I', raw[p + 48:p + 52])[0]
            q = p + 56
            for _ in range(nsects):
                sect = raw[q:q + 16].rstrip(b'\0').decode()
                segn = raw[q + 16:q + 32].rstrip(b'\0').decode()
                addr, sz, off = struct.unpack('<3I', raw[q + 32:q + 44])
                sects[(segn, sect)] = (addr, sz, base + off)
                q += 68
        elif cmd == 0x21:  # LC_ENCRYPTION_INFO
            cryptid = struct.unpack('<I', raw[p + 16:p + 20])[0]
        p += size
    return sects, cryptid


def read_token(path):
    raw = open(path, 'rb').read()
    sects, cryptid = parse(raw)
    if cryptid:
        return 'encrypted (cryptid %d), not readable' % cryptid
    taddr, tsz, toff = sects[('__TEXT', '__text')]
    caddr, csz, coff = sects[('__TEXT', '__cstring')]
    delta = toff - taddr  # file offset = va + delta inside __TEXT

    def cstr(va):
        o = va + delta
        return raw[o:raw.find(b'\0', o)]

    def lit(va):
        o = va + delta
        return struct.unpack('<I', raw[o:o + 4])[0]

    o = raw.find(b'Connecting to the game server', coff, coff + csz)
    if o < 0:
        return 'no connect string'
    needle = o - delta
    md = cs.Cs(cs.CS_ARCH_ARM, cs.CS_MODE_ARM)
    md.detail = True
    md.skipdata = True
    insns = [i for i in md.disasm(raw[toff:toff + tsz], taddr) if i.id != 0]

    def walk(seq):
        regs, stack = {}, {}
        for i in seq:
            m, ops = i.mnemonic, i.operands
            if m.startswith('ldr') and '[pc' in i.op_str and len(ops) == 2:
                regs[ops[0].reg] = ('lit', lit(i.address + 8 + ops[1].mem.disp))
            elif m.startswith('add') and 'pc' in i.op_str:
                rs = [x.reg for x in ops if x.type == arm.ARM_OP_REG]
                other = [r for r in rs[1:] if r != arm.ARM_REG_PC] or [rs[0]]
                v = regs.get(other[0])
                if v and v[0] == 'lit':
                    regs[rs[0]] = ('str', (v[1] + i.address + 8) & 0xffffffff)
            elif m == 'mov' and len(ops) == 2 and ops[1].type == arm.ARM_OP_REG:
                regs[ops[0].reg] = regs.get(ops[1].reg)
            elif m == 'str' and ops[1].type == arm.ARM_OP_MEM and ops[1].mem.base == arm.ARM_REG_SP:
                stack[ops[1].mem.disp] = regs.get(ops[0].reg)
            elif m == 'ldr' and ops[1].type == arm.ARM_OP_MEM and ops[1].mem.base == arm.ARM_REG_SP:
                regs[ops[0].reg] = stack.get(ops[1].mem.disp)
            yield i, regs
            if m == 'bl':
                regs = {}

    start = None
    for k, (i, regs) in enumerate(walk(insns)):
        if i.mnemonic.startswith('add') and 'pc' in i.op_str:
            v = regs.get([x.reg for x in i.operands if x.type == arm.ARM_OP_REG][0])
            if v == ('str', needle):
                start = k
                break
    if start is None:
        return 'no reference to the connect string (not ARM mode?)'
    calls, done = [], False
    for i, regs in walk(insns[start:start + 600]):
        if i.mnemonic == 'bl':
            v = regs.get(arm.ARM_REG_R1)
            if v and v[0] == 'str':
                s = cstr(v[1])
                if s == b'Done.':
                    done = True
                elif done:
                    calls.append((i.operands[0].imm, s))
            if len(calls) >= 12:
                break
    singles = [(t, s) for t, s in calls if len(s) == 1]
    if not singles:
        return 'no one-character appends after "Done."'
    target = Counter(t for t, _ in singles).most_common(1)[0][0]
    return b''.join(s for t, s in singles if t == target).decode()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print('%s: %s' % (p, read_token(p)))
