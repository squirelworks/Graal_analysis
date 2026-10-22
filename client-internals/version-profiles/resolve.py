"""Resolve the inheritance in a version-profile TOML file.

usage: python3 resolve.py 141-217.toml [--json | --md]

Each profile copies its `base`, then applies its own keys. `x_add` / `x_remove`
edit the inherited list `x`; any other key replaces the inherited value. The
`features` sub-table merges key by key. Identity keys (md5, builds, revs, linked,
notes) are not inherited.

Every resolved key carries a source tag in `src`: the profile's own `src` entry, else
its `src_default` (`src_features` for features). When a profile with no binary
(`src_default` other than bin) inherits a binary-read value, the tag becomes
`inf (as <base>)`, because that value was not checked in this version.

Output is the flattened profiles as JSON (default) or one markdown block per version.
"""
import copy, json, sys, tomllib

MERGED = ('features',)
IDENTITY = ('md5', 'builds', 'revs', 'linked', 'token_alt', 'notes', 'src_default')


def resolve(doc):
    defaults = doc.get('defaults', {})
    done = {}

    def get(name):
        if name in done:
            return done[name]
        raw = doc[name]
        if 'base' in raw:
            out = copy.deepcopy(get(raw['base']))
            for k in IDENTITY:
                out.pop(k, None)
        else:
            out = copy.deepcopy(defaults)
            out['src'] = {k: 'bin' for k in defaults}
        tag = raw.get('src_default', 'bin')
        ftag = raw.get('src_features', 'doc+forms' if tag == 'bin' else 'doc')
        own = raw.get('src', {})
        if 'base' in raw and 'bin' not in tag:
            for k, t in out['src'].items():
                if 'bin' in t or 'forms' in t:
                    out['src'][k] = f"inf (as {raw['base']})"
        for k, v in raw.items():
            if k in ('base', 'src'):
                continue
            if k == 'features':
                for f in v:
                    out['src']['features.' + f] = own.get('features.' + f, ftag)
            elif k not in IDENTITY:
                out['src'][k.rsplit('_', 1)[0] if k.endswith(('_add', '_remove')) else k] = own.get(k, tag)
            if k.endswith('_add') or k.endswith('_remove'):
                key = k.rsplit('_', 1)[0]
                cur = list(out.get(key, []))
                cur = sorted(set(cur) | set(v)) if k.endswith('_add') else [x for x in cur if x not in v]
                out[key] = cur
            elif k in MERGED:
                out.setdefault(k, {}).update(v)
            else:
                out[k] = copy.deepcopy(v)
        out['id'] = name
        done[name] = out
        return out

    return [get(n) for n, v in doc.items() if isinstance(v, dict) and n != 'defaults']


def ranges(ids):
    out, run = [], []
    for i in ids:
        if run and i == run[-1] + 1:
            run.append(i)
        else:
            if run:
                out.append(run)
            run = [i]
    if run:
        out.append(run)
    return ', '.join(f'{r[0]}' if len(r) == 1 else f'{r[0]}-{r[-1]}' for r in out)


def fmt(v):
    if isinstance(v, list) and v and all(isinstance(x, int) for x in v):
        return ranges(v)
    if isinstance(v, list):
        return '; '.join(map(str, v))
    if isinstance(v, dict):
        return ', '.join(f'{k}={fmt(x)}' for k, x in v.items())
    return str(v)


def markdown(profiles):
    lines = []
    for p in profiles:
        lines.append(f"## {p.get('label', p['id'])}\n")
        src = p.get('src', {})
        for k, v in p.items():
            if k in ('id', 'label', 'src', 'src_default', 'features', 'notes'):
                continue
            lines.append(f"- {k}: {fmt(v)}" + (f"  [{src[k]}]" if k in src else ''))
        for k, v in p.get('features', {}).items():
            lines.append(f"- features.{k}: {fmt(v)}  [{src.get('features.' + k, '?')}]")
        for n in p.get('notes', []):
            lines.append(f"- note: {n}")
        lines.append('')
    return '\n'.join(lines)


if __name__ == '__main__':
    doc = tomllib.load(open(sys.argv[1], 'rb'))
    profiles = resolve(doc)
    print(markdown(profiles) if '--md' in sys.argv else json.dumps(profiles, indent=1))
