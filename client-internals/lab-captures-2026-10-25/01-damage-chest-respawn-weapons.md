# Lab captures 2026-10-25: chests, damage, CURPOWER, respawn, default weapon ids (2.22, derived facts only)
Experiments: A chests, B damage powers, C CURPOWER and packet 40, D end-of-respawn save, E default weapon ids. Verdicts are marked settled or OPEN in each section.
Method: see the end of this file.

## Part 0: facts decoded from earlier-attempt leftovers (labm/res/*.out, real 2.22 client c1 as victim; server->client packets injected through proxy2.py; c2 = a second real 2.22 client, other player id 3)
Harness caveat: positions are read from the client's own X/Y props; hearts are also read from screenshots.

### C. CURPOWER semantics (settled for 2.22)
- CURPOWER (prop 0x22) is in HALF hearts; MAXPOWER (prop 0x21) is in hearts. Injecting MAX=10, CUR=28 then taking a half-heart hit made the client send CUR=19: the client clamps CUR to MAX*2 (20) before subtracting. MAX=3, CUR=10 then a half-heart hit sent CUR=5 (clamp to 6, minus 1); the screen showed 2.5 hearts.
- The client does not send anything when the server sets CUR/MAX (no echo).
- After a hit the client sends ONE props message: CURPOWER (new value) + GANI `hurt` + one more prop (0x31). Our own CURPOWER write on injected CUR=0: client sends `dead` GANI and prop 0x32, no CURPOWER.
- After the death key (arrow key) the client sends CURPOWER = hearts by AP bracket (MAX=10): AP 10 and 19 -> 6 (3 hearts); AP 20 and 39 -> 10 (5 hearts); AP 40, 60, 100 -> 20 (10 hearts = full). (lab result file)

### B. Packet 40 (hurt player), real client as victim (settled for the cases below)
- Payload as accepted: attacker id (2 bytes), dx byte, dy byte, power byte. Hit applied only when the attacker id is a player the client knows (ids 99, 0, 2 here: ignored, no damage, no knockback).
- Power byte (byte-0x20) is in HALF hearts: 0 -> knockback only, no hearts; 1 -> half heart (CUR 6->5); 2, 3, 4, 15, 31 -> one heart (CUR 6->4). So the cap is 2 half hearts, matching the decompile ("capped at one heart").
- Knockback: direction from (dx-0x60, dy-0x60); always 5 tiles (50 ms steps); diagonal (0x70,0x70) gives (3.5, 3.5) so the vector is normalised. 0x61/0x68 gave the same as 0x70 (sign/direction only), 0x5f/0x50 went the other way.
- A trailing 4-byte field (sent as 20 20 20 20) made the hit do NOTHING (no damage, no knockback); 2 trailing bytes were still accepted, 3 were not. So the NPC-id field (when present as the 4th extra byte) is looked up: an unknown NPC id 0 drops the hit. (Open: what a real NPC id does.) The earlier distance test (exp40d) used the 4-byte form, so its "no hit at distance^2 81..132" is NOT evidence for a distance gate; re-test is in Part 1.
- Server-sent bomb (PLO 11) and arrow (PLO 19) injected near the victim: half-heart hit (CUR 6->5) with a 5-tile knockback directly away from the bomb/arrow start. Damage showed 4 (a full heart) in a few runs (bomb field 0x23, 0x2b; arrow last byte 0x24) without a clear rule: OPEN.
- Real arrow shot by c2 (last byte 0x21 on the wire) never hurt c1 in realarrow2, and an injected arrow with last byte 0x20-0x22 did nothing while 0x23-0x2c hurt: OPEN what that byte means.
- (superseded by the Part 2 bomb notes below) Bomb hit zone from the first sweep was misread.

