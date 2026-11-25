# Lab: baddy props 11 and up, compiled gani scripts, and the 2.31 start-params step

Date: 2026-11-19. Issues #645, #646 and #647. Loopback lab in the Linux lab VM. The probe
proxy (`../tools/probe/`) sat between each client and a gs2emu lab world. Results rows are in
[`probe-results.tsv`](probe-results.tsv). Captures, logs and shots are kept off the repo.
Evidence `LAB-RESEARCH-UNKNOWNS-20261119` ([index](../docs/evidence-index.tsv)).

## Baddy props 11 and up on 6.03r7 (#645)

**Static read (Linux 6.03r7).** The `PLO_BADDYPROPS` (2) handler takes the baddy id
(first byte − 32), finds or creates the baddy, and passes the rest of the message to the
baddy's prop reader. That reader loops over `GCHAR id` + value. It only has cases for ids
**0 to 10** (gs2lib `BDPROP_ID` to `BDPROP_VERSEDEATH`). Any id of 11 or more **ends the
message**. The reader returns, and every prop after it is dropped. It does not skip a byte
the way an unknown player prop id does on 4.x–6.x. **[bin]**

| Id | gs2lib name | 6.03r7 |
|---:|---|---|
| 0 | `ID` | one byte |
| 1, 2 | `X`, `Y` | one byte each, half-tiles |
| 3, 4, 6, 7 | `TYPE`, `POWERIMAGE`, `ANI`, `DIR` | have a case (4 can carry a gani name) |
| 5 | `MODE` | one byte; mode 9 removes the baddy |
| 8, 9, 10 | `VERSESIGHT`, `VERSEHURT`, `VERSEDEATH` | GCHAR length + text |
| 11 and up | — | no case: the rest of the message is dropped |

**Lab (run `kc`, a kill test that does not depend on position).** The probe baddies walk
on their own, so the test used mode 9 (remove) as the canary instead of a position.
**[lab]**

| Sent | Result |
|---|---|
| `5 = 9` alone | the baddy is removed |
| `11`, then `5 = 9` | the baddy stays: id 11 ended the message, so the removal was never read |
| `20`, then `5 = 9` | the same |
| `5 = 9` again, alone | the baddy is removed |

So 6.03r7 has no baddy props above 10. A server should never send one, because the props
after it in the same message are lost. **[bin][lab]**

### Baddy modes and the client's own reports (fuzz, 2026-11-19)

A baddy that `PLO_BADDYPROPS` creates is run by the client's own AI, and the level leader
reports its changes back to the server as `PLI_BADDYPROPS` (15). The fuzz round used that
report as an observer, with no screenshot. Per mode on 6.03r7 **[lab]**
([fuzz](../live-runs/fuzz-2026-11-19/README.md)):

| Mode | What the client does and reports |
|---|---|
| 0–4, 8 | walks; reports x, y, ani and dir |
| 5 | ani counts down from 55 to 0 (dying), then the reports stop |
| 6 | animates in place; reports ani only |
| 7 | jumps in place; reports ani and one y |
| 9, 10 | no reports at all (9 removes the baddy, as above) |

4.20r8 also reports ani and dir within 1.6 s but sent no x/y in that window. With a silent
mode-10 baddy and mode 0 as the canary, ids 11–30 end the message on 4.20r8 and 2.22 as well.

## Compiled gani scripts on 6.03r7 (#646)

The body of `PLO_GANISCRIPT` (134) is a `GCHAR` name length, the gani name, then the compiled GS2
script. It went out behind `PLO_RAWDATA` (100). The packet has **no checksum field**: the
client takes the body on its name alone. **[lab]**

Each run sent a 134, then made the player play that gani. The script was compiled with
seihai-core's GS2 compiler. **[lab]**

| Body | Result |
|---|---|
| Valid script: `onCreated` sets the player's chat text, `onTimeout` fires after a timeout | **The script runs.** `onCreated` fires (the client sent the new chat as a `PLI_PLAYERPROPS` (2)), then `onTimeout` about 3 s later. The client also sent `PLI_WANTFILE` (23) and `PLI_UPDATEGANI` (157) for the gani |
| The same script with one bytecode byte flipped | No script event and no crash |
| Empty script part | No events and no crash |

