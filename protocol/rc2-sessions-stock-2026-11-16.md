# RC2-line sessions: post-signature, weapons, and tokens (stock)

Date: 2026-11-16. Tags: **[lab]** for a held RC3↔lab-gserver decode; **[bin]** for receive tables / tokens.

Leads-only against a third-party RemoteControl claim. No keys or hosts. Extends [`rc-list-online.md`](rc-list-online.md) and App. E#405.

## After the signature packet

On a stock **RC3** session against a lab gserver (same `GSERV025` family as RC2 2.05):

- After S→C **25** (signature) then **194** (clear-weapons), the client sends C→S **154** server-text of the form `GraalEngine,irc,login,-` (plus other lister/pm texts). **[lab]**
- So the post-signature **IRC login request** is stock-aligned. **[lab]**

## Clear-weapons does **not** drive prop 35 + `location`

A third-party claim that S→C **194** causes prop **35** = 1 and then C→S **94** `location` is **not** what stock RC3 does. **[lab]**

- After 25/194, stock sends C→S **2** with prop **53** (status/nickname family) — **never** prop 35 in that window. **[lab]**
- C→S **94** `location` appears when a **`(Server)`** player is present (NC-on-server discovery), after S→C **55**, not as an unconditional 194 reaction. Without `(Server)`, no `location` in the post-login window. **[lab]**
- RC3 published receive tables **omit 194** (handler may ignore). **[bin]**

Keep `location` tied to **(Server)/NC discovery**, not to clear-weapons. **[lab][bin]**

## Weapons (GUI) ≠ RC-socket 140 GS2 hosting

Stock RC2/RC3/Linux images contain **Weapons (GUI)** UI strings, but that surface is the **NC weapon list/editor**, not RC-socket GS2 bytecode hosting. **[bin]**

- RC3 (and RC2-line) receive tables **lack S→C 140** (and 194) on the RC socket. **[bin]**
- Lab session: **no** S→C **140** delivered to RC3. **[lab]**
- NC weapon traffic uses **115/116** ↔ **167/192** (or **33** on older NC tokens) — not RC **140**. **[bin][lab]**

## `GSERV025` is not every RC2-shaped build

| Build | Token | Tag |
| --- | --- | --- |
| RC2 2.05 / RC3 | **`GSERV025`** | [bin] |
| Batch-2 Linux **2005/12/09** | **`GSERV024`** | [bin] |
| Batch-2 Linux **2006/01/20** | **`GSERV025`** | [bin] |

Accept both on RC login. This narrows App. E#405: builds that send `GSERV025` are identified; earlier ladder rungs still send `GSERV024`. **[bin]**

## Still open

- Live RC2 2.05 session (blocked in this lab); RC3 stands as the GSERV025-era proxy. **[lab]**
- Optional static 194 handler confirm on RC2/RC3 (wire already settles no prop35+location). **[bin]**
