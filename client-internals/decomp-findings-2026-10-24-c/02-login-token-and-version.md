# 02 Login token and version string

All tokens come from the binaries (the 8 characters are built one byte at a time from immediates, so a text search misses them). Table: `version_tokens.tsv`.

## Token per build
| build | token |
|---|---|
| 2.00, rev1, rev2, rev3 | GNW24011 |
| 2.01, 2.01 rev1 | GNW23021 |
| 2.02, 2.02 rev1 | GNW15041 |
| 2.02 rev2 | GNW20041 |
| 2.03 | GNW06051 |
| 2.04 | GNW24061 |
| 2.05, rev1, rev2 | GNW03081 |
| 2.1 test2, test3 | GNW03081 (same as 2.05) |
| NewWorld beta1, beta2 | G2N15041 (different prefix, same digits as 2.02) |
| NewMain 24, 26 | GNW08011 |

## Reading the digits [inferred]
- The shape is prefix + dd + mm + y (day, month, last digit of the year). Read that way, 2.00 is 24 Jan 2001, 2.01 is 23 Feb, 2.02 is 15 Apr, 2.02 rev2 is 20 Apr, 2.03 is 6 May, 2.04 is 24 Jun, 2.05 is 3 Aug. All sit inside the year-2001 changelog (`newfeatures2001.txt`) and rise in order, so this is very likely a build date.
- NewMain (08011 = 8 Jan) is older than 2.00 by this reading, which fits a branch that was frozen before the 2.00 release.
- NewWorld beta carries "G2N" and the 2.02 date, so it branched from the 2.02 code line. Its class list agrees (see 09).
- Revisions within one version do not change the token (2.00 rev1-3, 2.01 rev1, 2.02 rev1, 2.05 rev1/rev2) except 2.02 rev2, the only rev that changes both token and login behaviour. A server allow-list therefore needs one entry per version, plus an extra entry for 2.02 rev2.

## Login string shape (unchanged across all 20 builds)
- Type 0 packet: one random key byte (GCHAR of key & 0x7F), the 8-character token, GCHAR(len) + account, GCHAR(len) + password. Account and password are plain.
- Straight after it, 2.02 rev2 and every later 2.x build (also NewWorld) send PLI 37 with the language string. 2.00 to 2.02 rev1 do not. This matches the vendor changelog for 2.02 rev1 ("the server knows the language of the client", planned) and the actual send shows up in rev2.

## What changed in the login function between revisions
- 2.02 rev1 to rev2: only the token and the extra id-37 send. No other login changes.
- 2.00 rev3: a change in a player-creation routine and the tab-control handler, not in login.
- 2.05 rev1/rev2: changes only in main-form creation and mouse handling.

## Server consequence
A lab or Seihai server that wants all of these clients must list all token strings above. Tokens never contain a version number as such, only the date code, so the server cannot derive a build's capabilities from the token alone: see `04` and `05` for what each build can send/handle.
