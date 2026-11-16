# Official GS2 bodies: trailing newline scan (enlarged)

Date: 2026-11-16. Tags: **[cap]** for the offline body walk; **[bin]** for the existing stock `setScript` reading.

Leads-only confirm. No third-party code. Bodies, keys and names stay out of this repository — counts only.

## Trailing `0x0A`

The published nineteen-body note already reports **no** bytes after segment 4 and **no** trailing `0x0A` on official 6.113-era caches. **[cap]** ([gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md))

An enlarged offline walk with an independent reader over **660** held GS2 bodies finds trailing `0x0A` in **0 / 660**. **[cap]**

Leading `0xAC` file wrappers are likewise absent from the official nineteen plaintext bodies. **[cap]**

## Stock readers (existing static)

On 4.2.0.8, 5.0.0.7 and unpacked 6.00, `setScript` walks big-endian type/length segments for types 1–4. A trailing `0x0A` is not a segment, so it ends the walk the same way a non-segment would — the already-decoded script is kept. A leading `0xAC` file wrapper is **not** stripped and yields no instructions. Packet **140** carries a GSHORT info-length envelope, not that file form. **[bin]** ([gs2-client-vm.md](gs2-client-vm.md))

So: official caches omit the trailer; stock clients that see one still load the segments. Matching official cache bytes means **not** appending `0x0A` after segment 4. **[cap][bin]**

## Still open

- Optional loopback fixture with and without a trailer on **4.20r8**, **5.12**, and **6.03r7** (static already predicts both load).
- Wire packaging of 140 / 197 vs any file-side wrapper remains a separate packaging question (PG7 / existing client-vm note).
