# Gen-5 cipher step count on 5.00r7 and 5.12

Date: 2026-11-16. Research-list rank **#4** (focus 5.007, 5.120). Consolidates E#2 and the lab notes without a new binary session.

Tags: **[bin]** engine frame codec; **[wire]** lab / proxy / stress; **[cap]** earlier Windows dumps; **[inf]** unread builds.

## Settled for Windows 5.12 (`G3D14097`)

**Claim A holds for 5.12.** For zlib (type 4) and bz2 (type 6) frames, 5.12 steps the gen-5 iterator **`len / 4` times, rounded down**, still capped at 4. Uncompressed (type 2) frames round **up**, like later builds. 5.12 encodes the same way when sending and often compresses short bodies, so a stock round-up server drifts after the first short compressed frame. **[bin][wire]** (`v5v6-lab-play.md` § “5.12's cipher step count”).

Lab and stress confirmation:

- A translating proxy that decodes 5.12 with round-down and re-encodes for GServer-v2 lets 5.12 log in and play with no “illegal data” errors. **[wire]**
- Seihai’s 5.12 profile uses `Gen5::round_down` / `protocol.gen5_round_down`. Stress against a lab gserver with `GS_LAB_512_ROUNDDOWN` matches; stock gs2lib round-up fails short compressed bodies. **[wire]** (Seihai `documentation/v5v6-profiles.md`, `documentation/stress-test-2026-10-31.md`).

**Claim B** (every later frame of ten 5.x/6.x captures, including 5.12, decoded with round-up) does not contradict Claim A if those captures never held a compressed frame shorter than 16 bytes whose length was not a multiple of 4 — the only lengths that separate the two rules. Prefer Claim A for server and proxy profiles. **[inf]**

Mac PowerPC 4.04r2 / 4.20r6 / 5.12 receivers also advance compressed bodies by whole groups only (round-down) and raw bodies with a partial last group (round-up). That static Mac result agrees with Claim A’s compressed rule and does not by itself prove Windows 5.00r7. **[bin]** (`protocol/macos-ppc-receive-framing.md`, `client-internals/mac-ppc-404-512/SUMMARY.md`).

## Still open: Windows 5.00r7 (`G3D22067`)

No frame-codec read of the 5.00r7 engine for the short-compressed step rule is on record in this repo. Seihai’s 5.00r7 row uses the **default round-up** rule (every other gen-5 build except 5.12). A stock GServer-v2 accepted real 5.00r7 in the 2026-10-31 lab beside Seihai without a round-down proxy, which is consistent with round-up (or with a session that never hit a discriminating short compressed frame). **[wire][inf]** (`documentation/v5v6-profiles.md` lab check; not a closed proof).

**Do not** copy 5.12’s round-down onto 5.00r7 until the 5.00r7 decoder is read or a discriminating capture is decoded both ways.

## Server / proxy checklist

| Client | Compressed-body steps | Lab against stock GServer-v2 |
|---|---|---|
| 5.12 | round **down** (`len/4`, cap 4) | needs proxy or `GS_LAB_512_ROUNDDOWN` |
| 5.00r7 | treat as round **up** until read | worked without round-down in the 2026-10-31 stock check |
| 5.24r4 and later (focus 6.037 too) | round **up** | normal |

## Open

- [ ] Static read of Windows 5.00r7 frame codec (short zlib/bz2, len not multiple of 4), both directions.
- [ ] Optional: publish one 5.12 capture snippet that contains such a short compressed frame so Claim B can be retired in E#2 with a cited decode.
- [ ] Confirm whether any non-5.12 Windows 5.x build shares 5.12’s round-down (none claimed today).
