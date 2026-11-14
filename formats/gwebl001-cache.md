# GWEBL001: the web-level cache (`weblevels/*.code`)

Date: 2026-10-21

Traced from the 2.05 rev 2 cache reader and writer, then confirmed on 144 real cache files from a 2.22 install: every one decrypts, passes the checksum, parses, and re-encrypts byte for byte. Tags: **[2.05]** read from the client · **[2.31]** read from the 2.31 client · **[test]** confirmed on real files.

## What it is

A local copy of a server level, keyed by the level's modification time, so the client can skip downloading a level it already has.

- **Written** when the server sends the level's 5-byte modification time (server packet id 39, `PLO_LEVELMODTIME` in GServer naming). The client saves the level it currently holds, with that time. **[2.05]**
- **Read** when the client enters a level: if a cache file exists, the client builds the level from it. **[2.05]** It presumably then only needs the server to send levels that have changed. **[inf]**
- A file whose header doesn't match the current server is **deleted**. **[2.05]**

## Path

```
<exe dir>\weblevels\<server host>\<level>-<server port>.code
```

`<level>` is the level's file name, lowercased, with any path removed. The reader also tries `<level>.code` without the port. **[2.05]** Real example: `weblevels\<game-server-host>\bank.nw-14803.code`. **[test]**

## File layout (encrypted)

```
int32 LE   N            = padded plaintext length + 8
N-8 bytes  ciphertext   DES-ECB, one fresh key per 8-byte block
8 bytes    checksum     bytewise sum (mod 256) of all plaintext blocks, per byte position
```

The plaintext is padded with `0x0A` to a multiple of 8. **[2.05]**

### Per-block keys

The key for each block is 8 calls to Delphi `Random(256)`, drawn fresh for every block in file order. The generator is seeded first:

```
RandSeed = 0x04A80B38
for each byte c of <level> (lowercased name, no path):
    RandSeed = RandSeed * c            (32-bit wrap)
```

Delphi `Random(n)`: `RandSeed = RandSeed * 0x08088405 + 1`, then `(RandSeed * n) >> 32` (unsigned). The DES key bytes are bit-reversed as in `client-internals/saved-passwords.md`. **[2.05]** **[test]**

The "encryption" therefore needs only the level name. A wrong name shows up as a checksum mismatch.

## Plaintext layout

```
"GWEBL001"
GCHAR len + server host          must equal the connected host
GCHAR hi, GCHAR lo               server signature byte, as (hi-32)*128 + (lo-32)
5 bytes                          level modification time, 5 × 7-bit GCHAR, big-endian
GCHAR len + level name           must equal <level> above
level body                       GR-V1.03 (2.05) or GR-V1.03 / GR-V1.04 (2.31)
```

