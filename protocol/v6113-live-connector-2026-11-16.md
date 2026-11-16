# Windows 6.113 live connector check (2026-11-16)

Date: 2026-11-16. Lab check of a stock Windows 6.1.1.3 client against the
live connector / Login path. Captures, caches, keys, hosts and digests stay
off git. Tags: **[lab]** this run · **[cap]** prior Windows 6.113 captures ·
**[bin]** existing connector / unpack notes.

Companion status hub: [`v6113-status.md`](v6113-status.md). Fetch and script
order: [`connector-script.md`](connector-script.md).

## What this settles

| Claim | Status |
| --- | --- |
| A stock Windows 6.113 client still obtains a connector script before the Login UI loads | Settled **[lab]** (2026-11-16) |
| That script is written into the client cache as an encrypted `GRESCR01` body under the start-script name `StartScript_Connector` | Settled **[lab]** |
| After that cache write, Login chrome (backgrounds, logo, heads) downloads and a Login session can open | Settled **[lab]** (partial; no account login completed) |
| Compiled-in Login hostnames are **not** the HTTP `conf.gs` connector host | Settled **[lab]** (HTTP `/conf.gs` to those names failed) |
| The public site path `/conf.gs` is not a connector script body | Settled **[lab]** (redirect only; no script) |
| Guessed connector DNS labels under the public site domain do not resolve | Settled **[lab]** (NXDOMAIN) |
| Some 6.113 install trees carry an on-disk license-style host list | Settled for one lab tree **[lab]** (see below) |

This does **not** close the loopback `conf.gs` harness, login-step argument
order, `?p=` binding, or post-decrypt Login reply contract. Those stay open
in `v6113-status.md`.

## Live path (behaviour only)

1. Stock launcher + 6.113 game client started on the lab Windows host.
2. Before the Login GUI finished loading, the client wrote
   `StartScript_Connector` into its script cache. The file magic is
   `GRESCR01` (encrypted body; not plaintext GS). A short companion
   `StartScript_MessageBoxDialog` cache appeared beside it. **[lab]**
3. Console progress then showed Login UI asset downloads. A TCP session to
   the Login service (`HOST:PORT` form) was established. **[lab]**
4. Full account login was **not** completed (no credentials in the lab env;
   no GUI automation). Handshake field dumps (`?p=`, encryption-out args,
   prop bodies) were **not** extracted this pass. **[lab]**

The run is enough to say the connector path is still served and still gates
Login UI for this build. It is not a full wire decode of the post-hello
RC4 stream (already settled elsewhere: `v611-outgoing-cipher.md`). A same-day
official `HOST:14900` handshake reconfirm (clear hello, RC4-from-287, no keys)
is separate: `v6113-live-handshake-2026-11-16.md`.

## What is not the connector

Probes that failed or redirected, and must not be mistaken for `conf.gs`:

- HTTP `/conf.gs` aimed at the **compiled-in Login hostnames** the launcher
  strings still name → connection failed. Those names are Login/game hops,
  not the connector HTTP endpoint. **[lab][bin]**
- HTTP `/conf.gs` on the public site host → redirect only; no connector
  script body. **[lab]**
- Guessed first labels (`con` / `con2` / `connector` style) under that site
  domain → NXDOMAIN. The real connector hostname remains the scrambled /
  binary-held name described in the Mac/Windows connector notes; this run
  did not need to print it. **[lab][bin]**

## License-style file on one tree

The 6.113 status table previously treated late 6.x as “no `license.graal`”
(hosts compiled in / connector path). One lab 6.113 tree still carries an
on-disk license-style host list: **eight lines**, hosts and ports only, no
account line. **[lab]**

That does not replace `conf.gs`. The live run still wrote the connector
cache before Login UI. Treat “no license file” as **not universal** across
every 6.113 tree; treat the connector fetch as the gate for `GNP1905C`.
**[lab][inf]**

## Loopback harness (still open)

A loopback connector responder that a stock or redirected 6.113 accepts was
**not** started this pass. Seeding it needs either a lab-held clear
connector reply body or a decrypt of the `GRESCR01` `StartScript_Connector`
cache with session script keys. Packet capture on the lab host was not
available without elevation. **[lab]**

Until that harness exists, keep using:

- Mac 6.111 offline connector replay for cipher / id-table facts
  (`v611-outgoing-cipher.md`, `v611-id-tables.md`);
- this note only for “Windows 6.113 still hits a live connector before
  Login”.

## Non-goals / scrub

- No hosts, IPs, digests, key bytes, `?p=` values, account names or raw
  cache bodies in this note.
- No GLauncher decompile text; no third-party REA copy.
- No claim that Gen5 `G3D0311C` labs stand in for this path
  (`v6113-status.md`).
