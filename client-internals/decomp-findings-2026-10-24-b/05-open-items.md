# Open items after the 2.00 / 2.17.1 / 2.22 / 2.31 decompile pass

## Settled by this pass (for reference)
- **`PLO_HIDENPCS` (151)** removes the NPCs with ids 1 to 999 of the active level. Id 0 is excluded. (Earlier note: "probably ids below 1000".)
- **`PLO_SIGNATURE` (25)** value 1 makes the client quit. Value 0 makes it quit unless the connected host string is `127.0.0.1`. Any other value is ignored. Identical in 2.17.1, 2.22 and 2.31, and the id is handled from 2.00 on. The value 73 that public servers send at login ("more than eight players") is in the ignored group, so it never triggers the quit rule.
- **Tamper check:** how the 10 bytes are built (`01-tamper-check-id39.md`), and why 2.31 repeats it every 3.2 s (`03-periodic-ids-2.31.md`).
- **2.00 login** and its allow-list requirement (`04-v2.00-client.md`).

## Still open
| Item | State | What would settle it |
|---|---|---|
| Client `PLI_SHOWIMGPLAYER` (24), 1-byte payload value 9 (2.31 only, about every 5.1 s) | The 5.1 s cadence fits the 5000 ms timer armed in the 2.31 main-form timer (inference, not traced to the end). The 9 is a constant in the sender and is not tied to anything else. Meaning unknown. | Trace the sender's caller chain; or see whether any server reacts to a different value |
| Client `PLI_ENTERLEVEL` (46), payload `GCHAR 1` | Sent once at login in the lab (2.31 only). Looks like a per-level "entered" signal; no dependency on server data. Purpose not resolved. | Lab run that changes level several times, to see whether it repeats |
| `PLO_SERVERWARP` (178) field meanings | Comma text with at least 4 fields; fields 1 to 3 go to a connect-to-other-server routine, field 0 is ignored. Which field is name, host or port is not resolved. | Follow the routine's callee in 2.22 or 2.31 |
| `PLO_BOARDMODIFY2` (186) trailer | After the `w*h` GSHORT tiles there is a trailer that the handler does not decode here. The length check only requires `6 + 2*w*h`. | A public or lab capture of 186 with a non-empty trailer, or a longer read of the handler |
| `PLO_SETACTIVELEVEL` (156), extra step in 2.31 | 2.31 adds a follow-up step (a call with all-zero arguments, then another call) that 2.17.1 and 2.22 lack. Purpose not resolved. No wire change. | A longer read of the 2.31 handler |
| Client to server ids 36, 42 and 45 in 2.22 | Not matched to a call site. This pass scanned 2.0x only, not 2.17/2.22/2.31, for client senders. In 2.0x, 36 is sent from 2.01 on; 42 and 45 never appear in any 2.0x or 2.1 test build. 45 is the reply to `PLO_HASPROCESSRUNNING` (183) per the 2.22 and 2.31 receive side. | The same send-site scan over the 2.17.1, 2.22 and 2.31 decompiles |
| 2.00 listserver login frames | Not exercised. The list host is DES-hidden and 2.00 does not read `arrays2.dat`. | Lab run with the host name redirected to the lab listserver (`04-v2.00-client.md`) |
| 2.31 window-title blacklist (cheat-tool scan inside the 50 ms timer) | Deliberately not decoded. What the client does on a hit is not traced, and the scan result was not found feeding the tamper words. | Not needed unless a server is seen to enforce the tamper check |
| Per-build handled-id sets for 2.01 to 2.04 and the 2.1 test builds | Read from dispatch tables only, no handler bodies. | A decompile of those builds (not yet available) |
| `PLO_NPCACTION` (26) in 2.00 to 2.03 | Handled, payload not decoded. | A decompile of 2.00 to 2.03 handlers |
| 2.1 to 2.16 and 2.3 | No binaries anywhere (`../drive-clients-inventory.md`). | New binaries |
