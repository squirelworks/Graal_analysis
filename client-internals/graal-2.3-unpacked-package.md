# What the "Graal v2.3 [Unpacked][Cracked]" package is

Date: 2026-11-12. A static comparison only: no executable was run. The package (held as both a
`.7z` and a `.rar` with the same members) was hashed member by member and compared with every
other copy of the same file names in the held installs. **[file]**

| Member | What it is | Tag |
| --- | --- | --- |
| `Graal.exe` | byte-identical to the `Graal v2.310 [unThinstall][unPeTite-Bass.dll][CRC-Fix]` package's exe, and to the 2.31 client (`Graal_231.exe`) found in many installs. So "2.3" is **2.31** with the Thinstall wrapper removed and a CRC check patched; no differing copy exists to locate the patch | [file] |
| `bass.dll` | identical only to the v2.310 package's copy: the **unpacked** BASS library (rebuilt import sections), whose timestamp matches the packed BASS shipped with 2.22. The 2.22 install itself ships a different packed BASS | [file] |
| `GraalEditor.exe` | identical to the 2.22 / Reborn copies, still packed | [file] |
| `RemoteControl.exe` | the same size as the 2.22 / Reborn copies, but 4 bytes differ in the code that builds the listserver host name one character at a time. This copy builds the **original** official list host with port 14922; the 2.22 / Reborn copy builds the Reborn replacement host. So this RC is the unpatched original | [file] |
| `GraalShop.exe` | version 1.0.0.0, an older build than 2.22's 1.1.1.0 (not a patch) | [file] |
| `GraalLevelGen.exe` | a different build from the NewMain copy; no other copy held | [file] |
| `gif2mng`, `TerrainGenerator`, `dungeongen`, `hvdi.dll` | identical to the 2.22 copies | [file] |

So the package adds no new client build: it is 2.31 with its wrapper removed, plus the original
(unpatched) 2.22-era RemoteControl and older tool builds. For 2.31 itself see
[build-catalogue.md](build-catalogue.md) and [../protocol/client-versions.md](../protocol/client-versions.md);
for the RC host patch see [../tools/remotecontrol-lineage.md](../tools/remotecontrol-lineage.md).
