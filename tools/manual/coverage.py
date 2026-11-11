#!/usr/bin/env python3
"""Coverage report: which distinctive terms of each cited note the manual lacks.

Standard library only. Roadmap item 0.0.5 (a) in issue #191.

    python tools/manual/coverage.py                 # summary per Part
    python tools/manual/coverage.py --notes         # also one line per note with misses
    python tools/manual/coverage.py --tsv out.tsv   # every miss: path, part, term
    python tools/manual/coverage.py --strict        # exit 1 on any unexplained miss

A note is measured when its `manual/sources.tsv` row is `cited` and it is a
Markdown file. Its distinctive terms are the ones `check_carry.py` uses
(message names, hex constants, format magics, short inline-code spans). A
term is a miss when it does not appear in the manual text.

`check_carry.py` only fails a note below a 30% floor. This report lists
every miss, so the per-Part prose passes can either carry each term or
explain it in `manual/coverage-explained.tsv` (columns `path`, `term`,
`reason`; a `term` of `*` explains every miss of that note). The 0.0.5
target is a report with no unexplained misses.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_carry  # noqa: E402

EXPLAINED = Path('manual') / 'coverage-explained.tsv'
PARTS = {'0': '0', '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V', '6': 'VI',
         '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X', '11': 'XI'}


def part_of(sections: list[str]) -> str:
    """The Part of a note's first numbered citing section, else its first appendix."""
    for s in sections:
        head = s.split('.')[0]
        if head in PARTS:
            return PARTS[head]
    return f'App. {sections[0]}' if sections else '?'


def load_explained(root: Path) -> dict[str, dict[str, str]]:
    path = root / EXPLAINED
    out: dict[str, dict[str, str]] = defaultdict(dict)
    if not path.is_file():
        return out
    with open(path, encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            if (row.get('reason') or '').strip():
                out[row['path']][row['term']] = row['reason']
    return out


def run(root: Path) -> list[dict]:
    """One record per measured note: path, part, terms, missing, unexplained."""
    mtext = check_carry.manual_text(root)
    explained = load_explained(root)
    records = []
    for row in check_carry.load_rows(root):
        if row.get('status') != 'cited':
            continue
        rel = row['path']
        tc = check_carry.term_carry(root, rel, mtext)
        if tc is None:
            continue
        n, _carry, missing = tc
        ex = explained.get(rel, {})
        unexplained = [] if '*' in ex else [t for t in missing if t not in ex]
        records.append({
            'path': rel,
            'part': part_of(check_carry.section_list(row.get('sections') or '')),
            'terms': n,
            'missing': missing,
            'unexplained': unexplained,
        })
    return records


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--notes', action='store_true', help='one line per note with misses')
    ap.add_argument('--tsv', type=Path, help='write every miss to this TSV file')
    ap.add_argument('--strict', action='store_true', help='exit 1 on any unexplained miss')
    args = ap.parse_args(argv)
    records = run(args.root)

    by_part: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_part[r['part']].append(r)
    order = list(PARTS.values())
    print(f'{"Part":8} {"notes":>5} {"terms":>6} {"missed":>6} {"unexpl.":>7} {"carried":>7}')
    for part in sorted(by_part, key=lambda p: (order.index(p) if p in order else 99, p)):
        rs = by_part[part]
        terms = sum(r['terms'] for r in rs)
        missed = sum(len(r['missing']) for r in rs)
        unexpl = sum(len(r['unexplained']) for r in rs)
        print(f'{part:8} {len(rs):5d} {terms:6d} {missed:6d} {unexpl:7d} {1 - missed / terms:7.0%}')
    total_terms = sum(r['terms'] for r in records)
    total_missed = sum(len(r['missing']) for r in records)
    total_unexpl = sum(len(r['unexplained']) for r in records)
    print(f'{"total":8} {len(records):5d} {total_terms:6d} {total_missed:6d} {total_unexpl:7d} '
          f'{1 - total_missed / max(total_terms, 1):7.0%}')

    if args.notes:
        for r in sorted(records, key=lambda r: (-len(r['unexplained']), r['path'])):
            if r['unexplained']:
                print(f'{len(r["unexplained"]):4d}/{r["terms"]:<4d} {r["part"]:6} {r["path"]}: '
                      f'{", ".join(r["unexplained"][:8])}')

    if args.tsv:
        with open(args.tsv, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t', lineterminator='\n')
            w.writerow(['path', 'part', 'term', 'explained'])
            for r in records:
                for t in r['missing']:
                    w.writerow([r['path'], r['part'], t, 'no' if t in r['unexplained'] else 'yes'])

    if args.strict and total_unexpl:
        print(f'coverage: {total_unexpl} unexplained miss(es)')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
