# New World mode in the 2.1x–2.3x clients (2026-11-27)

Checks a set of community claims about the "NW mode" left in the main-line 2.x client, against the
Windows clients 2.1.0.4 (Graal 2002 v22), 2.17.1, 2.22 and 2.31, with 2.05 rev 2 and the two NewWorld
betas as controls. It then describes a client patch that unlocks the dormant parts. Static reads are
**[bin]**; lab results are **[lab]**, in [Lab](#lab). Captures and client binaries stay with the owner.

## Verdict

| Claim (paraphrased) | Verdict |
| --- | --- |
| 1. The 2.x clients have a New World mode switch, and a server packet turns it on | **True.** Server packet 177 (`PLO_NEWWORLDMODE`, no payload) sets it, from 2.1.0.4 v22 to 2.31. Nothing clears it again. **[bin]** |
| 2. In NW mode the COLORS prop takes 8 colours instead of 5 | **True,** in both directions: the client reads 8 and sends 8. **[bin]** |
| 3. …only for players, not NPCs | **Half true.** Server to client, NPC COLORS (NPC prop 19) is read as 8 in NW mode too, so NPCs can have 8 colours. Client to server it is capped: the NPC props the client sends (`PLI_NPCPROPS`, 3) always carry 5. See [NPC props](#npc-props-the-5-colour-cap). **[bin]** |
| 4. The code that recolours the body is hard-wired to the 5 classic colours, and the NW palette layout is different | **True.** The recolour routine always writes exactly 5 palette entries (5, 6, 4, 3, 1) and never looks at the mode. NW bodies use 8 slots with 3 shades each at different palette entries. The other 3 colours are stored and even copied to the draw buffer, but never applied. **[bin]** |
| 5. "Probably an ifdef rather than a check on the flag" | **Consistent.** The NW recolour code (shade tables, `bodycolors.txt` loader) is simply absent from the main line, while the 8/5 width checks test the flag at run time. **[bin][inf]** |
| 6. NW shields don't work because the client ignores the GANI for SHIELD sprites and uses its own configuration | **Partly true.** The GANI's SHIELD rect is used, but it is rescaled by (shield image width / 38, height / 20), a built-in classic 38×20 sheet size. NW shield sheets are 96×20 with frames past x = 38, so every rect lands in the wrong place. No NW-mode exception. **[bin]** |
| 7. 8-colour bodies were in the betas | **True.** Both NewWorld betas (Aug and Oct 2001) recolour 8 slots × 3 shades from `bodycolors.txt` and ship `bodynw.png`. **[bin]** |

Feasibility: unlocking both is a small, self-contained client patch, and the server only needs to send 177
and 8-byte COLORS. A patch tool is in [`tools/nw-unlock/`](../tools/nw-unlock/README.md).

## The mode flag and packet 177

| Build | 177 handled | Flag storage | Read through |
| --- | --- | --- | --- |
| 2.05 rev 2, 2.1 test 2/3, NewWorld betas, Graal 2002 ver13 | no (dispatcher bound below 177) | — | — |
| 2.1.0.4 (Graal 2002 v22) | yes | one plain byte | a pointer to that byte |
| 2.17.1, 2.22, 2.31 | yes | two obfuscated copies in the main form: each stores `~(random(4) + 4·on)` | a getter that decodes both copies (`(~b) >> 2`), returns copy 1 == 1, and on a mismatch raises the client's tamper flag |

Packet 176 (Kingdoms mode) sits next to it with the same shape. Both handlers set the flag to on; no packet turns
it off. In 2.17.1, 2.22 and 2.31 the NW getter has 141, 141 and 123 call sites. Besides the colour widths below,
NW mode (like Kingdoms mode) switches off client sword judging, several baddy/chest/horse prop paths and other
classic gameplay (see [combat-baddy-tile-by-version.md](combat-baddy-tile-by-version.md#sword-judge-gates)). **[bin]**

Because of the double storage, a memory patch that flips only one copy trips the tamper flag. Set the mode
through packet 177, or patch both copies.

## COLORS widths

In 2.1.0.4, 2.17.1, 2.22 and 2.31 the same "8 if NW mode, else 5" test appears at four places, and nowhere else:

| Where | Prop | Width in NW mode |
| --- | --- | --- |
| own player props, client to server (writer) | 13 | 8 |
| own player props, server to client | 13 | 8 |
| other player props, server to client | 13 | 8 |
| NPC props, server to client | 19 | 8 |
| NPC props, client to server (writer) | 19 | **5** (no test) |

A character keeps 8 colour slots in all these builds. The GANI drawer copies all 8 into the body-draw buffer
before every body sprite. **[bin]**

### NPC props: the 5-colour cap

The NPC side is asymmetric. **[bin]**

- **Server to client:** in NW mode, NPC prop 19 is read as 8 values (2.1.0.4, 2.17.1, 2.22, 2.31). The NPC keeps them in
  the same 8 slots a player uses, and the GANI drawer copies all 8 for NPC bodies as well, so a server-driven NPC can
  carry 8 colours.
- **Client to server:** the client builds a snapshot of an NPC's props with a writer that has no NW test and always
  writes NPC prop 19 as exactly 5 values (a 6-byte record with its id). It compares the snapshot with the previous one
  and sends the changed props to the server as `PLI_NPCPROPS` (3), prefixed with the NPC id. So colours 6–8 can never
  leave the client, and a change confined to them is not even detected. Read in 2.17.1 and 2.22; the 2.31 writer was
  not located.
- That snapshot is the client-to-server sync of NPCs a client changes itself (client-side scripts on level NPCs). NPCs
  whose looks come from the server are not affected.

A server in NW mode therefore has to send 8 COLORS values for NPCs but still parse 5 in a client's `PLI_NPCPROPS`.

The patch does **not** need to touch this path for display: server-sent NPC colours already arrive as 8 and the patched
recolour applies them, like a player's. Only client-side NPC changes would lose slots 6–8. Extending the writer to
send 8 in NW mode is possible, but it would also require servers to parse 8 there, so it is left out.

A server that switches a client into NW mode must therefore send 8 COLORS bytes for players (prop 13) and NPCs
(prop 19) from then on. A 5-byte value desynchronises the rest of that prop stream. It must also read 8 in the
player props the client sends, but 5 in its NPC props (below).

## Body recolour

| Build | Slots applied | Palette entries written |
| --- | --- | --- |
| 2.05 rev 2, 2.1.0.4, 2.17.1, 2.22, 2.31 | 5, fixed count | slot *k* → entry 5, 6, 4, 3, 1 (skin, coat, sleeves, shoes, belt), one shade from the 20-colour table ([body-colours-and-attributes.md](body-colours-and-attributes.md)) |
| NewWorld beta 1 and 2 | 8 | slot *k* → entries *k*, *k* + 9, *k* + 18, from three 20-colour shade tables |

- The main-line routine has no flag test. The count, the slot-to-entry table and the single colour table are all
  constants. **[bin]**
- In the betas the three shade tables start as copies of the main colour table and are overwritten from
  `bodycolors.txt` at start-up (57 lines, `r,g,b`, three per colour: mid, shadow, highlight). Highlight is the
  plain colour for most entries; mid and shadow are about 0.9 and 0.8 of it, hand-tuned for the dark colours.
  The betas also tint the three shades by the day/night light before writing them. **[bin]**
- `bodynw.png` (144×2304) matches that layout: entries 0–7 are the 8 colour slots, 9–16 and 18–25 their
  shadow and highlight shades, entry 8 is the clear colour. A classic `body.png` uses entries 0–6. **[bin]**
- The NewWorld beta `headsconfig.txt` gives each NW head a default colour list; that file is not read by 2.x.

So in NW mode a 2.x client receives and stores 8 colours, draws an NW body with the classic 5-entry mapping, and
the NW body's own colour entries 0, 2, 7 and all 16 shade entries keep the picture's built-in colours.

## Shield sprites

| Build | SHIELD sprite rect |
| --- | --- |
| NewWorld beta 1 and 2 | the GANI's rect, as written |
| 2.1 test 3, 2.17.1, 2.22, 2.31 | the GANI's rect, scaled by (image width / 38) in x and width and (image height / 20) in y and height when the image is not 38×20; the sprite position moves left/up by half of the growth |

The classic shield sheet is 38×20 (four frames: up 0–5, left 6–13, down 14–29, right 30–37). The scaling lets a
double-size sheet (76×40) reuse the classic GANIs. NW shields are 96×20 sheets with extra blocking frames; the NW
GANIs address frames up to x = 96 (for example up at 78, 18 wide). On a 2.x client those rects are multiplied by
96/38 ≈ 2.5 and point past or across frames. The rescale has no NW-mode test. **[bin]**

A GANI-side workaround (dividing every x and width by 2.5) cannot be exact, because the client rounds the scaled
values down.

## Unlocking it

### Client patch

[`tools/nw-unlock/nwunlock.py`](../tools/nw-unlock/README.md) finds the recolour loop, the SHIELD rescale and
the NW getter by byte pattern (all three found once each in 2.17.1, 2.22 and 2.31), adds one small code
section and redirects two places to it. Both changes test the NW getter first, so a classic session (no 177)
runs the original code unchanged.

- **Colours:** in NW mode, recolour 8 slots × 3 shades exactly as the betas do (entries *k*, *k* + 9,
  *k* + 18), from shade tables built into the patch (from `bodycolors.txt` if given, otherwise 0.9/0.8 of the
  client's colours). No day/night tint.
- **Shield:** in NW mode, skip the 38×20 rescale and use the GANI's rect.

Checked by running both patched paths of all three builds in an x86 emulator: with the mode off the palette
writes are identical to the original (entries 5, 6, 4, 3, 1); with it on, 24 entries are written and the clear
entries 8, 17, 26 are left alone. **[bin]**

Side effects:
- The patched exe's code checksum changes, so its tamper-check value (PLI 39, [feature-specs/08-tampercheck.md](feature-specs/08-tampercheck.md)) is no longer the stock one. Our lab servers do not check it.
- In NW mode a classic `body.png` is recoloured with the NW layout and looks wrong. NW mode means NW bodies.
- In NW mode a double-size classic shield sheet is no longer rescaled.

### Server side

A server that wants NW looks on these clients needs to:

1. send 177 once after login (or per level, if only some levels are NW);
2. from then on send COLORS as 8 bytes, both player prop 13 and NPC prop 19; read 8 in the client's player props but 5 in its `PLI_NPCPROPS`;
3. serve NW bodies, shield sheets and GANIs.

Nothing in the stock 2.x client tells the server it supports NW mode, so the server has to know the client
(for example from its version token and a server option). GServer-v2 and Seihai's gserver do not send 177 today.
For the lab the probe proxy injects 177 and 8-colour props ([`tools/probe/`](../tools/probe/README.md)).

## Lab

**[lab]** 2026-11-27. 2.22 under Wine in the Linux lab VM, loopback-only namespace, the GServer-v2 build
(classic world) behind `gen5probe.py` and our listserver. Same plan (`nw-unlock.plan`, owner-held) on the stock exe
and on the `nwunlock.py --bodycolors` exe: a classic look, then 177, then `bodynw.png`, the NW 96×20 shield sheet and
the NW idle GANI with three 8-colour sets. The NW files were fetched from the server by the client. Screens compared
as changed pixels in an 80×80 crop around the player; a repeat run of each build gave identical crops.

| Step | Stock 2.22 | Patched 2.22 |
| --- | --- | --- |
| Classic look, no 177 | reference | identical to stock (0 px), also in a patched run that never sent 177 |
| 177, NW body, colour set 1 | NW body drawn with the classic 5-entry mapping: mostly the picture's own dark colours | recoloured in all 8 slots (604 px from stock) |
| Set 2: only slots 6–8 changed | no change at all (0 px) | body changes (339 px) |
| Set 3: only slots 1–5 changed | partial change (208 px), wrong places | full change (608 px from set 1) |
| Face left (shield visible) | wrong frame: the rescaled rect picks the large front-facing shield art | the narrow side frame at the GANI's offset |
| 8-colour prop, then rupees | next prop applied: the 8-byte width is right | same |
| 5-colour prop after 177, then a direction | the direction bytes are eaten as colours 6–7; the stream desyncs | same (and the eaten bytes show as colours) |

- Neither build crashed. The patched exe's tamper-check value differs from stock; our server ignored it.
- Right after 177 both builds send their own COLORS as 8 values. The classic GServer-v2 reads 5 and mis-parses
  the rest (the player's nickname came back as "unknown"), so a server must handle the 8-byte form before NW mode
  is usable.
- NW mode hides the whole classic HUD (hearts, counts, A/S/D) in both builds.
- In every NW shot the area behind the player is dark green in both builds: `bodynw.png`'s clear entry is index 8,
  but the client treats a different entry as clear. An asset or loader issue, not the patch.
- Two of four patched launches did not log in within the timeout; both retries did. The login-click driver is the
  likely cause, but the screen was not recorded, so the patch is not ruled out.
- The NPC 8-colour read and the 5-colour `PLI_NPCPROPS` cap were not tested live; only the player's own body was.

## Open

- [x] ~~Lab result.~~ [Lab](#lab).
- [ ] Live check of the NPC 8-colour read and of other players' NW bodies.
- [ ] Which palette entry 2.22 treats as clear on an NW body (the green background).
- [ ] What the NW mode changes in the 2.x level loader (`GLEVNW01`) and HUD; only the colour, shield and sword paths were read here.
- [ ] Day/night shading of NW bodies (the betas tint by light; the patch does not).
