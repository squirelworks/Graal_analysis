"""Build the command-by-build matrix from gs1scan.py results.

    python -I matrix.py <dir with KEY.json files> > ../../npc-library/gs1-commands-by-version.tsv
    python -I matrix.py <dir> --changes        # markdown change table for the note

Build order and labels come from builds.tsv next to this script. Commands are
compared without the trailing space some tables use to mark "takes arguments".
"""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
rows = [l.split('\t') for l in (here / 'builds.tsv').read_text().splitlines()[1:]]
src = Path(sys.argv[1])
builds = []
for key, label, line, date, _source, _md5, _mode in rows:
    cmds = json.loads((src / f'{key}.json').read_text())['commands']
    builds.append((key, label, line, date, [c.strip() for c in cmds]))

order = []
for b in builds:
    for c in b[4]:
        if c not in order:
            order.append(c)


def first_last(line):
    out = {}
    for c in order:
        have = [b[1] for b in builds if b[2] == line and c in b[4]]
        out[c] = (have[0], have[-1]) if have else ('', '')
    return out


if '--changes' in sys.argv:
    print('| Build | Line | Date | Commands | Added | Removed |')
    print('|---|---|---|---:|---|---|')
    prev = None
    for key, label, line, date, cmds in builds:
        if prev is None or prev[2] != line and line == 'engine':
            base = prev[4] if prev else []
        else:
            base = prev[4]
        add = [c for c in cmds if c not in base]
        rem = [c for c in base if c not in cmds]
        fmt = lambda xs: ', '.join(f'`{x}`' for x in xs) if xs else '—'
        same = prev is not None and not add and not rem
        print(f'| {label} | {line} | {date} | {len(cmds)} | {"same as previous" if same else fmt(add)} | {"" if same else fmt(rem)} |')
        prev = (key, label, line, date, cmds)
    sys.exit()

fd, fe = first_last('delphi'), first_last('engine')
print('\t'.join(['command', 'first_delphi', 'last_delphi', 'first_engine', 'last_engine'] + [b[1] for b in builds]))
for c in sorted(order):
    print('\t'.join([c, *fd[c], *fe[c]] + ['1' if c in b[4] else '' for b in builds]))
