# `weblevels` per-server folders and `.code` roles

Date: 2026-11-16

Inventory of real client `weblevels` trees (legacy 2.22, a mixed v4 install, v5, and a 6.1.1.3 cache dump) plus format checks against the existing GWEBL / GRESCR / gpak notes. Tags: **[test]** on-disk files · **[bin]** prior static readings cited below · **[lab]** not re-run here for folder creation.

Placeholders only: `<server-ip>`, `<hostname>`, `<port>`, `<server-name>`, `<name>`, `<md5-hex32>`. No real hosts, ports from live networks, or machine paths.

## Claim under test

Real clients keep a per-server folder under `weblevels/`. On legacy clients, server-scoped cache files live directly under that folder. `.code` is a cache/package extension used for more than one payload family — not one format.

## Folder naming (confirmed on disk)

### Level cache folders

| Era (install / dump) | Folder under `weblevels/` | File name shape | Port in folder? |
|---|---|---|---|
| 2.22 | `<server-ip>` only in the sampled tree | `<level>-<port>.code` | **No** — port is only in the file name |
| Mixed v4 install | `<server-ip>` **or** `<hostname>` | `<level>-<port>.code` | **No** |
| v5 install | `<server-ip>` **or** `<hostname>`, plus typed dirs below | `<level>-<port>.code` under the host folder | **No** |
| 6.1.1.3 dump | `<md5-hex32>` (32 lowercase hex chars) | `<level>-<port>.code` | **No** in the folder name |

**[test]** On 2.22, every sampled level `.code` decrypts as GWEBL001 with `tools/file-formats/gwebl.py`, and the plaintext host field **equals** the folder name (IPv4 in that tree). Port is not part of the folder name.

**[test]** On the 6.1.1.3 dump, level files sit only under four `<md5-hex32>` folders. Filename ports observed in that dump were lab-style values already used elsewhere in this repo’s docs (not repeated here as identifying endpoints). One folder’s hash matched `md5( host || port )` (UTF-8, **no** separator) for a host string recovered from an escaped login host-list folder name in the same dump. The other three folders did not match any host string available from `weapons/` / `classes/` names in that dump. Treat “MD5 of connect host concatenated with port” as a **strong lead**, not fully closed, until a 6.1.1.3 binary path confirms the input.

### Weapon / class / gani folders (5.x / 6.x dumps)

| Path | What the middle segment is |
|---|---|
| `weblevels/weapons/<server-name>/…` | Server or world display name, or a login host-list |
| `weblevels/classes/<server-name>/…` | Same escaping rules |
| `weblevels/ganis/` | Flat in the 6.1.1.3 dump (no per-server child) |

**[test]** Non-alphanumeric bytes in `<server-name>` are stored as `%0NN` with **decimal** `NN` (space → `%032`, `.` → `%046`, `:` → `%058`, `,` → `%044`). One `weapons/` child decoded to a comma-separated `host:port` list with those escapes. Other children decoded to ordinary world names (spaces escaped).

This matches the same `%032` style already noted for update-package folders in the manual (`updatepackages/<server…>`).

### What 4.20r8 does for weapons (**[bin]**, prior)

Static readings already in-tree for Windows 4.04r2 / 4.20r8 build the weapon script cache as:

```
weblevels/weapons/<name>.code
```

with **no** host or server-name segment (`protocol/unknown-ids-2026-11-06.md`, `protocol/gs2-client-vm.md`, `protocol/v4x-clients.md`). That is the stock v4 path for PLO 132 / 193.

A mixed v4 install’s on-disk tree also had `weblevels/weapons/<server-name>/…` files with `GRESCR01` magics. Those files are a **later** cache shape sharing a folder; they are not evidence that 4.20r8 itself writes the middle segment. Others Work’s `weblevels/weapons/<server>/<name>.code` lead therefore applies to post-v4 / GRESCR layouts, not to the 4.20r8 193 path we already documented.

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

**[test]** All 117 level files in the dump share the same four bytes immediately after the LE length field. Classic name-seeded GWEBL ciphertext does **not** do that across different level names. Combined with `gwebl.py` failure, the dump’s level caches are **not** byte-compatible with the 2.05/2.22 reader. Whether they are still GWEBL001 under a shared/session key (first plaintext block identical → identical first ciphertext block) remains open. Do not treat them as `.gpake`.

## Sanitization summary

| Surface | Rule |
|---|---|
| Level folder (2.x–5.x) | Connect host string as used by the client: dotted IPv4 **or** hostname; **no** `:port` |
| Level file | `<level-basename>-<port>.code` (lowercase level name; port in the name) |
| Level folder (6.1.1.3 dump) | `<md5-hex32>`; input likely host∥port — confirm on binary |
| Weapon/class folder (5.x/6.x dumps) | Server/world name or escaped host-list; `%0NN` decimal escapes |
| 4.20r8 weapon file | `weblevels/weapons/<name>.code` only **[bin]** |

## Loopback

Seihai gserver is not expected to emit `.code` files. A loopback check is only for whether a real client creates `weblevels/<server…>/` (and typed children) after connect. **Not run in this pass.**

## Corrections to earlier wording

- Keep documenting **4.04r2–5.12** weapon CRC files as `weblevels/weapons/<name>.code` (**[bin]**).
- Document **GRESCR-era** script caches as `weblevels/weapons/<server-name>/…` and `weblevels/classes/<server-name>/…` on disk (and `weblevels/<host>/weapons/…` in the 6.03r7 static path table in `gwebl001-cache.md` — reconcile host vs display-name on a focus 5.24+ binary when that lab runs).
- Do not equate `.code` with `.gpak`/`.gpake`.
