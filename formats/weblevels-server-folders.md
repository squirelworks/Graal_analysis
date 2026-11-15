# `weblevels` per-server folders and `.code` roles

Date: 2026-11-16

Inventory of client `weblevels` trees (legacy 2.22, a mixed v4 install, v5, and a 6.1.1.3 cache dump) plus format checks against the existing GWEBL / GRESCR / gpak notes. Tags: **[test]** on-disk files · **[bin]** prior static readings cited below · **[lab]** not re-run here for folder creation.

Placeholders only. Allowed path shapes in this note:

- `weblevels/<escaped-server-name>/`
- `weblevels/<md5-hex32>/`
- `<level>.nw-<port>.code`
- connect host (IP or hostname)

No real sample file or folder names, no real escaped server folders, no real md5 hex folder names, no worked hashes over real hosts, and no live IPs, hostnames, or ports.

## Claim under test

Real clients keep a per-server folder under `weblevels/`. On legacy clients, server-scoped cache files live directly under that folder. `.code` is a cache/package extension used for more than one payload family — not one format.

## Folder naming (confirmed on disk)

### Level cache folders

| Era (install / dump) | Folder under `weblevels/` | File name shape | Port in folder? |
|---|---|---|---|
| 2.22 | connect host (IP or hostname); sampled tree was IP-shaped | `<level>.nw-<port>.code` | **No** — port is only in the file name |
| Mixed v4 install | connect host (IP or hostname) | `<level>.nw-<port>.code` | **No** |
| v5 install | connect host (IP or hostname), plus typed dirs below | `<level>.nw-<port>.code` under the host folder | **No** |
| 6.1.1.3 | `weblevels/<md5-hex32>/` (`MD5(host∥decimal_port)` lowercase) **[bin]** | `<level>.nw-<port>.code` | **No** in the folder name |

**[test]** On 2.22, sampled level `.code` files decrypt as GWEBL001 with `tools/file-formats/gwebl.py`, and the plaintext host field **equals** the folder name (connect host). Port is not part of the folder name.

**[bin]** On stock Windows 6.1.1.3, the level-folder name is lowercase hex of
`MD5(host_bytes ∥ decimal_port_ascii)` (no separator). **[test]** On the 6.1.1.3 dump,
level files sit only under those `<md5-hex32>` folders (port still only in the file name).
No worked hashes over live hosts. Era path table, offline hash lead, and level `.code` vs
`GRESCR01`: `formats/weblevels-code-residuals.md`.

### Weapon / class / gani folders (5.x / 6.x dumps)

| Path | What the middle segment is |
|---|---|
| `weblevels/weapons/<escaped-server-name>/…` | Server or world display name, or a login host-list |
| `weblevels/classes/<escaped-server-name>/…` | Same escaping rules |
| `weblevels/ganis/` | Flat in the 6.1.1.3 dump (no per-server child) |

**[test]** Non-alphanumeric bytes in the server-name segment are stored as `%0NN` with **decimal** `NN` (space → `%032`, `.` → `%046`, `:` → `%058`, `,` → `%044`). Some `weapons/` children decode as comma-separated connect-host lists with those escapes; others decode as ordinary world names (spaces escaped). Real decoded names stay out of this repository.

This matches the same `%032` style already noted for update-package folders in the manual.

### What 4.20r8 does for weapons (**[bin]**, prior)

Static readings already in-tree for Windows 4.04r2 / 4.20r8 build the weapon script cache as:

```
weblevels/weapons/<name>.code
```

with **no** host or server-name segment (`protocol/unknown-ids-2026-11-06.md`, `protocol/gs2-client-vm.md`, `protocol/v4x-clients.md`). That is the stock v4 path for PLO 132 / 193.

A mixed v4 install’s on-disk tree also had `weblevels/weapons/<escaped-server-name>/…` files with `GRESCR01` magics. Those files are a **later** cache shape sharing a folder; they are not evidence that 4.20r8 itself writes the middle segment. Others Work’s lead that inserts a server segment under `weapons/` therefore applies to post-v4 / GRESCR layouts, not to the 4.20r8 193 path we already documented.

