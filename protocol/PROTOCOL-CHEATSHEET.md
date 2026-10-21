# Protocol Cheat Sheet — 39ster 2.1 / Seihai

Default port: **14822**

## Frame
```
[u16 BE length] [zlib payload]
```
Payload = one or more messages separated by `0x0A`.

## GCHAR
```
enc1(v) = (v + 32) & 0xFF
dec1(b) = (signed char)(b - 32)

encN(v, n): for i = n-1 downto 0: emit (((v >> (7*i)) & 0x7F) + 32)
```
Used for opcodes, most props, coords, IDs. Frame length and raw tiles are **not** GCHAR.

## Login (first packet, unscrambled)
```
type:u8_gchar
[key:u8_gchar]          // only if type == 0 (PLAYER)
version:7|8 raw bytes
mystery:1 raw byte
namelen:u8_gchar + name
passlen:u8_gchar + pass
```

## Player scramble (every later packet)
```
iterator = 0x04A80B38 initially
iterator = iterator * 0x8088405 + key
pos = (iterator & 0xFFFF) % count + 1
drop byte at pos-1
```
RC clients: no scramble.

## Outgoing
Append message + `\n`. Compress (zlib) when ≥ 4096 bytes or on flush. Prefix 2-byte BE compressed length. Send in 1024-byte slices.

## File ops (server → client)
- 100 = FILELEN
- 101 = TILES
- 102 = FILEBLOB

## Start map
`level13.graal`

## Note (2026-10-21)

The "player scramble" above is gs2lib **gen 3** as seen by the server, which deletes one byte per message. On the 2.05 client side the byte is inserted, and its value is `((it >> 16) & 0x7F) + 0x20`. Insertion starts with the second message. The login's "key" GCHAR comes right after the type byte. RC 1.x is also gen 3. Only the web client is unscrambled. See `codec-and-framing.md`.
