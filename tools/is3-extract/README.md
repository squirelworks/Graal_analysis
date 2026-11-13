# is3-extract

Unpacks an InstallShield 3 data archive (`_SETUP.1`, `DATA.Z`) statically, so the game files of the 1999 installers
(1.21, 1.25, 1.27) can be read without running `SETUP.EXE`. Standard library only; it never executes anything.

```
python -I is3x.py list    _SETUP.1
python -I is3x.py extract _SETUP.1 <outdir>
```

The 1.25 and 1.27 installers are self-extracting zips; open them with any zip tool first to get `_SETUP.1`.
`extract` writes `<outdir>/<group>/<name>` and marks each line `OK` when the unpacked size matches the directory entry.
The archive layout and the decoder (a port of the PKWARE DCL `blast` algorithm) are described in the docstring.

Checked on the 1.21 package: the unpacked `Graal.exe`, `GServer.exe` and `remotecontrol.exe` have the MD5s that
`client-internals/build-catalogue.md` records for 1.21. Results: [`client-internals/gserv-125-127-builds.md`](../../client-internals/gserv-125-127-builds.md).

Run it from a directory outside the extracted archives. Leave any account, password or guild lists the packages carry
out of notes and commits.