## `.code` is not one format

Every file under `weblevels` in these trees ends in `.code`. Magics and loaders differ.

| Kind | On-disk head | Loader family | Zip / `.gpak` container? |
|---|---|---|---|
| Level web-cache (classic) | Encrypted blob; plaintext magic `GWEBL001` after name-seeded DES | `formats/gwebl001-cache.md` | **No** |
| Level web-cache (6.1.1.3 dump) | 4-byte LE length, then high-entropy bytes; **no** `PK` / `GPAK` magic; classic `gwebl.py` fails | Open (likely still level cache, different keying) | **No** on samples tested |
| Weapon/class script cache (5.x+ / 6.1.1.3) | `GRESCR01` + encrypted body | `formats/gwebl001-cache.md`, `protocol/gs2-official-bytecode-6113.md` | **No** |
| Weapon script cache (4.x pre-GRESCR) | Raw cached script bytes; CRC is zlib CRC32 of the file | PLO 193 path above | **No** |
| Resource package | `.gpak` / `.gpake` / `.zip` under `levels/gpaks/` (etc.) | `formats/gpak.md` | **Yes** — ZIP via minizip; `.gpake` encrypts **entry contents** only |

### Owner hypothesis: “`.code` ≈ zip/gpak encoded like `.gpake`”

**[test]** Rejected for the `weblevels` samples checked here:

- No level or script `.code` opened as a ZIP (`PK\x03\x04` absent; `zipfile` fails on whole file and on a 4-byte skip).
- Repo `sample.gpake` **does** start with `PK\x03\x04` (ZIP container, per-entry DES). That is a different path and extension.
- GRESCR01 bodies use DES-ECB with a **session key from PLO 197** (bit-reversed key bytes, same DES quirk family as `.gpake`), but the file is **not** a ZIP: magic + body only. Keys stay out of this repository.

So: same **cipher family** as `.gpake` for script caches; **not** the ZIP/gpak container.

### 6.1.1.3 level `.code` note

**[test]** Level files in the dump begin with a 4-byte little-endian length `L`, then a body whose length is `L` rounded up to a multiple of 8. They share the same first eight body bytes across every level file. Classic name-seeded GWEBL ciphertext does **not** do that across different level names, and the classic Win wrapper (`N = padded_plaintext + 8` with `N` equal to the whole post-header body) does not match this `L`. Combined with `gwebl.py` failure, those level caches are **not** byte-compatible with the 2.05/2.22 reader. Whether they are still GWEBL001 under a shared/session key remains open. Do not treat them as `.gpake` or as `GRESCR01` (script caches keep the `GRESCR01` magic at offset 0). Details: `formats/weblevels-code-residuals.md`.

## Sanitization summary

| Surface | Rule |
|---|---|
| Level folder (2.x–5.x) | connect host (IP or hostname); **no** port in the folder name |
| Level file | `<level>.nw-<port>.code` |
| Level folder (6.1.1.3) | `weblevels/<md5-hex32>/` = `MD5(host∥decimal_port)` lowercase **[bin]** |
| Weapon/class folder (5.x/6.x dumps) | `weblevels/weapons/<escaped-server-name>/` and `weblevels/classes/<escaped-server-name>/` (`%0NN` decimal escapes) |
| 4.20r8 weapon file | `weblevels/weapons/<name>.code` only **[bin]** |

## Loopback

Seihai gserver is not expected to emit `.code` files. A loopback check is only for whether a real client creates `weblevels/<escaped-server-name>/` or `weblevels/<md5-hex32>/` (and typed children) after connect. **Not run in this pass.**

## Corrections to earlier wording

- Keep documenting **4.04r2–5.12** weapon CRC files as `weblevels/weapons/<name>.code` (**[bin]**).
- Document **GRESCR-era** script caches as `weblevels/weapons/<escaped-server-name>/…` and `weblevels/classes/<escaped-server-name>/…` on disk (and reconcile with the 6.03r7 static host-keyed weapons table in `gwebl001-cache.md` on a focus 5.24+ binary when that lab runs).
- Do not equate `.code` with `.gpak`/`.gpake`.
