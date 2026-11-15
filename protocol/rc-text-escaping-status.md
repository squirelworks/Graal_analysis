# Original RC text escaping (gap #41)

Date: 2026-11-16. Research-gaps / research-list rank **#41**. Tracks seihai-rc#56 (escaped-backslash half) and related E#422 folder-rights quoting. Staff tooling only.

**Question:** How did the original gserver and RC2/RC3 escape backslashes and empty fields in script GET/SET text? That settles the beta4 and “original” server profiles in rc.

**Answer so far:**

| Piece | Status | Evidence |
|---|---|---|
| Tokenized CSV: quote when needed; `""` → one `"` | **Settled** (general) | RC capture notation; seihai-rc decoder **[cap][doc]** |
| Trailing empty field must be retained on NPC/class script readback | **Settled in seihai-rc** | seihai-rc#57 / #56 partial **[doc][test]** |
| Bare backslash in unquoted text round-trips as one `\` | **Settled for seihai-gserver path** | seihai-rc preserves literals **[doc][test]** |
| Quoted lines with `\` on the **GServer-v2 fork** arrive with **doubled** backslashes | **Settled as fork behaviour** | seihai-rc#56 (source comparison, not GUI) **[doc]** — do not copy GPL encoder |
| Same bytes mean different logical text depending on producer | **Settled** | owner comment on #56 **[doc]** |
| **Original** RC2 2.05 / RC3 decode of escaped `\` | **Open** | need S of those clients, then L |
| Original / upstream beta4 encode rule vs fork | **Open** | owner wants beta4 profile pinned from its source **[doc]** |
| Folder-rights quoting (CSV vs bare) | **Related open** | E#422 / `rc-capture-2026-11-04.md` **[cap]** — fork returned unquoted `rw levels/*` |

Tags: **[cap][doc][test]**. No new RC binary session in this pass. No GPL code copied.

## Owner direction (already decided — not “Squirrel decides” again)

From seihai-rc#56 (2026-11-16): use **server version profiles** on the rc connection (same idea as client profiles), not one global decode rule:

| Profile | Decode rule |
|---|---|
| **seihai-gserver** (default / unknown) | Keep backslashes as sent (rc follows gserver, not the reverse) |
| **gserver-v2 `seihai` branch** | Doubled backslashes inside quoted lines |
| **gserver-v2 beta4 (upstream)** | Pin from upstream beta4 behaviour |

One fixture per profile; quirks live in one table. Implementation belongs in **seihai-rc** (and optional seihai-gserver identity string), not in this note.

## Still open for gap #41 evidence

| Item | Status |
|---|---|
| S: RC2 2.05 and RC3 script GET/SET text decoders (backslash + empty fields) | **Open** |
| L: round-trip against an original-era server reply (or a capture of one) | **Open** |
| Pin beta4 encode facts into the beta4 profile table | **Open** (seihai-rc) |
| E#422 folder-rights CSV on an original 2.x server | **Open** (separate lab; same CSV family) |

## Next steps

1. S of RC2/RC3 text builders/readers → fill the “original” column for the profile table.
2. seihai-rc: implement the three profiles + fixtures (tracked on #56 / NEXT).
3. Optional: E#422 capture with flags≠0 or original rights reply.