So a compiled gani script sent in 134 runs on 6.03r7 like any other compiled script, and
a bad body fails quietly. **[lab]**

**4.20r8 and 5.24r4 under Wine (runs `gani646-420`, `gani646-524`).** The same three bodies gave
the same results. With the valid script, the client fetched the gani (`PLI_WANTFILE` 23,
`PLI_UPDATEGANI` 157), then `onCreated` and `onTimeout` both fired. The corrupt and empty
bodies fired no events, and neither client crashed. So 4.20r8, 5.24r4 and 6.03r7 all run a
compiled gani script from 134 the same way. **[lab]**

## 2.31 start parameters after 156 (#647)

This lab run confirms the static read in [`plo-156-setactivelevel-231.md`](plo-156-setactivelevel-231.md). **[lab]**

| Run | Command line | Result |
|---|---|---|
| `link647` | `graal://A GS1 Control/hello` (the lab world's list name) | After the first 156 the client sent one `PLI_TRIGGERACTION` (38): npc 0, x 0, y 0, `serverstartparams,hello`. An injected second 156 sent nothing |
| `nolink647` | none (login form and server list) | It logged in and got 156, and sent no trigger action |

Client: Windows 2.31 (`GNW28015`) under Wine. Server: the GS1 lab world behind `gen5probe.py`.

## Lab note

On this VM's system Python, `run603.sh`'s black-screen check could not import Pillow, so
it never retried and each run kept whatever it got first. Runs here used a copy that calls
a Python with Pillow installed. Install Pillow for the harness Python before relying on
the retry.

## DEFAULT* gani lines: static follow-up (G261, 2026-11-25)

Static read of the 4.20r8 engine, the 5.12 engine memory image and the 6.03r7 third-party unpack; nothing run. In the 6.03r7 unpack the gani keyword strings are hidden, so its keyword list and slot ranges were taken from 6.00r4, which has them in plain text; the 6.03r7 draw path was read directly. **[bin]**

**Verdict.** In all three clients the `DEFAULT*` lines are parsed and stored on the gani but never read. The 2026-11-19 result (no visible change, no file requested) is therefore expected for every drawn character, not only the player's own. The guess that a default fills in for an NPC with no head of its own is not supported.

- **Keywords.** Only `DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTPARAM1`–`8` and `DEFAULTATTR1`–`9` are recognised. `DEFAULTSWORD`, `DEFAULTSHIELD`, `DEFAULTHORSE`, `DEFAULTSPRITE` and `DEFAULTCOLOR` do not exist and are ignored like any unknown line. Numbers outside those ranges are dropped, and `DEFAULTHEAD` with no value is skipped. The values go into 19 text slots on the gani object (same layout in 4.20r8 and 5.12; 6.x shifted).
- **Readers.** In 4.20r8 the only code touching those slots is the gani's parse, create, copy, clear and free paths. The routine that picks each sprite's image (4.20r8, 5.12 and 6.03r7 alike) takes head, body, attributes and params from the drawn character. An empty character value draws nothing; there is no fallback to the gani default. The one fallback found is unrelated: an attached object borrows its parent's params.
- **No file request.** The pass that requests missing images walks the same character values, so a default's file name is never looked up at all, not merely deferred until first drawn.
- **Builds.** 4.20r8 and 5.12 are identical; 6.03r7 draws the same way.

The manual's gani keyword table (§3.3) describes the editor, where these lines fill the preview; that is separate from the clients above.

A negative-control lab case, not run: an NPC with `showcharacter`, no head or attributes set, and a gani with `DEFAULTHEAD head19.png`, `DEFAULTATTR1 hat0.png` and HEAD/ATTR1 sprites, on 4.20r8 and 6.03r7. Expected: those sprites draw nothing and no file is requested. Positive control: set the NPC's head to `head19.png`, which should then be requested and drawn.

## Open

- [x] ~~#646 on 4.20r8 and 5.24r4 under Wine.~~ Same as 6.03r7 (above). 5.12 not run.
- [x] ~~The `DEFAULT*` header lines in 195 (still no visible effect).~~ [Static read 2026-11-25](#default-gani-lines-static-follow-up-g261-2026-11-25): stored but never read on 4.20r8, 5.12 and 6.03r7. **[bin]**
