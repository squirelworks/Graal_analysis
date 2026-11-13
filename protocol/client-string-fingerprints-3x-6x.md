# String fingerprints of the 3.x to 6.x clients

Date: 2026-11-14. A plain string probe of seven client images: which marker strings each one contains. Nothing was run and no code was read. Tags: **[bin]** found (or not found) in the image by the probe.

The probe is `tools/string-fingerprint/probe.py`. It reports a string as present in ASCII, present only as UTF-16, or absent. Absence only means the bytes are not stored in the clear. A string can still be built at run time, or sit inside a compressed or encrypted block, so an absent marker does not prove the feature is missing.

This page collects the cuts between versions that a server author can use to tell builds apart, plus a few facts the per-version notes do not have yet. Protocol behaviour lives in those notes: `v3x-clients.md`, `v4x-clients.md`, `v5x-clients.md`, `v5v6-windows-unpacked.md`, `v6x-clients.md`, `v6-repro-facts.md`, `v6113-pli.md` and `v6-props.md`.

## The images

| Column | Build | FileVersion | sha256 prefix |
|---|---|---|---|
| 3.04 | Linux 3.04 `graalexe` (ELF32, i386) | none (ELF) | `6e9e35a3` |
| 4.20 host | Windows 4.20r8, unpacked folder, Delphi host exe | 4.2.0.8 | `32d67755` |
| 4.20 engine | Windows 4.20r8, unpacked folder, `GraalEngine.dll` | — | `828e9311` |
| 5.30 | Windows 5.30r3, unpacked dump | 5.303 | `1174175b` |
| 5.31 | Windows 5.31r4, unpacked dump | 5.314 | `fc2ff99f` |
| 6.03 | Windows 6.0.3.7, unpacked dump | 6.037 | `2be6bf4b` |
| 6.11 | Windows 6.1.1.3, unpacked dump | 6.113 | `1049be8d` |

5.0.0.7 is left out: the only unpacked copy here comes from a folder that also holds a modified launcher. The 5.00r7 facts are in `v5x-clients.md`.

## The table

Y = ASCII, w = UTF-16 only, · = not found. **[bin]**

| Marker | 3.04 | 4.20 host | 4.20 engine | 5.30 | 5.31 | 6.03 | 6.11 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `Torque Game Engine Demo`, `SimObject`, `Con::` | Y | · | · | · | · | · | · |
| `descipher` | Y | · | · | · | · | · | · |
| `TGraalConnection` | Y | · | Y | Y | Y | Y | Y |
| `graal://`, `graal3://` | · | Y | Y | Y | Y | Y | Y |
| `setGraalProtocolString` | · | Y | Y | · | · | · | · |
| `getGraalLoginInfo` | · | · | Y | · | · | · | · |
| `hvdiPacketEncode`, `hcryptEncryptPacket` | · | · | Y | · | · | · | · |
| `fixedudpport`, `noudp` | Y | Y | Y | Y | Y | · | · |
| `14899` | · | Y | · | · | · | · | · |
| `14900` | · | · | · | Y | Y | · | · |
| `quattro_lib` | · | · | · | Y | Y | Y | Y |
| `GRESCR01` | · | · | · | Y | Y | Y | Y |
| `GSERVL01`, `Z3-V1.04` | Y | · | Y | Y | Y | · | · |
| `GRMAP001`, `GWEBL001`, `GR-V1.04` | Y | · | Y | Y | Y | Y | Y |
| `GRPKG001`, `.gupd` | · | · | Y | Y | Y | Y | Y |
| `Illegal characters in the outgoing data` | · | · | · | Y | Y | Y | Y |
| `Received illegal data (1)` / `(2)` | · | · | · | Y | Y | Y | · |
| `Received invalid data (1)` / `(2)` / `(3)` | · | · | · | · | · | · | Y |
| `Cannot send data, socket is not initialized yet.` | · | · | · | · | · | · | Y |
| `Arc4Process`, `Arc4SetKey` | · | · | · | · | · | Y | Y |
| `DOQLHRbY` | · | · | · | · | · | · | Y |
| `StartScript_Connector`, `StartScript_Fail`, `scriptip`, `scriptsslcipher` | · | · | · | · | · | · | Y |
| `StartScript_Profiles` | · | · | Y | Y | Y | Y | Y |
| `StartScript_QuitDialog` | · | · | Y | Y | · | · | · |
| `onSend…` names (count) | 0 | 0 | 0 | 0 | 0 | 0 | 55 |
| `tclient_` | · | · | · | · | · | · | Y |
| `onReceiveUDPData`, `onReceiveDataPackage`, `onBind` | · | · | · | Y | Y | Y | Y |
| `switchToOpenGL` | · | · | · | Y | Y | · | · |
| `setplayerprop`, `playerhp` | Y | · | Y | · | · | · | · |
| `sendServerText` | · | Y | Y | · | · | · | · |
| `onPlayerLogin`, `onRemotePlayerChats` | · | · | Y | Y | Y | Y | Y |
| `Mass message:` | Y | · | Y | Y | Y | Y | Y |
| `guest_` | · | · | Y | Y | Y | Y | Y |
| `-guestaccount` | · | Y | · | Y | Y | Y | Y |
| `Client-version: ` | · | · | · | Y | Y | Y | Y |
| `User-Agent: Graal/` | · | · | Y | · | · | Y | Y |
| `Linux Cyberjoueur` | · | w | · | Y | Y | Y | Y |
| `Eurocenter Games` | · | · | · | · | · | · | w |

