#!/usr/bin/env python3
# MSVC switch scanner: finds `jmp [reg*4+TBL]` dispatches, with optional byte index table
# (`mov/movzx r8, byte ptr [reg+IDX]`), the bound (`cmp reg, N` / `ja`), and an optional bias (`add/sub reg, K`
# or `lea reg,[reg-K]`). Prints, per switch, the cases whose target differs from the default target.
# usage: swscan.py file.exe|file.dll [minN] [maxN]
# Prints switch locations for the analyst's own navigation. Do not copy them into notes (AGENTS.md).
import sys, struct, re, pefile, capstone
f = sys.argv[1]; lo = int(sys.argv[2]) if len(sys.argv) > 2 else 60; hi = int(sys.argv[3]) if len(sys.argv) > 3 else 400
pe = pefile.PE(f); IB = pe.OPTIONAL_HEADER.ImageBase
img = pe.get_memory_mapped_image()
def u32(va): return struct.unpack('<I', img[va - IB:va - IB + 4])[0]
def u8(va): return img[va - IB]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
text = [s for s in pe.sections if s.Characteristics & pefile.SECTION_CHARACTERISTICS['IMAGE_SCN_MEM_EXECUTE']]
pat = re.compile(rb'\xff\x24[\x85\x8d\x95\x9d\xb5\xbd\x80-\xbf]')
out = []
for s in text:
    base = IB + s.VirtualAddress; data = img[s.VirtualAddress:s.VirtualAddress + s.Misc_VirtualSize]
    for m in pat.finditer(data):
        j = m.start(); jva = base + j
        ins = list(md.disasm(data[j:j + 7], jva))
        if not ins or ins[0].mnemonic != 'jmp' or '*4 + 0x' not in ins[0].op_str: continue
        tbl = int(ins[0].op_str.split('+ 0x')[1].rstrip(']'), 16)
        # look back up to 48 bytes for the preamble
        best = None
        for back in range(6, 64):
            pre = list(md.disasm(data[j - back:j], jva - back))
            if not pre or pre[-1].address + pre[-1].size != jva: continue
            n = None; idx = None; bias = 0
            for i in pre:
                if i.mnemonic == 'cmp' and ', 0x' in i.op_str and 'ptr' not in i.op_str: n = int(i.op_str.split(', ')[1], 16)
                elif i.mnemonic == 'cmp' and re.match(r'^\w+, \d+$', i.op_str): n = int(i.op_str.split(', ')[1])
                mm = re.match(r'^\w+, byte ptr \[\w+ \+ 0x([0-9a-f]{6,})\]$', i.op_str)
                if i.mnemonic in ('mov', 'movzx') and mm:
                    idx = int(mm.group(1), 16)
                if i.mnemonic == 'add' and re.match(r'^\w+, 0x[0-9a-f]+$', i.op_str) and 'esp' not in i.op_str:
                    v = int(i.op_str.split(', ')[1], 16)
                    bias = -((v - (1 << 32)) if v >= (1 << 31) else v)
                if i.mnemonic == 'sub' and re.match(r'^\w+, 0x[0-9a-f]+$', i.op_str) and 'esp' not in i.op_str:
                    bias = int(i.op_str.split(', ')[1], 16)
                if i.mnemonic == 'lea' and re.search(r'\[\w+ - 0x([0-9a-f]+)\]', i.op_str):
                    bias = int(re.search(r'- 0x([0-9a-f]+)\]', i.op_str).group(1), 16)
            if n is not None:
                best = (n, idx, bias); break
        if not best: continue
        n, idx, bias = best
        if not (lo <= n <= hi): continue
        try:
            if idx:
                ix = [u8(idx + k) for k in range(n + 1)]
                nt = max(ix) + 1; tg = [u32(tbl + 4 * k) for k in range(nt)]
                targ = [tg[x] for x in ix]
            else:
                targ = [u32(tbl + 4 * k) for k in range(n + 1)]
        except Exception:
            continue
        from collections import Counter
        dflt = Counter(targ).most_common(1)[0][0]
        cases = [k + bias for k, t in enumerate(targ) if t != dflt]
        out.append((jva, n, bias, idx is not None, cases))
for jva, n, bias, hasidx, cases in out:
    print('%08x n=%d bias=%d idx=%s ncase=%d' % (jva, n, bias, hasidx, len(cases)))
    print('   ', ','.join(map(str, cases)))