The signature check passes when the stored value equals the value the server sent in packet id 25 (`PLO_SIGNATURE`), or when the stored value is 1 and the server sent 73 (GServer's usual value). **[2.05]** All 144 test files hold 73. **[test]**

Decoding the modification time as a 35-bit integer gives Unix time. The test files decode to dates a little before their file timestamps (for example `bank.nw` decodes to 1247727798, 16 July 2009, and the file is dated 26 July 2009). **[test]**

## Level body as cached

The body is an ordinary GR-V level (`level-binary.md`, `level-binary-client.md`), but the writer fills only some sections:

| Section | Cached |
|---------|--------|
| Board | yes, 13-bit run-length stream |
| Links | yes, `dest x y w h newx newy` lines, then `#` |
| Baddies | no, terminator only (`FF FF FF 0A`) |
| NPCs | no, empty (`#`) |
| Chests | no, empty (`#`) |
| Signs | yes, `x+32, y+32, sign text, \n` |
| Heights | 2.31 only, as a `HEIGHTS` block when the level has a height map, which also switches the magic to `GR-V1.04` **[2.31]** |

## Tool

`tools/file-formats/gwebl.py`:

```
python3 gwebl.py weblevels/<game-server-host>/bank.nw-14803.code       # summary
python3 gwebl.py FILE.code --json                                      # full parse
python3 gwebl.py FILE.code --raw plain.bin                             # decrypted stream
```

The module also has `encrypt_stream` (re-creates files byte for byte), `read_board` / `write_board`, and `parse_grv` for plain `.graal` data.

## The Mac 4.x and 5.x cache (2026-11-12)

The Mac PowerPC 4.04r2, 4.20r6 and 5.12 clients share one folder, `~/.graal/graal4/weblevels/<host>/<level>-<port>.code`,
and write it only after a move to a named game server (the Login session writes none). The same
level from 4.04r2/4.20r6 and from 5.12 gave byte-identical files. **[lab]**

The plaintext is exactly GWEBL001 as above (header, host, signature, mod time, level name, then
`GR-V1.03`, or `GR-V1.04` with heights), with the same seed rule, DES and 8-byte checksum.
Two wrapper details differ, which is why a 2.05 reader rejects Mac files with a bad length header:
**[bin][test]**

1. The leading int32 is **big-endian** and holds the **unpadded** plaintext length + 8 (2.05
   stores little-endian, padded length + 8). Padding with `0x0A` still follows.
2. Each block key byte is the **low byte** of `seed = seed × 0x08088405 + 1`; 2.05's Delphi
   `Random(256)` takes the high byte.

A reader built on `tools/file-formats/gwebl.py` with those two changes decodes the Mac files with a
good checksum.
The Mac and Windows caches are therefore not interchangeable. **[test]**

## The 5.x and 6.x `.code` cache

Added 2026-11-06, read from the unpacked 5.24r4, 6.00b1, 6.00r2 and 6.03r7 Windows clients. Tags as above, plus **[bin]** read from those builds.

By 5.x `weblevels` holds more than levels. Every file in it is a download cache, named `.code`, so the next visit can skip a download. These files have nothing to do with the 1999 Guildmaker `guildname.code` / `reg.code` files in `graalsav.md`, apart from the extension.

| Kind | Path (6.03r7) | Format |
|---|---|---|
| Level | `weblevels\<host>\<level>-<port>.code` (the reader also tries `<level>.code`) | `GWEBL001`, as above |
| Weapon script | `weblevels\<host>\weapons\<name>.code` | `GRESCR01` |
| Class script | `weblevels\<host>\classes\<name>.code` | `GRESCR01` |
| Gani | `weblevels\<host>\ganis\<name>.code` | not traced |

- **[bin]** The weapon and gani caches and the `GRESCR01` reader and writer are in all four builds, so this started in 5.x. The class path was checked in 6.03r7 only.
- **[bin]** The gani and level caches share one file helper. The gani file contents have not been traced.

### `GRESCR01` (weapon and class scripts)

- The file is the 8-byte magic `GRESCR01`, then the script body, DES-ECB encrypted. **[bin]**
- Written when the server sends a script with 140 `PLO_NPCWEAPONSCRIPT` (header `type,name,cacheflag,i5,i5`, then the plain body) and the cache flag is 1. The two `i5` values, as little-endian 32-bit words, are the 8-byte DES key. **[bin]** (`protocol/v5x-clients.md`)
- The following historical description is qualified for the exact unpacked Windows 6.03 weapon path by the [success-output follow-up](windows-603-weapon-cache.md): its CRC covers the stored body before transformation, and returned bytes do not imply cache acceptance. Other builds/callers were not retraced. **[bin]**
- Historical description, not the corrected Windows 6.03 weapon contract: when the server says "use your cache" with 197 `PLO_LOADSCRIPT`, it sends the key and a CRC32. The client decrypts its copy and checks the CRC32 of the plaintext; on a match it loads the copy, otherwise it asks again with PLI 158 (`PLI_UPDATESCRIPT`). **[bin]**
- The key is never stored on disk, but it crosses the wire in clear on every connection, so the encryption only stops casual reading.
- The earlier source-text inference is not established by unencrypted transport alone; the [GS2 container study](../protocol/gs2-client-vm.md) separately identifies binary segment readers. Historical inference: the body is probably GS2 source text, not bytecode, because it arrives as plain text. **[inf]** No real file has been decrypted yet.
- Before 5.24, 4.04r2 to 5.12 used PLO 193 for the same job: `i5 crc32` + weapon name, checked against `weblevels/weapons/<name>.code` (`protocol/unknown-ids-2026-11-06.md`). **[bin]**

### File lookup skips them

- **[bin]** When 6.03r7 scans the game folder it ignores files ending in `.code` and does not enter the top-level `pms`, `profiles` or `weblevels` folders, the same rule as 2.22 (`client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md`). Other lookups also skip `.code`, so a cached copy never stands in for a real file.

### Still open

- ~~Decrypt a real `GRESCR01` file with a key from a capture, to confirm the body is GS2 source.~~ Done for 6.113 (2026-11-12): the body is compiled GS2, not source. The 197 CRC covers the stored, encrypted body, and the last `len % 8` bytes are stored in clear (`../protocol/gs2-official-bytecode-6113.md`). **[cap]**
- Trace the gani cache format.
- Check the class cache path in builds before 6.03r7.
