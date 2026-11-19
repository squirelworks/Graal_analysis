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
a bad body fails quietly. 4.20r8 and 5.24r4 were not run. **[lab]**

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

## Open

- [ ] #646 on 4.20r8, 5.24r4 and 5.12 under Wine.
- [ ] The `DEFAULT*` header lines in 195 (still no visible effect).
