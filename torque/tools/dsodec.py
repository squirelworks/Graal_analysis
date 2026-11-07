#!/usr/bin/env python3
"""Rough decompiler for Graal's TorqueScript .dso (v33) files.

Output is TorqueScript-like text. Control flow is left as labelled gotos
(if (!c) goto L12;), except && / || chains, which are folded back in.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsodis import DSO, OPS, NARGS

def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'

BIN = dict(CMPEQ='==', CMPGR='>', CMPGE='>=', CMPLT='<', CMPLE='<=', CMPNE='!=', XOR='^', MOD='%', BITAND='&',
           BITOR='|', SHR='>>', SHL='<<', AND='&&', OR='||', ADD='+', SUB='-', MUL='*', DIV='/')
CHR = {' ': 'SPC', '\t': 'TAB', '\n': 'NL'}

def varname(e):
    # "$a" @ idx  ->  $a[idx]
    if e and ' @ ' in e:
        head, tail = e.split(' @ ', 1)
        if head.startswith('"'): head = head[1:-1]
        return head + '[' + tail + ']'
    if e.startswith('"') and e.endswith('"'): return e[1:-1]
    return '[' + e + ']'

def decompile(d):
    code = d.code; out = []; ind = [0]
    def emit(t): out.append('  ' * ind[0] + t)
    S = None; strstack = []; I = []; F = []; frames = []; fresh = False
    curvar = curobj = curfield = None
    objstack = []; fn_end = []
    labels = set()
    for ip, n in walk(d):
        if n.startswith('JMP'): labels.add(code[ip + 1])
    pend = {}  # target ip -> list of (op, lhs expr) for && / ||
    for ip, n in walk(d):
        while fn_end and ip >= fn_end[-1]:
            fn_end.pop(); ind[0] -= 1; emit('}'); emit('')
        if ip in pend:
            for op, lhs in pend.pop(ip):
                rhs = I.pop() if I else '?'
                I.append('(%s %s %s)' % (lhs, op, rhs))
        elif ip in labels:
            emit('L%d:' % ip)
        a = code[ip + 1: ip + 1 + NARGS.get(n, 0)]
        infn = bool(fn_end)
        strs = d.fs if infn else d.gs; flts = d.ff if infn else d.gf
        if n == 'FUNC_DECL':
            name, ns, pkg = d.ident(ip + 1), d.ident(ip + 2), d.ident(ip + 3)
            argc = code[ip + 6]
            args = [d.ident(ip + 7 + i) or '%%arg%d' % i for i in range(argc)]
            args = [x if not x.startswith('<bad') else '%%unused%d' % i for i, x in enumerate(args)]
            hdr = 'function %s%s(%s)' % (ns + '::' if ns else '', name, ', '.join(args))
            if pkg: hdr += '   // package ' + pkg
            if code[ip + 4] or code[ip + 5] > ip + 7 + argc:
                emit(hdr + ' {'); ind[0] += 1; fn_end.append(code[ip + 5])
            else:
                emit(hdr + ';')
        elif n == 'LOADIMMED_STR': S = q(d.cstr(strs, a[0])); fresh = True
        elif n == 'TAG_TO_STR': S = "'" + d.cstr(strs, a[0]) + "'"; fresh = True
        elif n == 'LOADIMMED_IDENT': S = d.ident(ip + 1); fresh = True
        elif n == 'LOADIMMED_UINT': I.append(str(a[0]))
        elif n == 'LOADIMMED_FLT': F.append(repr(flts[a[0]]) if a[0] < len(flts) else '?f')
        elif n in ('SETCURVAR', 'SETCURVAR_CREATE'): curvar = d.ident(ip + 1)
        elif n in ('SETCURVAR_ARRAY', 'SETCURVAR_ARRAY_CREATE'): curvar = varname(S); fresh = False
        elif n == 'LOADVAR_UINT': I.append(curvar)
        elif n == 'LOADVAR_FLT': F.append(curvar)
        elif n == 'LOADVAR_STR': S = curvar; fresh = True
        elif n in ('SAVEVAR_UINT', 'SAVEVAR_FLT', 'SAVEVAR_STR'):
            v = {'SAVEVAR_UINT': I, 'SAVEVAR_FLT': F}.get(n)
            val = (v[-1] if v else '?') if v is not None else S
            emit('%s = %s;' % (curvar, val)); fresh = False
            if v is not None and v: v[-1] = curvar
            else: S = curvar
            emit_mark = True
        elif n == 'SETCUROBJECT': curobj = S; fresh = False
        elif n == 'SETCUROBJECT_NEW': curobj = None
        elif n == 'SETCURFIELD': curfield = d.ident(ip + 1)
        elif n == 'SETCURFIELD_ARRAY': curfield = (curfield or '?') + '[' + str(S) + ']'; fresh = False
        elif n.startswith('LOADFIELD_'):
            e = '%s.%s' % (curobj, curfield)
            {'LOADFIELD_UINT': I, 'LOADFIELD_FLT': F}.get(n, None).append(e) if n != 'LOADFIELD_STR' else None
            if n == 'LOADFIELD_STR': S = e; fresh = True
        elif n.startswith('SAVEFIELD_'):
            v = {'SAVEFIELD_UINT': I, 'SAVEFIELD_FLT': F}.get(n)
            val = (v[-1] if v else '?') if v is not None else S
            emit('%s = %s;' % (curfield if curobj is None else '%s.%s' % (curobj, curfield), val)); fresh = False
        elif n in ('STR_TO_UINT', 'STR_TO_FLT'):
            (I if n == 'STR_TO_UINT' else F).append(S); fresh = False
        elif n == 'STR_TO_NONE':
            if fresh and S and '(' in S: emit(S + ';')
            fresh = False
        elif n in ('FLT_TO_UINT', 'UINT_TO_FLT'):
            src, dst = (F, I) if n == 'FLT_TO_UINT' else (I, F)
            dst.append(src.pop() if src else '?')
        elif n in ('FLT_TO_STR', 'UINT_TO_STR'):
            src = F if n == 'FLT_TO_STR' else I
            S = src.pop() if src else '?'; fresh = True
        elif n in ('FLT_TO_NONE', 'UINT_TO_NONE'):
            src = F if n == 'FLT_TO_NONE' else I
            e = src.pop() if src else ''
            if e.startswith('new '): emit(e + ';')
        elif n in BIN:
            st = F if n in ('CMPEQ', 'CMPGR', 'CMPGE', 'CMPLT', 'CMPLE', 'CMPNE', 'ADD', 'SUB', 'MUL', 'DIV') else I
            # float compares pop floats, push uint
            x = st.pop() if st else '?'; y = st.pop() if st else '?'
            r = '(%s %s %s)' % (x, BIN[n], y)
            (F if n in ('ADD', 'SUB', 'MUL', 'DIV') else I).append(r)
        elif n == 'NEG': F.append('-' + (F.pop() if F else '?'))
        elif n == 'NOT': I.append('!' + (I.pop() if I else '?'))
        elif n == 'NOTF': I.append('!' + (F.pop() if F else '?'))
        elif n == 'ONESCOMPLEMENT': I.append('~' + (I.pop() if I else '?'))
        elif n == 'ADVANCE_STR': strstack.append((S, ' @ ')); fresh = False
        elif n == 'ADVANCE_STR_APPENDCHAR': strstack.append((S, ' %s ' % CHR.get(chr(a[0]), '@ ' + q(chr(a[0])) + ' @'))); fresh = False
        elif n == 'ADVANCE_STR_COMMA': strstack.append((S, ', ')); fresh = False
        elif n == 'ADVANCE_STR_NUL': strstack.append((S, None)); fresh = False
        elif n == 'REWIND_STR':
            p, sep = strstack.pop() if strstack else ('?', ' @ ')
            S = '%s%s%s' % (p, sep or ' @ ', S); fresh = True
        elif n == 'TERMINATE_REWIND_STR':
            p, sep = strstack.pop() if strstack else ('?', None); S = p
        elif n == 'COMPARE_STR':
            p, sep = strstack.pop() if strstack else ('?', None)
            I.append('(%s $= %s)' % (p, S)); fresh = False
        elif n == 'PUSH_FRAME': frames.append([])
        elif n == 'PUSH':
            (frames[-1] if frames else []).append(S); fresh = False
        elif n in ('CALLFUNC', 'CALLFUNC_RESOLVE'):
            fn, ns, ct = d.ident(ip + 1), d.ident(ip + 2), a[2]
            args = frames.pop() if frames else []
            if ct == 1 and args: S = '%s.%s(%s)' % (args[0], fn, ', '.join(map(str, args[1:])))
            elif ct == 2: S = 'Parent::%s(%s)' % (fn, ', '.join(map(str, args)))
            else: S = '%s%s(%s)' % (ns + '::' if ns else '', fn, ', '.join(map(str, args)))
            fresh = True
        elif n == 'CREATE_OBJECT':
            args = frames.pop() if frames else []
            cls = args[0] if args else '?'; nm = args[1] if len(args) > 1 else ''
            if nm in ('""', "''"): nm = ''
            extra = ', '.join(map(str, args[2:]))
            kw = 'datablock' if a[1] else 'new'
            par = d.ident(ip + 1)
            emit('%s %s(%s%s%s)%s {' % (kw, cls, nm, ', ' if extra and nm else '', extra, ' : ' + par if par else ''))
            ind[0] += 1; objstack.append('%s %s(%s)' % (kw, cls, nm))
        elif n == 'ADD_OBJECT': pass
        elif n == 'END_OBJECT':
            ind[0] -= 1; emit('};')
            o = objstack.pop() if objstack else 'new ?'
            if I and I[-1] == '0': I[-1] = '<' + o + '>'
        elif n.startswith('JMP'):
            t = a[0]
            if n == 'JMP': emit('goto L%d;' % t)
            elif n in ('JMPIF_NP', 'JMPIFNOT_NP'):
                lhs = I.pop() if I else '?'
                pend.setdefault(t, []).append(('||' if n == 'JMPIF_NP' else '&&', lhs))
            else:
                c = (F if n in ('JMPIFF', 'JMPIFFNOT') else I)
                e = c.pop() if c else '?'
                emit('if (%s%s) goto L%d;' % ('!' if 'NOT' in n else '', e, t))
        elif n == 'RETURN':
            if fresh and S is not None: emit('return %s;' % S)
            else: emit('return;')
            fresh = False
        else:
            emit('// %s %s' % (n, ' '.join(map(str, a))))
    while fn_end:
        fn_end.pop(); ind[0] -= 1; emit('}')
    return out

def walk(d):
    code = d.code; ip = 0
    while ip < len(code):
        o = code[ip]
        if o >= len(OPS): yield ip, 'BAD'; ip += 1; continue
        n = OPS[o]
        yield ip, n
        ip += 7 + code[ip + 6] if n == 'FUNC_DECL' else 1 + NARGS.get(n, 0)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        d = DSO(open(p, 'rb').read())
        print('// decompiled from %s (dso v%d)' % (os.path.basename(p), d.ver))
        print('\n'.join(decompile(d)))
