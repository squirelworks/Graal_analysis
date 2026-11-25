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
- [x] ~~Whether `getloginaccountname()` and a password GUI control exist on 4.20r8.~~ [Read 2026-11-25](#login-account-script-api-by-build-g323-2026-11-25): no `getloginaccountname()` on 4.20r8; a `password` flag on `GuiTextEditCtrl` exists in every build. **[bin]**
- [ ] Behaviour of a v6 `-LoginScreen` / `-Serverlist` weapon when pushed to a 4.x Login session (hidden vs bail on empty account-name).
- [ ] C21 event order: login-signature before weapons; PLO 190 relative to weapon delivery — for login-weapon authors.
- [ ] Listserver `VERIACC2` path when the world verifies accounts (our 4.04 lab used localhost / proxy accept without that check).

Public Login capture remains on the #2 plan-hold (Chiaki). Loopback stock-UI work does **not** wait for that plan.

## Login-account script API by build (G323, 2026-11-25)

Static read of the stock engines (the same files as G262: 4.20r8 unhooked engine, 5.00r7 stock engine, 5.12 memory image, 6.03r7 third-party unpack); nothing run. "Registered" means the name is paired with a native in the script-function table, not just present as a string. **[bin]**

| Build | `getLoginAccountName()` | Other account / password script functions | Password text field |
|---|---|---|---|
| 4.20r8 | **absent** (the name is nowhere in the binary, ASCII or UTF-16, any case) | `Adventure_setAccountName(s)`, `Adventure_setPassWord(s)`, `Adventure_updateAccountField()`; no `GuiAccountPasswordCtrl` | `password` (bool) on `GuiTextEditCtrl` |
| 5.00r7 | registered, returns a string | `Adventure_setAccountName`, `Adventure_setPassWord`, `Adventure_getEditAccountNames`; new `GuiAccountPasswordCtrl` (`applyPassword`, `clearPassword`, `isEmpty`, `setPasswordOfAccount(s)`); `updateAccountField` gone | `password` (bool) |
| 5.12 | registered | same as 5.00r7 | `password` (bool) |
| 6.03r7 | registered | same set as 5.x, names in lower case | `password` (bool), now derived from a new string field `inputtype` (`"password"` or `"default"`; the mobile builds also take `email`, `url`, `numbers`) |

What the natives do:

- `getLoginAccountName()` returns the account held by the current game-server connection (set on the "Connecting to the game server…" path), falling back to `getGraalAccountName()`, the account typed for the login frame. Which object holds that connection account is a medium-confidence reading.
- `Adventure_setAccountName(s)` sets the global login account and mirrors it into the local player; unless the name is `guest` or starts with `guest`, it is added to the account history and saved as the `accountname` pref.
- `Adventure_setPassWord(s)` sets the global password and saves it unless `dontsavepasswords` is set or the account is a guest. `GuiAccountPasswordCtrl.applyPassword` calls the same setter with the control's own text.
- `password` on the text-edit control: when set, drawing replaces each character with a hard-coded `*`, and the copy path returns early. There is no mask-character field and nothing named `passwordmask` or `ispassword`.

So a 4.20r8 login script has no `getLoginAccountName()` to read the account back; it uses a `GuiTextEditCtrl` with `password = true`, and calls `Adventure_setPassWord(text)` itself. A v5/v6 login weapon that calls `getLoginAccountName()` or creates a `GuiAccountPasswordCtrl` will not find them on 4.20r8.  Whether 4.20r8 exposes any other script getter for the login account was not part of this read.

## Server / script checklist

| Audience | Rule from settled rows |
|---|---|
| Lab Login for 4.x | Accept a typed / saved account on first connect; do not require a guest→reconnect dance. |
| Lab Login for 5.24+ / 6.03 | Expect `guest` first; use a clientside setter weapon (or equivalent) before world warp if flags must save. |
| Login-weapon authors | Treat 4.x and 5.x/6.x as different account machines until the open rows above are closed. |

## Open

- Stock 4.20r8 UI session (checkboxes above).
- Fold confirmed rows into `login-session-known.md` and the 4.20r8 profile once closed.
