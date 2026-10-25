"""Default listserver endpoint of every version profile, checked and printed.

usage: python3 list_ports.py [--check] [--md | --tsv]      (run from this directory)

Reads the three profile files (v133-v139.toml, 141-217.toml, ../../version-profiles/2.22-2.31.toml)
and prints one row per profile: label, host, port, kind (legacy or supported), status
(confirmed or assumed), and the built-in host and port the binary carries.

The rule (Seihai documentation/port-rule.md):
  - host is always listserver.graal.in
  - 14921 is dead and is never a default
  - the default follows the login type the profile sends (the public listserver picks its
    reply by login type, not by version or token; matrix of 2026-10-25):
    legacy = classic login (1.41 to 2.17, including 2.05) defaults to 14923,
    supported = gen-5 login (2.22, 2.3, 2.31) defaults to 14922
  - the binary's own host and port are history: built_in_host / built_in_port
--check exits 1 and prints every row that breaks the rule.
"""
import sys, tomllib
from pathlib import Path
import importlib.util

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('resolve', here / 'resolve.py')
resolve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resolve)

HOST = 'listserver.graal.in'
PORTS = {'legacy': 14923, 'supported': 14922}
# 141-217.toml ids in release order, with the labels the profile table uses.
IDS = [('v141r1', '1.41'), ('v142', '1.42'), ('v200', '2.00'), ('v201', '2.01'), ('v202', '2.02'),
       ('v202r2', '2.02 rev2'), ('v203', '2.03'), ('v204', '2.04'), ('v205', '2.05'),
       ('v21', '2.1'), ('v212', '2.12'), ('v213', '2.13'), ('v214', '2.14'), ('v215', '2.15'),
       ('v216', '2.16'), ('v217', '2.17')]


def rows():
    out = []
    for v in tomllib.load(open(here / 'v133-v139.toml', 'rb'))['version']:
        out.append(dict(label=v['label'], listserver=None))
    by_id = {p['id']: p for p in resolve.resolve(tomllib.load(open(here / '141-217.toml', 'rb')))}
    for tid, label in IDS:
        out.append(dict(label=label, listserver=by_id[tid]['listserver']))
    doc5 = tomllib.load(open(here / '../../version-profiles/2.22-2.31.toml', 'rb'))
    d5 = doc5['defaults']['gen5']['listserver']
    for v in doc5['version']:
        ls = dict(d5)
        if 'listserver_port_status' in v:
            ls['port_status'] = v['listserver_port_status']
        out.append(dict(label=v['label'], listserver=ls))
    return out


def check(rs):
    bad = []
    for r in rs:
        ls = r['listserver']
        if ls is None:
            continue
        L = r['label']
        if ls.get('host') != HOST:
            bad.append(f"{L}: host {ls.get('host')!r} is not {HOST}")
        if ls.get('port') == 14921:
            bad.append(f'{L}: default port is the dead 14921')
        kind = ls.get('kind')
        if kind not in PORTS:
            bad.append(f'{L}: kind {kind!r} is not legacy or supported')
        elif ls.get('port') != PORTS[kind]:
            bad.append(f"{L}: {kind} must default to {PORTS[kind]}, not {ls.get('port')}")
        if ls.get('port_status') not in ('confirmed', 'assumed'):
            bad.append(f"{L}: port_status {ls.get('port_status')!r} is not confirmed or assumed")
    labels = [r['label'] for r in rs if r['listserver']]
    split = {r['label']: r['listserver']['kind'] for r in rs if r['listserver']}
    for L in labels:
        want = 'supported' if L in ('2.22', '2.3', '2.31') else 'legacy'
        if split[L] != want:
            bad.append(f'{L}: expected {want} (classic login 1.41 to 2.17 legacy, gen-5 login 2.22 and later supported)')
    return bad


def table(rs):
    head = ['version', 'host', 'port', 'kind', 'port status', 'built-in host', 'built-in port']
    body = []
    for r in rs:
        ls = r['listserver']
        if ls is None:
            body.append([r['label'], '-', '-', 'no listserver', '-', '-', '-'])
        else:
            body.append([r['label'], ls['host'], str(ls['port']), ls['kind'], ls['port_status'],
                         ls.get('built_in_host', '-'), str(ls.get('built_in_port', '-'))])
    return head, body


if __name__ == '__main__':
    rs = rows()
    if '--check' in sys.argv:
        bad = check(rs)
        for b in bad:
            print(b)
        sys.exit(1 if bad else 0)
    head, body = table(rs)
    if '--tsv' in sys.argv:
        for r in [head] + body:
            print('\t'.join(r))
    else:
        print('| ' + ' | '.join(head) + ' |')
        print('|' + '---|' * len(head))
        for r in body:
            print('| ' + ' | '.join(r) + ' |')
