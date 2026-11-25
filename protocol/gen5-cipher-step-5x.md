# Gen-5 cipher step count on 5.00r7 and 5.12

Date: 2026-11-16; 5.00r7 static read added 2026-11-24. Research-list rank **#4** (focus 5.007, 5.120). Consolidates E#2 and the lab notes without a new binary session.

Tags: **[bin]** engine frame codec; **[wire]** lab / proxy / stress; **[cap]** earlier Windows dumps; **[inf]** unread builds.

## Settled for Windows 5.12 (`G3D14097`)

**Claim A holds for 5.12.** For zlib (type 4) and bz2 (type 6) frames, 5.12 steps the gen-5 iterator **`len / 4` times, rounded down**, still capped at 4. Uncompressed (type 2) frames round **up**, like later builds. 5.12 encodes the same way when sending and often compresses short bodies, so a stock round-up server drifts after the first short compressed frame. **[bin][wire]** (`v5v6-lab-play.md` § “5.12's cipher step count”).

Lab and stress confirmation:

- A translating proxy that decodes 5.12 with round-down and re-encodes for GServer-v2 lets 5.12 log in and play with no “illegal data” errors. **[wire]**
- Seihai’s 5.12 profile uses `Gen5::round_down` / `protocol.gen5_round_down`. Stress against a lab gserver with `GS_LAB_512_ROUNDDOWN` matches; stock gs2lib round-up fails short compressed bodies. **[wire]** (Seihai `documentation/v5v6-profiles.md`, `documentation/stress-test-2026-10-31.md`).

**Claim B** (every later frame of ten 5.x/6.x captures, including 5.12, decoded with round-up) does not contradict Claim A if those captures never held a compressed frame shorter than 16 bytes whose length was not a multiple of 4 — the only lengths that separate the two rules. Prefer Claim A for server and proxy profiles. **[inf]**

Mac PowerPC 4.04r2 / 4.20r6 / 5.12 receivers also advance compressed bodies by whole groups only (round-down) and raw bodies with a partial last group (round-up). That static Mac result agrees with Claim A’s compressed rule and does not by itself prove Windows 5.00r7. **[bin]** (`protocol/macos-ppc-receive-framing.md`, `client-internals/mac-ppc-404-512/SUMMARY.md`).

## Settled for Windows 5.00r7 (`G3D22067`)

**5.00r7 rounds down like 5.12.** A static read of the stock 5.00r7 engine (stock `GraalEngine.dll`, without the licence-check patch) settles G252. **[bin]** (2026-11-24 static read; nothing was run)

The engine has one receive routine and one send routine for gen-5 frames. Their cipher code is the same, so both directions follow one rule. `L` is the body length after the type byte: the frame length minus one on receive, and the length after compression on send.

| Frame type | Iterator steps | A partial last group (1–3 bytes) |
|---|---|---|
| 2 (raw) | `min(ceil(L / 4), 12)` | is stepped and XORed byte by byte with the low bytes of the iterator |
| 4 (zlib), 6 (bzip2) | `min(floor(L / 4), 4)` | is left as it is and takes no step; a body under 4 bytes takes no step at all |
| 1, 3, 5 | none | these share the raw, zlib and bzip2 handlers but are never XORed |

Each step is `it = it * 0x08088405 + key`, then XOR the next four body bytes with `it` (little-endian). **[bin]**

Other facts from the same read: **[bin]**

- Receive deciphers before it decompresses; send compresses before it enciphers.
- Send picks the frame type from the uncompressed size: 4096 bytes or more is bzip2 (6), 48 or more is zlib (4), and anything shorter is raw (2).
- Both iterators start at `0x04A80B38`. The receive key starts at 0 and the send key at `rand() % 128`.
- A fixed-type mode starts at 3 (the login frame). Once it is 0, each frame's own type byte is used. Where it is set to 0 and how the keys are exchanged were not traced here.
- About 90 other multiplications by `0x08088405` in the engine are `x * 0x08088405 + 1` random-number steps, not the frame cipher.

This matches the probe-proxy lab, where the real 5.00r7 ran 130 canary cases through a proxy that ciphers both directions with the round-down rule, with no lost client [lab] ([fuzz-4x-5x-win-2026-11-19.md](fuzz-4x-5x-win-2026-11-19.md)). The earlier stock GServer-v2 session without a round-down proxy (2026-10-31) must not have sent or received a short compressed body whose length was not a multiple of 4: zlib is only chosen from 48 bytes up, so such frames are uncommon in a short walk. **[inf]**

**Server and profile consequence.** A server or proxy talking to 5.00r7 needs the 5.12 rule (`Gen5::round_down`). Seihai's 5.00r7 row still uses the default round-up rule and should be switched (follow-up in that repository).

## Server / proxy checklist

| Client | Compressed-body steps | Lab against stock GServer-v2 |
|---|---|---|
| 5.12 | round **down** (`len/4`, cap 4) | needs proxy or `GS_LAB_512_ROUNDDOWN` |
| 5.00r7 | round **down** (`len/4`, cap 4), read in both directions | needs proxy or round-down; the 2026-10-31 stock session never hit a discriminating frame |
| 5.24r4 and later (focus 6.037 too) | round **up** | normal |

## Open

- [x] ~~Static read of Windows 5.00r7 frame codec (short zlib/bz2, len not multiple of 4), both directions.~~ Round down, both directions (G252, [above](#settled-for-windows-500r7-g3d22067)).
- [x] ~~Optional: publish one 5.12 capture snippet that contains such a short compressed frame so Claim B can be retired in E#2 with a cited decode.~~ Done (G253, [below](#a-short-compressed-512-frame-under-both-rules-g253-2026-11-25)).
- [x] ~~Confirm whether any non-5.12 Windows 5.x build shares 5.12’s round-down (none claimed today).~~ 5.00r7 does (G254, [above](#settled-for-windows-500r7-g3d22067)). 5.24r3 and later round up.

## A short compressed 5.12 frame under both rules (G253, 2026-11-25)

Windows 5.12 (packed `Graal.exe`) under Wine in the loopback-only lab VM, behind
the probe proxy, which deciphers zlib and bzip2 frames with round-down and raw
frames with round-up. A lab-only switch logged the iterator state, the key and
the raw bytes of each short compressed frame. Rows are in `probe-results.tsv`
under `raw512-a` and `raw512-b`. **[lab]**

**Normal play does not produce a discriminating frame.** The client compresses
only bodies of 48 bytes or more, and ordinary traffic compresses to about 50
bytes or more: in a 75-second baddy session (`raw512-a`) the smallest of 385
client zlib frames had L = 51, and the server's five compressed frames had L ≥ 47.
This is why the ten earlier captures (Claim B) decoded with round-up.

**A repetitive chat does.** A GS2 NPC set the player's chat to 44, 45, … 99 × `a`
every 0.7 s (`raw512-b`). Each chat packet compresses to 14 or 15 bytes: 64 of
the 66 client zlib frames had L < 16 and L % 4 ≠ 0. All 64 inflate under
round-down and none under round-up. The proxy reported no decode error for any
frame of the session in either direction, and each short frame's state after
round-down equals the logged state before the next client frame.

One of them, client to server, type 4, L = 15:

```
iterator before da556298 (hex), key 64
raw (len, type, body):  0010 04 40d112cda92bf370884aaabe2f1151
round-down, 3 steps:    789c53d2f1492401700100a42f1151
  -> inflates to 22 2c 4c + 44 x 61 + 0a: PLI 2 (player props), prop 12 (chat), 44 x "a"
  -> iterator after 1aaa4bf8 (hex)
round-up, 4 steps:      789c53d2f1492401700100a4374d6e
  -> zlib error (incorrect data check: the Adler-32 trailer is XORed)
```

Each step is `it = it * 0x08088405 + key`, then the next four body bytes are
XORed with `it` little-endian. The two rules agree on the first 12 bytes and
differ only on the partial last group. The next client frame (L = 15, raw
`0010 04 60c06ca649615d94a8be2cce6711b3`) inflates to the 45 × `a` chat from
state `1aaa4bf8` (hex) and fails from the round-up state, so a round-up decoder
loses the stream at the first such frame. The decode above was re-checked
offline from the quoted bytes.
