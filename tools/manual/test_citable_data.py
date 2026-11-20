"""docs/citable-data.md lists every citable data file and its columns (Graal_analysis#653).
Each listed file must exist and its header row must match the listed columns, in order."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs' / 'citable-data.md'
ROW = re.compile(r'^\| `([^`]+\.tsv)` \| (.+) \|$')


def listed():
    out = {}
    for line in DOC.read_text(encoding='utf-8').splitlines():
        m = ROW.match(line)
        if m:
            out[m.group(1)] = re.findall(r'`([^`]*)`', m.group(2))
    return out


def test_doc_lists_the_evidence_index_and_token_map():
    files = listed()
    assert 'docs/evidence-index.tsv' in files
    assert 'version-profiles/version-token-map.tsv' in files


def test_listed_columns_match_each_header():
    problems = []
    for name, columns in listed().items():
        path = ROOT / name
        if not path.exists():
            problems.append(f'{name}: listed but missing')
            continue
        header = path.read_text(encoding='utf-8').splitlines()[0].rstrip('\r').split('\t')
        if header != columns:
            problems.append(f'{name}: header {header} but docs/citable-data.md lists {columns}')
    assert problems == [], '\n'.join(problems)


def test_every_version_profile_table_is_listed():
    files = listed()
    missing = [str(p.relative_to(ROOT)).replace('\\', '/') for p in sorted((ROOT / 'version-profiles').glob('*.tsv'))
               if str(p.relative_to(ROOT)).replace('\\', '/') not in files]
    assert missing == [], f'add these to docs/citable-data.md: {missing}'
