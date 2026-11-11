<!-- manual: kind=reference status=complete -->
# 3.8 Web level cache (GWEBL001)

The web-level cache is a local copy of a server level, keyed by the level's modification time, so the client can skip downloading a level it already has. The format was traced in the 2.05 rev 2 reader and writer and confirmed on 144 real cache files from a 2.22 install: every one decrypts, passes the checksum, parses and re-encrypts byte for byte [2.05][test] (formats/gwebl001-cache.md).

## 3.8.1 When it is used

The web-level cache keeps copies of server levels on disk. Each row gives one event in its use and what the client does [2.05] (formats/gwebl001-cache.md#what-it-is).

| Event | Behaviour | Source |
| --- | --- | --- |
| write | when the server sends the level's 5-byte modification time (`PLO_LEVELMODTIME`, id 39), the client saves the level it holds with that time | [2.05] (formats/gwebl001-cache.md#what-it-is) |
| read | when the client enters a level and a cache file exists, it builds the level from the file | [2.05] (formats/gwebl001-cache.md#what-it-is) |
| benefit | the server then presumably only needs to send levels that have changed | [inf] (formats/gwebl001-cache.md#what-it-is) |
| mismatch | a file whose header does not match the current server is deleted | [2.05] (formats/gwebl001-cache.md#what-it-is) |

## 3.8.2 Path

```
<exe dir>\weblevels\<server host>\<level>-<server port>.code
```

| Rule | Detail | Source |
| --- | --- | --- |
| `<level>` | the level's file name, lowercased, with any path removed | [2.05] (formats/gwebl001-cache.md#path) |
| fallback | the reader also tries `<level>.code` without the port | [2.05] (formats/gwebl001-cache.md#path) |
| example | `weblevels\<public-host>\bank.nw-14803.code` | [test] (formats/gwebl001-cache.md#path) |

## 3.8.3 Encrypted file

```
s32le      N            padded plaintext length + 8
N-8 bytes  ciphertext   DES-ECB, one fresh key per 8-byte block
8 bytes    checksum     bytewise sum (mod 256) of all plaintext blocks, per byte position
```

| Rule | Detail | Source |
| --- | --- | --- |
| layout | as above | [2.05] (formats/gwebl001-cache.md#file-layout-encrypted) |
| padding | the plaintext is padded with `0x0A` to a multiple of 8 | [2.05] (formats/gwebl001-cache.md#file-layout-encrypted) |
| seed | `RandSeed = 0x04A80B38`; then for each byte `c` of `<level>`, `RandSeed = RandSeed * c` with 32-bit wrap | [2.05][test] (formats/gwebl001-cache.md#per-block-keys) |
| block key | 8 calls to Delphi `Random(256)`, drawn fresh for every block in file order | [2.05][test] (formats/gwebl001-cache.md#per-block-keys) |
| `Random(n)` | `RandSeed = RandSeed * 0x08088405 + 1`, then `(RandSeed * n) >> 32`, unsigned | [2.05][test] (formats/gwebl001-cache.md#per-block-keys) |
| DES key bytes | bit-reversed, as in the 2.05 DES elsewhere (→ §3.7.5.2) | [2.05][test] (formats/gwebl001-cache.md#per-block-keys) |
| strength | the encryption needs only the level name; a wrong name shows up as a checksum mismatch | [2.05] (formats/gwebl001-cache.md#per-block-keys) |

## 3.8.4 Plaintext

```
"GWEBL001"
GCHAR len + server host          must equal the connected host
GCHAR hi, GCHAR lo               server signature, (hi-32)*128 + (lo-32)
5 bytes                          level modification time, 5 × 7-bit GCHAR, big-endian
GCHAR len + level name           must equal <level> above
level body                       GR-V1.03 (2.05), or GR-V1.03 / GR-V1.04 (2.31)
```

| Rule | Detail | Source |
| --- | --- | --- |
| layout | as above | [2.05][2.31] (formats/gwebl001-cache.md#plaintext-layout) |
| signature check | passes when the stored value equals the value the server sent in `PLO_SIGNATURE` (id 25), or when the stored value is 1 and the server sent 73, GServer's usual value | [2.05] (formats/gwebl001-cache.md#plaintext-layout) |
| test files | all 144 hold 73 | [test] (formats/gwebl001-cache.md#plaintext-layout) |
| modification time | decoded as a 35-bit integer it is Unix time; the test files decode to dates a little before their file timestamps (`bank.nw` decodes to 1247727798, 16 July 2009, and the file is dated 26 July 2009) | [test] (formats/gwebl001-cache.md#plaintext-layout) |

## 3.8.5 Level body as cached

The body is an ordinary GR-V level (→ §3.1.2), but the writer fills only some sections [2.05] (formats/gwebl001-cache.md#level-body-as-cached):

| Section | Cached | Source |
| --- | --- | --- |
| board | yes, the 13-bit run-length stream | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| links | yes, `dest x y w h newx newy` lines, then `#` | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| baddies | no; terminator only, `FF FF FF 0A` | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| NPCs | no; empty, `#` | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| chests | no; empty, `#` | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| signs | yes, `x+32, y+32, sign text, \n` | [2.05] (formats/gwebl001-cache.md#level-body-as-cached) |
| heights | 2.31 only: a `HEIGHTS` block when the level has a height map, which also switches the magic to `GR-V1.04` (→ §3.1.2.7) | [2.31] (formats/gwebl001-cache.md#level-body-as-cached) |

## 3.8.6 Tool

The repository has a tool for these cache files. The table lists its commands and what each produces [src] (formats/gwebl001-cache.md#tool).

| Command | Effect | Source |
| --- | --- | --- |
| `python3 tools/file-formats/gwebl.py FILE.code` | summary | [src] (formats/gwebl001-cache.md#tool) |
| `… --json` | full parse | [src] (formats/gwebl001-cache.md#tool) |
| `… --raw plain.bin` | the decrypted stream | [src] (formats/gwebl001-cache.md#tool) |
| module | `encrypt_stream` re-creates files byte for byte; also `read_board`, `write_board` and `parse_grv` for plain `.graal` data | [src] (formats/gwebl001-cache.md#tool) |

## 3.8.7 Unpacked Windows 6.03 weapon-cache acceptance

[bin] In the exact inspected unpacked Windows 6.03 input, the reader first clears success. Missing key or cache flag other than 1 returns empty. At least eight bytes and GRESCR01 pass only preliminary checks. After stripping the magic, nonzero expected CRC is compared with CRC32 of the stored body **before transformation**; mismatch returns empty. Expected CRC zero skips comparison and may return transformed bytes, but success remains false. Returned bytes and cache acceptance are separate. [bin] (formats/windows-603-weapon-cache.md)

[bin] The inspected weapon caller constructs its weapon-cache .code path and branches on success: false dispatches request logical ID 158; true hands returned script bytes onward. For exactly eight magic bytes the stored body is empty; its CRC with the inspected zero initialization is zero. Expected CRC zero therefore leaves success false, and any nonzero expected CRC mismatches. Both follow the request branch if surrounding caller gates permit it. [bin] (formats/windows-603-weapon-cache.md)

[inf] Independently authored header-only, wrong-flag and missing-key vectors have static-derived expectations, not original-client executed results. This does not establish downstream framing, a positive cache, class-cache or all-caller behavior, decoded-container validity, transformation compatibility or GS2 execution. The input is an unpacked analysis image, not an authenticated runnable distribution; no new client/server run occurred. Other builds retain their own contracts. [inf] (formats/windows-603-weapon-cache.md)

## 3.8.8 Exact Linux 6.03 local-file helper

[bin] In the exact inspected Linux 6.03r7 x64 local cache helper, the output status starts false and a nonnull key/context plus mode exactly one are required. At least eight bytes and the GRESCR01 prefix pass recognition only. For a nonzero expected CRC, the helper compares CRC-32 over the stored body after the prefix before invoking its inverse-side block helper. Mismatch returns empty, while equality sets status. Expected CRC zero skips this comparison and leaves status false even if transformed bytes are returned. Returned bytes, status and a valid compiled program are separate outcomes. This is retained static file-format evidence, not a newly observed successful cache read. No original-client execution, transformation algorithm, full malformed-file contract or cross-build equivalence is established. [bin] (formats/linux-603-local-cache-helper.md)

## 3.8.9 Linux 6.x class cache

[bin] On Linux 6.03r7 x64 the class-cache writer transforms the body and then adds the `GRESCR01` prefix, and the reader checks the CRC before the inverse transform. The CRC therefore covers the stored, transformed body. Notes that say this build checks the plaintext after decryption are wrong for this input. [bin] (formats/linux-6x-class-cache.md#how-the-writer-and-reader-order-the-work)

[bin] Packet 197 parses its whole body as one metadata list that includes the expected CRC, with comma, quote and escape handling. When that CRC is zero, the class path skips the validator, deletes the cache entry and may load an empty program. When it is non-zero, it must equal the stored body's CRC, and a header-only file's empty body has CRC zero. So a header-only file is never a class cache hit on this path. On a miss the client sends logical 161 with the stored-body CRC as five offset-integer bytes and then the class name; the field is a CRC, not a modification time. [bin] (formats/linux-6x-class-cache.md#packet-197-and-the-zero-crc); [bin] (formats/linux-6x-class-cache.md#the-class-request-on-a-cache-miss)

[bin] Linux 6.01r1 x86 shows the same split: packet 140 carries a descriptor and a body, and packet 197 carries metadata, and both lead to the same class store. That store uses the modern class-code namespace, not the web-level cache in → §3.8.1–§3.8.5. Nothing here was run; fixtures, malformed files and script execution are untested (→ App. E#202). [bin] (formats/linux-6x-class-cache.md#linux-601-x86-two-delivery-shapes-one-class-store)
