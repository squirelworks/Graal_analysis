# RC props tail, SET2 last byte, and PLO 124 (gap #42)

Date: 2026-11-16. Research-gaps / research-list rank **#42**. Closes the *status* half of E#420 / E#421 and the 124 layout question from #254 / `unknown-ids-2026-11-06.md`.

**Questions:** Which count in the RC props tail is flags and which is chests? What is the last byte of `RC_PLAYERPROPSSET2` (76)? What is the layout of S→C **124**?

**Answer so far:**

| Item | Status | Evidence |
|---|---|---|
| Tail of 72/76 after props: `s`, `s`, then `c` weapon count + weapon `str`s | **Settled** | 2004 RC capture **[cap]** `rc-capture-2026-11-04.md` |
| Which `s` is flags vs opened chests | **Open** | both were **0** in the only capture; E#420 |
| Extra trailing byte on C→S **76** (absent on S→C **72**) | **Seen = 0**; meaning **open** | E#421 **[cap]** |
| PLO **124** name | **Settled as** `PLO_RC_PLAYERFLAGS` (proposed) | RC3 log text **[bin]** |
| Who handles 124 | **RC3 only** (not 2004, not 2010, not Linux 2005, not any game client 1.21–6.03r7) | `unknown-ids-2026-11-06.md` **[bin]** |
| 124 payload | **Unread** — RC3 logs and **discards** the body | same **[bin]** |

Tags: **[cap][bin][doc]**. No new capture or RC binary session in this pass.

## Settles-it labs (unchanged)

1. Capture 72 for a player with **some flags and no opened chests** (and the reverse) → assigns the two `s` counts (E#420).
2. S of the 2004 RC’s 76 builder, or a capture after editing other dialog fields → last byte (E#421).
3. 124 layout needs a **server that emits 124** plus either an RC3 memory/log dump of the body before discard, or a static read of the writer on an original/modern server that sends it. RC3 alone cannot settle the bytes.

## Focus / Seihai impact

Staff tooling only. Game focus builds are unaffected. seihai-rc profiles should keep both tail `s` counts and the 76 trailing byte as **unknown** until the lab above lands.
