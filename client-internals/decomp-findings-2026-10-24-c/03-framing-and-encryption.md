# 03 Framing and encryption (2.00 - 2.1, NewWorld, NewMain)

## What is the same everywhere
- Message = GCHAR(id) + payload + newline; id = byte - 0x20. GCHAR = byte - 0x20. GINT2 = (b0-0x20)*0x80 + (b1-0x20). GINT3 adds a third byte with multipliers 0x4000, 0x80, 1. These read patterns are used by handlers in all 20 builds with the same constants.
- Frames on the wire are a 2-byte big-endian length followed by a zlib body; the client's outgoing messages are collected and flushed as one zlib block. The shared Borland LCG constant occurs in every build (it is also used by the Delphi random-number routine, so by itself it does not prove the junk-byte step; the junk-byte description in batch b for 2.00 still applies). No build changes the flow in a way that needs a new decoder.
- PLO 100 (RAWDATA, GINT3 length) is handled in every build from 2.00 on, including NewWorld and NewMain. Ids 101/102 never appear as handled ids in any build (they travel behind 100).

## Where zlib comes from (the one real difference)
| builds | zlib source |
|---|---|
| 2.00 rev1-3, 2.01, 2.01 rev1 | compiled-in Pascal zlib unit (z_stream record visible in names) |
| 2.02, 2.02 rev1, 2.02 rev2 | external `zlib.dll` (import, with deflate/uncompress/deflateInit thunks) |
| 2.03 and later (2.04, 2.05, 2.1 test, NewWorld, NewMain) | compiled-in Pascal unit again |

- The 2.02 family therefore needs zlib.dll beside the exe, or a Wine override, to run. All other builds run without it.
- The change is link-level only; the wire format is the same.
- Possible reason [inferred]: a short-lived switch to the DLL during 2.02, then back. No changelog line mentions it.

## Encryption generations
- All 20 builds send type 0 login with the 8-character token in the first 8 bytes. A server that treats "first 8 bytes is a known token" as generation 2 (zlib, no cipher) serves them. The 2.05 behaviour (insert one junk byte per message after the first) is described in batch b for 2.00 and 2.05 and was not seen to change in 2.01-2.04.
- No build before 2.1 has bz2 or a per-frame compression-type byte. The 2.1 test builds also do not (they behave like 2.05 here).
- NewWorld beta1/2 and NewMain 24/26 use the same transport and the same login shape as 2.00-2.05.

## Not verified here
- Whether the gen-3 junk-byte step is byte-for-byte identical in 2.01-2.04 (the call structure matches 2.00 and 2.05, but I did not diff the exact insertion index formula per build).
