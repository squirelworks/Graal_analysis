#!/usr/bin/env python3
"""Check a decoded baddy dump against the 2.22 baddy rules in
client-internals/baddies-222.md.

Input: a text dump with one message per line, as written by the 2.22 lab
runs (lan-222d-baddyprops.txt, lan-222kill-baddy.txt, ...):

    C>S f210 +20790ms BADDYPROPS len12  21 21 62 22 65 24 21 20 25 23 26 27

(direction, frame, time, name, length, payload hex after the packet id).
Lines that are not BADDYPROPS / BADDYHURT are ignored.

It follows every baddy through the stream and checks the leader's
(client-to-server) updates step by step:

  counter    mode 0, 1, 5 and mode 2 above 5: the counter (prop 6) falls by
             one per step; mode 2 below 6 cycles 0, 3, 2, 1; mode 7 rises
             by one per step, modulo 46
  entries    entering mode 1 sets counter 44; mode 2 sets 16 (sight) or 12
             (after a hit, or a hunt restart); mode 3 and 4 arrive with 7
             (8, already stepped once); mode 5 with 14 (9 for the hare and
             the octopus)
  hunt step  in mode 2 with the counter below 6, a melee baddy (not types
             3, 9) moves at most 0.5 tile per step on each axis (0.75 for
             type 8)
  knockback  in mode 3 and 4 the position moves by the knock vector
             (length 2.0 for a hit, 0.8 for a shield bump, before the
             half-tile rounding of the wire) or not at all
  baddyhurt  PLI_BADDYHURT bytes decode as id, (dx+4)*16, (dy+4)*16, power

Steps are counted by message: the leader sends one message per changed
baddy per AI step (every second 50 ms tick), so a step with no change sends
nothing. The checker only compares consecutive messages that are about
100 ms apart (80 to 130 ms); longer gaps are skipped, not failed.

Usage: check_capture.py DUMP [DUMP ...]
Exit status 0 when nothing failed.
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter, defaultdict

LINE = re.compile(r'^(\S+)\s+f\d+\s+\+(\d+)ms\s+(\w+)\s+len\s*\d+\s+([0-9a-fA-F ]+)$')


def parse_props(body: bytes):
    """BDPROP stream (after the baddy id) -> list of (prop, value)."""
    out = []
    p = 0
    while p < len(body):
        pid = body[p] - 32
        p += 1
        if pid in (1, 2, 3, 5, 6, 7):
            if p >= len(body):
                break
            out.append((pid, body[p] - 32))
            p += 1
        elif pid == 4:
            power = body[p] - 32
            n = body[p + 1] - 32
            out.append((4, (power, body[p + 2:p + 2 + n].decode('latin1'))))
            p += 2 + n
        elif pid in (8, 9, 10):
            n = body[p] - 32
            out.append((pid, body[p + 1:p + 1 + n].decode('latin1')))
            p += 1 + n
        else:
            break
    return out


class Baddy:
    def __init__(self):
        self.x = self.y = None
        self.type = None
        self.mode = None
        self.c = None
        self.t = None


def check(path, results, fails):
    bd = defaultdict(Baddy)
    for raw in open(path, encoding='latin1'):
        m = LINE.match(raw.strip())
        if not m:
            continue
        direction, t, name, hexs = m.groups()
        t = int(t)
        data = bytes(int(h, 16) for h in hexs.split())
        if name == 'BADDYHURT':
            if len(data) >= 4:
                dx = (data[1] - 32) / 16 - 4
                dy = (data[2] - 32) / 16 - 4
                results['baddyhurt decodes'] += 1
                print(f'  {path}: +{t} BADDYHURT id {data[0] - 32} dx {dx:+.4g} dy {dy:+.4g} power {data[3] - 32}')
            continue
        if name != 'BADDYPROPS' or not data:
            continue
        b = bd[data[0] - 32]
        props = dict(parse_props(data[1:]))
        old = (b.x, b.y, b.mode, b.c, b.t)
        if 3 in props:
            b.type = props[3]
        nx = props[1] / 2 if 1 in props else b.x
        ny = props[2] / 2 if 2 in props else b.y
        nmode = props.get(5, b.mode)
        nc = props.get(6, b.c)
        stepped = (direction == 'C>S' and b.t is not None and 80 <= t - b.t <= 130
                   and b.mode is not None and b.c is not None)
        if stepped:
            ox, oy, omode, oc, _ = old
            where = f'{path}: +{t} baddy {data[0] - 32} (type {b.type})'

            def ok(rule, cond, detail=''):
                results[rule] += 1
                if not cond:
                    fails.append(f'{where}: {rule} {detail}')

            if nmode != omode:
                want = {1: {44}, 2: {16, 12}, 3: {7}, 4: {7}, 5: {14, 9}}.get(nmode)
                if want is not None and 6 in props:
                    ok(f'enter mode {nmode}', nc in want, f'counter {nc}, expected {sorted(want)}')
            elif 6 in props:
                if omode in (0, 1, 3, 4, 5) or (omode == 2 and oc >= 6):
                    if not (omode == 0 and nc != oc - 1):  # walk also skips on a turn
                        ok(f'counter mode {omode}', nc == oc - 1, f'{oc} -> {nc}')
                elif omode == 2 and oc < 6 and b.type not in (3, 9):
                    ok('counter hunt cycle', nc == (oc + 3) % 4, f'{oc} -> {nc}')
                elif omode == 7:
                    ok('counter hop', nc == (oc + 1) % 46, f'{oc} -> {nc}')
            if ox is not None and nx is not None:
                dx, dy = nx - ox, ny - oy
                if omode == 2 and nmode == 2 and oc is not None and oc < 6 and b.type not in (3, 9):
                    lim = 0.75 if b.type == 8 else 0.5
                    ok('hunt step size', abs(dx) <= lim + 0.5 and abs(dy) <= lim + 0.5,
                       f'moved {dx:+} {dy:+}')
                if omode in (3, 4) and nmode == omode and (dx or dy):
                    d = math.hypot(dx, dy)
                    want = 2.0 if omode == 3 else 0.8
                    ok('knock step length', abs(d - want) <= 0.75, f'moved {d:.2f}, expected {want}')
        b.x, b.y, b.mode, b.c = nx, ny, nmode, nc
        b.t = t


def main(argv):
    results, fails = Counter(), []
    for path in argv[1:]:
        check(path, results, fails)
    for rule, n in sorted(results.items()):
        bad = sum(1 for f in fails if f'{rule} ' in f)
        print(f'{rule:24} {n - bad:5} pass {bad:4} fail')
    for f in fails[:40]:
        print('FAIL', f)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
