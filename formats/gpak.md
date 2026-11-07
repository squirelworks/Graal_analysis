# `.gpak` and `.gpake`: resource packages

Date: 2026-11-06

Read from the 4.20r8 (`GraalEngine.dll`) and 6.03r7 clients, then loaded in a lab run with the
real 6.03r7 and 4.20r8 clients, plain and encrypted. Tags: **[bin]** read from a client binary · **[lab]** seen in a lab run ·
**[test]** checked here with the sample files · **[inf]** inferred.

The key packet (PLO 104) and the other ids read in the same pass are in
`protocol/unknown-ids-2026-11-06.md`.

## Status

| Point | Status |
|---|---|
| ZIP container read with minizip; entry limits; path and name mapping | confirmed in both clients **[bin]** |
| A plain `.gpak` loads in the real **6.03r7** client | **confirmed [lab]**: sent by the lab server, the package's image was drawn in game |
| A plain `.gpak` in 4.20r8 | **confirmed ignored [lab]**: saved but never loaded, whether pre-placed in `levels/gpaks/` or sent by the server; the same bytes renamed `.zip` load, so it is the name, not the contents **[bin][lab]** |
| `.gpake` = per-entry DES-ECB over full blocks, tail plain, no padding | confirmed in both clients' code **[bin]** |
| Key = PLO 104 halves, little-endian, looked up by lower-cased file name, switched on by 45 / 69 / 102 | confirmed in 4.20r8, 6.03r7 table matches **[bin]** |
| The client's DES is standard DES with every key byte bit-reversed (the 2.05 quirk) | confirmed by running the client's own DES code in an emulator: 6.03r7 and 4.04r2 **[bin]**; 4.20r8 decrypts a package built this way **[lab]** |
| An encrypted `.gpake` loads in the real **6.03r7** client | **confirmed [lab]**, once the writer used the bit-reversed key; a wrong key is refused |
| Packages in the real **4.20r8** client | **confirmed [lab]**: `.zip` loads (pre-placed and server-sent); `.gpake` loads and decrypts when PLO 104 comes first; `.gpak` does not load |
| Packages in the real **4.04r2** client | **none load [lab]**, under any name: its engine has no ZIP reader; its only `.gpak` / `.gpake` code picks the download folder **[bin]** |
| `a` must be 1 for a loose `.enc` in 6.03r7; ignored for packages | confirmed for that path **[bin]**; other values unknown |
| Stored entries work as well as deflate | **[inf]** (standard minizip) |

## What a package is for

A `.gpak` is one ZIP file holding many game files (images, ganis, sounds, scripts), so a
server can send them as one compressed download. The client saves a downloaded package under
`levels/gpaks/` (or `levels3d/gpaks/`). When it registers the file, it opens the ZIP and adds
every entry to its file table as if the file were loose in the levels folder. After that, a
level or script that asks for `tile.png` finds it inside the package by its bare, lower-cased
name. **[bin]**

`.gpake` is the encrypted form. The client refuses every entry until the server has sent the
key for that package (PLO 104) and then sent or confirmed the file. So the assets can't be
used outside a session on that server or read straight from the cache. `.enc` does the same
for one loose file with no ZIP around it. **[bin]**

## Container

- **[bin]** A standard PKZIP archive opened with minizip (`unzOpen`, `unzGetGlobalInfo`, then
  `unzGetCurrentFileInfo` / `unzGoToNextFile` per entry, `unzOpenCurrentFile` with no password
  and `unzReadCurrentFile`). No custom header, magic or index of its own.
- **[bin]** Limits: at most 10000 entries are read. An entry whose uncompressed size is over
  20 MiB (20,971,520 bytes) is skipped. The entry-name buffer is 256 bytes.
- **[bin]** Each entry becomes a resource at the virtual path
  `<package path>/<package file name>/<entry's folder part>/`, named by the lower-cased entry
  file name.
- **[bin]** Entries are found again later by their **index** in the central directory, not by
  name, so a package must not change while it is loaded.
- **[inf]** Compression: stored (0) and deflate (8). ZIP encryption is not used.

## Extensions by version

- **6.03r7 [bin]:** the archive extension list is `.gpake,.gpak,.zip,.wba,.mdt,.ods,.kmz`.
  `.gpake` (and the loose `.enc`) is marked encrypted. Every listed extension is opened as a ZIP.
- **4.20r8 [bin], odd:** when it creates a file resource, it returns nothing straight away for a
  file whose extension is `.gpak`, and goes on to open `.zip` and `.gpake` as packages. A later
  `.gpak` comparison in the same routine can never be reached. So 4.20r8 ignores a plain
  `.gpak`. Mac 4.20r6 has the same shape. Why is not known; it may be a deliberate "encrypted
  packages only" rule.
