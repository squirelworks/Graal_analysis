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
- The payload byte (value 9) is a constant in the sender; I could not tie it to anything else. Meaning NOT resolved (heartbeat-like by behaviour only). Treat as: send GCHAR 9 as PLI 24 every ~5 s on a 2.31 emulation; unknown whether servers care.

## PLI 46 once at login (GCHAR 1)
- Constant 1 byte (GCHAR 1), sent once per level entry (the lab saw it once at login). Purpose not resolved (looks like a client-side per-level 'entered' signal). No dependency on any server data. Not sent by 2.17/2.22.

## What to implement
- 2.31: after login send PLI 46 = GCHAR 1; then PLI 39 (constant) every 3.2 s; PLI 24 = GCHAR 9 every ~5.1 s.
- 2.22: PLI 39 at login and on each level change. 2.17: login only.
