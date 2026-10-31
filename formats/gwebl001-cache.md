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
