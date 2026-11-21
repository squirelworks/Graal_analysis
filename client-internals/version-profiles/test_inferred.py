"""Inferred behavior stays explicit, independently of token evidence (#439).

A profile is a table with a `token` in one of the version-profile TOMLs. Two rules:

1. A profile whose login token is graded L (list only) in
   `client-internals/version-token-catalogue.md`, with no B or W row for the same
   token, has no executable behind it, so it must carry `inferred = true`.
2. A profile with `inferred = true` must not give its values a binary default.
   A separately observed token may coexist with inferred behavior only when both
   packet sets remain explicitly inferred and the outgoing set is incomplete.

`inferred` is an identity key: `resolve.py` does not pass it to a profile that
names this one as its `base`.
"""
import importlib.util
import json
import pathlib, re, sys, tomllib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import resolve  # noqa: E402

TOMLS = sorted(HERE.glob('*.toml')) + sorted((ROOT / 'version-profiles').glob('*.toml'))
CATALOGUE = ROOT / 'client-internals' / 'version-token-catalogue.md'
SPEC = importlib.util.spec_from_file_location('token_map_for_inferred_profiles',
                                             ROOT / 'tools' / 'token-map' / 'generate.py')
TOKEN_MAP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOKEN_MAP)


def grades(text=None):
    out = {}
    for row in TOKEN_MAP.parse(CATALOGUE.read_text(encoding='utf-8') if text is None else text):
        if row['state'] == 'known' and re.fullmatch(r'[A-Z0-9]{8}', row['token']):
            # This token-level absence guard needs all supporting categories,
            # not a whole signature or the navigation bucket's primary grade.
            # B+ remains binary evidence; conflicts cannot establish an input.
            categories = {source['category'].rstrip('+')
                          for source in json.loads(row['source_records'])
                          if source['status'] == 'support'}
            out.setdefault(row['token'], set()).update(categories)
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
    return 'L' in g and not g.intersection({'B', 'W'})


def test_catalogue_parses():
    g = grades()
    assert len(g) > 60
    assert g['GNW14015'] == {'L'}          # 2.3
    assert 'W' in g['GNW22122']            # 2.17


def test_combined_evidence_preserves_absence_guard_categories():
    table = '### Family\n| ' + ' | '.join(TOKEN_MAP.HEADER) + ' |\n'
    rows = [
        ('GNW00000', 'WBL', '[W@wire] capture<br>[B@static] original<br>[L@report] table'),
        ('GNW00001', 'B+', '[B+@static] accepted lab, frame undecoded'),
        ('GNW00002', 'BL', '[B@static] original<br>[L@report] table'),
        ('GNW00003', 'L', '[L@report] table<br>[B@wrong!conflict] rejected attribution'),
    ]
    table += '\n'.join(f'| Build {i} | `{token}` | {signature} | {sources} | Windows | game-login | | |'
                       for i, (token, signature, sources) in enumerate(rows))
    result = grades(table)
    assert result == {'GNW00000': {'W', 'B', 'L'}, 'GNW00001': {'B'},
                      'GNW00002': {'B', 'L'}, 'GNW00003': {'L'}}
    assert not list_only(result['GNW00000'])
    assert not list_only(result['GNW00002'])
    assert list_only(result['GNW00003'])
    assert list_only({'L', 'C', 'U'})  # Other facets do not establish a read client.
    assert not list_only({'L', 'C', 'B'})


def test_list_only_tokens_are_inferred():
    g = grades()
    bad = [f"{f}: {p.get('label')} ({p['token']})" for f, p in profiles()
           if p.get('token') in g and list_only(g[p['token']]) and not p.get('inferred')]
    assert not bad, 'L-graded token without inferred = true: ' + ', '.join(bad)


def inference_errors(p, evidence):
    if not p.get('inferred'):
        return []
    errors = []
    if p.get('src_default', '') == 'bin':
        errors.append('binary default for inferred behavior')
    observed = set(re.findall(r'\b(bin|cap)\b', p.get('token_src', '')))
    if observed:
        support = evidence.get(p.get('token'), set())
        for tag, category in (('bin', 'B'), ('cap', 'W')):
            if tag in observed and category not in support:
                errors.append(f'{tag} token source lacks catalogue {category} support')
        for field in ('plo_known_src', 'pli_sent_src'):
            if p.get(field) != 'inf':
                errors.append(f'observed token requires separate {field} = inf')
        if p.get('pli_sent_complete') is not False:
            errors.append('observed token does not establish a complete send set')
    return errors


def test_inferred_profiles_preserve_behavior_limits():
    bad = []
    evidence = grades()
    for f, p in profiles():
        if errors := inference_errors(p, evidence):
            bad.append(f"{f}: {p.get('label')}: {'; '.join(errors)}")
    assert not bad, 'inferred profile overstates behavior evidence: ' + ', '.join(bad)


def test_observed_token_does_not_upgrade_inferred_packet_sets():
    profile = dict(inferred=True, token='GNW00000', token_src='cap', plo_known_src='inf',
                   pli_sent_src='inf', pli_sent_complete=False)
    evidence = {'GNW00000': {'W'}}
    assert not inference_errors(profile, evidence)
    # A real token observation cannot authorize measured packet sets, implicit
    # source tags, a complete outgoing set or a blanket binary default.
    for change in ({'plo_known_src': 'bin'}, {'pli_sent_src': 'cap'},
                   {'plo_known_src': ''}, {'pli_sent_complete': True},
                   {'src_default': 'bin'}):
        assert inference_errors(dict(profile, **change), evidence), change
    for missing in ('plo_known_src', 'pli_sent_src', 'pli_sent_complete'):
        incomplete = dict(profile)
        del incomplete[missing]
        assert inference_errors(incomplete, evidence), missing
    # Inference flags cannot manufacture a captured association for a list-only
    # token, an unlisted token, a missing token or a binary-only observation.
    for support in ({'GNW00000': {'L'}}, {}, {'GNW00000': {'B'}}):
        assert inference_errors(profile, support), support
    unbound = dict(profile)
    del unbound['token']
    assert inference_errors(unbound, evidence)
    assert inference_errors(dict(profile, token_src='bin'), evidence)


def test_inferred_is_not_inherited():
    for f, p in profiles():
        if '_resolved_inferred' in p:
            assert p['_resolved_inferred'] == bool(p.get('inferred')), f"{f}: {p.get('label')}"


def test_no_binary_releases_are_flagged():
    """The releases #439 lists with no executable in any collection."""
    want = {'2.12', '2.13', '2.14', '2.15 / 2.151', '2.16 (rev1-rev7)', '2.3'}
    have = {p.get('label') for _, p in profiles() if p.get('inferred')}
    assert want <= have, sorted(want - have)
