# RemoteControl builds 2000–2002

Date: 2026-10-21

Source: static read of seven Delphi RemoteControl executables (archive names `rc133`, `rc139rev2`, `rc1025`, `rc62101`, `rc8212001`, `rc201`, `rc141`). The forms were read from their DFM resources and the packet ids from the send call sites. Tags: **[bin]** · **[inf]**.

The archive names do not sort by date. "rc141" is the newest of the set, not "rc201".

## Builds

| Archive | Title string | Login token | Forms | Notes |
|---|---|---|---:|---|
| rc133 | "GServer2 Remote Control (C) Stefan Knorr" (no date) | `GSERV014` | 7 | oldest; accounts, players, send, update levels |
| rc139rev2 | 2000/8/19 | `GSERV019` | 15 | adds chat window, flag lists, toalls, SQL account list, options, warp |
| rc1025 | 2000/10/25 | `GSERV020` | 15 | same forms as 2000/8/19 |
| rc62101 | 2001/01/27 | `GSERV021` | 15 | same forms |
| rc8212001 | 2001/08/20 | `GSERV022` | 18 | adds rights, comments, local ban; server-option fields leave the start dialog |
| rc201 | 2002/01/04 | `GSERV022` | 18 | same forms, new main window layout |
| rc141 | 2002/05/02 | `GSERV023` | 26 | adds NPC Control, server list, file browser (see `npc-control.md`) |

The 2004 build in the Graal Reborn folder (`GSERV024`, type 6) is covered in `remotecontrol.md`.

## What stays the same **[bin]**

- Framing: `u16be length` + zlib body (zlib 1.1.2), messages `GCHAR id` + payload + `\n`. No cipher, no type byte, no key byte in any of these builds.
- Login: id **1**, then the token, `str account`, `str password`. The default account and password are `super` / `super`.
- Password storage: `controlconfig.txt` for options, `HKCU\Software\Graal\RemoteControl` for the account and the DES-obfuscated password (scheme in `npc-control.md`). The same key appears in every build.

## Start dialog and the old option packets **[bin]**

Up to 2001/01/27 the start dialog asks for server name (default: the loopback address), port (`14804`), account, password, and four server timers, each with a "don't change" box:

| Field | Default | Sent after login as | gs2lib name |
|---|---:|---:|---|
| Respawn time (bushes etc.) in sec | 10 | 55 | RC_RESPAWNSET |
| Horse lifetime in sec | 10 | 56 | RC_HORSELIFESET |
| Alignment increment time in sec | 1200 | 57 | RC_APINCREMENTSET |
| Baddies respawn time in sec | 60 | 58 | RC_BADDYRESPAWNSET |

Each value goes out as a GINT4 (four 7-bit groups, high first, each `+0x20`), only when its box is unticked. From 2001/08/20 the timers are gone from the dialog and 55–58 are no longer sent. In 2002/05/02 the address fields are gone too; the server comes from the listserver.

From 2000/8/19 the RC also sends a `PLI_PLAYERPROPS` (2) right after login with its nickname. Closing the player list with "Go in away mode" sends the nickname with ` - away` appended.

## Client → server ids per build **[bin]**

Constant ids at the RC socket's send call sites:

| Build | Ids |
|---|---|
| 1.33 | 1, 51–64 |
| 2000/8/19, 2000/10/25 | 1, 2, 6, 28, 55–58, 61–64, 67–79, 82 |
| 2001/01/27 | 1, 2, 6, 28, 55–58, 61–64, 68, 70–74, 76–79, 82 |
| 2001/08/20 | 1, 2, 6, 28, 61–64, 68, 70–79, 82–88 |
| 2002/01/04 | 1, 2, 6, 28, 61–64, 68–79, 82–88 |
| 2002/05/02 | 1, 2, 6, 28, 51–54, 61–64, 68–79, 82–92, 94, 96–98, plus the NC ids |

### Ids 51–54 changed meaning **[bin]**

In 1.33 the account dialog uses 51–54 and 59/60:

| Id | 1.33 use | Later gs2lib name |
|---:|---|---|
| 51 | account list: Edit (get account) | RC_SERVEROPTIONSGET |
| 52, 53 | edit account: Apply | RC_SERVEROPTIONSSET, RC_FOLDERCONFIGGET |
| 54 | account list: Delete | RC_FOLDERCONFIGSET |
| 59 | player list: Edit (get player props) | RC_PLAYERPROPSGET |
| 60 | edit player: Apply | RC_PLAYERPROPSSET |

From 2000/8/19 accounts move to 70–78 (`RC_ACCOUNT*`, `RC_PLAYERPROPS*2/3`), and 51–54 are unused until 2002/05/02 brings them back as server options and folder config. A server that has to talk to 1.33 cannot use the gs2lib names for 51–54. **[inf]**

## Feature timeline (from forms) **[bin]**

- 1.33: player list (nickname, account, level, head, id), disconnect, edit player, message, message to all, account list (add, delete, edit), update levels. The edit-account form already carries the full account: rights (Load only, Graalian Police, Trusted Admin, Administrator, No rights, Blocked), look, position, items, weapons, opened chests, NPC flags, MP, AP, spin attack.
- 2000/8/19: chat window (RTF), server flags, toalls, SQL account list with a filter dialog, message editor, options (ignore mass messages, no HTML in PMs, no images in PMs, away on close), warp player.
- 2001/08/20: edit rights, edit comments, local ban.
- 2002/05/02: NPC Control (NPC list, add NPC, local NPCs, classes, weapons, level list), listserver login and server list, file browser with drag and drop, short message popup.
