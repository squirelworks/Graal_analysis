#!/usr/bin/env python3
"""Unpack a Thinstall 2.x package (the Windows Graal4Setup.exe downloads) without running it.

usage: python3 -I unpack.py <packed.exe> <workdir> <outdir> [name-substring ...]

Step 1 (emu.py, first run): emulate the packer stub until it hands over to the Thinstall runtime it
unpacked into memory; save a snapshot.
Step 2 (emu.py, second run): emulate the runtime start-up with stubbed Windows APIs until it reaches
the virtual program's entry point, where it stops; save a second snapshot. The runtime's virtual file
directory is now in memory.
Step 3 (vfsx.py): read the directory from the snapshot and decode every file's 64 KiB blocks with
the runtime's own block decoder, called in the emulator.

No code of the packaged program is executed. emu.py needs argtab.json (stdcall argument counts),
made once by argtab.py from Wine's i386 PE DLLs.
"""
import os, subprocess, sys

exe, work, out = sys.argv[1:4]
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(work, exist_ok=True)
pref = os.path.join(work, 'pkg')
for p in (pref + '.snap', pref + '.snap3'):
    if os.path.exists(p): os.remove(p)
for step in (1, 2):
    r = subprocess.run([sys.executable, '-I', os.path.join(here, 'emu.py'), exe, pref], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())
    if not os.path.exists(pref + ('.snap' if step == 1 else '.snap3')):
        sys.exit('emulation step %d did not reach its stop point' % step)
subprocess.run([sys.executable, '-I', os.path.join(here, 'vfsx.py'), exe, pref + '.snap3', out] + sys.argv[4:], check=True)
