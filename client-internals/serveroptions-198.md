# PLO_SERVEROPTIONS (198): what the client does with it

What 5.x and 6.x clients do with server-to-client id 198 (`PLO_SERVEROPTIONS` in gs2lib's names) after the receive handler stores it. Answers a community question, together with a short answer on when `PLO_SETACTIVELEVEL` (156) arrived.

Cleaned note: no addresses, no decompiler output, no generated names.

## Short answer

**Nothing, in every client read.** The handler reads one GINT5 and writes it into a field of the game-connection object. No code in 5.24r3, Linux 6.03 or Windows 6.03r7 reads that field back, so the value never reaches scripts, the GUI, options, or the outgoing stream. **[bin]**

```
{198 + 32} {GINT5 value}
```

- The message must be longer than 4 bytes (so at least the 5-byte GINT5). A shorter one is dropped. **[bin]**
- The client sends nothing in reply. **[bin]**
- The connection constructor zeroes the field, and the reset on disconnect zeroes it again. Those and the handler's write are the only touches. **[bin]**

## Builds

| Build | Handles 198 | Where the value goes | Read anywhere else |
|---|---|---|---|
| 5.00r7, 5.12 | no | (`../protocol/v5v6-windows-unpacked.md`) | |
| 5.24r3 | yes | a field of the connection object | no: full decompile searched, plus a raw scan of every load of the connection object for an access to that field |
| 5.24r4, 6.00 betas, 6.01r1 | yes | same handler shape | not searched |
| 6.03 (Linux) | yes | a field of the connection object | no: the only touches are the handler and the reset. A one-line getter for the field exists but nothing calls it, and no pointer to it appears in any table |
| 6.03r7 (Windows) | yes | a field of the connection object | no direct reader found (`../protocol/v6x-clients.md#server--client-ids-601-603`) |

So 198 arrives with the early-2010 5.24 / 6.00-beta builds (`../protocol/v5v6-windows-unpacked.md`) and, up to 6.03, is stored and ignored. **[bin]**

## What it is probably for **[inf]**

- The name and the shape (one 32-bit-range number, stored on the connection) fit a bit-field of server feature flags that the client keeps for later. The unused getter in the Linux build suggests code was meant to ask for it.
- No string in 5.24r3 or 6.03 names a script variable or option tied to it, so the value is not exposed to GS2 in these builds.
- Whether a client after 6.03 reads it is **not known**: no later client is in these notes.

## For a server sending it

- Harmless to 5.24 and later clients; ignored by everything before 5.24 (default arm).
- Any value is accepted. Sending 0 is equivalent to not sending it, since the field starts at 0.

## Correction to an earlier lead

A first pass of this work took a 5.24r3 getter that returns a server-supplied time instead of the local clock to be the 198 value. It is not: that getter is fed by `PLO_NEWWORLDTIME` (42, GINT4) and drives the script `timevar`. It has nothing to do with 198.

## Side answer: when did `PLO_SETACTIVELEVEL` (156) arrive?

**2.01 (March 2001).** 2.00, 2.00 rev1, NewMain 24/26 and every 1.x build have no arm for 156; 2.01 and 2.01 rev1 handle it, and every later client in these notes does too. 2.03 reworked the handler into a much shorter one. **[bin]** (`decomp-findings-2026-10-24-c/04-plo-server-to-client.md`, `../version-profiles/plo-handled-ids-by-build.tsv`)

Before 2.01 the "active level" is simply the last level the server sent; see `npcaction.md` step 6 for one place this matters.
