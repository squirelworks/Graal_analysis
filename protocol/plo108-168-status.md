# PLO 108 sub 1 and PLO 168 — status

Date: 2026-11-16. Research-list rank **#43** (focus 4.208 / 6.037; adjacent 5.x). Consolidates `unknown-ids-2026-11-06.md`; **no new xref or idle/reconnect lab** this pass.

Tags: **[bin]** layout and handlers; **[cap]** 108→162 round trip; **[srv]** login-burst habit; **[inf]** open sub-1 reader and “login done” meaning.

## PLO 108 — ping / keepalive (settled for sub 0)

| Fact | Evidence |
|---|---|
| Layout ≥ 3 bytes: `c sub`, then `s value` | **[bin]** 4.20r8, 6.03r7 |
| `sub` 0 → client answers **PLI 162** with `!` + `s min(value, 0x6FFF)` | **[bin]**; **[cap]** Linux 6.03r7 vs seihai-gserver loopback, 30/30 echo |
| Game clients 4.20 / 6.x send 162 **only** from the 108 handler; 5.00r7–5.31r4 neither handle 108 nor send 162 | **[bin]** |
| RC3 / 2010 Linux RC: 162 empty body every 60 s; no 108 handler | **[bin]** |
| 100 and 108 are taken **before** the main switch on 4.20 / early 6.x; 6.11 loads 108 via the script table | **[bin]** |

Settles manual App. E#5 (id 162). A server can RTT-measure a game client with `{108}{c 0}{s seq}`.

## Still open: 108 `sub` 1

- Handler stores `value` on the connection object. On Windows 6.03r7 the field is written (setup, reset, this handler) and **no local reader** was traced; a reader through a pointer cannot be ruled out from a static scan. **[bin]**
- Beta4 gserver comment only says type 1 is stored. **[srv]**
- Lab sub-1 probe did not produce a valid run (lab server sent sub 0). **[cap]** residual
- 6.11 slot mapping was not traced for sub 1. **[bin]** residual

**Next:** **S** broader xref / data-flow on 6.03r7 and 4.20r8; **L** idle/reconnect once a lab can emit `sub` 1.

## PLO 168 — “logged in” flag (layout settled; meaning medium)

| Fact | Evidence |
|---|---|
| Empty body; every client from 2.05 on handles it | **[bin]** |
| 2.05–2.31 call a local-player routine with flag 1; 4.20 / 6.03r7 set one byte on the player object | **[bin]** |
| Gserver sends it right after the login burst | **[srv]** |
| Lab caps show empty 168 then 194 from GServer-v2 (server habit, not a public world) | **[cap]** |

**Confidence:** high that it is a one-shot empty flag; **medium** that the flag means “login done” rather than another session gate.

**Next:** **L** idle/reconnect / warp sessions that correlate the byte with UI or further packet acceptance (after #1 assets path).

## Open checklist

- [ ] Find any reader of the 108 sub-1 stored field (or prove none on focus builds).
- [ ] Emit `{108}{c 1}{s n}` on loopback and record client behaviour.
- [ ] Correlate 168’s player byte with post-login UI / packet gates on 4.208 and 6.037.
