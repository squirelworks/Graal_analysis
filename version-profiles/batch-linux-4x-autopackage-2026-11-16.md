# Batch Linux 4.03r1 / 4.10r2 / 4.11 (autopackage ELFs)

Date: 2026-11-16

The Batch-1 web autopackages for Linux **4.03r1**, **4.10r2** and **4.11** are byte-identical to the already-held setup packages whose extracted `graal` ELFs were inventoried with the 2026-11-14 archive work. This note records that identity, a static string ladder against the Known **4.04r2** Linux control, and what remains open. Tags: **[bin]** · **[file]** · **[inf]**. Evidence ids: `BATCH1-LINUX4-APKG-20261116`, `BATCH1-WIN411-THINSTALL-ID-20261116`.

Related: `protocol/v4x-windows-403r3-411.md` (Windows Thinstall twins), `protocol/v4x-clients.md`, `client-internals/version-token-catalogue.md`.

## Package identity

| Label | Autopackage `SoftwareVersion` | Login token (catalogue grade B) | vs Known / prior |
|---|---|---|---|
| 4.03r1 | `4.0301` | `G3D11125` | No repro folder; ELF already extracted beside the matching setup package |
| 4.04r2 (control) | `4.0402` | `G3D19026` | Batch-1 Known; wire-known |
| 4.10r2 | `4.102` | `G3D28076` | No repro folder; same extract path as above |
| 4.11 | `4.11` | `G3D28076` | Same token as Linux 4.10r2; Windows 4.11 is `G3D26076` |

The autopackage shell is Autopackage 1.0.7 (`skipLines` / `metaSize` / `dataSize`). The payload after the meta blob is **not** a plain gzip/bzip/tar stream; extracting it needs the autopackage tooling (or a prior extract). For this pass the Batch packages were hash-matched to those prior extracts, and the `graal` ELFs were read from there. They are ordinary ELF32 i386, not UPX. **[file][bin]**

Login tokens are **not** contiguous ASCII and `g3dref.py` does not recover them from these Linux images (encrypted / connect-routine table, as in the Batch METADATA pass). Values above are the 2026-11-13 catalogue reads, not a new wire capture. All four builds still carry the literals `GSERVL01` and `GLEVNW01`. **[bin]**

## String ladder (static)

Compared to Linux **4.04r2** as control:

**4.03r1 → 4.04r2**

- Adds tile-layer surface (`TTilesLayer`, `tilelayers`, `tilelayercount`, `layerindex`).
- Adds music status/tags (`getMusicStatus`, `getMusicTags`, `onMusicDataReceived`).
- Adds `findnpcbyid`, `particleeffect` / `weathereffect` prefs, and script help text for joining/leaving classes.
- Drops `onKeyRepeat`. **[bin]**

This matches the Windows engine callback story in `v4x-windows-403r3-411.md` (tile layers and music before packet 107). **[inf]**

**4.04r2 → 4.10r2**

- Large Flash / SWF stack appears (`TFlash*`, `TShowImg_Flash`, font types).
- TrueType preference (`$pref::Video::truetypefonts`), `getclass`, `isbuddy`, `TJoinedClassesProperty`.
- Server version-gate strings (“Please update your Graal…” / older-server warning).
- Binary is smaller; many stock Torque `ConcreteClassRep` names disappear from the string table (engine trim / rebuild, not proved here as behaviour loss). **[bin]**

**4.10r2 → 4.11**

- Adds `playerrotation`, `playerstretchx` / `playerstretchy`, `playerzoom` — the same script words called out for Windows 4.11. **[bin]**

## Windows Batch twins (identity only)

Batch-1 Web-Discovered `Graal4Setup.exe` for **4.03r3** and **4.11** are byte-identical to the Batch-1 Upload installer copies. Those are the Thinstall 2.x packages already unpacked and profiled in `protocol/v4x-windows-403r3-411.md` (tokens `G3D09125` / `G3D26076`, handled-id and callback deltas). No second Thinstall unpack was required for this note. **[file]**

## Open

1. Publish or script a reproducible autopackage payload extract (so future agents need not depend on a prior extract tree).
2. Full PLI/PLO / prop tables for Linux 4.03r1 and 4.10r2 comparable to 4.04r2 / 4.20 profiles.
3. Loopback labs for Linux 4.10r2 / 4.11 (Flash panel, class join, version-gate strings).
