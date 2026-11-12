# Official GS2 bytecode checked against the container reading (6.113 caches)

Date: 2026-11-12. Tags: **[cap]** for what the decrypted caches show, **[bin]** for the earlier engine readings they are checked against.

## Input

A live Windows 6.113 client, run read-only on the owner's own machine, joined one game server and the login server. Its `GRESCR01` caches were then decrypted with the keys that packet 197 carried in that session. That gave 19 script bodies: 6 class scripts from the game server and 13 weapon scripts from the login server. For every one of the 19, the CRC32 that 197 announced matched the cached file. Four more 197 descriptors had no cache file and were left out. **[cap]**

The bodies, keys, CRCs, script and server names stay out of this repository. This note gives structure and counts only.

## Cache file and packet 197

- **197 is a descriptor, not the body.** Its tokens are `type,name,1,key,crc`. The key is two GINT5 words and the CRC is one GINT5. That is Claim C of App. E#202 and the 5.x reading in `v5x-clients.md`. The body comes from the cache file, or from 140 on a miss. **[cap]**
- **The CRC covers the stored, still-encrypted body.** It is the CRC32 of the bytes after `GRESCR01`, before decryption, not of the plaintext. This matches the corrected Windows 6.03 weapon contract (`../formats/windows-603-weapon-cache.md`) and the Linux 6.x class cache (`../formats/linux-6x-class-cache.md`). It contradicts the older "CRC of the plain text" sentence for this build. **[cap]**
- **Encryption:** DES-ECB over whole 8-byte blocks. The last `len % 8` bytes are stored in clear. **[cap]**
- **The plaintext is compiled GS2, not source.** Every body starts with segment type 1. **[cap]**

## Container: what all 19 bodies show

Each body was walked with the reader that `gs2-client-vm.md` gives for 4.2.0.8, 5.0.0.7 and unpacked 6.00. That is a big-endian 32-bit type, then a 32-bit length, then the bytes, for types 1 to 4. **[cap]**

| Check | Result in all 19 |
| --- | --- |
| Segment order | 1, 2, 3, 4, once each |
| Bytes left after segment 4 | none. There is no trailing `0x0A` (the third-party compiler writes one) and no `0xAC` wrapper |
| Segment 1 | one 32-bit word, value 0 |
| Segment 2 | 2 to 110 functions per script. Every op index falls inside the script's own instruction count. 12 of the 19 scripts have names with the `public.` prefix |
| Segment 3 | NUL-terminated strings. The highest string index used is always the last string, so the table and its references line up exactly |
| Segment 4 | decodes with markers `F0`–`F6` at the widths in `gs2-client-vm.md`. No byte `F7`–`FF` appears as a marker. 40 to 15,031 instructions per script |

So the container reading of 4.2.0.8 to 6.00 also holds for what the official 6.113-era server compiler writes. **[cap][bin]**

## Opcodes seen

- **90 distinct opcodes**, the highest being 190. No opcode is 200 or above, which fits the 200–242 folds being made after decode and never written to the stream (`gs2-client-vm.md`, peephole). **[cap]**
- **Jumps:** opcodes 1 to 5 always carry an integer operand (`F3`–`F5`) from 0 to the script's instruction count. That fits jump targets counted in instructions, as `gs2-client-vm.md` says. **[cap]**
- Opcodes 21 and 22 always carry a string-table operand (`F0`–`F2`). Opcodes 45, 46, 80, 150 and 163 carry integer operands. **[cap]**
- **190 (`loadparams`) is emitted.** The third-party compiler has no `params` opcode and never emits 190 (`gs2-client-vm.md`). The official compiler does. **[cap]**
- 48, 49, 54 and 121, the cases added in 5.0.0.7 and 6.00, do not occur in any of the 19 bodies. **[cap]**

## What this settles

- **App. E#202:** on 6.113, 197 is the cache descriptor (`type,name,1,key,crc`), and the CRC is taken over the stored body. It does not carry bytecode. The 4.x bytecode ids (131, and 197 in the 4.x reading) are not covered by this capture. **[cap]**
- **App. E#207:** the four-segment container and the `F0`–`F6` operand encoding are now checked against real server output, not only against engine code and a third-party compiler. **[cap]**
- **App. E#208:** official GS2 bytecode does not use OpenGS1's layout (body offset, constant tables, 4-byte packed values). Whether 3.153's bytecode matches OpenGS1 stays open. **[cap]**

## Still open

- The meaning of opcodes 150, 163 and 180–189 in server output, and why segment 1 is always zero here (an event mask the server leaves empty, or a field the 6.x client ignores).
- Whether 4.x and 5.x servers wrote the same container. These 19 bodies are 6.113-era only.
