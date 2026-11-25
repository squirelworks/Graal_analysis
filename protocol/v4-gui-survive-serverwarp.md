# v4 GUI windows after server-warp (178)

Date: 2026-11-16. Research-list rank **#56** (comparison C5; focus 4.208). Adjacent to the v4 Login account contract (research **#2** / C4). Status note — **no loopback UI session** this pass (Share / stock 4.20r8 UI not run here).

Tags: **[bin]** Login-mode / 178 handlers; **[live]** 4.04r2 lab; **[doc]** existing login-session notes; Others Work C5 = **lead only**.

## Settled context (ours)

| Fact | Evidence |
|---|---|
| 4.x has **no listserver**; it dials a game server named `Login` and treats **S→C 178** as move-to host:port | `v4x-clients.md`; `live-behaviour-404.md` **[bin][live]** |
| While the server name starts with `login`, the draw-layer mask is 0 (no players / HUD) | same **[bin][live]** |
| 4.20r8 treats **S→C 190** as Login accepting the session | `login-session-known.md` **[bin]** |
| Scripted server-list / account GUIs are the **5.x/6.x** Login pattern; 4.x uses launcher/engine login callbacks | `login-session-known.md`; `named-login-5x-6x.md` **[bin][lab]** |

None of those rows prove what happens to an **open Login GUI window** after 178 on stock 4.20r8.

## Lead (Others Work — not settled)

Comparison C5: a login-server GUI that is still open after **178** remains on the play server unless scripts **hide** it first. Implication for Login weapons / server scripts, not a new packet id.

Treat as **[ASSIGNED]** until a stock 4.20r8 loopback run shows: open GUI → 178 → play server, with and without an explicit hide.

## Static read: what 178 keeps (G318–G320, 2026-11-25)

Static read of the stock 4.20r8 engine, with 4.04r2 and 5.00r7 for contrast; nothing run. **[bin]** unless marked.

**Verdict for C5: on stock 4.20r8 and 4.04r2, an open Login GUI window stays on screen on the play server unless a script hides or deletes it.**

- **What 178 does.** The handler only stores the target. The main loop then runs the same connect routine the Login connect uses: it removes the built-in server-list GUI, runs a disconnect clean-up, deletes the old connection, reloads the in-game GUI script, makes the game GUI container the screen content, and connects.
- **What the clean-up keeps.** It deletes every weapon except those added while the server name started with `login`; those stay, and their scripts keep running on the play server. It deletes every object scripts created with `new`, except objects made by a script on a `login` server (each new object inherits that mark from the script that created it). It then re-runs the built-in profiles script. `client.*` / `clientr.*` variables were not traced (probably reset with the player). **[inf]** for the variables.
- **Who owns a window.** `new GuiWindowCtrl(…)` puts the control in the client's global object list, not inside the weapon. Tearing a script down only stops its event listening; it does not delete what it created. So a window made by a Login weapon is a global object carrying the `login` mark, and it survives the warp.
- **Built-in start screen.** `MainMenuGui2D` (G322) is not hidden by a server-name check. It disappears on any connect, Login included, because the game GUI replaces it, and nothing brings it back.
- **Login draw mask.** Only the world painter (level, players, HUD) and the world mouse handler test it; GUI drawing never reads it. It never hid GUI controls, and on the play server it is back to drawing everything.
- **Other builds.** 4.04r2 has the same keep-`login`-objects check. 5.00r7 keeps objects whose level is 2 or higher and drops the rest (5.12 assumed the same); the level a window made by a Login-server script gets was not traced, so survival on 5.x stays open. 6.03r7 was not traced.

**Practical rule.** A 4.x Login weapon must hide or delete its own windows. Its weapon is still alive on the play server, so it can do that there, for example when the server name no longer starts with `login`.

## Lab checklist (loopback)

- [x] ~~Stock 4.20r8 (not packet-logger engine): Login-mode GUI visible → inject / real 178 → confirm whether the window is still drawn on the world session.~~ [Static read 2026-11-25](#static-read-what-178-keeps-g318g320-2026-11-25): it stays. A loopback run remains optional confirmation. **[bin]**
- [x] ~~Repeat with an explicit hide/destroy before warp.~~ Statically, only a script hide/delete removes it; the Login weapon survives the warp and can do so on the play server. **[bin]**
- [x] ~~Note whether 4.04r2 matches 4.20r8 (optional).~~ Same keep-`login`-objects check. **[bin]**
- [x] ~~Fold the result next to C4 / `login-session-known.md` (and the v4 Login contract note once that PR lands).~~ Linked from the v4 Login contract note.

No public Login capture required (plan-hold stays on research **#2** public leg).

## Open

- ~~Confirm or refute C5 on stock 4.20r8.~~ Confirmed statically (above).
- ~~Whether any built-in 4.x dialog auto-closes on 178 without script help.~~ The start screen goes on any connect; script windows do not.
- Whether a Login-made window survives on 5.x (object level) and on 6.03r7.