## What the table shows

- **3.04 is the only image with Torque's console and object system in it.** From the 4.20 split onwards the 2D engine has no `SimObject` or `Con::`. (The 4.x 3D plug-in is a separate DLL, see `v4x-clients.md`.) **[bin]**
- **`setGraalProtocolString` is a 4.20 name.** Both 4.20 images have it, and neither 5.3x nor 6.x does, though all of them still store the `graal://` and `graal3://` prefixes. **[bin]**
- **The voice codec names (`hvdi…`, `hcrypt…`) are only in the 4.20 engine.** They are not in the game cipher; the game cipher of 4.x is generation 5 (`v4x-clients.md#cipher-and-framing`). **[bin]**
- **`14899` is a 4.20 host and config value.** The 4.20 unpacked folder's `graal4config.txt` ships `fixedudpport=14899` and `noudp=true`; the engine DLL has the two key names but not the digits. **[bin][file]**
- **5.30r3 and 5.31r4 store a default login host and `14900`.** The host name and the port are adjacent strings. `v5x-clients.md` says the host and port normally come from `license.graal`; whether these built-in values are used when that file is missing is not checked. **[bin]** The two builds also store `switchToOpenGL`, which no other image here has. **[bin]**
- **The UDP preference names disappear in 6.x.** `fixedudpport` and `noudp` are in every image up to 5.31 and in neither 6.x image. 6.x keeps the scripted datagram hooks (`onBind`, `onReceiveUDPData`), which among these images first appear in 5.30. See `v6113-udp-code.md`. **[bin]**
- **Level file magics.** `GSERVL01` and `Z3-V1.04` are stored up to 5.31 and not in either 6.x image. `GRMAP001`, `GWEBL001` and `GR-V1.04` are in all except the 4.20 host exe. **[bin]**
- **The receive error wording changes between 6.03 and 6.11.** Up to 6.03 the client says "Received illegal data (1)" or "(2)". 6.11 says "Received invalid data", has a third case "(3)", and adds "Cannot send data, socket is not initialized yet.". The third case belongs to 6.11's server-defined header path (`v6-repro-facts.md`). **[bin]**
- **RC4 helper names first appear in 6.03.** `Arc4Process` and `Arc4SetKey` are in both 6.x images and in neither 5.3x image. Only 6.11 adds `DOQLHRbY` and the connector start script names. **[bin]**
- **The named send slots are 6.11 only.** 6.11 stores 55 distinct `onSend…` names and the `tclient_` prefix. No other image has either. The slot table is in `v6113-pli.md`. **[bin]**
- **5.30r3 has `StartScript_QuitDialog`; 5.31r4 does not.** Both have `StartScript_Profiles`. **[bin]**

## The script property list: 96 names in 6.03, 95 in 6.11

Both 6.x images store one comma-separated list of script-facing player property names, starting `account,alpha,ani,…`. **[bin]**

- 6.03 has **96** names. `ismuted` is entry **50** (counting from 0), between `ismale` and `ismuting`.
- 6.11 has **95** names. It is the 6.03 list with `ismuted` removed and nothing else changed, so every entry after 49 is one place earlier.
- None of the 3.04, 4.20 or 5.3x images stores such a list. The 4.20 engine and both 5.3x images do contain the word `ismuted` elsewhere.

These are script names. They are not the numbered wire property ids in `v6-props.md`, and the list position is not a wire id. **[bin]**

## Not settled here

- Whether 5.30r3 or 5.31r4 ever connects to the built-in login host when `license.graal` is present, missing or bad. Needs a lab run with each `license.graal` case and a local listener on 14900.
- Whether 6.11 ever uses the removed `ismuted` property from a script. Needs a script corpus search or a lab run.
- Why `User-Agent: Graal/` is stored in the 4.20 engine and both 6.x images but not in 5.3x. It may be built at run time there.
