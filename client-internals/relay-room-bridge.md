# Java Graal meets the Delphi betas: a relay room bridge (2026-10-31)

Question: can Java Graal (July 2000) and 5th Graal (October 1998) play in one
room? Both talk to Stefan Knorr's GServ relay lobby (`protocol/relay-1998.md`),
but they join different rooms. This note runs them, and 4th Graal alpha, live
against Knorr's own GServ, and tries a proxy that renames rooms.

Tags: **[live]** seen in running clients or on the wire, **[bin]** read from the
binaries' strings. No decompiler output is reproduced.

## Result

| Pair | Relay | Meet? | What went across |
|---|---|---|---|
| Java Graal + 4th Graal alpha | stock GServ | **yes** [live] | both drawn, nicknames, chat both ways |
| Java Graal + 5th Graal | stock GServ | no [bin, live rooms] | different rooms (`G2<level>` vs `G3<level>`) |
| Java Graal + 5th Graal | GServ behind the bridge, `G2` → `G3` | **yes** [live] | both drawn, nicknames, walking both ways (5th Graal's from run 4), chat both ways, a level change and back |

So the "Java Graal speaks 4th alpha's dialect" reading in
`precursors-and-fan-builds.md` holds on the wire, and its last open point is
closed: 4th alpha joins `G2` + the bare level file name (`G2level13.graal`), the
same string the applet builds. For every later beta a one-line rename in the
join is enough to put them together; the `D` payloads already line up.

## Rooms each build joins

Every Delphi beta opens **two** connections to the relay: one to a room per
level, one to a fixed game-wide room. The Java builds open one.

| Build | Level room | Game-wide room | Basis |
|---|---|---|---|
| 1st Graal | `Zhouse12` (`Z` + level, no extension) | `Zelda2` | [live] |
| 2nd Graal | as 1st | `Zelda2` | [bin] |
| 3rd Graal | `Ghouse1.graal` (`G` + level file) | `Graal` | [live] |
| 4th Graal | `G<level>` | `Graal` | [bin] |
| 4th Graal alpha | `G2level13.graal` | `Graal2` | [live] |
| 5th Graal | `G3level13.graal` | `Graal3` | [live] |
| 5th alpha, 6th to 1.1.9 | `G3` … `G8` + level | `Graal3` … `Graal8` | [bin] (1.1.9 also in `live-trace-early.md`) |
| Java Graal | `G2level13.graal` | none (a `Graal2` mode exists but is never selected) | [live] |
| Zelda Online 2 | `Zlevel11.6` (`Z` + base + `1.6`) | none | [live], 2026-10-30 |

1st Graal's `Zhouse12` is either `Z` + `house12` or `Z` + `house1` + `2` (the
`Z` + base + `2` branch in `early-clients.md`); one run does not tell them
apart. Either way it never equals Zelda Online 2's `Z<base>1.6`.

## How it was run

- **Server:** Zelda Online 2's `server/GServer.java` (Knorr's GServ
  Standalone), compiled with a current JDK and run unchanged on 14801.
- **Bridge:** `tools/relay-bridge/room_bridge.py` on 14802, in front of GServ.
  It passes every line unchanged except `N<room>#<name>` / `O<room>#<name>`,
  where a rule `OLD=NEW` swaps the room prefix (`G2=G3` turns
  `G2level13.graal` into `G3level13.graal`). It logs every line both ways.
  With no rule it is a plain logging proxy.
- **Java Graal:** the 2002 rip's `Graal.jar` (the loose class files in the rip
  are truncated), served over HTTP as the applet's codebase and started with
  `tools/relay-bridge/AppletRun.java`, a small `AppletStub` frame. The applet
  dials its codebase host on 14802, so it always goes through the bridge.
- **Delphi betas:** the shipped `Graal.exe` under Wine 9 (Xvfb, openbox, the
  Wine virtual desktop), started with `WINEDLLOVERRIDES="dinput=d"` so the
  arrow keys work (see run 4). `tools/relay-bridge/run_delphi_beta.sh` sets
  this up.
  From 3rd Graal on the server box is greyed out at Cyberjoueur's
  `204.85.8.128:14802`; that address was put on the loopback interface so the
  beta reached the bridge. 4th alpha and 1st Graal keep an editable
  `127.0.0.1:14801` and went straight to GServ (captured with tcpdump,
  decoded with `tools/relay-bridge/pcap_lines.py`).

Captures and screenshots: `live-runs/relay-bridge-2026-10-31/`.

## Run 1: Java Graal and 5th Graal through the bridge

