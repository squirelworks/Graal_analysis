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

## Lab checklist (loopback)

- [ ] Stock 4.20r8 (not packet-logger engine): Login-mode GUI visible → inject / real 178 → confirm whether the window is still drawn on the world session.
- [ ] Repeat with an explicit hide/destroy before warp.
- [ ] Note whether 4.04r2 matches 4.20r8 (optional).
- [ ] Fold the result next to C4 / `login-session-known.md` (and the v4 Login contract note once that PR lands).

No public Login capture required (plan-hold stays on research **#2** public leg).

## Open

- Confirm or refute C5 on stock 4.20r8.
- Whether any built-in 4.x dialog auto-closes on 178 without script help.
