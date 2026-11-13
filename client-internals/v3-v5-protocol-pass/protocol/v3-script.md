# v3 — script

Date: 2026-11-08 · Tags: **[bin]**

## GS1 text · **high**

`graal/scriptfunctions.cpp` embeds a large verb and expression table: control (`if`/`else`/`endif`/`while`), `say`/`say2`, `move`, `setimg`/`showimg`/`showani`, `shootarrow`/`putbomb`/`putnpc`, `setplayerprop`/`setcharprop`, `sendpm`/`sendtorc`/`sendtonc`, and a long `player*` / `npc*` read set. Format-letter hints sit beside several builtins. This is text GS1, not a Quattro GS2 opcode map.

Events/strings nearby include `created`, `//#CLIENTSIDE`, `timeout`.

## `.code` container · **high**

Level/NPC compile path writes a `.code` blob, encodes lengths with GCHAR (`+ 0x20`), then runs it through **descipher** (8-byte pad, length prefix, LCG-keyed block mix, checksum). Load checks the checksum and fails closed. There is **no** `GRESCR01` magic.

Gani files stay textual (`SCRIPT` / `SCRIPTEND`, `ANIEND`, `PLAYSOUND`, `ATTACHSPRITE`) under `graal/ganis.cpp`.

## Diff vs v4

v4 keeps GS1 in `SCRIPT` sections and does not show this `.code`+descipher wrapper. Neither build is GS2 `GRESCR`.