- **4.20r8 [lab]:** the extension match is case-sensitive: `tb.GPAK` is not treated as a package.
- **4.04r2 [bin][lab]:** no ZIP reader at all, so no package loads under any name. (The 3D
  plug-in's own Torque resource manager, `graal3d/torque-engine-4x.md`, is a separate thing.)
- Downloads **[lab]:** 4.20r8 and 6.03r7 save server-sent `.gpak` / `.gpake` files under
  `levels/gpaks/`. 4.20r8 saved a server-sent `.zip` under `levels/images/downloads/` and
  still loaded it.

## Encryption (`.gpake`, `.enc`)

- **[bin]** The ZIP structure is plain. Only the **uncompressed contents of each entry** are
  encrypted. After `unzReadCurrentFile` the client runs libtomcrypt `des_setup(key, 8, 0)` and
  then `des_ecb_decrypt` in place over each full 8-byte block. A tail shorter than 8 bytes is
  left as it is. No padding, so an entry's uncompressed size in the ZIP is its real size.
- **[bin][lab] Not textbook DES.** The client's libtomcrypt build reads every key byte with
  its bits reversed (bit 7 ↔ bit 0, 6 ↔ 1, …); the block cipher is otherwise standard. This is
  the same quirk as the 2.05 DES unit (`client-internals/saved-passwords.md`). Found by running
  the client's own `des_setup` and `des_ecb_encrypt` / `decrypt` in an emulator: the 6.03r7
  Windows client and the 4.04r2 `GraalEngine.dll` both give `CEE55ACD2386B23F` for key
  `133457799BBCDFF1` and block `0123456789ABCDEF` (textbook DES gives `85E813540F0AB405`), and
  match "standard DES with bit-reversed key bytes" on 200 of 200 (6.03r7) and 100 of 100
  (4.04r2) random key / block pairs. 4.20r8 was not emulated; it is very likely the same.
- **[test]** So to build a package for the PLO 104 key `K`, encrypt with standard DES-ECB under
  `bytes(bitreverse(b) for b in K)`, or use `tools/file-formats/graaldes.py` (the 2.05 cipher)
  with `K` as it is. `graaldes.py` gives the client's vector above and decrypts
  `samples/sample.gpake` back to the bytes of `samples/sample.gpak`.
- **[inf]** So a writer encrypts first and deflates second; the ZIP CRC and sizes describe the
  encrypted bytes, which is what minizip checks before the client decrypts.
- **[bin]** `.enc` is one loose file decrypted the same way, with no ZIP.
- **[bin]** The key is looked up by the package's **lower-cased file name with extension**
  (`sample.gpake`). It is used only once its record is switched on. The handlers of PLO 45
  (`PLO_FILEUPTODATE`), 69 (`PLO_LARGEFILEEND`) and 102 (`PLO_FILE`) switch it on for that
  file name, and the resource is then reloaded.
- **[bin]** In 6.03r7 a loose `.enc` decrypts only when PLO 104's byte `a` is 1. Packages don't
  check `a`, and 4.20r8 doesn't check it anywhere, so `a = 1` is safe for both.

### Key packet and send order

```
{chr(104+32)} {chr(len(name)+32)} {name} {chr(a+32)} {GINT5 lo} {GINT5 hi}
```

- `name`: the package file name, lower case, no path.
- `lo`, `hi`: key bytes 0–3 and 4–7, each read as a little-endian 32-bit value.
- GINT5: five 7-bit groups, most significant first, each plus 32. The clients work modulo
  2³², so a 32-bit value goes `(v>>28)&0x7f, (v>>21)&0x7f, (v>>14)&0x7f, (v>>7)&0x7f, v&0x7f`.
- **Order [bin]:** send 104 first, then the file (102, or 68 … 69 for a large file), or 45 if
  the client says it is up to date. A key sent after the file stays switched off until one of
  those three arrives.

## Lab results

**Run 2026-11-06 [lab]:** the Windows 6.03r7 client under Wine 9.0, offline in a
loopback-only network namespace, against the lab GServer-v2 behind the project's gen-5 proxy
(`tools/lab-servers/`, `tools/lab-setup.md`). After the 178 warp the proxy injected PLO 104, then
PLO 100 + 102 carrying the package.

- **Plain `sample.gpak`:** saved to `levels/gpaks/`, and a clientside `showimg` of
  `gpaksample_tile.png` drew the tile from inside the package.
- **Encrypted `sample.gpake`, key sent as `13 34 57 79 9B BC DF F1`, `a = 1`:** saved to
  `levels/gpaks/`, and the same `showimg` drew the tile. The client log has no "Failed to load"
  and no request for the file. A memory scan after 104 showed `13 34 57 79 9B BC DF F1` in the
  key record next to `a = 1`, so the two GINT5 values really are the little-endian halves.
- **Wrong-key control:** the same package with a wrong key in 104 gives
  `Failed to load gpaksample_tile.png`, and the client then asks the server for the file.
- **Before the DES fix:** packages built with textbook DES failed the same way for every key
  layout tried (halves swapped, big-endian halves, reversed, encrypt vs decrypt, double DES),
  and so did a plain PNG inside a `.gpake`. So the client decrypts every entry of a `.gpake`,
  and the only thing wrong was the DES variant.
- **Order used:** 104 first, then 102. A PLO 45 for the package 3 s later did no harm.
- Logs, screenshots and the emulator scripts are kept with the project's handoff files, not
  in this repo.

**Run 2026-11-06, 4.20r8 [lab]:** the Windows 4.20r8 `Graal4.exe` and `GraalEngine.dll`
(from the packet-logger build, with its logging hook undone as in the 2026-10-31 v4 lab and the
logger DLL left out) on top of a 4.04r2 install folder, under Wine 9.0 in a loopback-only
network namespace. Online: the lab GServer-v2 (`tools/lab-servers/run-lab.sh stock`) with
`G3D20126` allowed, behind the same gen-5 proxy, which injected the packets while the client
sat in the "Login" session (scripts still run and images are drawn there; no 178 warp). Each
test package held one 48 × 48 PNG in its own colour under a unique entry name, drawn by name
with `showimg`; a loose PNG in `levels/` was the control.

| Test | `.gpak` | `.zip` | `.gpake` |
|---|---|---|---|
| File already in `levels/gpaks/` at startup (offline) | not loaded | **loaded** | not loaded (no key offline, as expected) |
| The same `.gpak` bytes renamed `.zip` | — | **loaded** | — |
| `tb.GPAK` (upper case) | not loaded | | |
| Sent by the server (PLO 100 + 102) | saved to `levels/gpaks/`, not loaded | saved to `levels/images/downloads/`, **loaded** | PLO 104 first, then the file: saved to `levels/gpaks/`, **loaded and decrypted** (the sample's 16 × 16 tile drawn correctly) |
| 4.04r2 (its own exe and dll), files in `levels/gpaks/` | not loaded | not loaded | — |

This matches the disassembly: 4.20r8 returns nothing for `.gpak` and opens `.zip` and
`.gpake` as packages. The `.gpake` result also shows that 4.20r8's DES has the same
bit-reversed key bytes. Logs and screenshots are kept with the project's handoff files.

So a server that serves packages to every 4.20+ client should use `.gpake` (with PLO 104), or
`.zip`; a plain `.gpak` only works from 6.x on (5.x not tested).

### Other `.code` caches

The `GWEBL001` level cache already uses the bit-reversed DES (`formats/gwebl001-cache.md`,
`tools/file-formats/gwebl.py` imports `graaldes.py`). The 5.x / 6.x `GRESCR01` script cache is
DES-ECB too and very likely has the same quirk, so a decoder for it should start from
`graaldes.py`, not textbook DES. **[inf]** Not checked on a real file yet.

## Sample and tool

- `tools/file-formats/make_gpak.py` builds a plain package:
  `python3 make_gpak.py OUT.gpak a.png b.txt=dir/b.txt`, or `--sample DIR` for the two test
  files (it also writes the same bytes as `sample.zip` for 4.20r8).
- `tools/file-formats/samples/sample.gpak`: `gpaksample_note.txt` (88 bytes) and
  `gpaksample_tile.png` (16 × 16 RGBA, 352 bytes), both deflated. This is the package that
  loaded in 6.03r7.
- `tools/file-formats/make_gpake.py` builds an encrypted package and its PLO 104 packet
  (`--sample DIR`, `OUT.gpake --key HEX16 files…`, `--decrypt IN.gpake --key HEX16 DIR`,
  `--selftest`). It needs `pycryptodome`, and applies the key-byte bit reversal itself
  (`graal_des_key`).
- `tools/file-formats/samples/sample.gpake`: the same two files, encrypted for the PLO 104 key
  `133457799BBCDFF1` (textbook-DES equivalent `C82CEA9ED93DFB8F`). This is the package that
  loaded in 6.03r7. Its PLO 104 packet (`make_gpake.py --sample` also writes it):
  `88 2c 73 61 6d 70 6c 65 2e 67 70 61 6b 65 21 27 6a 7c 88 33 2f 2e 9e 99 3b 0a`
  = `104` · length 12 · `sample.gpake` · `a = 1` · GINT5 lo · GINT5 hi · line end.
