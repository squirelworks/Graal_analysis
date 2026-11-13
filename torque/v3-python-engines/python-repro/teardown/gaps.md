# Gaps

| gap | what was tried |
| --- | --- |
| English names of login strings A (a client field), B, C, and the id-37 payload | xrefs fall in a client routine and the login functions. The literals are not in those functions. a client routine was larger than the dump cutoff |
| Byte at `connection+0x13` on the first record | the object is zero-filled. No later store was found. Treated as `0x20` only if it stays zero |
| a client routine and a client routine | called from the flush for modes 3–6. Not decompiled. `inflate 1.1.3` has no code reference |
| LCG key words at `connection+0x08`, `+0x10`, and the 4 bytes at `+0x0B` | the XOR formula is in a client routine. The values written before login were not read, so a remote host cannot be reproduced byte-for-byte |
| Login accept opcode | no matcher. Inbound player parse stops outside ids 0–10 |
| a client routine (`setplayerprop`, `playerhp`) | decompile failed |
| Property-id tables a client global and a client global | the VA range reads as zeros in this project. The loop in a client routine is real. The id list is not |
| Most property ids past sword, shield, and head | the switch encodes them. The fields have no name |
| NPC and baddy property streams | section names and object sizes only |
| Walk step, blocking tile, water tile, ledge | keys and animation names exist. The 64-bound is in the board writer. No step function |
| `GRMAP001` body | a client routine is 22 KB and was not walked |
| Gani call order | three functions reference `.gani`. Order not recovered |
| One send at an address | the id register was not an immediate |
| vtable bytes at an address | the slot reads as zero in the mapped image. Callers still show `(*a client field)` with the same id immediates a client routine uses, so that slot is the sender. Confidence medium |
