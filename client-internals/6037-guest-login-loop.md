# 6.037 guest login loop and login-script gotchas (status)

Date: 2026-11-16

Status note for research-list **C7–C9** / assigned lead **L4** (6.037 guest
login). Confirmed pieces from existing **[bin]** / **[lab]** notes; Others Work
script gotchas stay **unconfirmed** until a stock Win 6.03r7 loopback session
(assets) or an owner-approved light public Login capture under the traffic
rules.

Tags: **[bin]** · **[lab]** · **[inf]** · lead-only where marked.

## What we already settle **[bin]** **[lab]**

| Fact | Evidence |
|---|---|
| 6.01/6.03 open a normal game connection to a server named **`Login`**; no separate list protocol | `protocol/v6x-clients.md`, `protocol/login-session-known.md` |
| Login hosts are **compiled in** (scrambled); no `license.graal` path like 4.x | `v6x-clients.md` |
| Guest logins send account `guest` with a password decrypted at run time from compiled-in bytes | `v6x-clients.md` — **do not** publish the password or raw key bytes |
| Auto-guest at the login screen is the observed Windows 5.x/6.x habit in lab | `protocol/v5v6-windows-unpacked.md`; manual §2.3 |
| Named (non-guest) world login works when a Login weapon calls `adventure_setaccountname` / `adventure_setpassword` before `serverwarp` | `protocol/named-login-5x-6x.md` **[lab]** on 5.24r4 and Linux 6.03r7 |
| After that setter, `getloginaccountname()` can still read `guest` on 6.03r7 | same note — setter changes the **next** connect, not necessarily the current script view |
| **178** ends Login mode and reconnects to a play server | `login-session-known.md` |

Built-in guest password values stay **out of this repo** (AGENTS / conventions).

## Others Work leads (C7–C9) — unconfirmed

Folded into L4 / research **#2**. Treat as locator claims until stock **S+L**.

| Id | Claim (lead only) | Our stance |
|---|---|---|
| **C7** | Full guest → account form → reconnect with typed account is the stock 6.037 Login path | **Partial.** Guest-first and compiled Login hosts are **[bin]**; the full form/reconnect loop is **not** written as a step checklist from our own Win 6.03r7 session yet. |
| **C8** | Password-control **text is always empty**; scripts must emptiness-test / apply-password, never read the control text | **Unconfirmed.** No stock UI control-text lab in the public notes. |
| **C9** | Handler-name binding; reject dialog appears **behind** the form; form re-create on guest reconnect drops weapon locals; only `lowercase(str)` exists (`lower` / `str.lowercase` missing, silent unless missing-function log is on) | **Unconfirmed** as a cluster. Related: named-login lab already uses underscore `adventure_*` names that exist on 6.03r7. |

## Contrast with 4.208 (C4)

4.20r8 Login entry is a **built-in account dialog** with the **typed** account on first connect (no guest-first step on the 4.2 engine profile). That write-up is a separate research track (open PR for the v4 login contract). Do not merge 6.037 guest-first behaviour into the v4 contract.

## Open (needs assets / Win 6.037 / traffic light)

1. Loopback **L** on Win 6.03r7 with base assets: guest → form → typed reconnect → 178, as a numbered checklist.
2. Stock **S** (or UI session) for C8 password-control emptiness and C9 handler / dialog / `lowercase` claims.
3. Public Login light capture only under owner traffic rules + Chiaki plan (**#2**) — not required to finish the loopback checklist.
4. Whether Linux `G3D0511C` and Win `G3D0311C` differ on any C7–C9 step (**#7** adjacency).

## Implications for Seihai / labs

- Lab Login may start clients as `guest`; use the named-login weapon pattern when account files must persist.
- Do not encode Others Work C8/C9 script rules into server or weapon docs until stock confirms them.
- Keep guest password material local; public notes say only that a compiled-in guest password exists.
