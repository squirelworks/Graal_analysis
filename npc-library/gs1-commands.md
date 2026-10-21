# GS1 command catalog (cleaned)

Date: 2026-10-14

Derived from the public command tables, the Reborn scripting guide, the 3,187 scraped scripts, and observed offline behavior. No decompile material.

> For what each command actually does in client 2.05, see [gs1-command-reference-205.md](gs1-command-reference-205.md). It corrects the pattern letters below (`R` is a number, `D` is up 0, left 1, down 2, right 3) and notes that `warp` / `jump` are not GS1 commands.

## Control flow

- `if` / `else` — conditional. The nearby form is used for range checks against the player or other objects.
- `jump` — unconditional transfer to a label.
- `function` — named block. Early clients treat this as a no-op or simple call; later clients expand it.

The offline interpreter already executes arithmetic, comparison, and jumps. The missing piece is the command call itself.

## Commands observed in the scraped set

| Command | Typical effect | Notes |
|---------|----------------|-------|
| `hide` | Make the NPC invisible | Extremely common in `playertouchsme` |
| `show` | Make the NPC visible | Paired with hide |
| `setlevel` | Change the current level | Used by level-warp scripts |
| `warp` | Move the player to a new x,y | Local and cross-level |
| `hurt` | Apply damage to the player | Combat and hazard scripts |
| `say` | Display a text box | Dialogue scripts |
| `set` / `unset` | Set or clear a flag | Triggers, doors, state |
| `setfocus` | Direct camera or attention | Rare in the scraped set |
| `resetfocus` | Clear focus | Rare |
| `spyfire` | Observation or debug hook | Present in public tables, rare in scripts |
| `loadmap` | Load a map overlay | Present in public tables |
| `canwarp` / `canwarp2` | Query whether a warp is allowed | Used before warp |
| `join` | Attach to another object | Rare |
| `freezeplayer` / `unfreezeplayer` | Lock or unlock player input | Used in cutscenes |

The public command table also lists draw-layer commands (`setbacktile`, `drawovertrees`, `setz`, `updateterrain`) and a few others that do not appear in the 3,187 scraped scripts.

## Pattern letters

When a command expands a template string, the letters are replaced as follows:

- B — baddy name
- C — color name
- D — direction (0 up, 1 left, 2 down, 3 right; corrected 2026-10-21)
- F / Q — filename
- I — item name
- L — carried object name
- M / S — arbitrary string
- O — object name
- R — numeric expression (corrected 2026-10-21; earlier read as the literal “real”)

These letters appear in both the public tables and in a small number of the scraped scripts.

## Offline wiring priority

CmdCall is currently a no-op. The highest-value first wires, based on frequency in the scraped set, are:

1. `hide` / `show` — appears in the majority of `playertouchsme` scripts.
2. `warp` / `setlevel` — appears in transport and level-change scripts.
3. `hurt` — appears in combat and hazard scripts.
4. `say` — appears in dialogue scripts.
5. `set` / `unset` — appears in trigger and door scripts.

Wiring the first two is enough for an offline session to respond to player touch by hiding an NPC or warping the player. That is the smallest change that makes a level feel interactive instead of static.

## Event frequency (reminder)

From the 3,187 scripts:

- `playerenters` — 2,268
- `playertouchsme` — 1,986
- `timeout` — 1,456
- `playerendsreading` — 1,123
- `compusdied` — 1,122
- `playertouchsother` — 1,074
- `wasshot` — 728

Most of these events call one of the commands listed above.

## Update 2026-10-21

- The full 2.05 command table (159 entries, op = 600 + index) and the function/variable table (ids 100–825) are in `gs1-reference-205.md`, together with built-in event flags, constants, and differences from 2.22.
- 2.05 interprets a parse tree built from script **text**. It does not run OpenGS1-style bytecode. The `Call`/`CmdCall` gap in Seihai is therefore a command-dispatch problem: map each command name to a host function, using the table's argument signatures.
- `hide` and `show` are not entries in the 2.05 table even though most scraped scripts use them. Treat them as aliases of `hidelocal`/`showlocal` offline until the 2.05 parser is traced. **[inf]**
- `setfocus`/`resetfocus`, `spyfire`, `loadmap`, `canwarp`/`canwarp2`, `join`, `freezeplayer`, and `unfreezeplayer` are all present in 2.05. `freezeplayer` takes a time argument.
