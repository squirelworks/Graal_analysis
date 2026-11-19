# Appendix E lab runs on GwenTea2 (2026-11-20)

Date: 2026-11-19/20. Evidence: **[lab]**. Real clients in the GwenTea2 Debian lab VM, on loopback
only: Wine 10, a gs2emu lab gserver and the `gen5probe` injecting proxy. One probe ran at a time
on an idle VM. Captures and screenshots stay in the lab. Probe rows are appended to
[`probe-results.tsv`](probe-results.tsv).

## Key emote on 2.05 (E#322)

Client: 2.05 rev 2 (`Graal.exe`, token `GNW03081`). Plan: `e322-205.plan`, run `fz-e322-205-g`.

| Input | Client to server |
| --- | --- |
| Ctrl+A | one `PLI_UPDATEFILE`-style file check (34) for `emoticon_afk_stay.mng`, once per session; three more presses send nothing |
| Ctrl+S, Ctrl+D | only their own file checks, `emoticon_smile.png` and `emoticon_dgrin.png` |
| plain a, Alt+A, Shift+A, F1–F12 | nothing |

Ctrl+A draws the AFK thought bubble locally. The client sends no `PLI_SHOWIMG` (24) and no
props, so the server has nothing to relay to other players. A second client was not run, because
nothing relayable leaves the first.

## GS2 class path on 4.20r8 (E#202 leftover)

Client: 4.20r8 (`G3D20126`) under Wine. Plan: `gs2deliver420.plan`, run `fz-gd420-g`. The body is
a Seihai-compiled `keylog.gs2` whose `onCreated` timer chats `D0` within 0.1 s if it runs.

- Ten frames were sent:
  - 197 as text, i5 weapon, i5 class, empty, and name only;
  - 140 with a weapon body with no cache, with `cache=1`, after a 197 with the same key, with
    the header length short by 2, and with an empty body.
- No case ran the script. After any 197 the client sent no request at all, and it stayed alive
  throughout.
- So 4.20r8 does not honour the 6.x class path (a 197 descriptor, then the body in 140) as sent
  here. NPC bytecode in 131 behind 100 still runs on 4.20r8
  ([script-fuzz-2026-11-19.md](script-fuzz-2026-11-19.md)).

## Shot last byte on 2.22 (E#312, partial)

Client: 2.22 (`GNW03014`). Plan: `shotbyte222.plan`, sweeping the last byte from 0x20 to 0x7e,
owners 3 and 999.

- 0x23 to 0x7e: the shot ends in a bomb-style blast, and the client fetches `bomb.wav`.
- 0x20 to 0x22: no blast. 0x20 fetches `arrow.wav`.
- In both sweeps the lab's block NPC stood in the shot's path, and nothing hurt the player. A sweep
  on open ground is still to run.

## NPC prop widths on 2.22 and 2.31 (not settled)

- The width plan's canary never landed, because its reset packet did not move NPC 300 back. The
  canary on its own does move the NPC on 2.22, so the plan needs a working reset.
- 2.31 reacts visibly to props 75–77: the NPC moves or vanishes.

## v7 Worlds 614 at the date boundary (E#615)

A Windows 10 VM with no network adapter, and the guest clock set before each standalone start.

| Guest date | Runs | Result |
| --- | --- | --- |
| 2024-10-12 | 2 | start-up and environment init, failed connector attempts (no network), then OpenGL initialised; window stays up |
| 2024-10-13 | 2 (12:00 and 00:30) | start-up and environment init only; OpenGL never initialises; window stays up, black |

Neither date quits within 2–4 minutes, and no quit line or reason text reaches the player log. So
past the boundary the gate shows up, standalone, as start-up stalling before graphics init. It does
not show as `QuitInstant` or a reason string. Whether a quit would follow with a server present is
not known.
