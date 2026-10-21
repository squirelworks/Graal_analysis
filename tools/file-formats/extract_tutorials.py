#!/usr/bin/env python3
"""Extract the embedded offline-tutorial levels from a Graal 2.0x client exe.

usage: extract_tutorials.py Graal.exe OUTDIR [--json]
Needs: pefile (pip install pefile).
Writes tutorial_<x>-<n>.graal files (raw GR-V1.03 data, as the client loads them)
and, with --json, a parsed .json next to each.
"""
import os, sys, json
import pefile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwebl import parse_grv

# RCDATA resource name -> level file name the client asks for
NAMES = {
    'TUTORIALA1': 'tutorial_a-1.graal', 'TUTORIALA2': 'tutorial_a-2.graal',
    'TUTORIALA3': 'tutorial_a-3.graal', 'TUTORIALA4': 'tutorial_a-4.graal',
    'TUTORIALB1': 'tutorial_b-1.graal', 'TUTORIALB2': 'tutorial_b-2.graal',
    'TUTORIALB2H': 'tutorial_b-2_house.graal', 'TUTORIALB3': 'tutorial_b-3.graal',
    'TUTORIALB4': 'tutorial_b-4.graal', 'TUTORIALC1': 'tutorial_c-1.graal',
    'TUTORIALC2': 'tutorial_c-2.graal', 'TUTORIALC3': 'tutorial_c-3.graal',
    'TUTORIALC4': 'tutorial_c-4.graal',
}

def main():
    exe, out = sys.argv[1], sys.argv[2]
    want_json = '--json' in sys.argv
    os.makedirs(out, exist_ok=True)
    pe = pefile.PE(exe)
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if t.id != pefile.RESOURCE_TYPE['RT_RCDATA']:
            continue
        for e in t.directory.entries:
            name = str(e.name) if e.name else None
            if name not in NAMES:
                continue
            d = e.directory.entries[0].data.struct
            data = pe.get_data(d.OffsetToData, d.Size)
            path = os.path.join(out, NAMES[name])
            open(path, 'wb').write(data)
            lv = parse_grv(data)
            print('%-26s %6d bytes  %s  links=%d npcs=%d chests=%d signs=%d' % (
                NAMES[name], len(data), lv['version'], len(lv['links']),
                len(lv['npcs']), len(lv['chests']), len(lv['signs'])))
            if want_json:
                json.dump(lv, open(path[:-6] + '.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
