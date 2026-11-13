"""Each version profile with no binary behind it says so in data (Graal_analysis#439).

A profile is a table with a `token` in one of the version-profile TOMLs. Two rules:

1. A profile whose login token is graded L (list only) in
   `client-internals/version-token-catalogue.md`, with no B or W row for the same
   token, has no executable behind it, so it must carry `inferred = true`.
2. A profile with `inferred = true` must not claim a binary or wire source for its
   own values (`src_default = "bin"`, or `bin`/`cap` in `token_src`).

`inferred` is an identity key: `resolve.py` does not pass it to a profile that
names this one as its `base`.
"""
import pathlib, re, sys, tomllib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import resolve  # noqa: E402

TOMLS = sorted(HERE.glob('*.toml')) + sorted((ROOT / 'version-profiles').glob('*.toml'))
CATALOGUE = ROOT / 'client-internals' / 'version-token-catalogue.md'
ROW = re.compile(r'^\|[^|]*\|\s*`([A-Z0-9]{8})`[^|]*\|\s*\**([A-Z—+]+)\**')


def grades():
    out = {}
    for line in CATALOGUE.read_text(encoding='utf-8').splitlines():
        m = ROW.match(line)
        if m:
            out.setdefault(m.group(1), set()).add(m.group(2).rstrip('+'))
    return out


def profiles():
    for path in TOMLS:
        doc = tomllib.loads(path.read_text(encoding='utf-8'))
        if 'version' in doc:
            for v in doc['version']:
                yield path.name, v
        else:
            named = {k: v for k, v in doc.items() if isinstance(v, dict) and 'token' in v}
            for p in resolve.resolve(doc):
                if p['id'] in named:
                    yield path.name, dict(named[p['id']], **{'_resolved_inferred': p.get('inferred', False)})


def list_only(g):
    return g == {'L'}


def test_catalogue_parses():
    g = grades()
    assert len(g) > 60
    assert g['GNW14015'] == {'L'}          # 2.3
    assert 'W' in g['GNW22122']            # 2.17


def test_list_only_tokens_are_inferred():
    g = grades()
    bad = [f"{f}: {p.get('label')} ({p['token']})" for f, p in profiles()
           if p.get('token') in g and list_only(g[p['token']]) and not p.get('inferred')]
    assert not bad, 'L-graded token without inferred = true: ' + ', '.join(bad)


def test_inferred_profiles_claim_no_binary():
    bad = []
    for f, p in profiles():
        if not p.get('inferred'):
            continue
        if p.get('src_default', '') == 'bin' or re.search(r'\b(bin|cap)\b', p.get('token_src', '')):
            bad.append(f"{f}: {p.get('label')}")
    assert not bad, 'inferred profile claims a binary source: ' + ', '.join(bad)


def test_inferred_is_not_inherited():
    for f, p in profiles():
        if '_resolved_inferred' in p:
            assert p['_resolved_inferred'] == bool(p.get('inferred')), f"{f}: {p.get('label')}"


def test_no_binary_releases_are_flagged():
    """The releases #439 lists with no executable in any collection."""
    want = {'2.12', '2.13', '2.14', '2.15 / 2.151', '2.16 (rev1-rev7)', '2.3'}
    have = {p.get('label') for _, p in profiles() if p.get('inferred')}
    assert want <= have, sorted(want - have)