### D. End-of-respawn save (open, partial)
- After death the client sends: CURPOWER 0 + GANI dead; arrow key -> a warp request (client msg id 30) carrying (x,y,level) = (30.0, 30.5, lv_a.nw) = the level's login/entry point, not the death spot (26.0 / 23.5). Second death after the server's warp reply (with the reply delayed 8 s or not delayed): request again (30.0, 30.5). So after the reply arrives the saved point is the entry point either way.
- NOT tested: dying again inside the delay window (before the reply), which is the only case where "save at end of respawn" would show the death spot.

## Part 1 (fresh runs, 2026-10-25 ~22:50-23:10 JST): A. Chests (real 2.22 client, labm lab, PLO_LEVELCHEST (id 4) injected)
- Full (closed) form `00 x y item sign` (each +32) is drawn as a closed chest, short form `01 x y` as an OPEN chest (dark inside). Each is a 32x32 px block = 2x2 tiles at x,y (top-left), drawn over the grass board; no board tile needed. Settled for 2.22.
- A closed chest is solid like a wall: walking into it from any side stops the player when the 12 body probes touch its 2x2 box (matches #61). Pushing against it plays `push.gani`.
- OPENING: only when the player faces UP (the chest is above, the player below it) and presses the action key (A). Facing down, left or right with the player stopped against the chest and A pressed: NOTHING is sent (3 sides tested, each with a chest adjacent). Settled for 2.22; 2.05 not checked.
- On opening (facing up) the client at once: asks for `chest.wav` (WANTFILE), sends PLI_OPENCHEST (20) with x,y = the chest's top-left tile (whole tiles, +32), and draws the chest open locally (no server reply needed). About 1.2 s later it sends packet 13 with x*2,y*2 = (chest.x, chest.y-1), i.e. one tile above the chest. It does NOT send a rupee/props update; the rupee counter stayed 0 (the lab server did not know the injected chest, so the reward cannot be judged here). Open: what the server sends back for a known chest.
- Compare Seihai (documentation/chest-drawing.md, #65): drawing and short/full forms agree. Difference: Seihai opens a chest from any facing (offline: the point one tile ahead of the feet); the real 2.22 client only from below facing up.

### B/C addendum (fresh runs 23:10-23:30 JST): packet 40 distance gate
- Clean packet (attacker id 3, dx dy power, no trailing bytes), victim c1 on the same row, attacker c2 fixed at x=33.0: hit (CUR 6->4, knockback) at squared distance 64, 81, 90.25, 100.0; NO hit (hearts unchanged, no knockback) at 110.25 and 121.0. So the gate is distance^2 <= 100 (10 tiles), settled for 2.22. The earlier "no hit at 81" results used the NPC form and are explained by the NPC rule below.
- NPC field: the trailing field is 3 bytes (GINT3 npc id). With 3 or 4 trailing bytes (`20 20 20` = id 0, `20 20 21` = id 1, `2a 2a 2a`) the real client refuses the hit completely (no damage, no knockback); with 2 trailing bytes it still hits. This is exactly Seihai's `parse_hurtplayer` (npc only when >= 6 bytes follow the id) plus `Reject::NpcSource`.
- Zero knockback vector (dx=dy=0x60): knocked 5 tiles EAST in every run. Matches the decompile ("a zero vector is replaced by one tile east") and #55.
- Everything else in packet 40 (power cap 2 half hearts, power 0 = knockback only, unknown attacker refused, 5-tile normalised knockback) already matches Seihai #55: no Seihai change needed for packet 40.

### D. End-of-respawn save (settled for 2.22, same-level respawn)
Run respawn5.py: die at x=26 (hearts 1), hold the server's reply for 9 s, press an arrow key (warp request (30.0, 30.5, lv_a.nw) at +3.1 s), then INSIDE the 9 s window reset hearts, die again at x=28.5 and press a key: the second warp request is again (30.0, 30.5, lv_a.nw), not the death spot (28.5 / 26). After the held replies arrive the player is at (30.0, 30.5). So the respawn routine's extra save does not make the next respawn point the death spot, with or without the delayed reply. Seihai's current behaviour (respawn at the level's entry point; no end-of-respawn save) agrees. (Seihai documentation said "needs capture"; update the doc.)

### E. Default weapon ids -> images (real 2.22; only what the captures show)
- Login with the server's PLO_DEFAULTWEAPON (43) frames filtered to id 7 alone: the client asks `wbowi1.png` (then `wbomb1.png`). Login with ids filtered to none, or to 8 alone: `wbomb1.png` is asked and `wbowi1.png` is NOT. So id 7 -> `wbowi1.png` is settled; `wbomb1.png` is asked regardless of id 8 (it comes with the client's own bomb item), so id 8 -> `wbomb1.png` is NOT shown by the capture.
- Ids sent after login (one per second, ids 0..39): the client asked for a file only for: 12 -> `wbomb2.png`, 20 -> `wbowi2.png`, 21 -> `wbowi3.png`, 22 -> `wbowi4.png`, 23 -> `wbomb3.png`. Ids 7 and 8 asked nothing (already asked at login); all other ids 0..39 asked nothing. So the table above (7, 12, 20, 21, 22, 23) is all that is known; "bow = 7, bomb = 8" from the server source is only half confirmed (7 yes, 8 not isolated).

