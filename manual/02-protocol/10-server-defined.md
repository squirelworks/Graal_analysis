<!-- manual: kind=reference status=draft -->
# 2.10 The 6.11 server-defined protocol

In 6.11 the client has no fixed protocol: a script fetched at login sets the framing, the cipher and both id tables. The classic generation-5 transport (→ §2.2) stays the default until that script switches it.

> Status: draft. The connector script itself was never captured (→ App. E#3), so the wire layout a 6.11 server uses is not in the notes.

## 2.10.1 The connector request

Mac 6.11 does not know how to log in on its own. It first fetches a connector from the official host. The rules below describe that request [bin] (protocol/v6x-clients.md#connector-request).

| Rule | Builds | Source |
| --- | --- | --- |
| On login the client sets the server name to `Login` and requests `con.png` and `con.gs` over HTTPS and `conf.gs` over plain HTTP from the official connector host (`<login-host>`) | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-request) |
| Each step is retried up to twice, using a second host whose first label differs; after three failures the client shows a warning | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-request) |
| The query is `?p=` + a comma-joined list `g=<client id>,p=mac,v=<version>,b=<build date and time>`, DES-ECB encrypted under a compiled-in key (whole 8-byte blocks only), base64-encoded with the client's own alphabet, then URL-encoded | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-request) |
| The HTTPS connection checks the server against a certificate bundle compiled into the client, and sends `User-Agent: Graal/<version>` | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-request) |

