# PCID: where the "PC id" comes from

Date: 2026-11-13, extended the same day with how each hash is computed. Static reads of held clients, the existing login captures, the GServer-v2 source and the gs2lib enum table. No lab run for this note, and no contact with public servers.

**Short answer.** A PCID is a number the **listserver** hands to a game server for each login. The game server does not compute it. The client does not compute it either: the client sends a comma list of machine fields after its password, the game server forwards that list unchanged to the listserver, and the listserver answers with a decimal PCID. How the official listserver turns the fields into that number is not in any binary or source we hold. **[src][bin][inf]**

Tags: **[bin]** static read of a held binary, **[cap]** a held capture, **[lab]** a lab run, **[src]** GServer-v2 or gs2lib source, **[inf]** inference, **[doc]** a statement from outside our evidence.

## What the client sends

The machine fields arrive after the password in the first login message, as one comma list. Earlier summaries are in [`v4x-clients.md`](v4x-clients.md#login-packet), [`v5x-clients.md`](v5x-clients.md#login), [`v5v6-windows-unpacked.md`](v5v6-windows-unpacked.md#login-message), [`v6x-clients.md`](v6x-clients.md#login-message-601-and-603) and manual §2.3.5. This section goes one level down: what each hash is computed over, and what makes it change. Builds read for it: the Windows 4.20 engine (with the 4.04r2 engine checked by strings), the unpacked Windows 6.03r7 (with 5.24r3 to 6.00r4 checked by strings), Mac 4.20r6 and Linux 6.03r7 x64. **[bin]**

### How every field is encoded

- **The hash.** Each hardware field is plain MD5 over the raw bytes listed below, written as 32 lowercase hex digits. There is no salt, no key and no mixing between fields. The same helper does this in every build read. **[bin]**
- **Missing values.** When the client cannot read a value it sends an empty field. It does not send the MD5 of nothing. **[bin]**
- **Quoting.** The list is joined with commas. A field is wrapped in double quotes when it is empty or holds a space, comma, quote or backslash. That is why an empty field shows as `""` and the OS-version field is always quoted. **[bin][cap]**
- **Field order.** Platform word, then fields 0 to 3 in that order. The 6.03r7 builder loops over four field numbers; field 3 is text, not a hash. **[bin]**

### Windows

| Field | 4.04r2 and 4.20 engine | 5.24r3 to 6.03r7 | Source |
| --- | --- | --- | --- |
| platform | `win` | `win` | [bin] |
| product id | MD5 of the binary `DigitalProductId` registry value (up to 512 bytes), read from `HKLM\Software\Microsoft\Windows\CurrentVersion` and, if that is empty, from `HKLM\Software\Microsoft\Windows NT\CurrentVersion` | the same two keys, each tried for `DigitalProductId` and then `DigitalProductId4`; the first non-empty value wins | [bin] |
| network | MD5 of the 6-byte node of a `UuidCreateSequential` UUID (`UuidCreate` if the sequential call is missing). On Windows 2000 and later this node is a network card's MAC | MD5 of the 6-byte hardware address of the **first adapter in `GetAdaptersInfo` order that has an IPv4 address** (an adapter whose address is all zeros is skipped). No UUID fallback on this path: with no such adapter the field is empty | [bin] |
| disk | MD5 of the 4-byte volume serial of `C:\` (little-endian, from `GetVolumeInformationA`) | the same | [bin] |
| OS version | none | `"<major>.<minor> <build> <service pack>"` from `GetVersionExA`; not hashed | [bin][cap] |

Notes on the Windows fields:

- **The product-id slot is often empty on 64-bit Windows.** The client opens the registry with plain read access and no 64-bit-view flag. A 32-bit program on 64-bit Windows therefore reads the redirected 32-bit view of `Windows NT\CurrentVersion`, where the product-id values are normally absent. This explains the `""` in the 6.03r7 capture on Windows 10. **[bin]** for the flag, **[cap]** for the empty field, **[inf]** for the cause. On a modern 64-bit PC, only two hardware fields carry anything.
- **The earlier claim that 5.24 and later hash a different product id from 5.12 needs a recheck.** In 6.03r7, `DigitalProductId` is tried before `DigitalProductId4` in each key. On any system where the first key is empty, the value hashed is the same `DigitalProductId` the 4.x engine hashes. **[bin]**
- **The network field follows whichever adapter has an address.** If the user switches between cable and Wi-Fi, or a VPN or virtual-machine adapter is listed first with an address, a 5.24+ client sends a different hash. If no adapter has an address, the field is empty. Windows can also give Wi-Fi a random hardware address per network. 4.x used the RPC UUID node instead, which does not depend on which link is up. **[bin][inf]**
- **The disk field changes when `C:` is formatted** (a Windows reinstall). It is the same on every PC restored from one disk image, and Wine reports its own made-up serial. **[inf]**
- **The OS-version field changes with Windows feature updates and service packs.** **[inf]**

### Mac (4.20r6)

| Field | Input | Source |
| --- | --- | --- |
| platform | `mac` | [bin] |
| network | MD5 of the 6 raw bytes of `IOMACAddress` on the Ethernet interface marked `IOPrimaryInterface` (the built-in port). Empty if there is none; an emulated card counted only once it was marked built-in | [bin][lab] |
| second | MD5 of 4 bytes taken from `stat("/etc")`, probably the inode number as on Linux | [bin][inf] |
| third | empty | [bin] |

### Linux (6.01r1, 6.03r7)

| Field | Input | Source |
| --- | --- | --- |
| platform | `linux` | [bin] |
| network | MD5 of the 6-byte hardware address the `SIOCGIFHWADDR` ioctl returns for the interface named **`eth0`** | [bin] |
| second | MD5 of the low 4 bytes of the `/etc` inode number | [bin] |
| third | empty | [bin] |
| OS version | `uname` release and version text; not hashed | [bin] |

- **The `eth0` result is not checked.** On systems that name their interfaces differently (most distributions since about 2015 use `enp…`, `wlp…`), the call fails, the buffer stays zeroed, and the client sends the MD5 of six zero bytes, `7319468847d7b1aee40dbf5dd963c999`. Every such machine sends that same value. **[bin][inf]**
- **The `/etc` inode changes on a reinstall** and is the same on machines installed from one image. **[inf]**

### What the hashes do and do not hide

- No server needs to decode them, and nothing does. **[src]**
- They are not secret, though. Each is an unsalted MD5 of a short input. A 4-byte volume serial or `/etc` inode can be recovered by trying all 2³² values, and a MAC by trying the 2²⁴ device numbers under each known vendor prefix. Store them as you would the raw values. **[inf]**
- Anyone can send any values. Clients and proxies that fake them (as our own lab tools do) are indistinguishable from real ones. **[bin][inf]**

### What this means for matching

| Field | Changes when | Shared by unrelated machines when | Weight |
| --- | --- | --- | --- |
| product id | Windows reinstalled or re-licensed | volume-licensed or cloned installs | medium; often empty on 64-bit Windows |
| network (4.x) | network card replaced | rarely | high |
| network (5.24+) | the active adapter changes, MAC randomisation, offline | rarely | medium: real but jumpy |
| network (Linux) | — | the interface is not named `eth0` (the six-zero-byte hash) | none when it is the six-zero-byte hash |
| disk / `/etc` inode | reinstall or format | restored from one image | high on one install |
| OS version | updates | almost always | none; do not match on it |

For a 2-of-3 rule this means:

1. **Count only fields that carry a value.** Treat an empty field, `""` and the six-zero-byte Linux hash as missing. They are not evidence.
2. **On modern 64-bit Windows, "3" is really 2.** With the product-id slot empty, 2-of-3 becomes "network and disk both match". The first adapter switch then breaks the match. Remember **every** network hash a machine has sent, not only the last one, so a disk match plus any earlier network hash still counts.
3. **Do not use the disk field alone to merge machines.** Imaged PCs share it. A disk-only match is a weak hint, not the same PCID.
4. **Keep platforms apart.** A `win` row never matches a `mac` or `linux` row.
5. **Key the table by platform plus field.** Field positions mean different things per platform.

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
3. **Use a machines table, not a hash.** Split the identity on commas (quotes allowed), keep the platform and the hardware digests, and drop the OS-version text. Match as in [What this means for matching](#what-this-means-for-matching); create a row when nothing matches. Use the row number as the PCID.
4. **Clients with no fields (1.x to 3.x, and any 6.11+ connector that sends none) get no PCID.** Send nothing, or send 0. Do not invent one from the IP address.
5. **Treat a PCID as a hint.** Clients can send any values, so a PCID ban stops casual repeat offenders only. Keep account and IP bans alongside it.
6. **Store digests only.** They are all the client sends; do not log the full identity string at normal log levels.

The lab listserver in `tools/lab-servers/listserver.py` logs the identity it receives and does not send `ASSIGNPCID` yet. Adding it there would let a lab GServer-v2 show PCIDs in the RC ban window.

## Open

- [ ] The official listserver's PCID rule (hash or lookup, which fields).
- [x] ~~Whether the Windows MAC digest is over raw bytes or hex text.~~ Raw bytes, in every build read.
- [ ] Why the product-id slot is empty on 6.03r7 under Windows 10: the 32-bit registry view is the likely cause (above); not yet confirmed in a lab.
- [ ] Whether 5.12 reads the product id the same way (its unpacked image did not show the strings).
- [ ] What `getlockcomputer` compares.
- [ ] What 6.11+ connector scripts send as machine fields.
