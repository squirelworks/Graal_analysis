# v4 Login account contract (4.20r8 focus)

Date: 2026-11-16. Research-list rank **#2** fold **C4** (focus 4.208). Consolidates existing notes; no new binary or public-Login session.

Tags: **[bin]** 4.x engine / launcher; **[live]** 4.04r2 Wine lab; **[cap]** 5.x/6.x guest path; **[doc]** cross-links. Others Work claims stay **leads** until a stock 4.20r8 UI session confirms them.

## Settled from our evidence

| Claim | Behaviour | Evidence |
|---|---|---|
| No listserver protocol | 4.x dials a game server named `Login` from `license.graal` (host + two fallbacks). The server list lives inside that session. | `v4x-clients.md` **[bin]**; `4.04-4.20.toml` `listserver = "none"` |
| Login frame carries account + password | After type, key and token: GCHAR-length account, GCHAR-length password, then platform and machine fields. | `v4x-clients.md`; `4.04-4.20.toml` `login_layout` **[bin][cap]** |
| Guest accounts are not saved | Accounts named `guest` or starting with `guest` are never written to the account store. | `v4x-clients.md` **[bin]** |
| Login-mode draw mask | While the lowercase server name starts with `login`, the draw-layer mask is 0 (no players, no HUD). S→C 178 moves the client to the named host:port. | `live-behaviour-404.md`; profiles **[bin][live]** |
| S→C 190 on 4.20r8 | Treated as the Login server accepting the session (`onServerListerConnect`). | `login-session-known.md` **[bin]** |
| Nickname ≠ account | Own prop 0 is the start-screen Nickname field, not the login account string. | `live-behaviour-404.md` (`Real404`) **[live]** |

Contrast with **5.x / 6.x** (same Login-as-game-server shape, different account UX):

| Era | First Login account | How a named world account is reached |
|---|---|---|
| 4.x (4.04r2 / 4.20r6 / 4.20r8) | The account string in the login frame (typed / saved). Guest names are refused for save. | Same account on 178 reconnect unless scripts change it. |
| 5.24r4 / 6.03r7 | Built-in **`guest`** with a family password (private notes). | Lab: Login weapon calls `adventure_setaccountname` / `adventure_setpassword` before warp; world login uses the new name. **[lab]** `named-login-5x-6x.md` |

So the “no guest step on first connect” part of C4 is already the **4.x vs 5.x/6.x** split in our profiles (`guest_login = true` only on the 5.00–6.03 table). **[cap][doc]**

The 4.x Delphi launcher hands the engine login-related callbacks through the `graal_set…` exports (same pattern as 5.x’s `graal_setOnServerLogin` / `graal_setOnServerListerConnect`). That is consistent with a **host-side account UI**, but this note does not claim the exact dialog layout from a stock 4.20r8 UI capture. **[bin][inf]**

## Still open (leads / stock UI)

Others Work C4 / G3 claims below are **not** promoted to settled behaviour. Confirm on **stock** 4.20r8 (not the packet-logger engine) under loopback before citing as ours:

- [ ] Built-in account dialog layout and which fields feed the first Login frame (account vs nickname vs password).
- [ ] Whether `getloginaccountname()` and a password GUI control exist on 4.20r8 (named-login notes cover 5.24r4 / 6.03r7 only).
- [ ] Behaviour of a v6 `-LoginScreen` / `-Serverlist` weapon when pushed to a 4.x Login session (hidden vs bail on empty account-name).
- [ ] C21 event order: login-signature before weapons; PLO 190 relative to weapon delivery — for login-weapon authors.
- [ ] Listserver `VERIACC2` path when the world verifies accounts (our 4.04 lab used localhost / proxy accept without that check).

Public Login capture remains on the #2 plan-hold (Chiaki). Loopback stock-UI work does **not** wait for that plan.

## Server / script checklist

| Audience | Rule from settled rows |
|---|---|
| Lab Login for 4.x | Accept a typed / saved account on first connect; do not require a guest→reconnect dance. |
| Lab Login for 5.24+ / 6.03 | Expect `guest` first; use a clientside setter weapon (or equivalent) before world warp if flags must save. |
| Login-weapon authors | Treat 4.x and 5.x/6.x as different account machines until the open rows above are closed. |

## Open

- Stock 4.20r8 UI session (checkboxes above).
- Fold confirmed rows into `login-session-known.md` and the 4.20r8 profile once closed.
