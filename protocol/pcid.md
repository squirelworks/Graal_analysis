# PCID: where the "PC id" comes from

Date: 2026-11-13. Static reads of held clients, the existing login captures, the GServer-v2 source and the gs2lib enum table. No lab run for this note, and no contact with public servers.

**Short answer.** A PCID is a number the **listserver** hands to a game server for each login. The game server does not compute it. The client does not compute it either: the client sends a comma list of machine fields after its password, the game server forwards that list unchanged to the listserver, and the listserver answers with a decimal PCID. How the official listserver turns the fields into that number is not in any binary or source we hold. **[src][bin][inf]**

Tags: **[bin]** static read of a held binary, **[cap]** a held capture, **[lab]** a lab run, **[src]** GServer-v2 or gs2lib source, **[inf]** inference, **[doc]** a statement from outside our evidence.

## What the client sends

The machine fields arrive after the password in the first login message. Field layouts per build are in [`v4x-clients.md`](v4x-clients.md#login-packet), [`v5x-clients.md`](v5x-clients.md#login), [`v5v6-windows-unpacked.md`](v5v6-windows-unpacked.md#login-message), [`v6x-clients.md`](v6x-clients.md#login-message-601-and-603) and manual §2.3.5. In summary:

| Builds | Fields after the password | Source |
| --- | --- | --- |
| 1.x, 2.x, 3.x | nothing; no machine fields | [bin] |
| Windows 4.20r8, 5.00r7 | `win`, MD5 of the product id, MD5 of the adapter MAC, MD5 of the `C:\` volume serial | [bin] |
| Windows 5.12 to 6.03r7 | as above, plus a fifth field, the quoted Windows version | [bin][cap] |
| Windows 6.03r7 on Windows 10 | `win`, an **empty quoted string** in the product-id slot, two MD5 hex values, `"6.2 9200 "` | [cap] (`login-session-observed.md`) |
| Mac 4.20r6 | `mac`, MD5 of the 6 raw hardware-address bytes (not their hex text), a hash of 4 bytes of `stat("/etc")`, empty | [bin][lab] (client-harness 2026-11-13) |
| Linux 6.01r1, 6.03r7 | `linux`, MD5 of the `eth0` MAC, MD5 of the `/etc` inode number, empty, kernel release and version | [bin] |
| 6.11 and later | built by the server's connector script, not by the client; unmeasured | [bin] (`connector-script.md`) |

Points that matter for PCID:

- Every hardware value is an MD5 digest sent as 32 hex digits. The raw MAC, serial or product id never leaves the client. Nothing on the server side can turn the digests back into the raw values. **[bin]**
- The fields are plain text inside the login message. A client, a proxy or a modified build can send any values it likes. They identify a machine only as far as the client is honest. **[bin][inf]**
- The OS-version field changes when Windows is updated, so it is a poor key for a stable id. **[inf]**
- Why 6.03r7 on Windows 10 leaves the product-id slot as `""` is not settled. A likely cause is a 32-bit program not finding the `DigitalProductId` value in its registry view, but this was not traced. **[inf]**
- Whether the Windows MAC hash is over the raw 6 bytes, as on the Mac, or over hex text is not pinned.

## Game server to listserver: `VERIACC2` and `ASSIGNPCID`

GServer-v2 added PC-id support on 2022-09-04 ("Support for pc-ids"). Its behaviour, read from the source: **[src]**

1. **The login parser keeps the machine list as one string.** After the account and password, everything to the end of the message is read as the "identity". The server logs it and takes only the first token (`win`, `mac`, `linux`) as the player's OS. It never splits, decodes or hashes the MD5 fields. (`server/src/TPlayer/TPlayer.cpp`, login parse.)
2. **It forwards the string to the listserver unchanged**, appended to `SVO_VERIACC2` (17): account, password, player id, player type, then a two-byte length and the identity string. (`TServerList::sendLoginPacketForPlayer`.)
3. **The listserver answers with `SVI_ASSIGNPCID` (30)**: GSHORT player id, GCHAR player type, then a GCHAR-length string holding the PCID in decimal. The game server parses it with `std::stoll` into a signed 64-bit `deviceId`. (`TServerList::msgSVI_ASSIGNPCID`; id 30 from gs2lib `IEnums.h`.)
4. **Ordering.** GServer-v2 drops `ASSIGNPCID` for a player who is already loaded. A player becomes loaded when the server sends the account after `SVI_VERIACC2` reports `SUCCESS`. So the listserver must send `ASSIGNPCID` **before** the `VERIACC2` reply. **[src][inf]**
5. **The PCID lives in memory only.** It is not written to the account file, and it is 0 for any player the listserver gave no PCID. **[src]**
6. **A non-numeric PCID string would make `std::stoll` throw**, so a listserver must send digits only. **[src][inf]**

What this shows: the decision to give a machine a PCID, and the value, belong to the listserver. That matches the community statement that the two hashes "don't get decoded, they're just used for generating your PCID". **[src][doc]**

## Where the PCID is used

| Place | What happens | Source |
| --- | --- | --- |
| RC (scripted RC of the 5.x/6.x era) | The RC command `/openaccess <account>` makes GServer-v2 send `PLO_SERVERTEXT` `GraalEngine,lister,ban,<account>,<pcid>` to the RC. The RC's scripted ban window opens for that account and that PC id. | [src] (`TPlayerRC.cpp`) |
| Listserver ban queries | GServer-v2's text-command list documents `lister getbanhistory <account>` and `lister getbanbyid <id>`, both answered by the listserver. Ban history is kept at the listserver, not on the game server. | [src] (`docs/graal_requesttext_sendtext_info.txt`) |
| Login server list | The 6.03r7 Login session's server-list weapon asks `getlockcomputer`. By its name this is the "lock account to this computer" option. What it compares was not seen. | [cap] (`login-session-observed.md`); [inf] |
| Game scripts | No GS2 variable or function exposing a PCID was found in our GS2 notes. | [bin] (absence) |
| 1999 to 2002 servers and RCs | The 1.25 and 1.27 GServers and RemoteControl 1.33 to 2.01 have no machine id. The RCs' ban window bans an account ("Local Ban of account", with a time and reason). | [bin] |

## Can a PCID be derived from the login fields?

Not from anything we hold.

- **Proven:** the PCID is a signed 64-bit decimal number from the listserver; the input it has available is the identity string (plus account, password and the connecting game server). **[src]**
- **Not proven:** which fields it uses, whether it is a hash or a lookup. An MD5 is 128 bits and the PCID is a 64-bit decimal, so it is not simply one of the sent digests. **[src][inf]**
- **Most likely (guess):** a row number from a listserver table of machines, found by matching the hardware hashes, with a new row when nothing matches. This fits a decimal 64-bit value, it fits "used for generating your PCID", and it lets a ban hold when only one of the hashes changes. A truncated hash of the fields would fit the number too. Only the official listserver, or a capture of its `ASSIGNPCID` replies for known inputs, would settle it. **[inf]**
- The official listserver is not held. The held `serverlist3` (an early 2000s ELF listserver) predates machine fields, and the held C# listserver rewrite only serves the client lobby. **[bin][src]**

Because of the AGENTS rules, settling this by sending crafted identity strings to the official listserver is out of scope.

## What a Seihai listserver should do

These are recommendations for the clean-room servers, written from the behaviour above.

1. **Keep the game server dumb.** It forwards the identity string in `VERIACC2` and stores whatever `ASSIGNPCID` returns. That keeps GServer-v2 and Seihai game servers interchangeable behind one listserver.
2. **Assign the PCID at the listserver**, and send `SVI_ASSIGNPCID` (30) before the `SVI_VERIACC2` reply. Send a decimal string that fits a signed 64-bit integer.
3. **Use a machines table, not a hash.** Split the identity on commas (quotes allowed), keep the platform and the hardware digests, and drop the OS-version text. Look up an existing machine that shares any hardware digest on the same platform; create one if none does. Use the row number as the PCID. Treat `""`, empty fields and the MD5 of an empty string as "missing", not as a match.
4. **Clients with no fields (1.x to 3.x, and any 6.11+ connector that sends none) get no PCID.** Send nothing, or send 0. Do not invent one from the IP address.
5. **Treat a PCID as a hint.** Clients can send any values, so a PCID ban stops casual repeat offenders only. Keep account and IP bans alongside it.
6. **Store digests only.** They are all the client sends; do not log the full identity string at normal log levels.

The lab listserver in `tools/lab-servers/listserver.py` logs the identity it receives and does not send `ASSIGNPCID` yet. Adding it there would let a lab GServer-v2 show PCIDs in the RC ban window.

## Open

- [ ] The official listserver's PCID rule (hash or lookup, which fields).
- [ ] Whether the Windows MAC digest is over raw bytes or hex text.
- [ ] Why the product-id slot is empty on 6.03r7 under Windows 10.
- [ ] What `getlockcomputer` compares.
- [ ] What 6.11+ connector scripts send as machine fields.