```
room_bridge.py --listen 14802 --server 127.0.0.1:14801 --map G2=G3
```

- Java Graal joined `G2level13.graal`; the bridge sent `NG3level13.graal#def`.
  5th Graal joined `G3level13.graal` and `Graal3`. GServ announced each to the
  other (`+`), both sent `P`, and the state burst followed.
- 5th Graal drew the Java player, its walking (a run of `P` lines) and its
  chat (`hi from java`). Java Graal drew the 5th Graal player with its
  nickname (`Fifth`) and chat (`hello from 5th`).
  (`run1-java-to-5th.png`, `run1-5th-to-java.png`.)
- Java Graal walked into `house10.graal` and back: it sent `C` and `-`, then
  joined `G2house10.graal` (bridged to `G3house10.graal`), and on return
  `G3level13.graal` again, and the 5th Graal player was there again.
- `D` types sent in the run: Java Graal `T P C N D`; 5th Graal
  `T P Y C N S`. Java Graal ignores `Y` and `S` (colours), so the 5th Graal
  player shows in default colours there. Nothing broke on either side.
- 5th Graal's own walking was not seen in this run: its arrow keys did not
  reach the game under Wine, so its player stood still. Run 4 fixes that and
  shows the walking.

## Run 4: 5th Graal walks in the shared room

Same setup as run 1 (`--map G2=G3`), with 5th Graal started under
`WINEDLLOVERRIDES="dinput=d"`.

- **Why the keys were lost.** 5th Graal reads the keyboard through DelphiX
  `TDXInput`, which loads DirectInput. Wine's `+dinput` trace shows the
  keyboard data format it sets: `dwDataSize 256, dwNumObjs 1`, one object at
  offset 1 (`run4-dinput-format.txt`). Windows fills the whole 256-byte key
  buffer anyway. Wine fills only the objects listed, so the arrow-key bytes
  stay zero. Chat typing and mouse clicks arrive as window messages, which is
  why they worked. This is the same fault as in the 1.x clients
  (`live-trace-early.md`, `live-gserver13.md`).
- **The fix.** With `dinput=d` the DirectInput load fails, DelphiX falls back
  to `GetKeyboardState`, and `xdotool keydown` reaches the game. This is the
  setting the 2026-10-30 six-era runs used
  (`version-profiles/matrix/live-runs-2026-10-30.md`). No change to the exe
  and no memory patch is needed. The game window must have focus
  (`xdotool windowactivate`/`windowfocus`), which the openbox + virtual
  desktop setup allows.
- **Before:** without the override, holding Right for 1.5 s sent nothing.
  **After:** holding Right, Down and Left sent a stream of `D #P…` lines, one
  every 100 ms while a key was held, each relayed to Java Graal
  (`run4-5th-java-walk-bridge.log`). [live]
- Java Graal drew the `Fifth` player walking right across the level13 yard
  (`run4-5th-walks-java-view.png`, before and after). [live]
- 5th Graal's own screen often stops repainting the board under Wine (as
  noted for 2.05 in `board-respawn.md`), so judge its movement from the wire
  or from the other client, not from its own window.

## Run 2: Java Graal and 4th Graal alpha, no rename

Bridge with no rules (Java side), 4th alpha straight to GServ.

- 4th alpha joined `G2level13.graal` and `Graal2`; Java Graal joined
  `G2level13.graal`. Same room, so GServ paired them with no help.
- Chat went both ways (`java meets fourth`, `fourth says hi`), and each drew
  the other with its nickname (`run2-4thalpha-java-chat.png`).
- 4th alpha sent `T P Y C N S`, Java Graal `T P C N D`, as in run 1.

## Run 3: rooms of 3rd and 1st Graal

Only the joins were needed: 3rd Graal sent `NGhouse1.graal#def` and
`NGraal#def`; 1st Graal sent `NZhouse12#def` and `NZelda2#def`.

## What this means

- A relay that serves these builds together needs only the join rename. The
  `D` lines are already the same dialect from Zelda Online 2 through 1.1.9,
  and each side ignores the types it does not know.
- The rename must keep the level part: mapping a level room onto a game-wide
  room (for example `G2<level>` onto `Graal3`) would put players on different
  levels in one room.
- Bridging other pairs is the same rule with other prefixes (`G2=G5` for
  Java Graal with 7th to 9th Graal, and so on). Only 4th alpha and 5th Graal
  were run.
- Seihai lists all of these builds as offline-only (it has no relay client);
  its rows carry the rooms above (`documentation/offline-only-builds.md` in
  Seihai).
