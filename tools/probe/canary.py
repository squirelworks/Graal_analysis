#!/usr/bin/env python3
"""canary: classify the HUD bomb count in probe screenshots against two reference shots.

  canary.py RUNDIR [REF_LOST REF_LANDED] [x0 y0 x1 y1]

Each `shot` in RUNDIR is compared with the reference shots (default ref-01.png: the count
was reset and the canary was lost; ref-99.png: the canary landed) inside the bomb-count box
(default 320 44 360 66 on a 1024x768 6.03r7 window). Prints one line per shot: name,
verdict (landed / lost / unclear), and the two distances.
"""
import glob, os, sys
from PIL import Image


def box(path, b):
    return list(Image.open(path).convert('L').crop(b).getdata())


def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def main():
    d = sys.argv[1]; a = sys.argv[2:]
    lost, landed = (a[0], a[1]) if len(a) >= 2 else ('ref-01.png', 'ref-99.png')
    b = tuple(int(x) for x in a[2:6]) if len(a) >= 6 else (320, 44, 360, 66)
    rl, rd = box(os.path.join(d, lost), b), box(os.path.join(d, landed), b)
    for f in sorted(glob.glob(os.path.join(d, '*.png'))):
        n = os.path.basename(f)[:-4]
        if n.startswith('ref-'):
            continue
        x = box(f, b); dl, dd = dist(x, rl), dist(x, rd)
        v = 'landed' if dd < dl * 0.5 else 'lost' if dl < dd * 0.5 else 'unclear'
        print('%s\t%s\t%.1f\t%.1f' % (n, v, dd, dl))


if __name__ == '__main__':
    main()
