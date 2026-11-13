#!/usr/bin/env python3
# Build {dll!name: nargs} from Wine's PE dlls: nargs = imm16/4 of the first `ret imm16` reached
# by linear disassembly from each export (stdcall). Writes argtab.json.
import sys, os, json, pefile, capstone
W = sys.argv[1]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
tab = {}
pes = {}
def load(n):
    if n not in pes:
        p = os.path.join(W, n + '.dll')
        pes[n] = pefile.PE(p) if os.path.exists(p) else None
    return pes[n]
def nargs(dll, name, depth=0):
    p = load(dll)
    if p is None or depth > 3: return None
    for e in p.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.name and e.name.decode() == name:
            if e.forwarder:
                f = e.forwarder.decode(); d2, n2 = f.split('.', 1)
                if d2.lower().startswith('api-ms-'): d2 = 'kernelbase'
                return nargs(d2.lower(), n2, depth + 1)
            off = p.get_offset_from_rva(e.address)
            code = p.__data__[off:off + 0x3000]
            for i in md.disasm(code, e.address):
                if i.mnemonic == 'ret':
                    return int(i.op_str, 16) // 4 if i.op_str else 0
                if i.mnemonic == 'jmp' and i.op_str.startswith('dword ptr ['):
                    slot = int(i.op_str[11:-1], 16) - p.OPTIONAL_HEADER.ImageBase
                    for d in getattr(p, 'DIRECTORY_ENTRY_IMPORT', []):
                        for im in d.imports:
                            if im.address - p.OPTIONAL_HEADER.ImageBase == slot and im.name:
                                dn = d.dll.decode().lower().rsplit('.', 1)[0]
                                if dn.startswith('api-ms-'): dn = 'kernelbase'
                                return nargs(dn, im.name.decode(), depth + 1)
                    return None
            return None
    return None
for dll in sys.argv[2:]:
    p = load(dll)
    if p is None: continue
    for e in p.DIRECTORY_ENTRY_EXPORT.symbols:
        if not e.name: continue
        n = e.name.decode()
        try: k = nargs(dll, n)
        except Exception: k = None
        if k is not None: tab[n] = k
json.dump(tab, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'argtab.json'), 'w'))
print(len(tab))
