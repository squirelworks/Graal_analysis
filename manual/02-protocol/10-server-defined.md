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
| None of this exists in 6.01 or 6.03: no connector, no RC4 or AES, no script-set id tables | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#what-the-script-controls) |
| gs2lib names `PLI_SET_ENC_KEY` and `PLO_SET_ENC_KEY` (252, setting an AES or RC4 key and IV) and `PLI_BUNDLE` and `PLO_BUNDLE` (253, several messages in one); both are above 223, so they cannot be sent as one GCHAR | server library | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |

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
| `sendraw` appends the caller's bytes with no packet id and no header, which is the path that can write those eight bytes | 6.1.1.3 | [bin] (protocol/v6113-hello.md#the-eight-characters) |
| `setprotocol` writes an `I`/`L`/`T`/`E` header. `L` is the header length plus the body length. `E` 1 is zlib and `E` 2 is bzip2 at block size 5. The template is not in the image | 6.1.1.3 | [bin] (protocol/v6113-hello.md#the-six-bytes-after-the-token) |
| A 6-byte header plus the capture's 273-byte zlib member is 279, and `01 17` sits in the captured header. The cipher after that member was not found | 6.1.1.3 | [bin][cap] (protocol/v6113-hello.md#what-the-cipher-is) |
| Unpacked 6.0.3.7 stores `g3d0311c`, upper-cases it, and sends it as id 5. 6.1.1.3 has no such string | 6.0.3.7 and 6.1.1.3 | [bin] (protocol/v6113-hello.md#against-unpacked-6037) |

## 2.10.6 Unpacked Windows 6.1.1.3

The unpacked Windows image still contains the generation-5 LCG: seed `0x04A80B38`, step times `0x08088405` plus 1. It has no compiled-in `G3D` or `GNP` token. Each outgoing sender compares its own slot with `0xFE` and then calls a script event; the Mac slot numbers in the table above are not the order of the names in this image. `onSendNPCProperties` is the one Mac event name this image does not have. `StartScript_Connector`, `StartScript_Fail` and the three `scriptssl*` fields are present. `setprotocol`, `setindatahandlers` and `con.gs` are not plaintext strings. [bin] (protocol/unpacked-6113-wire.md#generation-5-cipher); [bin] (protocol/unpacked-6113-wire.md#script-send-slots); [bin] (protocol/unpacked-6113-wire.md#connector-names)