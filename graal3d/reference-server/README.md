# Graal3D reference server

`g3dserver.py` is a small server for the February 2000 Graal3D client, written from [../protocol.md](../protocol.md). It is plain Python 3 with no dependencies. It exists to show that the notes are enough to host the real client; it is not a copy of `GServer.exe`.

```
python3 g3dserver.py --port 14901 --levels levels --accounts accounts.json
```

- `levels/` holds the `.x` level files. `startlevel.x` is where players start; copy it from the Graal3D archive.
- `accounts.json` maps names to `{"password", "level" (0–3), "loadonly", "disabled"}`. The server saves each bound account's props there when the player leaves. Without `--accounts`, any name and password log in as a load-only account.
- Clients need the level's textures (`grass.bmp` and so on) in their own folder; the protocol never sends them.

## What it does

- Accept and login, including the `GR3DV001` and account error texts.
- Player ids 1–200, saved props, the login order the original uses.
- Level text in packet 0 (empty if already sent to that player), the leader packet, prop 50.
- Props relay with the UDP rule (props 1–5 and 13 skipped when both ends have UDP), nickname guild tags (`guilds/guild<name>.txt` next to the levels folder), prop 15 broadcast.
- Disconnect (prop 51, admin 56).
- Admin login with the account list and player list, message to all (63), message to one (64), kick (61).

Not done: admin account editing (51–54, 59, 60), level reload (62), the file request (2), the 4096-byte send batching. Changing a player's level is only possible from code (`enter_level`), as in the original, where only an admin edit moves a player.

## How it was checked (2026-10-30)

- A scripted two-player session (login, moves with and without UDP, UDP hand-over, chat, prop 14, leave, then a second login with saved props) produced the same messages from this server as from the original `GServer.exe` under Wine, apart from the random UDP ports.
- The real `Graal3D.exe` logged in, received its props and the level, and saved a byte-identical `startlevel.x`. See [../lab-2026-10-30.md](../lab-2026-10-30.md) for why the real client could not be taken further under Wine.
