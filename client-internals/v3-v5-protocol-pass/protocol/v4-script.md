# v4 — script (GS1)

Date: 2026-11-08 · Tags: **[bin]**

## Kind · **high**

**GS1**-style NPC/level scripting (event names + verb builtins), **not** the later `GRESCR01` / `.code` GS2 container (those magics are **absent** here).

### Level / NPC script container · **high**

Level file section tags in Engine include:

`BOARD`, `LINK`, `CHEST`, `SIGN`/`SIGNEND`, `NPC`/`NPCEND`, `BADDY`/`BADDYEND`, `SCRIPT`/`SCRIPTEND`, `DESCRIPTION`/`DESCRIPTIONEND`, plus map headers `GSERVL01`, `GRMAP001`, `GWEBL001`, height/level-name blocks (`LEVELNAMES`/`LEVELNAMESEND`, `HEIGHTMAP`/`…`, `RANDOMSEEDS`/`…`).

Gani encryption helpers: `loadScriptEncrypted` / `saveScriptEncrypted` on `TGraalAni`.

### Events (sample) · **high**

`playerenters`, `playerchats`, `playerhurt`, `playerdies`, `playertouchsme`, `playertouchsother`, `playerlaysitem`, `playerendsreading`, `created`, `timeout`, `exploded`, `keypressed`, mouse events, `compusdied`, etc.

### Builtins (sample) · **high** (names) · **medium** (format letters)

Adjacent format hints (`isdd`, `iddis`, `idddsss`, …) sit next to verbs such as:

| Group | Names |
|---|---|
| Show | `showimg`/`showimg2`, `showani`/`showani2`, `showtext`/`showtext2`, `showpoly`, `showcharacter`, `showlocal` |
| Hide / img | `hideimg`, `hideimgs`, `setimg`, `setimgpart`, `changeimg*` |
| Combat | `shootarrow`, `shootfireball`, `shootnuke`, … |
| Carry / block | `canbecarried`, `dontblock`, `throwcarry`, `takehorse`, … |
| World put | `putbomb`, `puthorse`, `putexplosion`, `putcomp`, … |

Opcode/bytecode VM map: **not applicable** in the GS2 sense — this is text/verb GS1. Full builtin table and what a modern compiler omits: open (see gaps).

### StartScript UI · **high**

`StartScript_Profiles`, `MainMenu`, `GraalGui`/`GraalGui3D`, `OptionsWindow`, `PlayerProfile`, `LoadLevelGui`, `MoveMap2D`/`3D`, `QuitDialog`, `MessageBoxDialog`, `SetupDialog`, `SelectFileDialog` — **no** `StartScript_Connector`.