[cap] A lab run of the unmodified Mac 6.11r1 client in a Lion guest with no internet confirmed the order. It looked up the connector host and then the `con2` host, never the 4.x login or list hosts. It sent a TLS 1.2 ClientHello on 443 with no SNI, only the `signature_algorithms` extension and RSA-only suites including NULL and RC4. When that failed it sent `GET /conf.gs?p=…` over HTTP/1.0 on port 80 with `User-Agent: Graal/6.111`, and with no reply it showed "Couldn't connect to the server". A lab 6.11 client therefore needs a `conf.gs` responder that returns a connector script; it cannot connect to a gserver directly. [cap] (protocol/v6x-clients.md#the-connector-request-in-a-lab-run)

## 2.10.2 The connector script

The connector is a script, and it takes over the connection. The rules below say how it is loaded, what it is given, and what that leaves to the server [bin] (protocol/v6x-clients.md#connector-reply).

| Rule | Builds | Source |
| --- | --- | --- |
| The reply is loaded as the script object `StartScript_Connector`, and its `onCreated` runs; `scriptip`, `scriptsslcipher`, `scriptsslsubject` and `scriptsslissuer` are set first so the script can check where it came from | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-reply) |
| If no connector script loads, a built-in `StartScript_Fail` is used | 6.11 Mac | [bin] (protocol/v6x-clients.md#connector-reply) |
| The connection object gives the script `connecttogameserver`, `setprotocol`, `sendraw`, `senddata(id, data)`, `flush`, `setsslparameters`, `getsslcipher`/`subject`/`issuer`, `setencryptionparsekey`, `setencryptionout(type, key, iv)`, `getpassword`, `setloginaccount`, `requestbasefiles`, `setoutdatahandlers`, `clearindatahandlers`, `setindatahandlers`, `defaultinhandler(id, data)` and `tclient_setencryptionin(type, key, iv)` | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| The script builds and sends the login itself, so the token, ids, header layout and cipher of 6.11 live in the server's script, not the client | 6.11 Mac | [bin][inf] (protocol/v6x-clients.md#what-the-script-controls) |

## 2.10.3 Framing and encryption

The connector can redefine the frame and turn on a cipher. The rules below give the template language for the header and the ciphers on offer, and confirm that 6.01 and 6.03 have none of it [bin] (protocol/v6x-clients.md#what-the-script-controls).

| Rule | Builds | Source |
| --- | --- | --- |
| `setprotocol(template)` replaces the generation-5 framing with a header described by the template; the header is as long as the template | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| Each template letter marks a field and repeating it sets the width, at most 4 bytes, big-endian: `I` packet counter (starting at 1), `L` length, `T` packet id, `E` another field | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| In that mode the stream can be wrapped in RC4 or AES-CBC (blocks padded with `0xFF`), set separately per direction; other names turn it off; TLS is also possible | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| On the 6.11 login link each end sends one clear `0xfd` wrapping an inner `0xfc` with a 256-byte RSA block, then switches cipher. The client's block carries its own 16-byte RC4 key for client-to-server. The server's block carries the server-to-client cipher type, key and IV, wrapped to a private key that the connector script gives the client through `setEncryptionParseKey`. Until a valid server `0xfc` arrives, the client reads server data as plaintext | 6.11 Mac, 6.113 | [lab][cap] (protocol/connector-script.md#4c-the-servers-key-frame-each-direction-has-its-own-key-2026-11-13) |
| The 6.111 connector script's live id tables keep the classic gs2lib wire ids for almost every message both ways; the incoming set adds the special pairs 252 (key frame) and 253 (bundle) | 6.11 Mac | [lab] (protocol/v611-id-tables.md) |
| None of this exists in 6.01 or 6.03: no connector, no RC4 or AES, no script-set id tables | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| gs2lib names `PLI_SET_ENC_KEY` and `PLO_SET_ENC_KEY` (252, setting an AES or RC4 key and IV) and `PLI_BUNDLE` and `PLO_BUNDLE` (253, several messages in one); both are above 223, so they cannot be sent as one GCHAR | server library | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |

**Settled question, formerly E#18: Mobile clients' outer framing and cipher.** How the Android and iPhone clients frame, compress and cipher their stream was open. iPhone Classic+ 1.13 had been read; the Android native layer had not. A read of the Android Classic 1.8 engine library settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-l.md#what-this-settles).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | iPhone Classic+ 1.13 uses the desktop generation-5 frame: two-byte length (or `FF FF` and four bytes), compression byte, partial XOR with round-down for compressed bodies, and a type-5 login with a key byte in one zlib frame | [bin] (protocol/ios-classic-plus-113-framing.md) |
| Settled | Android Classic 1.8 has the 6.11 connection class: a classic mode by default, the `I`/`L`/`T`/`E` template mode, per-direction `RC4` or `AES`, TLS, and the `StartScript_Connector` start-up | [bin] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-connection-class) |
| Settled | Its classic mode is generation 5: the same frame header, types 2, 4 and 6 chosen by size (zlib from 48 bytes, bzip2 from 4,096), the partial XOR with seed `0x04A80B38` and min(ceil(n/4), 12) or min(floor(n/4), 4) groups, a key of UTC time AND 127 used both ways, and a first frame of fixed type 3 whose first message carries the key byte after its id | [bin] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-classic-mode-sending) |
| Settled | It receives with the same rules, splitting the body at line feeds; after a raw-length message the next message is a counted block. Outgoing, only ids 93 and 163 may carry line feeds (behind message 50); any other such message is refused, as on iPhone | [bin] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-classic-mode-receiving) |
| Verdict | Verified by read, as the best guess had it: Android uses the 6.1x connector front end and the desktop generation-5 frame until the connector script changes it | [bin][inf] (client-internals/static-reads-appendix-e-2026-11-20-l.md#what-this-settles) |
| Left over | What the official Android connector script selects; the other six Android packages; the template receive path in detail | [inf] (client-internals/static-reads-appendix-e-2026-11-20-l.md#not-covered) |

## 2.10.4 Id tables

The connector also sets which wire id means what, in both directions. The rules below describe the two tables and the native handlers they point to [bin] (protocol/v6x-clients.md#what-the-script-controls).

| Rule | Builds | Source |
| --- | --- | --- |
| `setoutdatahandlers` loads a 256-entry table from internal message number to wire id; `0xFE` sends the message to a script event instead of the wire | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| `setindatahandlers` takes (wire id, handler) pairs; a handler below `0x5F` is one of 95 native handlers, `0xFE` sends the packet to the script, `0xFF` ignores it, and `0xFC`/`0xFD` set two special ids | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| The native handlers are also exposed to script by name, about 90 `tclient_*` functions, from `tclient_setplayerprops` and `tclient_setlevelboard` to `tclient_setghostsnear` and `tclient_setpackageend` | 6.11 Mac | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| Slot 54 and slots above 56 have no event; the login and language messages are sent by the script itself; the slot order is not the wire order, so a 6.11 server must send the table | 6.11 Mac | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |

The named send slots, each with the event 6.11 raises when its slot holds `0xFE`:

| Slot | Event | Slot | Event | Slot | Event | Source |
| ---: | --- | ---: | --- | ---: | --- | --- |
| 0 | `onSendWantWeaponScript` | 19 | `onSendTakeExtra` | 38 | `onSendLevelWarp` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 1 | `onSendWantClassScript` | 20 | `onSendRemoveExtra` | 39 | `onSendLevelWarpModtime` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 2 | `onSendWantGaniScript` | 21 | `onSendOpenChest` | 40 | `onSendDownloadFile` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 3 | `onSendToAllChat` | 22 | `onSendShot` | 41 | `onSendBoardModify` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 4 | `onSendIsPKer` | 23 | `onSendBaddyProperties` | 42 | `onSendBoardModify2` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 5 | `onSendCarryThrown` | 24 | `onSendBaddyHurt` | 43 | `onSendPreloadLevel` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 6 | `onSendAddHorse` | 25 | `onSendWeaponImage` | 44 | `onSendPlayerProperties` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 7 | `onSendDelHorse` | 26 | `onSendRCChat` | 45 | `onSendNPCProperties` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 8 | `onSendAddBomb` | 27 | `onSendRequestText` | 46 | `onSendFlag` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 9 | `onSendDelBomb` | 28 | `onSendSetText` | 47 | `onSendUnsetFlag` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 10 | `onSendServerWarp` | 29 | `onSendFileDeletion` | 48 | `onSendProjectile` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 11 | `onSendTriggerAction` | 30 | `onSendFolderDeletion` | 49 | `onSendUpdatePackage` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 12 | `onSendFireSpying` | 31 | `onSendFileRename` | 50 | `onSendPrivateMessage` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 13 | `onSendExplosion` | 32 | `onSendFilesMove` | 51 | `onSendUploadStart` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 14 | `onSendWeaponHit` | 33 | `onSendHaveWindow` | 52 | `onSendSaveFile` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 15 | `onSendPlayerHurt` | 34 | `onSendEnterLevel` | 53 | `onSendUploadEnd` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 16 | `onSendDeleteNPC` | 35 | `onSendWantImage` | 55 | `onSendPingAnswer` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 17 | `onSendDeleteWeapon` | 36 | `onSendImageUpdate` | 56 | `onSendWindowList` | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |
| 18 | `onSendExtra` | 37 | `onSendImageUpdateCRC` | | | [bin] (protocol/v6x-clients.md#the-611-named-send-slots) |

## 2.10.5 The Windows 6.1.1.3 hello

Unpacked Windows 6.1.1.3 has the same script methods. The port 14900 capture's first bytes are the clear token `GNP1905C` and then a six-byte header (→ §1.8.7).

| Rule | Builds | Source |
| --- | --- | --- |
| `GNP1905C` is not a stored string, scrambled or clear, and `graalversion` (the number 6.113) is not turned into the digits `1905`. How those digits are chosen was not found | 6.1.1.3 | [bin] (protocol/v6113-hello.md#the-eight-characters) |
| The token comes from the server: a captured, RSA-signed connector script calls `setProtocol("EILLLT")` and then `sendRaw("GNP1905C")`, so the client sends the script's literal string and computes nothing | 6.111 Mac, 6.113 Windows | [lab] (protocol/v6-login-token-explained.md) |
| `sendraw` appends the caller's bytes with no packet id and no header, which is the path that can write those eight bytes | 6.1.1.3 | [bin] (protocol/v6113-hello.md#the-eight-characters) |
| `setprotocol` writes an `I`/`L`/`T`/`E` header. `L` is the header length plus the body length. `E` 1 is zlib and `E` 2 is bzip2 at block size 5. The template is not in the image | 6.1.1.3 | [bin] (protocol/v6113-hello.md#the-six-bytes-after-the-token) |
| A 6-byte header plus the capture's 273-byte zlib member is 279, and `01 17` sits in the captured header. The cipher after that member was not found | 6.1.1.3 | [bin][cap] (protocol/v6113-hello.md#what-the-cipher-is) |
| The clear prefix ends at stream offset 287, after the first `EILLLT` packet (id 0xfd, wrapping an inner id 0xfc with a 256-byte body). From there the client's stream, headers included, is plain RC4 with a 16-byte key made per session; no IV is used | 6.111 Mac, 6.113 Windows | [lab][cap] (protocol/v611-outgoing-cipher.md) |
| Unpacked 6.0.3.7 stores `g3d0311c`, upper-cases it, and sends it as id 5. 6.1.1.3 has no such string | 6.0.3.7 and 6.1.1.3 | [bin] (protocol/v6113-hello.md#against-unpacked-6037) |

## 2.10.6 Unpacked Windows 6.1.1.3

The unpacked Windows image still contains the generation-5 LCG: seed `0x04A80B38`, step times `0x08088405` plus 1. It has no compiled-in `G3D` or `GNP` token. Each outgoing sender compares its own slot with `0xFE` and then calls a script event; the Mac slot numbers in the table above are not the order of the names in this image. `onSendNPCProperties` is the one Mac event name this image does not have. `StartScript_Connector`, `StartScript_Fail` and the three `scriptssl*` fields are present. `setprotocol`, `setindatahandlers` and `con.gs` are not plaintext strings. [bin] (protocol/unpacked-6113-wire.md#generation-5-cipher); [bin] (protocol/unpacked-6113-wire.md#script-send-slots); [bin] (protocol/unpacked-6113-wire.md#connector-names)

### 2.10.6.1 Header fill order, the id-50 prefix and the script events

The rows give what the unpacked 6.0.3.7 and 6.1.1.3 listings show beyond §2.10.5. Nothing was run [bin] (protocol/v6-repro-facts.md#field-order-chat-arguments-and-bind-events-in-unpacked-6x).

| Rule | Builds | Source |
| --- | --- | --- |
| `setprotocol` stores the template length as the header length and finds `I`, `L`, `T` and `E`; a field's width is the letter's repeat count capped at 4, big-endian; other template bytes stay zero; a numbered send is refused until both `L` and `T` were found | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#how-a-setprotocol-header-is-filled) |
| On a numbered send the fields are written as `T` (id), then `I` (a counter from 1, +1 per send) when present, then `E` (zlib above 48 bytes, bzip2 at block size 5 above 4096), then `L` (header plus compressed body); if the compressor returns nothing, `E` is rewritten as 0 and the original body goes out | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#how-a-setprotocol-header-is-filled) |
| `sendraw` is the send with id −1: no header, id or counter; `senddata` is the numbered send | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#how-a-setprotocol-header-is-filled) |
| On the generation-5 framer, a send of id 93 or 163 is preceded by id 50 whose body is a three-byte length (original body + 2, capped at 3670015, seven-bit groups + 32); the packet then goes as id + 32, body and newline, skipping the newline refusal | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#ids-93-and-163-on-the-generation-5-path) |
| Any other generation-5 send holding a newline is refused with "Illegal characters in the outgoing data"; a buffer reaching 4096 bytes is flushed; 6.0.3.7 has the same refusal and exemption but no id-50 prefix that could be found | 6.1.1.3, 6.0.3.7 | [bin] (protocol/v6-repro-facts.md#ids-93-and-163-on-the-generation-5-path) |
| `onToall` is registered with parameters `o`, `s`; its feeder reads a two-byte player id ((b0 − 32) × 128 + (b1 − 32)), a third byte − 32 as the text length, and the text from the fourth byte; bodies of two bytes or fewer push nothing; no caller and no PLO id were found | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#what-ontoall-is-given) |
| The port-binding method logs "Binding of port " and opens no socket when its allow check fails; success raises `onBind`, failure `onBindFailed`, both with no parameters; `onReceiveUDPData` takes `s`, `s`, `i` (data, sender ip, …) | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#bind-events) |
| Before the connector runs, the client looks up `StartScript_Connector`, else `StartScript_Fail`; if `onCreated` exists and the SSL argument is set it writes `scriptip`, `scriptsslcipher`, `scriptsslsubject` and `scriptsslissuer`, then runs the script | 6.1.1.3 | [bin] (protocol/v6-repro-facts.md#before-the-connector-script-runs) |

## 2.10.7 v7 Worlds: the same connector

The Unity-hosted Worlds clients (→ §1.8.10) use the 6.11 connector design unchanged. The rules below come from a lab run of build 614 in a Windows guest with every name lookup answered locally, plus the engine's export inventory [lab][bin] (protocol/v7-connector-live-20261111.md).

| Rule | Builds | Source |
| --- | --- | --- |
| Start-up order: an unrelated local probe, then TLS to the Worlds connector host on 443 with the host as SNI, then on TLS failure a plain-HTTP `GET /conf.gs?p=<blob> HTTP/1.0` with `User-Agent: Graal/6.77` and `Connection: Keep-Alive`, then the same request to a second host whose first label differs | 614 | [lab] (protocol/v7-connector-live-20261111.md#2-connector-request-order-lab) |
| The `?p=` blob has the 6.11 shape (→ §2.10.1); its compiled-in key was not recovered | 614 | [doc] (protocol/v7-connector-live-20261111.md#2-connector-request-order-lab) |
| Reply container: a 4-byte marker `00 00 01 00`, a 256-byte RSA-2048 block, a 4-byte inner length, then a high-entropy payload that differs on every request; `conf.gs`, `con.gs` and `con.png` return the same container; it is byte-for-byte the 6.11 Mac container from the same server banner | 614, 6.11 Mac | [lab] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab) |
| The RSA block is a signature the client verifies against a public key baked into it; the engine exports both AES-CBC and RC4 and selects between them for the payload | 548–71243 | [bin] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab) |
| A genuine reply verifies only for the per-launch `?p=` request it was signed for: replayed to the same request it is accepted (6.11 Mac), served to a fresh launch it is rejected and the client stays on its built-in skeleton and fail path | 614; 6.11 Mac | [lab][inf] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab) |
| Inline hooks on the engine's own exports make the process exit about 15 s into start-up; a read-only memory scan is tolerated | 614 | [lab] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab) |
| A stock v7 client cannot be brought online against a lab server, because a lab responder cannot sign a reply the client accepts; the routes are a client with a replaced public key, or a reproduction client that speaks the post-connector protocol directly | 548–71243 | [lab][inf] (protocol/v7-connector-live-20261111.md#4-online-play-reach-labinf) |
| The plaintext connector script, the game host/port it names and the login it builds | all | unmeasured → App. E#616 |

## 2.10.8 Windows 6.1.1.3 in a loopback lab

The unmodified packed Windows 6.1.1.3 ran in a lab VM that could reach only loopback forwards; its state was read from host-side memory snapshots. The rules below are what that run showed about getting it past login [lab] (protocol/v6113-login-lab-method.md#there-are-two-gates-not-one).

| Rule | Builds | Source |
| --- | --- | --- |
| Start-up has two gates that fail independently: first a classic login-and-list step ("Connecting to the login server…"), then, for the game server, the signed connector script that supplies the token and sets up RC4. With the login host unreachable the client never reaches the connector | 6.1.1.3 | [lab][bin] (protocol/v6113-login-lab-method.md#there-are-two-gates-not-one) |
| The `conf.gs?p=` request was byte-identical across two fresh launches: it binds nothing per launch, unlike the v7 request (→ §2.10.7) | 6.1.1.3 | [lab] (protocol/v6113-login-lab-method.md#the-connector-request-is-deterministic-across-launches) |
| In a launch where no connector reply was accepted, the client's memory held no copy of the login token, `setprotocol` or the `EILLLT` template; the client does not hold those words until the script runs | 6.1.1.3 | [lab] (protocol/v6113-login-lab-method.md#the-token-and-framing-are-not-in-the-client-at-all--shown-from-the-other-side) |
| A stock client cannot be given a forged reply, since it checks the signature against a compiled-in public key before decrypting; a genuine reply is not blocked at the request level on later launches of the same build, unless the script itself carries a short-lived value | 6.1.1.3 | [bin][cap][inf] (protocol/v6113-login-lab-method.md#replay-forge-and-the-only-lab-bypass) |
| The planned lab path for a stock client was to make it trust a lab key, by swapping the public modulus in memory after unpacking and serving a lab-signed script on loopback | 6.1.1.3 | [bin][inf] (protocol/v6113-login-lab-method.md#replay-forge-and-the-only-lab-bypass) |
| That swap does not work: the protector virtualizes the signature check and consumes the modulus inline, so a swapped modulus in memory leaves a lab-signed reply rejected | 6.1.1.3 | [lab] (protocol/v6113-login-lab-2026-11-19.md#1-the-stock-client-trust-anchor-swap-does-not-flip-the-verdict-lab) |
| A second attempt reversed the at-rest obfuscation of the key blob (a deterministic rolling XOR with a one-bit-rotating key) and crafted a blob that the client's own decrypt turned into the lab key; the readable key region then held the lab modulus, but the signature still failed and the script handler was never reached, so that region is a decoy and the verify uses a copy made inside the protector | 6.1.1.3 | [lab] (protocol/conf-gs-fuzzing.md#the-key-patch-attempted-and-why-it-is-a-no-go-on-the-real-binary) |
| The client's house cipher is DES-ECB, the same primitive as the `GRESCR01` cache (→ §3.8.10); none of its readable DES entry points is on the connector-reply path, so the reply's payload decryption is also inside the protector | 6.1.1.3 | [bin][lab] (protocol/conf-gs-fuzzing.md#the-confgs-payload-cipher-also-behind-the-vm-wall) |
| The faithful 6.1.1.3 token `GNP1905C` is not in the open-source server's version catalogue, so a lab server cannot yet accept that token as sent; the token reaches the wire only from the connector script's `sendRaw` | 6.1.1.3; server | [lab][srv] (protocol/v6113-login-lab-2026-11-19.md#3-server-side-version-catalogue-gap-labsrv) |

A full logged-in session of the real client, its post-RC4 login message, and whether the first-hop login token is classic or connector-supplied are still open → App. E#616 [lab] (protocol/v6113-login-lab-method.md#still-open-carried-not-closed).

**Settled question, formerly E#17: the 6.1.1.3 login after the RC4 switch, settled as far as the project will take it.** What the stock 6.1.1.3 client sends as its login once the stream turns to RC4 is not fully known, and the project will not pursue it further. The handshake is read, a 6.1.1.3-shaped login works end to end in the project's own stack, and the stock client's exact login-argument order is left at a best guess (→ §2.10) [lab] (protocol/v6113-login-lab-method.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled (handshake) | The clear hello `GNP1905C` comes from the connector script; the outgoing stream is clear up to offset 287 and plain RC4 with a 16-byte session key after it; the server's key arrives RSA-wrapped in a clear `0xfc` message. The connector request is a pure function of the build, so a genuine reply stays valid on every later launch | [lab][cap] (protocol/v6113-status.md); [lab] (protocol/v6113-login-lab-method.md) |
| Settled (our stack) | The clean-room client repro builds, verifies and decrypts its own signed `conf.gs` and runs the hello and two-way key exchange; seihai-core's secure login completes against our own server. A working 6.1.1.3-shaped login exists for the project's own client, with the argument order and payload cipher chosen by us | [lab][inf] (protocol/v6113-login-lab-method.md); [lab] (protocol/conf-gs-fuzzing.md) |
| Best guess (stock client) | The stock client's post-RC4 login body is the 6.0x body (→ §2.3.5) under RC4, framed as `EILLLT` bundles: client type, key, the 8-byte token `GNP1905C`, account `str`, password `str`, then the comma-separated machine list. The connector's step names fit this split: `sendLoginNewProtocol` sends the opening and account, `sendPasswordAndIDs` the password and machine list. The same field order is what our server reads from real 4.20r8, 5.x and 6.03r7 logins. Confidence: moderate to high; an extra field added only by the official connector would not have been seen | [inf] (protocol/v6113-login-lab-method.md); [doc] (protocol/connector-script.md); [bin] (protocol/v4x-clients.md#login-packet) |
| Not pursued | Confirming the stock client's exact account and password framing would need either reading its login key out of the protected client (a key-swap shown to be a dead end in the lab) or a capture against the live official service. The project has chosen to do neither, so the best guess stands | [lab] (protocol/conf-gs-fuzzing.md) |
| Verdict | Settled as far as the project will take it: the project's own 6.1.1.3-style login works, and the stock client's exact body is left at the best guess and not chased | [inf] (protocol/v6113-login-lab-method.md) |

## 2.10.9 Malformed connector replies

The reply container is read and sized before the signature check decides, so its framing can be tested on a stock client with only a loopback connector; the decrypted script behind it cannot, because a stock client discards any payload it did not verify (→ §2.10.8) [bin][lab] (protocol/conf-gs-fuzzing.md#what-is-being-fuzzed-and-why-the-deep-layer-needs-the-key).

| Layer | What the client does with it | Testable on a stock client | Source |
| --- | --- | --- | --- |
| container framing: the 4-byte marker, the 256-byte signature, the 4-byte inner length, the payload buffer | read and sized before the verify's verdict | yes | [bin][lab] (protocol/conf-gs-fuzzing.md#what-is-being-fuzzed-and-why-the-deep-layer-needs-the-key) |
| decrypted script: the GS2 body, the id-table pairs, the token, the key material and cipher settings | reached only after the signature passes and the payload is decrypted and run | no; only through a client that owns its own key | [bin][lab] (protocol/conf-gs-fuzzing.md#what-is-being-fuzzed-and-why-the-deep-layer-needs-the-key) |

Eighteen one-field mutations of the container (marker, signature, inner length, and payload shorter or longer than declared) were served to the real packed client on loopback and compared with a clean-room copy of the check. Every one failed closed: the client stayed up and showed its connect-error dialog, with no crash, no hang and no accept. The largest declared length and the length-against-body mismatches did not over-read, so the client validates the container length before it uses it [lab] (protocol/conf-gs-fuzzing.md#results-2026-11-19-lab).

Two-field and transport-timing mutations against the real client, and script-content mutations through a client that owns its key, were not run [lab] (protocol/conf-gs-fuzzing.md#still-open--next).

