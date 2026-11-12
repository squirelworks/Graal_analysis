# The 6.11 / 7.x connector script: what is known, in one place

Date: 2026-11-12. This note covers #397. Most of it adds no new reading: it puts the facts already spread across the protocol notes into the order that a reproduction client, or a lab `conf.gs` responder, needs them. Every line keeps the tag and the source of the note it comes from. No host names, key bytes, reply bodies or request blobs are given.

From 6.11 on, the desktop clients and the 7.x Worlds clients do not hold their own login. They fetch a signed connector reply, and the script inside it sets the framing, the cipher and the id tables, connects, and sends the login.

## 1. Fetching the reply

- The client tries **HTTPS to the connector host first**. If that fails, it requests `conf.gs` over plain HTTP. If both fail, it tries a second host whose first label differs (`con` → `con2` on 6.11, `…ios` → `…ios2` on 7.x). Each step is retried. **[bin][cap]** (`v6x-clients.md#connector-request`, `v6x-clients.md#the-connector-request-in-a-lab-run`, `v7-connector-live-20261111.md` §2)
- The query is `?p=` followed by a comma-joined `g=…,p=…,v=…,b=…`. That string is DES-ECB encrypted under a compiled-in key, encoded with the client's own base64 alphabet, then URL-encoded. **[bin]** (`v6x-clients.md`)
- The `User-Agent` is `Graal/<version>`: `Graal/6.111` on the Mac 6.11r1, and `Graal/6.76` or `Graal/6.77` on 7.x (the split is at build 613). **[cap][lab][bin]** (`v6x-clients.md`, `v7-connector-live-20261111.md` §1)
- HTTPS checks the server against a certificate bundle compiled into the client, so a lab certificate is expected to fail. **[bin]** (`v6x-clients.md`)

## 2. The reply container

| Field | Size | What |
| --- | --- | --- |
| Marker | 4 | `00 00 01 00` |
| Signature | 256 | RSA-2048, checked against a public key compiled into the client |
| Inner length | 4 | `00 00` plus a 16-bit length |
| Payload | that length | the encrypted script; different on every request |

**[lab]** (`v7-connector-live-20261111.md` §3). The same container is used by 6.11 and 7.x. The signature is over the bare 32-byte SHA-256 fingerprint, with no DigestInfo label. **[lab]** (`v6-login-token-explained.md`, method notes)

- The client checks the signature **before** it decrypts the script, and a reply that fails is never run. **[lab]** (`v6-login-token-explained.md`)
- A reply verifies only for the per-launch `?p=` request it was signed for. A reply captured for one launch is rejected by a fresh launch. **[lab]** (`v7-connector-live-20261111.md` §3)
- What the per-launch value binds, beyond "the request", is not known (see Open).

## 3. Before the script runs

The reply becomes a script object named `StartScript_Connector`. Before its `onCreated` runs, the client sets `scriptip`, `scriptsslcipher`, `scriptsslsubject` and `scriptsslissuer` on it. **[bin]** (`v6x-clients.md#connector-reply`) Until a script calls `setprotocol`, the connection uses classic gen-5 framing, and until it passes id pairs, no incoming wire id has a handler. **[bin]** (`v6x-clients.md`, `v6113-handlers.md`, `v6-repro-facts.md`)

## 4. The script's steps, in order

From the decrypted 6.111 script, replayed in a lab Mac VM. The order comes from the script's string table; argument order was not read from the bytecode. **[lab]** (`v611-outgoing-cipher.md#the-switch`, `v6-login-token-explained.md`)

1. `setProtocol("EILLLT")`: a six-byte header. `E` compression, `I` counter, `LLL` big-endian length of header plus body, `T` raw id (no +32). (`v611-outgoing-cipher.md`, `v6-repro-facts.md` for the fill order)
2. `sendRaw("GNP1905C")`: the token, with no header. The token is a literal in the script, not in the client. (`v6-login-token-explained.md`, `v6113-hello.md`)
3. `flush`.
4. `setEncryptionParseKey`, with cipher type `"RC4"` and a key from `generate16ByteKey()`.
5. `rsa_encrypt` of that key, using a 2048-bit public key carried in the script.
6. `sendData`: an outer `0xfd` packet (zlib) that wraps an inner `0xfc` packet with the 256-byte wrapped key. Both are sent in the clear, and they end at stream offset 287. (`v611-outgoing-cipher.md`)
7. `setEncryptionOut`: everything after that is plain RC4 with the session key, headers included. (`v611-outgoing-cipher.md#the-cipher`)

Steps the script must also take, from the method surface, but whose order and arguments were not read: `connecttogameserver`, `setoutdatahandlers` / `setindatahandlers`, `setloginaccount`, `getpassword`, and the login `senddata`. **[bin][inf]** (`v6x-clients.md#what-the-script-controls`)

## 4a. The 6.113 Windows script, from a live run **[lab]**

An owner-authorised live 6.113 session on a Windows PC was read with read-only process-memory reads (no debugger, nothing injected), and its port-14900 traffic was captured. The connector script `StartScript_Connector` was resident in memory, so its string table could be read. The numeric arguments (the id lists) are bytecode operands, not strings, and were not recovered.

