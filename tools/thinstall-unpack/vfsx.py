#!/usr/bin/env python3
# Thinstall 2.x VFS extractor for the Graal4Setup.exe downloads.
# Directory: parsed from the runtime's decompressed directory in the emulator snapshot (.snap3).
# Data: 64 KiB blocks, each decompressed by calling the runtime's own block decoder
# (cdecl decode(src, srclen, dst, dstlen), found by its prologue bytes) in unicorn.
# Only packer code runs, never Graal code.
# usage: vfsx.py packed.exe snap3 outdir [name-substring ...]
import sys, os, re, struct, pickle
from unicorn import *
from unicorn.x86_const import *

exe, snapf, outd = sys.argv[1:4]
MB = 1 << 20
API = 7 << 28
HEAPBASE = 1 << 29
raw = open(exe, 'rb').read()
st = pickle.load(open(snapf, 'rb'))
mem = {a: (sz, perm, data) for a, sz, perm, data in st['mem']}

# --- directory -------------------------------------------------------------------------------
entries = {}
for a, (sz, perm, data) in mem.items():
    if not (HEAPBASE <= a < API): continue
    for m in re.finditer(rb'%[A-Za-z]+%\\[\x20-\x7e]{1,200}', data):
        s = m.start()
        if s < 2: continue
        n = struct.unpack('<H', data[s - 2:s])[0]
        name = data[s:s + n]
        if len(name) != n or not all(32 <= c < 127 for c in name): continue
        p = s + n
        if p + 8 + 32 + 2 > len(data): continue
        off, size = struct.unpack('<II', data[p:p + 8])
        nb = struct.unpack('<H', data[p + 40:p + 42])[0]
        if nb != (size + 0xffff) // 0x10000: continue
        bs = struct.unpack('<%dI' % nb, data[p + 42:p + 42 + 4 * nb])
        if off + sum(bs) > len(raw) or any(b == 0 or b > 2 * 65536 for b in bs): continue
        entries.setdefault(name.decode(), (off, size, bs))
dirs = {n.lower().rsplit('\\', 1)[0] for n in entries}
entries = {n: e for n, e in entries.items() if n.lower() not in dirs}
print('entries', len(entries))

# --- decoder ---------------------------------------------------------------------------------
mu = Uc(UC_ARCH_X86, UC_MODE_32)
for a, (sz, perm, data) in mem.items():
    mu.mem_map(a, sz, UC_PROT_ALL); mu.mem_write(a, data)
REGS = [UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI, UC_X86_REG_EDI,
        UC_X86_REG_EBP, UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EFLAGS]
GDT = 0x7fff << 16
mu.reg_write(UC_X86_REG_GDTR, (0, GDT, 0x28, 0)); mu.reg_write(UC_X86_REG_FS, 3 << 3)
for r in (UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_GS): mu.reg_write(r, 2 << 3)
IO = 3 << 29; mu.mem_map(IO, MB)
RET = 0x6ff << 20; mu.mem_map(RET, 0x1000); mu.mem_write(RET, b'\xf4')
# the decoder dispatches on the block's method byte; its prologue is the same in all three builds
DSIG = bytes.fromhex('558bec83ec148b45088a08884dfc8b55fc81e2ff0000008955ec8b45ec2dd7')
# The packer leaves an unrelocated copy of the runtime in memory too; take the copy whose
# method-byte jump table (the operand of the first `jmp [ecx*4+table]`) points into its own region.
DEC = None
for a, (sz, perm, data) in mem.items():
    i = data.find(DSIG)
    if not (HEAPBASE <= a < API) or i < 0: continue
    j = data.find(b'\xff\x24\x8d', i, i + 64)
    if j > 0 and a <= struct.unpack('<I', data[j + 3:j + 7])[0] < a + sz: DEC = a + i
if DEC is None: sys.exit('block decoder not found')
api_hits = []
def hook_api(uc, addr, size, ud):
    api_hits.append(st['S']['names'].get(addr, hex(addr))); uc.emu_stop()
mu.hook_add(UC_HOOK_CODE, hook_api, begin=API, end=API + MB)

def decode(src, dlen):
    mu.mem_write(IO, src)
    esp = 2 * MB - 65536
    mu.mem_write(esp, struct.pack('<5I', RET, IO, len(src), IO + 0x40000, dlen))
    mu.reg_write(UC_X86_REG_ESP, esp)
    del api_hits[:]
    try: mu.emu_start(DEC, RET, count=200_000_000)
    except UcError as e: raise RuntimeError('decode fault %s at %x' % (e, mu.reg_read(UC_X86_REG_EIP)))
    if api_hits: raise RuntimeError('decoder called api %s' % api_hits)
    if mu.reg_read(UC_X86_REG_EIP) != RET: raise RuntimeError('decoder did not return')
    return bytes(mu.mem_read(IO + 0x40000, dlen)), mu.reg_read(UC_X86_REG_EAX)

os.makedirs(outd, exist_ok=True)
want = [x.lower() for x in sys.argv[4:]]
ok = bad = 0
for name, (off, size, bs) in sorted(entries.items()):
    rel = name.split('\\', 1)[1] if '\\' in name else name
    if want and not any(w in name.lower() for w in want): continue
    dst = os.path.join(outd, name.split('\\')[0].strip('%'), *rel.split('\\'))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    out = bytearray(); p = off
    try:
        for i, b in enumerate(bs):
            dl = min(0x10000, size - 0x10000 * i)
            if b == dl:  # stored
                out += raw[p:p + b]
            else:
                d, r = decode(raw[p:p + b], dl); out += d
            p += b
        open(dst, 'wb').write(bytes(out[:size])); ok += 1
    except RuntimeError as e:
        print('FAIL', name, e); bad += 1
print('ok', ok, 'fail', bad)
