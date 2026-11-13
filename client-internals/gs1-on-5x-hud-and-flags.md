# GS1 scripts on 5.x clients: the HUD "x" and 99/99, and flag and built-in probes

Date: 2026-11-13. Lab: the real Windows 4.20r8, 5.12 and 5.24r4 clients against a loopback lab
server, walking a GS2-era world twice: once with level scripts compiled by gs2-parser, once by
an alternative compiler (Seihai) that keeps GS1 meaning, and swapping the compiled bytecode on
the way **[lab][shot]**. Packet counts were read at the lab server's log **[run]**. The engine
bisection is tracked in squirelworks/seihai-core #32 **[doc]**. No addresses; no world script text.

## The HUD difference on 5.x

With the GS1-keeping compiler, both 5.x clients show **a small red "x" to the right of the
HP/AP bar**, and the arrow and bomb counters read **99/99** instead of 40/40. It showed at 5 of 8
stops on 5.12 and 2 of 3 on 5.24r4, and never with gs2-parser. 4.20r8 does not show it
**[lab][shot]**. Script errors were 0 with both compilers, and packet counts showed no compiler
effect **[run]**.

Bisected on 5.24r4's start level, two level NPC scripts each produce one symptom. Both are GS1
scripts in a GS2 world **[lab]**:

| Symptom | Script construct | gs2-parser output | GS1-keeping output |
| --- | --- | --- | --- |
| 99/99 arrows and bombs | a GS1 event-flag guard, `if (<event>) { player.<prop> = <const>; … }` | the event name compiled as an ordinary variable, never true, so the block never runs | the event handler, which fires on entry and sets the ammunition |
| red "x" | a bare GS1 command with no parentheses inside the `created` guard | a lone push of a variable (a no-op) | a real zero-argument call; the command turns on the level's no-player-killing mode, and the red crossed icon is its indicator |

So the 5.x engine draws a no-PK indicator next to the HP/AP bar when a level script enables
that mode, and the GS1 reading is the one a player of the era would have seen if the server ran
these scripts as GS1 **[lab][inf]**. See [../npc-library/gs2-strict-probes-2026-11-13.md](../npc-library/gs2-strict-probes-2026-11-13.md)
for how the two compilers treat GS1 constructs.

## Flags and built-ins on 5.12 and 5.24r4

Two authored probe weapons, run on the real 5.24r4 and 5.12 **[lab]**:

| Probe | Result | Tag |
| --- | --- | --- |
| flag delivery | the server sends the account's flags unprefixed (`PLO_FLAGSET`) before any NPC bytecode | [cap] |
| reading a flag | `player.<flag>` and the bare flag name both read it, for a boolean flag and for `name=value` | [lab] |
| `player.flags` | does not list them | [lab] |
| `set("x")` | "Function set not found" on 5.x; nothing is sent to the server | [lab] |
| `player.hearts` | 2.5 | [lab] |
| `player.fullhearts` | 3 | [lab] |
| `player.weapons.size()` | 2 | [lab] |
| bare `selectedweapon` | 1 | [lab] |
| `player.weaponscount`, `player.selectedweapon`, bare `weaponscount`, bare `playerhp` | empty | [lab] |
| `player.selectedweapon = 0` | nothing visible | [lab] |

Both compilers behaved the same on both probes.

## 5.12 draws a black level: a stale file-name cache

A 5.12 install whose 2D view stayed black (only the HUD text drew) had a stale
`FILENAMECACHE.txt` in its folder: 128 entries, mostly GUI files, without
`levels/tiles/pics1.png` or the sprite images. With `cachefilenames=true`, 5.12 trusts that
list instead of scanning its folder, so it could not see its own tileset and sprites; it asked
the server for `pics1.png`, `door.png`, `head0.png` and similar, got no reply, and drew nothing
image-based. Deleting the file fixes it: the client rebuilds the list at launch (1,943 entries)
and levels draw, with `cachefilenames` left on **[lab][shot]**. Ruled out: the login mode, a
missing tileset, Direct3D 7 texturing, `lowresourcesmode` and bitmap fonts.

5.12 also crashed at start-up when the guest clock was far past its build date; with the clock
set near its link date (October 2007) it ran for the full 120 s in 7 of 7 launches **[lab]**.

## Not known

- The command's name is not recorded in the lab summary, and the indicator was not checked on
  builds other than 5.12 and 5.24r4.
- Why 4.20r8 shows neither symptom with the same scripts.
- The 5.12 world walk with real level screenshots, now that the black view is solved.
