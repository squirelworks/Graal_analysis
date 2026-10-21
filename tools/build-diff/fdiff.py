"""Match functions between two builds' ExportFeatures JSONL and classify identical / changed / added / removed.

usage: fdiff.py A.feat.jsonl A.exe B.feat.jsonl B.exe out.json
Passes: unique RTTI names, unique exact shapes, unique string sets, then callee/caller propagation.
"""
import sys, json, hashlib, collections, difflib, struct, pefile

def load(feat, exe):
    pe = pefile.PE(exe, fast_load=True); ib = pe.OPTIONAL_HEADER.ImageBase
    mem = pe.get_memory_mapped_image()
    def lstr(va):
        o = va - ib
        if o < 8 or o >= len(mem): return None
        rc, n = struct.unpack_from('<iI', mem, o - 8)
        if rc != -1 or not 0 < n < 400: return None
        s = mem[o:o + n]
        if mem[o + n:o + n + 1] != b'\0': return None
        return s.decode('latin1')
    F = {}
    for l in open(feat):
        r = json.loads(l)
        r['strs'] = [s for s in (lstr(int(d, 16)) for d in r['drefs']) if s]
        r['h'] = hashlib.md5(r['shape'].encode()).hexdigest()
        F[r['entry']] = r
    callers = collections.defaultdict(list)
    for e, r in F.items():
        for c in r['callees']: callers[c].append(e)
    return F, callers

SKIPV = set(sys.argv[6].split(',')) if len(sys.argv) > 6 else set()

def generic(n): return n.startswith(('FUN_', 'thunk_FUN', 'Unwind')) or '::FUN_' in n

def shifted(n): return '::virt_' in n and n.split('::')[0] in SKIPV

def match(A, B):
    (FA, CA), (FB, CB) = A, B
    m = {}; used = set()
    def pair(a, b):
        if a in m or b in used: return False
        m[a] = b; used.add(b); return True
    def unique_pass(key):
        ka = collections.defaultdict(list); kb = collections.defaultdict(list)
        for e, r in FA.items():
            if e not in m:
                k = key(r)
                if k: ka[k].append(e)
        for e, r in FB.items():
            if e not in used:
                k = key(r)
                if k: kb[k].append(e)
        n = 0
        for k, la in ka.items():
            lb = kb.get(k)
            if lb and len(la) == 1 and len(lb) == 1 and pair(la[0], lb[0]): n += 1
        return n
    stats = {}
    stats['name'] = unique_pass(lambda r: None if generic(r['name']) or shifted(r['name']) else r['name'])
    stats['shape'] = unique_pass(lambda r: r['h'] if r['ninsn'] >= 6 else None)
    stats['strings'] = unique_pass(lambda r: tuple(r['strs']) if r['strs'] else None)
    stats['imms'] = unique_pass(lambda r: tuple(r['imms']) if len(r['imms']) >= 3 else None)
    # propagate through ordered callee lists and caller sets
    prop = 0
    changed = True
    while changed:
        changed = False
        for a, b in list(m.items()):
            ca, cb = FA[a]['callees'], FB[b]['callees']
            if len(ca) == len(cb):
                for x, y in zip(ca, cb):
                    if x in FA and y in FB and x not in m and y not in used and abs(FA[x]['ninsn'] - FB[y]['ninsn']) <= max(4, FA[x]['ninsn'] // 3):
                        pair(x, y); prop += 1; changed = True
            # single unmatched caller on both sides
            ua = [x for x in CA.get(a, []) if x not in m]; ub = [y for y in CB.get(b, []) if y not in used]
            if len(ua) == 1 and len(ub) == 1:
                pair(ua[0], ub[0]); prop += 1; changed = True
        if not changed:
            # unique shape among the unmatched, any length
            n = unique_pass(lambda r: r['h'])
            if n: prop += n; changed = True
    stats['propagated'] = prop
    return m, used, stats

def sim(ra, rb):
    sa = ra['shape'].split(';'); sb = rb['shape'].split(';')
    return difflib.SequenceMatcher(None, sa, sb, autojunk=False).ratio()

def main():
    A = load(sys.argv[1], sys.argv[2]); B = load(sys.argv[3], sys.argv[4])
    m, used, stats = match(A, B)
    FA, FB = A[0], B[0]
    out = {'stats': stats, 'countA': len(FA), 'countB': len(FB), 'identical': [], 'changed': [], 'removed': [], 'added': []}
    for a, b in m.items():
        ra, rb = FA[a], FB[b]
        rec = {'a': a, 'b': b, 'name': rb['name'] if not generic(rb['name']) else ra['name'], 'nameA': ra['name'], 'ninsnA': ra['ninsn'], 'ninsnB': rb['ninsn']}
        if ra['h'] == rb['h']: out['identical'].append(rec)
        else:
            rec['sim'] = round(sim(ra, rb), 3)
            rec['strs_added'] = sorted(set(rb['strs']) - set(ra['strs']))
            rec['strs_removed'] = sorted(set(ra['strs']) - set(rb['strs']))
            out['changed'].append(rec)
    for a, r in FA.items():
        if a not in m: out['removed'].append({'a': a, 'name': r['name'], 'ninsn': r['ninsn'], 'strs': r['strs'][:12]})
    for b, r in FB.items():
        if b not in used: out['added'].append({'b': b, 'name': r['name'], 'ninsn': r['ninsn'], 'strs': r['strs'][:12]})
    out['changed'].sort(key=lambda r: r['sim'])
    json.dump(out, open(sys.argv[5], 'w'), indent=1)
    print(json.dumps(stats), 'A', len(FA), 'B', len(FB), 'identical', len(out['identical']), 'changed', len(out['changed']),
          'removed', len(out['removed']), 'added', len(out['added']))

if __name__ == '__main__':
    main()
