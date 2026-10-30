#!/usr/bin/env python3
"""Disassembler for Torque Game Engine compiled scripts (.dso, version 33) as shipped with Graal 3.x-5.x."""
import struct, sys
OPS = """FUNC_DECL CREATE_OBJECT UNK2 UNK3 ADD_OBJECT END_OBJECT JMPIFFNOT JMPIFNOT JMPIFF JMPIF JMPIFNOT_NP JMPIF_NP JMP RETURN
CMPEQ CMPGR CMPGE CMPLT CMPLE CMPNE XOR MOD BITAND BITOR NOT NOTF ONESCOMPLEMENT SHR SHL AND OR ADD SUB MUL DIV NEG
SETCURVAR SETCURVAR_CREATE SETCURVAR_ARRAY SETCURVAR_ARRAY_CREATE LOADVAR_UINT LOADVAR_FLT LOADVAR_STR
SAVEVAR_UINT SAVEVAR_FLT SAVEVAR_STR SETCUROBJECT SETCUROBJECT_NEW SETCURFIELD SETCURFIELD_ARRAY
LOADFIELD_UINT LOADFIELD_FLT LOADFIELD_STR SAVEFIELD_UINT SAVEFIELD_FLT SAVEFIELD_STR
STR_TO_UINT STR_TO_FLT STR_TO_NONE FLT_TO_UINT FLT_TO_STR FLT_TO_NONE UINT_TO_FLT UINT_TO_STR UINT_TO_NONE
LOADIMMED_UINT LOADIMMED_FLT TAG_TO_STR LOADIMMED_STR LOADIMMED_IDENT CALLFUNC_RESOLVE CALLFUNC UNK72
ADVANCE_STR ADVANCE_STR_APPENDCHAR ADVANCE_STR_COMMA ADVANCE_STR_NUL REWIND_STR TERMINATE_REWIND_STR COMPARE_STR
PUSH PUSH_FRAME BREAK INVALID""".split()
OP = {n: i for i, n in enumerate(OPS)}
NARGS = {n: 0 for n in OPS}
NARGS.update(CREATE_OBJECT=3, ADD_OBJECT=1, END_OBJECT=1, JMPIFFNOT=1, JMPIFNOT=1, JMPIFF=1, JMPIF=1,
             JMPIFNOT_NP=1, JMPIF_NP=1, JMP=1, SETCURVAR=1, SETCURVAR_CREATE=1, SETCURFIELD=1,
             LOADIMMED_UINT=1, LOADIMMED_FLT=1, TAG_TO_STR=1, LOADIMMED_STR=1, LOADIMMED_IDENT=1,
             CALLFUNC_RESOLVE=3, CALLFUNC=3, ADVANCE_STR_APPENDCHAR=1)
CALLTYPE = {0: 'func', 1: 'method', 2: 'parent'}

class DSO:
    def __init__(s, data):
        o = 0
        def u32():
            nonlocal o; v = struct.unpack_from('<I', data, o)[0]; o += 4; return v
        s.ver = u32()
        n = u32(); s.gs = data[o:o + n]; o += n
        c = u32(); gf = data[o:o + 8 * c]; o += 8 * c
        n = u32(); s.fs = data[o:o + n]; o += n
        c = u32(); ff = data[o:o + 8 * c]; o += 8 * c
        # The PPC Mac build writes F64s big-endian although everything else is little-endian.
        s.fend = '<'
        def bad(v): return any(x != 0 and not (1e-30 < abs(x) < 1e30) for x in v)
        def unp(b, e): return struct.unpack('%s%dd' % (e, len(b) // 8), b)
        if bad(unp(gf + ff, '<')) and not bad(unp(gf + ff, '>')): s.fend = '>'
        s.gf, s.ff = unp(gf, s.fend), unp(ff, s.fend)
        clen = u32(); nlb = u32()
        code = []
        for _ in range(clen):
            b = data[o]; o += 1
            if b == 0xFF: code.append(u32())
            else: code.append(b)
        s.lb = [u32() for _ in range(nlb * 2)]
        s.idents = {}
        for _ in range(u32()):
            off = u32(); st = s.cstr(s.gs, off)
            for _ in range(u32()): s.idents[u32()] = st
        s.code = code; s.rest = len(data) - o

    @staticmethod
    def cstr(tab, off):
        if off >= len(tab): return '<bad %d>' % off
        return tab[off:tab.index(b'\0', off)].decode('latin1')

    def ident(s, ip):
        return s.idents.get(ip, '' if s.code[ip] == 0 else '?%d' % s.code[ip])

    def lines(s):
        code = s.code; ip = 0; infn = None; out = []
        while ip < len(code):
            infn_now = infn is not None and ip < infn
            strs = s.fs if infn_now else s.gs; flts = s.ff if infn_now else s.gf
            if infn is not None and ip >= infn: infn = None
            o = code[ip]
            if o >= len(OPS): out.append((ip, 'BAD %d' % o)); ip += 1; continue
            n = OPS[o]
            if n == 'FUNC_DECL':
                name, ns, pkg = s.ident(ip + 1), s.ident(ip + 2), s.ident(ip + 3)
                body, end, argc = code[ip + 4], code[ip + 5], code[ip + 6]
                args = [s.ident(ip + 7 + i) for i in range(argc)]
                full = (ns + '::' if ns else '') + name
                out.append((ip, 'FUNC %s(%s)%s%s end=%d' % (full, ', '.join(args), ' package=' + pkg if pkg else '', '' if body else ' [nobody]', end)))
                if body: infn = end
                ip += 7 + argc; continue
            a = code[ip + 1: ip + 1 + NARGS[n]]
            if n in ('LOADIMMED_STR', 'TAG_TO_STR'): t = '%r' % s.cstr(strs, a[0])
            elif n == 'LOADIMMED_FLT': t = repr(flts[a[0]]) if a[0] < len(flts) else '<badf>'
            elif n in ('LOADIMMED_IDENT', 'SETCURVAR', 'SETCURVAR_CREATE', 'SETCURFIELD'): t = s.ident(ip + 1)
            elif n in ('CALLFUNC', 'CALLFUNC_RESOLVE'):
                fn, ns = s.ident(ip + 1), s.ident(ip + 2)
                t = '%s%s [%s]' % (ns + '::' if ns else '', fn, CALLTYPE.get(a[2], a[2]))
            elif n == 'CREATE_OBJECT': t = 'parent=%s datablock=%d fail=%d' % (s.ident(ip + 1), a[1], a[2])
            elif n == 'ADVANCE_STR_APPENDCHAR': t = repr(chr(a[0]))
            else: t = ' '.join(map(str, a))
            out.append((ip, n + (' ' + t if t else '')))
            ip += 1 + NARGS[n]
        return out

if __name__ == '__main__':
    for p in sys.argv[1:]:
        d = DSO(open(p, 'rb').read())
        print('##### %s  ver=%d code=%d trailing=%d' % (p, d.ver, len(d.code), d.rest))
        for ip, t in d.lines(): print('%5d  %s' % (ip, t))
