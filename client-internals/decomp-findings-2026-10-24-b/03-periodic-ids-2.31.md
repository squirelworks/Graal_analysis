# 2.31 periodic traffic: PLI 24, PLI 39 re-send, PLI 46

Mapping of the lab observations to the client's behaviour (all values are durations).

## PLI 39 re-send every ~3.2 s
- The main form of 2.31 has a 50 ms timer. Its handler keeps a counter modulo 64 (64 = length of the 64-character alphabet string used there), so one full cycle = 64 x 50 ms = 3.2 s.
- Phases of the cycle (counter value -> action):
  - 1: anti-debug probe (a privileged port-I/O instruction guarded by an exception handler, then a breakpoint-trap check), and a 5000 ms timer is armed.
  - 10: recompute CRC word A of the tamper check.
  - 20: scan all top-level windows (title and class) against an obfuscated blacklist (cheat-tool detection). The list was not decoded and is not needed.
  - 30: recompute CRC word B.
  - 31: send PLI 39 with the freshly computed A+B.
- Because A and B recompute to the same constant each time (see 01), the 10 bytes are identical on every re-send (lab confirmed). I did not find the blacklist scan or the probe result feeding into the words; what the client does on a hit was not traced.
- 2.17.1 and 2.22 have no such timer. 2.22 only re-sends from the level-change routine.

## PLI 24 about every 5.1 s (1 byte, lab value 9)
- 2.31 only. The 5.1 s cadence fits the 5000 ms timer armed in phase 1 (5.0 s plus timer granularity). That link is an inference, not traced to the end.
- **Lab batch c (`08-lab-findings-levelchange-24-178.md`):** 2.31 sends it at login and every 5.11 to 5.17 s (median 5.13 s) whatever it is doing, in every level; level changes neither trigger nor reset it. **2.22 also sends 24 = 9** every 5.1 s, but only while another player is in the same level (0 in 3 solo sessions), so "2.31 only" is wrong for two-player 2.22. The stock server relays any payload unchanged as `PLO_SHOWIMGPLAYER` (32) to the others in the level; injected payloads caused no reaction.
- The payload byte (value 9) is a constant in the sender; I could not tie it to anything else. Meaning NOT resolved (heartbeat-like by behaviour only). Treat as: send GCHAR 9 as PLI 24 every ~5 s on a 2.31 emulation; unknown whether servers care.

## PLI 46 on every level entry (GCHAR 1)
- Constant 1 byte (`GCHAR 1`). **Updated by the lab run of batch b2:** it is sent on every level entry, not only at login (7 sends in one gmap run: login plus six edge crossings), always just before the props message that carries the cell prop (43 or 44) and the wrapped coordinate. Details: `07-lab-findings-46-186-200.md`.
- 2.31 does not re-send PLI 39 at a crossing. Not sent by 2.17/2.22.
- **Lab batch c:** also sent on doors, edge links and server-side warps (always just before the first props of the new level; in the same frame as a cached-level link request, otherwise in the first frame after the server's level answer). 2.31 does not re-send 39 there either. 2.22 sent no 46 in 0 of 8 transitions, but sent 39 after each client-initiated link request. Details: `08-lab-findings-levelchange-24-178.md`.

## What to implement
- 2.31: send PLI 46 = GCHAR 1 at login and on each level change; PLI 39 (constant) every 3.2 s; PLI 24 = GCHAR 9 every ~5.1 s.
- 2.22: PLI 39 at login and after each client-initiated level-link request (not after a server-side warp); no 46; PLI 24 = 9 every ~5.1 s while another player is in the level. 2.17: login only.