- **Same framing and hello as 6.111.** The script holds `setProtocol` with `EILLLT`, `sendRaw` with `GNP1905C`, `setEncryptionParseKey`, `setEncryptionOut`, `rsa_encrypt` and `generate16ByteKey`. That matches the 6.111 replay above, so the 6.11 Mac and 6.113 Windows scripts share the handshake.
- **Two protocols in one script.** It has `setDataHandlersOldProtocol` and `setDataHandlersNewProtocol`, a `usenewprotocol` setting, and `sendLoginNewProtocol` next to `sendPasswordAndIDs`. So the script can log in to a server either way, and it picks per server. The legacy `G3D2204D`, `G3D2304D`, `G3D2404D` and `G3D2504D` tokens are also in the table, which fits the old path.
- **Login settings the script reads:** `loginservers`, `logintype`, `usenewprotocol`, `ciphertype` / `ciphertypeint`, `cipherkey`, `initvector`, `keydata`, `passcode`, `reconnections`, `clientversion` and `idlist`. It also uses `des_decrypt` and `base64decode`.
- **Account calls:** `getLoginAccountName`, `setLoginAccount`, `getPassword`, `getplatform`.
- **Events:** `onCreated`, `onServerLogin`, `onCannotConnect`, `onServerListerConnect`. The game-server join is not run from `onCreated`. `connectToGameServer` is reached from the server-list script's Start path (`doLogin`), after the login dialog. A `graal://` launch link still stops at that dialog.
- **No incoming-cipher name.** As on 6.111, the table has no `setEncryptionIn` or `tclient_setencryptionin` name, yet the server stream is encrypted too (section 4b). How the client keys its incoming direction is not shown by the script's strings.

## 4b. Both directions on the wire (6.113) **[cap]**

| Direction | Clear part | Then |
| --- | --- | --- |
| Client → server | `GNP1905C` (8 bytes), then one `0xfd` frame of 279 bytes: zlib, wrapping the 262-byte inner `0xfc` packet. That ends at offset 287. | Encrypted from 287 |
| Server → client | One `0xfd` frame (`E` 1, `I` 2), 290 bytes in this session. That ends at offset 290. | Encrypted from 290 |

The server side answers the incoming-direction question in #396 halfway: **the server also sends exactly one clear `0xfd` frame and then switches to ciphertext.** Its frame length varies by session (an earlier 6.113 capture had a length field of 289). Whether the server's stream uses the client's RC4 session key or a key of its own is still open. The session key was not recovered in this run, because it is held in a script variable and no debugger was used.

## 5. The id tables (mechanism only)

- **Outgoing:** `setoutdatahandlers` loads a 256-entry table from internal message number to wire id. `0xFE` routes a message to a script event instead of the wire. **[bin]** (`v6x-clients.md`, `v6113-pli.md`)
- **Incoming:** `setindatahandlers` takes pairs of (wire id, handler):
  - a handler below 95 is a native function;
  - 255 clears the id;
  - 254 means "do not call";
  - 253 and 252 store special ids;
  - 95 and above, apart from those four values, is skipped.

  `clearindatahandlers` zeros all 256 slots. **[bin]** (`v6113-handlers.md`, `v6113-plo.md`)
- **Encryption ids:** `0xfc` and `0xfd` match gs2lib's `PLI_SET_ENC_KEY` (252) and `PLI_BUNDLE` (253). **[srv][inf]** (`v611-outgoing-cipher.md`)

The actual pair lists that the production script passes are **not** in any note. Without them, no table of gs2lib names against 6.1x/7.x wire ids can be written (see Open).

## 6. Failure paths

- No connector reply: the client shows "Couldn't connect to the server / Connecting to the login server...". **[cap]** (`v6x-clients.md`)
- No connector script loaded: the built-in `StartScript_Fail` runs instead. **[bin]** (`v6x-clients.md`)
- A reply signed for another launch: only the built-in skeleton and the fail path are in memory, with the string `Problem setting up the networking`. **[lab]** (`v7-connector-live-20261111.md` §3)

## 7. By build

| | 6.11 Mac (6.111) | 6.113 Windows | 7.x Worlds (6.76 / 6.77) |
| --- | --- | --- | --- |
| Request order and container | HTTPS → `conf.gs`; same container **[cap][lab]** | same design **[bin][cap]** | same design and container **[lab]** |
| Script read | yes, decrypted in a lab replay **[lab]** | string table read from memory in a live run; id lists not recovered **[lab]** | no; anti-tamper ends inline-hook traces **[lab]** |
| Token | `GNP1905C` from the script | `GNP1905C` from the script and on the wire **[lab][cap]** | not established |

None of this exists in 6.01 or 6.03 (no connector, no RC4/AES, no script-set id tables). **[bin]** (`v6x-clients.md`)

## Open

- [ ] The pair lists that `setoutdatahandlers` and `setindatahandlers` receive. This needs the decrypted script's bytecode (owner-held lab record) or a lab memory read. It blocks the id table for #378.
- [ ] The arguments and order of the login steps (`connectToGameServer`, `setLoginAccount`, `getPassword`, `sendLoginNewProtocol` / `sendPasswordAndIDs`). The names are confirmed for 6.113 (section 4a); their arguments are not.
- [ ] What the per-launch `?p=` value binds in the signature.
- [ ] Whether the 7.x script differs from the 6.11 one (token, template, cipher). This needs a 7.x reply decrypted for its own launch.
- [x] ~~Does the server's stream follow the same clear-then-cipher pattern?~~ Yes: one clear `0xfd` frame, then ciphertext (section 4b).
- [ ] Which key the server's stream uses, and how the client sets it with no `setEncryptionIn` in the script (also open in #396).
- [ ] Old versus new protocol: what the `OldProtocol` handler set is, and which servers set `usenewprotocol`.
