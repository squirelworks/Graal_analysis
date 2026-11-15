# `weblevels` residuals: md5 folders, 4.20r8 paths, level `.code` vs GRESCR01

Date: 2026-11-16

Follow-on to `formats/weblevels-server-folders.md`. Own inventory and format tests on a
6.1.1.3 `weblevels` cache dump (held off-repo), plus prior in-tree **[bin]** path readings for
4.20r8. Placeholders only. Tags: **[test]** on-disk · **[bin]** prior static · **[inf]** offline
hash lead.

Allowed shapes in this note:

- `weblevels/<md5-hex32>/`
- `weblevels/<escaped-server-name>/`
- `weblevels/weapons/<name>.code`
- `weblevels/weapons/<escaped-server-name>/<name>.code`
- `<level>.nw-<port>.code`
- connect host (IP or hostname); lab ports only when a port example is needed

No real sample folder names, no real md5 hex, no worked hashes over live hosts, and no live
IPs, hostnames, or non-lab ports.

## 1. `<md5-hex32>` level-folder input

### On disk

**[test]** In the 6.1.1.3 dump, every level `.code` sits under a 32-hex lowercase folder. Each
such folder has exactly one port value in its `<level>.nw-<port>.code` names (port is still only
in the file name, not in the folder string).

### Offline hash lead (not a binary proof)

**[inf][test]** Against escaped `host:port` material already present under that dump’s
`weapons/` / `classes/` segments (login host-list and world names; real values not published):

| Candidate UTF-8 input to MD5 (hex lowercase) | Folders matched |
|---|---|
| `<host>` digits of `<port>` concatenated, **no** separator | **some** (one folder matched a login-list host∥port pair) |
| `<host>:<port>`, `<host>\|<port>`, `<host>/<port>`, host only, UTF-16LE forms, host + binary LE/BE port words | **none** |

So the best offline reading remains: folder name = MD5 of connect **host** bytes followed
immediately by the **decimal ASCII port** (no `:` / `|` / other separator). That is not yet
a full dump match, because most level folders’ connect hosts are not among the escaped login
host-list segments (game-server hosts after warp are expected). World-display-name segments
do **not** hash to any level folder.

### Binary

**[bin]** Not closed in this pass. No 6.1.1.3 / 6.03 client image was available in the cloud
workspace to trace the path builder. Treat the table above as a lead until a focus binary
session confirms the sprintf/concat form and character set.

## 2. Path layout: 4.20r8 vs later

| Surface | 4.20r8 (and 4.04r2–5.12 weapon CRC path) | GRESCR-era / 6.1.1.3 dump |
|---|---|---|
| Level folder | `weblevels/<host>/` (IP or hostname; port **not** in folder) **[test]** on older installs; **[bin]** path shape in `formats/gwebl001-cache.md` | `weblevels/<md5-hex32>/` **[test]** |
| Level file | `<level>.nw-<port>.code` (fallback `<level>.code`) | same file-name shape **[test]** |
| Weapon cache | `weblevels/weapons/<name>.code` — **no** server segment **[bin]** (`protocol/unknown-ids-2026-11-06.md`, `protocol/v4x-clients.md`) | `weblevels/weapons/<escaped-server-name>/<name>.code` with `%0NN` decimal escapes **[test]** |
| Class cache | no weapons-style `.code` on the v4 133 path (see `protocol/class-bytecode-v4.md`) **[bin]** | `weblevels/classes/<escaped-server-name>/…` **[test]** |
| Gani cache | not the focus of the 4.20r8 193 path | flat `weblevels/ganis/` in the 6.1.1.3 dump **[test]** |

**[test]** A mixed v4 *install folder* can also contain later `weapons/<escaped-server-name>/`
`GRESCR01` files. Those are not evidence that stock 4.20r8 writes the middle segment.
Others Work’s `weapons/<server>/` lead stays a lead for live 4.20r8 until a stock-binary lab
sees the file create.

**[bin]** Static 6.03r7 notes still describe `weblevels\<host>\weapons\` and
`weblevels\<host>\classes\` under the **host** folder (`formats/gwebl001-cache.md`). The
6.1.1.3 dump instead uses top-level `weapons/` and `classes/` with an escaped server-name
child. Reconcile on a focus 5.24+ / 6.03 binary when that lab runs; do not collapse the two
shapes yet.

## 3. Level `.code` vs GRESCR01

### Level files (6.1.1.3 dump)

**[test]** Every level `.code` in the dump:

```
uint32 LE   L          logical length
L' bytes    body       L' = L + pad, pad = (8 - (L mod 8)) mod 8
```

- `L' == L + pad` holds for **all** sampled level files.
- Body after the length field is high-entropy; first eight body bytes are **identical** across
  every level file in the dump (shared leading block → shared/session keying is plausible;
  classic per-level-name GWEBL keying is not).
- No `GRESCR01` magic at offset 0 or after the length field.
- Not a ZIP / `.gpak` / `.gpake` container (no `PK` magic; `zipfile` fails).
- Classic `tools/file-formats/gwebl.py` fails: the 2.05/2.22 wrapper uses
  `N = padded_plaintext_length + 8` as the LE field with `N` equal to the post-header body
  (ciphertext + 8-byte checksum). Here `L` is **not** that contract (`L` equals the body
  length only when `L` is already a multiple of 8).

Decrypt path for these level bodies remains open (not GRESCR/197; not classic name-seeded
GWEBL as shipped in `gwebl.py`).

### Weapon / class files (same dump)

**[test]** Every `weapons/**/*.code` and `classes/**/*.code` file begins with the eight-byte
magic `GRESCR01`, then an encrypted body. That family is documented in
`formats/gwebl001-cache.md` and `protocol/gs2-official-bytecode-6113.md` (DES-ECB, session key
from PLO 197, CRC over the stored body after the magic). Keys stay out of this repository.

So: **same extension, two formats.** Level caches use a length-prefixed opaque body; script
caches use `GRESCR01`.

### Gani files (brief)

**[test]** Flat `ganis/*.code` files in the dump also look length-prefixed (varying LE heads;
not the shared post-length dword of the level set; not `GRESCR01`). Format not traced further
here.

## Corrections / keep

- Keep 4.20r8 weapon caches as `weblevels/weapons/<name>.code` (**[bin]**).
- Keep documenting 6.1.1.3 level folders as `weblevels/<md5-hex32>/` with md5 input still
  **[inf]** pending **[bin]**.
- Do not equate level `.code` with `GRESCR01` or with `.gpak`/`.gpake`.

## Still open

1. **[bin]** Confirm md5 input string on a 6.1.1.3 (or sibling) client path builder.
2. Decrypt / identify the 6.1.1.3 level body after the LE length (session vs other seed).
3. Loopback: whether a real client creates `weblevels/<md5-hex32>/` against Seihai (structure only).
4. Stock 4.20r8 live check of weapon path vs Others Work’s `weapons/<server>/` lead.
5. Reconcile 6.03r7 host-keyed `weblevels\<host>\weapons\` static table with dump’s
   top-level `weapons/<escaped-server-name>/`.
