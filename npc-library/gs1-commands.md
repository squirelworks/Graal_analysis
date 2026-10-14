# GS1 command catalog (cleaned)

Date: 2026-10-14

Derived from the public command tables, the Reborn scripting guide, and observed script patterns. No decompile material.

## Control flow

- `if` / `else` — conditional. Nearby is a special form used for range checks.
- `jump` — unconditional transfer.
- `function` — named block (not fully expanded in early clients).

## Common commands observed in the 3,187 scripts

| Command | Effect | Frequency note |
|---------|--------|----------------|
| `hide` / `show` | Toggle NPC visibility | Very common on touch |
| `setlevel` | Change current level | Level warps |
| `warp` | Move player to x,y | Local and level warps |
| `hurt` | Apply damage | Combat scripts |
| `say` | Display text | Dialogue |
| `set` / `unset` | Flag operations | Triggers and state |
| `setfocus` / `resetfocus` | Camera or attention | Rare in scraped set |
| `spyfire` | Debug or observation | Present in tables, rare in scripts |
| `loadmap` | Load a map overlay | Present in tables |

## Pattern letters

When a command expands a template, the letters mean:

- B — baddy name
- C — color name
- D — direction
- F / Q — filename
- I — item name
- L — carried object name
- M / S — string
- O — object name
- R — the literal “real”

## Offline status

The offline interpreter already executes arithmetic, comparison, and jumps. CmdCall remains a no-op until the command set above is wired. The highest-value first wire is `hide` / `show` and `warp` / `setlevel`, because those appear in the majority of `playertouchsme` and `playerenters` scripts.
