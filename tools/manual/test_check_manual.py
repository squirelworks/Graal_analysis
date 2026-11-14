"""Tests for tools/manual/check_manual.py. Standard library + pytest."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import check_manual  # noqa: E402

HEADER = 'path\tstatus\tsections\tplanned\treason\n'


def make_repo(tmp_path: Path, files: dict[str, str], sources: str | None = None) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    if sources is None:
        notes = check_manual.walk_notes(tmp_path)
        sources = HEADER + ''.join(f'{n}\tpending\t\t\t\n' for n in notes)
    (tmp_path / 'manual').mkdir(exist_ok=True)
    (tmp_path / 'manual' / 'sources.tsv').write_text(sources, encoding='utf-8')
    return tmp_path


def errors(root: Path, final: bool = False) -> list[str]:
    return check_manual.run(root, final=final).errors


REF = '<!-- manual: kind=reference status=draft -->\n'
STUB = '<!-- manual: kind=reference status=stub -->\n'


def test_real_manual_passes():
    assert errors(REPO) == []


def test_untagged_fact_fails(tmp_path):
    root = make_repo(tmp_path, {
        'protocol/a.md': '# A\n',
        'manual/01-x.md': REF + '# 1 X\n\nThe frame length is big-endian.\n',
    })
    errs = errors(root)
    assert any('no `[tag] (path)` source' in e for e in errs)


def test_tagged_fact_and_table_pass(tmp_path):
    root = make_repo(tmp_path, {
        'protocol/a.md': '# A\n',
        'manual/01-x.md': REF + (
            '# 1 X\n\nThe frame length is big-endian [srv][2.05] (protocol/a.md#frame).\n\n'
            '| Field | Source |\n| --- | --- |\n| length | [cap] (protocol/a.md) |\n'
        ),
    }, sources=HEADER + 'protocol/a.md\tcited\t1\t\t\n')
    assert errors(root) == []


def test_untagged_table_row_fails(tmp_path):
    root = make_repo(tmp_path, {
        'protocol/a.md': '# A\n',
        'manual/01-x.md': REF + '# 1 X\n\n| Field | Source |\n| --- | --- |\n| length | none |\n',
    })
    assert any(':6: factual line' in e for e in errors(root))


def test_missing_cited_path_fails(tmp_path):
    root = make_repo(tmp_path, {
        'manual/01-x.md': REF + '# 1 X\n\nA fact [bin] (protocol/missing.md).\n',
    })
    assert any('does not exist' in e for e in errors(root))


def test_citing_note_must_list_section(tmp_path):
    root = make_repo(tmp_path, {
        'protocol/a.md': '# A\n',
        'manual/01-x.md': REF + '# 1 X\n\nA fact [bin] (protocol/a.md).\n',
    })
    assert any('not listed in its sections column' in e for e in errors(root))


def test_note_without_row_fails(tmp_path):
    root = make_repo(tmp_path, {'protocol/a.md': '# A\n', 'manual/01-x.md': STUB + '# 1 X\n'},
                     sources=HEADER)
    assert any('protocol/a.md has no row' in e for e in errors(root))


def test_pending_fails_only_in_final(tmp_path):
    root = make_repo(tmp_path, {'protocol/a.md': '# A\n', 'manual/01-x.md': STUB + '# 1 X\n'})
    assert errors(root) == []
    assert any('still pending' in e for e in errors(root, final=True))


def test_excluded_needs_reason_and_cited_needs_sections(tmp_path):
    root = make_repo(tmp_path, {
        'protocol/a.md': '# A\n', 'protocol/b.md': '# B\n', 'manual/01-x.md': STUB + '# 1 X\n',
    }, sources=HEADER + 'protocol/a.md\texcluded\t\t\t\nprotocol/b.md\tcited\t\t\t\n')
    errs = errors(root)
    assert any('needs a reason' in e for e in errs)
    assert any('needs the sections' in e for e in errs)


def test_unresolved_cross_reference_fails(tmp_path):
    root = make_repo(tmp_path, {
        'manual/01-x.md': REF + '# 1 X\n\n## 1.1 Y\n\n→ §1.1 and → §1.2\n\nSee → App. E#3.\n',
        'manual/app-e.md': STUB + '# Appendix E. Open\n\n### E#1 One\n',
    })
    errs = errors(root)
    assert any('§1.2 does not resolve' in e for e in errs)
    assert not any('§1.1 does not' in e for e in errs)
    assert any('App. E#3 does not resolve' in e for e in errs)


def test_stub_rejects_content(tmp_path):
    root = make_repo(tmp_path, {
        'manual/01-x.md': STUB + '# 1 X\n\n> Status: stub.\n\nSome text [bin] (manual/01-x.md).\n',
    })
    assert any('stub file has content' in e for e in errors(root))


def test_missing_header_fails(tmp_path):
    root = make_repo(tmp_path, {'manual/01-x.md': '# 1 X\n'})
    assert any('missing `<!-- manual' in e for e in errors(root))


def test_leak_patterns(tmp_path):
    lines = [
        'FUN_' + '0040' + '1000',
        '0x' + '0040' + '1a2b',
        'loc' + 'alhost',
        'host 10.' + '1.2.3',
        'graal' + 'online.com',
    ]
    body = '\n\n'.join(f'{line} [bin] (manual/01-x.md)' for line in lines)
    root = make_repo(tmp_path, {'manual/01-x.md': REF + '# 1 X\n\n' + body + '\n'})
    errs = [e for e in errors(root) if 'leak' in e]
    assert len(errs) >= len(lines)


def test_version_string_is_not_an_ip(tmp_path):
    root = make_repo(tmp_path, {
        'manual/01-x.md': REF + '# 1 X\n\nFileVersion 2.2.2.0 [bin] (manual/01-x.md).\n',
    })
    assert not any('dotted IP' in e for e in errors(root))


def test_message_index_completeness(tmp_path):
    ids = '| Id | Wire | Name |\n|---:|:---:|---|\n| 0 | 0x20 | `PLO_LEVELBOARD` |\n| 1 | 0x21 | `PLI_LEVELWARP` |\n'
    root = make_repo(tmp_path, {
        'protocol/packet-ids.md': '# Ids\n\n' + ids,
        'manual/app-a.md': ('<!-- manual: kind=reference status=draft -->\n# Appendix A. Messages\n\n'
                            '| Name | Section | Source |\n| --- | --- | --- |\n'
                            '| PLO_LEVELBOARD | → §1 | [srv] (protocol/packet-ids.md) |\n'),
    }, sources=HEADER + 'protocol/packet-ids.md\tpending\tA\t\t\n')
    errs = errors(root)
    assert any('PLI_LEVELWARP' in e for e in errs)
    assert not any('PLO_LEVELBOARD from' in e for e in errs)


def test_prop_index_completeness(tmp_path):
    props = ('# Props\n\n## PLPROP (player)\n\n| Id | Name |\n|---|---|\n| 0 | NICKNAME |\n| 1 | MAXPOWER |\n\n'
             '## BDPROP (baddy)\n\n| Id | Name |\n|---|---|\n| 2 | MODE |\n')
    root = make_repo(tmp_path, {
        'protocol/player-props.md': props,
        'manual/app-b.md': ('<!-- manual: kind=reference status=draft -->\n# Appendix B. Props\n\n'
                            '| Kind | Id | Source |\n| --- | --- | --- |\n'
                            '| PLPROP | 0 | [srv] (protocol/player-props.md) |\n'),
    }, sources=HEADER + 'protocol/player-props.md\tpending\tB\t\t\n')
    errs = errors(root)
    assert any('PLPROP 1 ' in e for e in errs)
    assert any('BDPROP 2 ' in e for e in errs)
    assert not any('PLPROP 0 ' in e for e in errs)


def test_real_props_note_parses():
    props = check_manual.required_props(REPO)
    kinds = {kind for kind, _ in props}
    assert {'PLPROP', 'NPCPROP', 'BDPROP'} <= kinds
    assert len(check_manual.required_message_names(REPO)) > 100


def test_build_ids_need_rows_in_their_direction(tmp_path):
    source = 'version-profiles/plo-handled-ids-by-build.tsv'
    root = make_repo(tmp_path, {
        source: 'build\thandled_server_to_client_ids\nexample\t101-102,196\n',
        'manual/app-a.md': REF + (
            '# Appendix A. Messages\n\n## A.1 Client to server\n\n'
            '| Id | Name | Source |\n| --- | --- | --- |\n'
            f'| 101 | other direction | [bin] ({source}) |\n\n'
            '## A.2 Server to client\n\n'
            f'Ids 101, 102 and 196 are mentioned here [bin] ({source}).\n'
        ),
    }, sources=HEADER + f'{source}\tpending\tA\t\t\n')
    errs = errors(root)
    for mid in (101, 102, 196):
        assert any(f'PLO id {mid} ' in e for e in errs)


def test_build_ids_accept_named_and_unnamed_rows(tmp_path):
    source = 'version-profiles/plo-handled-ids-by-build.tsv'
    root = make_repo(tmp_path, {
        source: 'build\thandled_server_to_client_ids\nexample\t101-102,196\n',
        'manual/app-a.md': REF + (
            '# Appendix A. Messages\n\n## A.2 Server to client\n\n'
            '| Id | Name | Source |\n| --- | --- | --- |\n'
            f'| 101 | PLO_BOARDPACKET | [bin] ({source}) |\n'
            f'| 102 | PLO_FILE | [bin] ({source}) |\n'
            f'| 196 | (no name) | [bin] ({source}) |\n'
        ),
    }, sources=HEADER + f'{source}\tpending\tA\t\t\n')
    assert errors(root) == []


def test_build_pli_ids_are_checked_separately(tmp_path):
    source = 'version-profiles/pli-sent-ids-by-build-20x.tsv'
    root = make_repo(tmp_path, {
        source: 'build\tclient_to_server_ids_the_binary_can_send\nexample\t0-1,80\n',
        'manual/app-a.md': REF + (
            '# Appendix A. Messages\n\n## A.1 Client to server\n\n'
            '| Id | Name | Source |\n| --- | --- | --- |\n'
            f'| 0 | PLI_LEVELWARP | [bin] ({source}) |\n'
            f'| 1 | PLI_BOARDMODIFY | [bin] ({source}) |\n\n'
            '## A.2 Server to client\n\n'
            '| Id | Name | Source |\n| --- | --- | --- |\n'
            f'| 80 | other direction | [bin] ({source}) |\n'
        ),
    }, sources=HEADER + f'{source}\tpending\tA\t\t\n')
    errs = errors(root)
    assert len(errs) == 1
    assert 'PLI id 80 ' in errs[0]