### B. Bombs, arrows, baddies: who owns the damage (Part 2, fresh runs)
- No hit packet is sent. Across every bomb and arrow trial (leftover logs plus new runs, >100 hits) the real client sent no PLI 26 (hurt player), 46 (hit objects) or 41; the only messages after a hit were the props message (CURPOWER + `hurt` GANI) and the knockback walk. The victim's own client judges the damage when a server-sent bomb (PLO 11) explodes near it or a server-sent arrow (PLO 19) reaches it, whoever owns it. A client's own bomb hurts the owner too (c2's own bomb: c2 lost half a heart, knocked 5 tiles away; each trial 1 half heart).
- Damage seen: 1 half heart (CUR 6->5) with a 5-tile knockback away from the bomb/arrow (victim centre minus the blast point), in every deterministic trial; a few runs showed 4 (a full heart) without a rule: OPEN (maybe a second overlapping hit).
- Bomb zone with a 7.5 s wait (explosion done): victim at (30,30.5), bomb x=30: hits at y offsets +1, +3, -3 (bomb y 31.5, 33.5, 27.5); NO hit at 0, +2, -2 (30.5, 32.5, 28.5). With bomb y = victim y+1: hits at x offsets +4, +5, -4. Row offset 0: nothing at x offset 0, +1, -1. This is not a plain radius; it looks like a pattern keyed on the bomb's half-tile y (the first, 4.5 s-wait sweep had hits at every .0/.5 offset except the integers 0, +-2): OPEN, needs the 2.05/2.22 explosion routine, not guessed here.
- Arrows: an injected PLO 19 arrow (owner 3) hurt only when its last byte was 0x23 or more; bytes 0x20 to 0x22 did nothing; the real arrow c2 fires carries 0x21 and never hurt c1: OPEN (probably a flight/lifetime field).
- Baddies: not tested (the lab server has no baddies). OPEN.
- What Seihai should do: nothing changes for bombs/arrows yet; documentation/damage-respawn.md can say "judged by the victim, half heart, 5-tile knockback away from the blast; blast shape open".

## Seihai changes that came out of this
- Chests open only facing up: squirelworks/seihai#73.
- Login asks the images of default weapon ids 7, 12, 20-23: squirelworks/seihai#74.
- Packet 40 (range, cap, NPC refusal, zero vector), CURPOWER clamping and the respawn hearts by AP already matched Seihai (#55); no change.

## Method (no traces kept here)
Real 2.22 client under Wine in a private network namespace against the lab GServer and list server; server-to-client messages injected by a re-encoding proxy; client messages read from the proxy's decoded log. Hearts also read from screenshots. No public server, no credentials.
