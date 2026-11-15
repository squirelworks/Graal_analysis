# `weblevels` residuals: md5 folders, 4.20r8 paths, level `.code` vs GRESCR01

Date: 2026-11-16

Follow-on to `formats/weblevels-server-folders.md`. Own inventory and format tests on a
6.1.1.3 `weblevels` cache dump (held off-repo), prior in-tree **[bin]** path readings for
4.20r8, and a focus **[bin]** path-builder confirm on stock 6.1.1.3 (with 6.03r7 same-era
tokens). Placeholders only. Tags: **[test]** on-disk · **[bin]** static · **[inf]** offline
hash lead (superseded for the md5 input).

Allowed shapes in this note:

- `weblevels/<md5-hex32>/`
- `weblevels/<escaped-server-name>/`
- `weblevels/weapons/<name>.code`
- `weblevels/weapons/<escaped-server-name>/<name>.code`
- `<level>-<port>.code`
- connect host (IP or hostname); lab ports only when a port example is needed

No real sample folder names, no real md5 hex, no worked hashes over live hosts, and no live
IPs, hostnames, or non-lab ports. No owner paths, drive letters, or machine names.

## 1. `<md5-hex32>` level-folder input

### On disk

**[test]** In the 6.1.1.3 dump, every level `.code` sits under a 32-hex lowercase folder. Each
such folder has exactly one port value in its `<level>-<port>.code` names (port is still only
in the file name, not in the folder string). Sampled leaves often look like
`<level>.nw-<port>.code`.

### Binary confirm (6.1.1.3)

**[bin]** On the stock Windows 6.1.1.3 unpacked client, the level-cache per-server folder name
is:

```
<md5-hex32> = lowercase_hex( MD5( host_bytes ∥ decimal_port_ascii ) )
```

| Piece | Behaviour |
|---|---|
| `host_bytes` | Connect-host string as the client already holds it (IP or hostname bytes; no extra encoding step on this path) |
| Separator | **None** — not `:`, `/`, or NUL |
| `decimal_port_ascii` | Game-server port as decimal ASCII digits (no extra width / zero-pad beyond the natural decimal) |
| Hash | MD5 over that concatenation |
| Hex | **Lowercase** `0123456789abcdef`; 32 characters |

On connect / server-select the client stores that hex string as the level-folder name and joins:

```
weblevels/<md5-hex32>/<level>-<port>.code
```

(platform path separator; literal `-` between level leaf and port). Same MD5/hex helpers and
`weblevels` / `.code` / `GRESCR01` tokens are present on 6.03r7.

### Offline hash lead (supporting)

**[inf][test]** Against escaped `host:port` material already present under that dump’s
`weapons/` / `classes/` segments (login host-list and world names; real values not published):

| Candidate UTF-8 input to MD5 (hex lowercase) | Folders matched |
|---|---|
| `<host>` digits of `<port>` concatenated, **no** separator | **some** (one folder matched a login-list host∥port pair) |
| `<host>:<port>`, `<host>\|<port>`, `<host>/<port>`, host only, UTF-16LE forms, host + binary LE/BE port words | **none** |

That table is now supporting **[test]** for the **[bin]** rule above, not a substitute for it.
Most dump level folders still need game-server hosts (after warp), which are not among the
escaped login host-list segments. World-display-name segments do **not** hash to any level
folder.

## 2. Path layout: 4.20r8 vs later

| Surface | 4.20r8 (and 4.04r2–5.12 weapon CRC path) | GRESCR-era / 6.1.1.3 |
|---|---|---|
| Level folder | `weblevels/<host>/` (IP or hostname; port **not** in folder) **[test]** on older installs; **[bin]** path shape in `formats/gwebl001-cache.md` | `weblevels/<md5-hex32>/` **[bin]** (6.1.1.3); **[test]** on dump |
| Level file | `<level>-<port>.code` (fallback `<level>.code`) | same file-name family **[bin]**/**[test]** |
| Weapon cache | `weblevels/weapons/<name>.code` — **no** server segment **[bin]** (`protocol/unknown-ids-2026-11-06.md`, `protocol/v4x-clients.md`; stock 4.20r8 has `weblevels`+`.code`, no `GRESCR01`) | `weblevels/weapons/<escaped-server-name>/<name>.code` with `%0NN` decimal escapes **[test]**; path-builder **[bin]** on 6.1.1.3 |
| Class cache | no weapons-style `.code` on the v4 133 path (see `protocol/class-bytecode-v4.md`) **[bin]** | `weblevels/classes/<escaped-server-name>/…` **[test]** |
| Gani cache | not the focus of the 4.20r8 193 path | flat `weblevels/ganis/` in the 6.1.1.3 dump **[test]** |

**[bin]** Escape rule for the 6.1.1.3 weapons/classes middle segment: bytes not accepted as-is
become `%` + **decimal** digits, zero-padded to three (`%0NN`). Same family already seen on
disk as **[test]**.

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

**[test]** Every level `.code` in the dump (117/117):

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

**[test]** Every `weapons/**/*.code` (489/489) and `classes/**/*.code` (287/287) file begins
with the eight-byte magic `GRESCR01`, then an encrypted body. That family is documented in
`formats/gwebl001-cache.md` and `protocol/gs2-official-bytecode-6113.md` (DES-ECB, session key
from PLO 197, CRC over the stored body after the magic). Keys stay out of this repository.

So: **same extension, two formats.** Level caches use a length-prefixed opaque body; script
caches use `GRESCR01`.

### Gani files (brief)

**[test]** Flat `ganis/*.code` files in the dump (47) also look length-prefixed (varying LE
heads; not the shared post-length dword of the level set; not `GRESCR01`). Format not traced
further here.

## Corrections / keep

- Keep 4.20r8 weapon caches as `weblevels/weapons/<name>.code` (**[bin]**).
- Document 6.1.1.3 level folders as `weblevels/<md5-hex32>/` with input
  `MD5(host∥decimal_port)` lowercase hex (**[bin]**).
- Do not equate level `.code` with `GRESCR01` or with `.gpak`/`.gpake`.

## Still open

1. Decrypt / identify the 6.1.1.3 level body after the LE length (session vs other seed).
2. Loopback: whether a real client creates `weblevels/<md5-hex32>/` against Seihai (structure only).
3. Stock 4.20r8 live check of weapon path vs Others Work’s `weapons/<server>/` lead.
4. Reconcile 6.03r7 host-keyed `weblevels\<host>\weapons\` static table with dump’s
   top-level `weapons/<escaped-server-name>/`.
