# `#n` in `setcharprop` (server brief A3.6)

Date: 2026-10-31

Question: when an original server runs `setcharprop` and the **value** contains
`#n`, does that expand to the **NPC's** nickname or the **player's**?

## Answer

On servers that run GS1 themselves, `#n` inside a `setcharprop` **value** expands
to the **action player's** nickname (the player who triggered the script), not
the NPC's. Optional `#n(id)` picks another player by server id. Tag: **[srv]**

The property **code** `#n` (first argument) is separate: it writes the expanded
value into the NPC's own nickname field. Tag: **[srv]**

## Evidence

### 1. GServer13 (1999) cannot settle the value question by lab

The Linux `gserver13` binary from the GServer 1.31 source tree (dated 1999-12-22)
and its matching C++ sources have player and NPC **props** (including an NPC
`nickname` field) but **no** GS1 command table and **no** `setcharprop` /
`showcharacter` strings. NPC scripts in that era were carried to clients and run
there; the 1999 server did not interpret `setcharprop`. Tag: **[bin]** (binary
and source inventory under Drive `GServer 1.31`; not committed).

So a Wine loopback of GServer13 + a 2.05 client does not exercise server-side
`#n` expansion. That path only appears once the server takes over NPC scripting.

### 2. Server-side GS1 (GServersource archive)

The later server NPC engine (`npcs.cpp` in the Drive `GServersource` tree) does
the following. Tag: **[srv]** (plain behaviour from that source; no code quoted).

1. Message-code expansion (`GetRealMessage`) treats `#n` as the nickname of
   `actionplayer` (default), or of `GetPlayer(id)` when written `#n(id)`.
2. `setcharprop` always runs the **second** argument through that expander before
   applying it.
3. When the **first** argument is `#n`, the expanded text is stored as both the
   NPC object's nickname and the `showcharacter` avatar's nickname, and marks the
   NPC nickname prop dirty for send.

So `setcharprop #c,Hi #n` becomes chat text containing the **player's** nick,
and `setcharprop #n,Guard` sets the **NPC's** nick to `Guard` (after expanding
any codes inside `Guard`).

GServer 1.34's Windows binary lists `showcharacter` but not `setcharprop`, so it
is not a useful lab host for this command either. Tag: **[bin]**

### 3. Client 2.05 (for the online client-run path)

`npc-library/gs1-command-reference-205.md`: string arguments are trimmed and
message codes are expanded before use; `setcharprop`'s first argument names the
property (`#n` = nickname on the character NPC). Tag: **[2.05]**

`setplayerprop` on 2.05 does **not** handle property code `#n` (only `#1 #2 #3
#5 #8 #C0..#C5 #P1..#P5 #c`). Nickname changes for a character figure go through
`setcharprop`. Tag: **[2.05]**

A loopback capture that proves the server-side expansion on a live script-running
server (GServer-v2 lab or similar) with 2.05 rev 2 is still open. Tag: **[lab]**
needed.

## What Seihai / forks should keep

- Expand `#n` in `setcharprop` **values** as the triggering player's nickname
  (same as other message text).
- Do not substitute the NPC's current nickname for bare `#n` in that value.
- Keep property code `#n` as "set this NPC's nickname".

## Still open

- **[lab]** Run a level NPC under a script-running lab server with
  `setcharprop #c,seen:#n;` (and a distinct NPC nick via `setcharprop #n,Npc`)
  and confirm the chat/NPC props on the wire match the player nick. Preferred
  host: lab GServer-v2 on loopback; client 2.05 rev 2 under Wine. GServer13 is
  the wrong host for this command.
- Whether any pre-GServersource Windows server already ran `setcharprop` (none
  found in the downloadable GServer 1.19 / 1.31 / 1.34 packages).
