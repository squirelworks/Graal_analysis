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

- [x] ~~Built-in account dialog layout and which fields feed the first Login frame (account vs nickname vs password).~~ [Read 2026-11-25](#built-in-account-dialog-and-the-first-login-frame-g322-2026-11-25): engine-side GS2 start screen; account + password in the frame, nickname sent later as prop 0. **[bin]**
- [x] ~~Whether `getloginaccountname()` and a password GUI control exist on 4.20r8.~~ [Read 2026-11-25](#login-account-script-api-by-build-g323-2026-11-25): no `getloginaccountname()` on 4.20r8; a `password` flag on `GuiTextEditCtrl` exists in every build. **[bin]**
- [x] ~~Behaviour of a v6 `-LoginScreen` / `-Serverlist` weapon when pushed to a 4.x Login session (hidden vs bail on empty account-name).~~ [Read 2026-11-25](#v6-login-screen-weapons-on-a-420r8-login-session-g324-2026-11-25): hidden, because 4.20r8 drops 140/197 and the weapon gets no script. **[bin]**
- [x] ~~C21 event order: login-signature before weapons; PLO 190 relative to weapon delivery — for login-weapon authors.~~ [Read 2026-11-25](#login-event-order-for-login-weapon-authors-g325-2026-11-25): 25 gates nothing; weapons must be loaded before 190 to see `onServerListerConnect`; ghost mode drops weapon packets. **[bin]**
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

## Built-in account dialog and the first Login frame (G322, 2026-11-25)

Static read of the 4.20r8 launcher (`Graal4.exe`) resources and the same 4.20r8 and 5.00r7 engines as G323; nothing run. **[bin]**

**Where the dialog lives.** The 4.20r8 launcher has no account form among its Delphi form resources (Options, controls, player list, profile and message forms only). The dialog is in the engine: the engine carries 13 compressed, compiled GS2 scripts, and one of them builds the start screen (`MainMenuGui2D`). It was decoded with our GS2 opcode table.

| Control | Class | Label / role | Notes |
|---|---|---|---|
| `NickEdit` | `GuiTextEditCtrl` | Nickname: | Separate input; not derived from the account |
| Play as: Guest / Member | radio pair | account kind | Guest is hidden; on wake the dialog always checks Member |
| Save password | checkbox | tied to the `dontsavepasswords` pref | |
| `AccountEdit` | `GuiPopUpEditCtrl` | Account name: | Drop-down of the account history |
| `PassEdit` | `GuiTextEditCtrl` | Password: | `password` flag set |
| Start | button | starts the login | see below |
| Become a Member / Options / Offline Test | buttons | signup URL, options, offline mode | |

No edit field sets a maximum length. Account, password and nickname are each cut to 223 bytes only when the packet is built.

**What Start does.** It calls `Adventure_setNickName`, `Adventure_setAccountName` and `Adventure_setPassWord` with the three field values, clears the password field, then calls `Adventure_openServerList`, which connects to the server named `Login` (a game server on 4.x). The hidden Guest path would pass `guest` as both account and password instead.

- Each native setter fills its own global and saves a pref; the account name is also copied to the local player.
- The account history keeps five entries. Names that are `guest` or start with `guest_` are never saved.
- Each account's password is saved under its own per-account pref and refilled when that account is picked from the history (unless `dontsavepasswords` is set).

**The first Login frame** (type 5) carries the version token, then the account as a length-prefixed string, then the password the same way, then the PC-id list; a language packet follows. **The nickname is not in the Login frame.** It goes out afterwards as own player prop 0 in a player-props packet, which matches the `Real404` lab row above. The account-before-password order and the frame contents agree with `login_layout` in the 4.04–4.20 profile; the event that sends the nickname after login was not pinned down.

**`-guestaccount` and `setDefaultGuestAccount`.** The launcher passes the switch value to the engine at startup (empty without the switch). It only prefills: when no account is saved, account and password both become that name. It never skips the dialog, and because the dialog blanks any `guest`/`guest_*` name on wake, such a value is not actually shown. What does skip the dialog is `-connect` or a `graal://` URL, and only when Member is checked and a saved password exists.

**5.00r7 for contrast.** There is no built-in start dialog. The client logs in first with no user input: account = the `-guestaccount` value if given, else `guest`, with a built-in password the client decodes at run time (not decoded here); or, when a browser-plugin cookie is set, account `cookie` with the cookie as password. The Login server's script then asks for the real account, using the new getters (nickname, account history, `getLoginAccountName()`). Login details are held scrambled in memory rather than in plain globals, and `cookie` joins the never-saved names. The Login frame has the same shape as 4.20r8, and the nickname is still separate.

So the first Login frame on 4.20r8 carries whatever the player typed (or picked from history) as the account, never the nickname; on 5.00r7 it carries the guest (or cookie) identity, and the real account arrives only after the Login script runs.

## Login event order for login-weapon authors (G325, 2026-11-25)

Static read of the 4.20r8 engine, the 5.12 engine memory image and the 6.03r7 third-party unpack; nothing run. **[bin]**

**`PLO_SIGNATURE` (25) gates nothing.** In all three builds it stores the signature, calls the launcher's login hook and fires `onServerLogin`. The stored value is used only to label and check cached web levels; a level that arrives before 25 is still accepted. The other state the login handlers touch is a progress counter that handlers only raise; no handler tests it to drop or delay a packet. Packets are queued by the network thread in arrival order, independent of 25.

**The one real drop is ghost mode.** While `PLO_GHOSTMODE` (170) is on, weapon adds (33) and the weapon-script packets 193, 132 and 196 are discarded, not queued.

**`PLO_SERVERLISTCONNECTED` (190)** reads no body. It calls the launcher hook (5.12 and 6.03r7 also hide the "connecting to the login server" box) and fires `onServerListerConnect` once, to the scripts that exist at that moment. Nothing queues or replays it, so **a weapon that must react to `onServerListerConnect` has to be loaded before 190 arrives.** `onServerLogin` from 25 behaves the same way.

**When a weapon's script first runs** (medium confidence):

- 4.20r8: 33 creates the weapon at once; a weapon carrying a script gets `onPlayerEnters` while 33 is still being handled. `onCreated` is posted to the weapon's own event list on a path not tied to a specific packet here. 4.20r8 never handles 140 or 197: its weapon scripts come inside 33 or from its local script cache (193, answered by a `PLI_UPDATESCRIPT` (158) request).
- 5.12 and 6.03r7 load the compiled script from 140 (and 197). 6.03r7 no longer handles 193.

**Ordering rule for a Login server that should work on all three:**

| Step | Send | Status |
|---|---|---|
| 1 | 25 | convention; the client does not require it first |
| 2 | ghost mode (170) off while weapons are sent | required |
| 3 | each weapon complete: 33 with its script (33/193 for 4.20r8; 140/197 for 5.12 and 6.03r7) | required before step 4 for any weapon that uses `onServerListerConnect` |
| 4 | 190 | after the weapons, so the event reaches them |
| 5 | the level | before or after 190 |

The GServer-v2 login path sends 190 before the weapon list (its source comment says so). On these clients, login weapons sent that way would not see `onServerListerConnect`. **[src][inf]** That server-side point is from the read of the fork's login path, not a lab run.

## v6 login-screen weapons on a 4.20r8 Login session (G324, 2026-11-25)

Static read of the 4.20r8 engine, with the 6.03r7 third-party unpack for its function list; nothing run. **[bin]** unless marked.

**Verdict: the weapons stay hidden because their script never arrives, not because the script bails out on an empty account name.**

1. **Sent the 6.x way** (33, then the compiled script in 140 or 197). 33 creates the weapon object with no script. 4.20r8 has no case for 140 or 197; it drops them with no log and no state change, and the stream stays aligned. The weapon list ends up holding script-less `-LoginScreen` and `-Serverlist` weapons: no `onCreated`, no GUI. With the Login-mode draw mask (no players, no HUD) the player sees an empty Login screen.
2. **Forcing a compiled script in another way.** 4.20r8 has no script compiler. Compiled scripts enter only through its local script cache (193, checked by CRC); on a match the script installs and `onCreated` runs at once. How 4.20r8 receives a fresh compiled script after its `PLI_UPDATESCRIPT` (158) request was not found. The compiled-script container is the same in 4.x and 6.x, but 4.20r8 has no handler for newer opcodes, among them the one-step computed member store (54) and string-join `+` (121), plus other 5.x/6.x-only ones. It skips them silently, leaving wrong values for the instructions that follow, so a 6.x-compiled script that joins strings would misbehave quietly.
3. **If the script did load.** Missing on 4.20r8, from a comparison of the 6.03r7 built-in function table: `getLoginAccountName`, `GuiAccountPasswordCtrl` (both as in G323), the newer list-selection functions (`selectedrow`, `setselectedrows` and the like), text-selection functions, the JSON functions, `clearcontrols`, the TCP object and about 120 more. Present: `requesttext`/`sendtext` with `lister`, the `onReceiveText` event, `serverwarp`, `setaccountname`, `openurl`, and the main GUI controls (window, scroll, text list, multi-line text, button, text edit). A missing function logs `Function X not found`, returns 0, and the script carries on; too few parameters is also non-fatal. The `adventure_*` functions work only for weapons from a server whose name starts with `login`; elsewhere they fail with `Unauthorized call of adventure_…`.

If such a script were force-loaded, `getLoginAccountName()` would return 0, which compares equal to an empty name, so a typical v6 screen would take its no-account branch, have no password box and show half-working lists: a partly broken screen that logs errors, not a clean hide. **[inf]**

Still open: how 4.20r8 receives a fresh compiled script after 158, what the `#c#` weapon property does, and what `new` does with an unknown control class.

## Server / script checklist

| Audience | Rule from settled rows |
|---|---|
| Lab Login for 4.x | Accept a typed / saved account on first connect; do not require a guest→reconnect dance. |
| Lab Login for 5.24+ / 6.03 | Expect `guest` first; use a clientside setter weapon (or equivalent) before world warp if flags must save. |
| Login-weapon authors | Treat 4.x and 5.x/6.x as different account machines until the open rows above are closed. |

## Open

- Stock 4.20r8 UI session (checkboxes above).
- Fold confirmed rows into `login-session-known.md` and the 4.20r8 profile once closed.
