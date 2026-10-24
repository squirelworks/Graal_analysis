# Tamper-check (client PLI 39): how the 10 bytes are built

Derived facts only. All six lab values (two captures each of 2.17.1, 2.22 and 2.31) were reproduced offline from the client executables, so the description below is verified, not guessed. Lab captures and re-send timings: `version-profiles/tampercheck-values.tsv`.

## What the 10 bytes are
- Two 32-bit words, A then B, each written as 5 bytes. The 5-byte form is NOT the normal GINT5 and NOT masked:
  - byte 1 = ((v >> 28) & 0x0F) + 0x20
  - byte 2 = ((v >> 21) + 0x20) & 0xFF
  - byte 3 = ((v >> 14) + 0x20) & 0xFF
  - byte 4 = ((v >> 7)  + 0x20) & 0xFF
  - byte 5 = (v & 0x7F) + 0x20
  Only bytes 1 and 5 are range-limited, so bytes 2-4 can be below 0x20 or above 0x7F. That is why the lab saw bytes under 0x20 and why "two GINT5" is wrong. (Layout is the same in 2.17.1, 2.22, 2.31.)
- Both words are standard reflected CRC-32 values (polynomial 0xEDB88320, initial value 0xFFFFFFFF) computed over the client's OWN memory image (the running exe, in memory), chained: the first call finishes with the usual final inversion, its result is used as the starting value of the next call, and the last call of each word skips the final inversion.
- Word A covers 8-9 contiguous ranges of the code section (a sliding selection of code, not the whole section).
- Word B covers one large code range plus one block of static data (a table of string pointers in the data section).
- Nothing in the input depends on login key, account, level or time. So per build the result is a constant, exactly as the lab saw. The value only changes if the exe bytes change (a patched or re-packed exe changes it; an unpatched original does not).

## Per-build values (words in hex, lab bytes in hex)
See `version-profiles/tampercheck-words.tsv`. Short form:
- 2.17.1: A ab637cbe, B 3e48dc0c, bytes 2a7bad195e231243d82c
- 2.22: A 5dcb77f6, B bc736311, bytes 250e4d0f962b03ede631
- 2.31: A 9ecd4bc0, B ecea65e2, bytes 291655b7602e87c9eb82

## What a Seihai client must do
- Replaying the constant per emulated build is enough (it is what the real client sends). Computing it needs the original exe bytes plus the range lists, which are inside each exe; not needed unless Seihai wants to accept patched exes.
- Position/timing per build: see `03-periodic-ids-2.31.md` and the table at the end of this file.

## When it is sent
| build | login | later |
|---|---|---|
| 2.17.1 | yes, once | never in ~90 s of lab |
| 2.22 | yes | re-sent by the level-change routine on every level change (so each gmap edge crossing in the lab); no timer |
| 2.31 | yes | every 3.2 s; a 50 ms main-form timer drives it (see 03) |

## Does the server verify it?
Lab: GServer-v2 accepts all three and logs nothing. The decompiles only show the sender; no check on the receive side of the client. Treat as sent-and-ignored for a compatible server.
