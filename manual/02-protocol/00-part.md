<!-- manual: kind=reference status=draft -->
# 2 Wire protocol

> Status: draft. Each chapter carries its own status line.

## 2.0 Reading this Part

The Graal wire protocol is one message vocabulary carried by several transports. From 1.21 to 6.03 a message is an id byte, a payload and a newline, and the id is logical: the wire byte is the id plus `0x20`. [srv] (protocol/packet-ids.md); [srv][2.05] (protocol/packet-layouts.md) What changes from build to build is the frame around those messages, the cipher over the frame, and which ids each side sends and handles. A reader of this Part should first fix the build's encryption generation (→ §1.4), because that decides how to read every byte that follows. [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering)

**Printable integers, and no lengths.** Graal's own integer types add `0x20` to every 7-bit group, so an encoded value never contains a newline and a message can end at `\n`. [srv][2.05] (protocol/codec-and-framing.md#graal-integer-types) Bodies that may hold any byte go behind the raw-data escape (§2.1.3). The same economy shows in prop streams: a stream is `(id, value)` pairs with no per-prop length, so a reader must know the encoding of every id up to the highest it expects, and in 2.05 to 2.31 one unknown id early in a stream hides every prop after it. [srv] (protocol/player-props.md); [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231)

**Six generations of transport.** The 1998 builds speak text lines through a relay that knows nothing about the game. 1.21 to 1.39 add zlib frames and no cipher. 1.41 rev1 to 2.17 insert one junk byte into each client message from a shared LCG. 2.19 and later apply a partial XOR after compression, and 2.22 and later choose their compression per frame. [bin] (protocol/relay-1998.md#summary); [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) In 6.11 the client has no fixed protocol at all: a connector script fetched at login sets the framing, the cipher and both id tables. [bin][inf] (protocol/v6x-clients.md#what-the-script-controls) §2.1 and §2.2 give the frames and ciphers, and §2.3 gives each generation's login.

**Ids are a per-build set, and silence is normal.** The client-to-server (PLI) and server-to-client (PLO) references in §2.4 and §2.5 give each id's layout where a note measured or read it, and say `unmeasured` otherwise. Every handler in 2.05 to 2.31 checks a minimum length and drops a short message silently, and an id with no case falls to a shared default arm and is ignored. [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205); [2.05] (protocol/packet-ids.md#server--client-plo_) A server that sends an id a build does not handle therefore sees no error, only missing behaviour, which is why the per-build id sets in §2.4.2, §2.5.2 and App. C matter. [bin][srv] (protocol/client-versions.md#server--client-ids-handled)

**Beside the game connection.** Files ride the same connection, with request lists and replies whose layout follows the server's token table (§2.7). [srv] (protocol/file-transfer.md#requests-client--server) From 1.28 beta 2 to 3.04 the clients also run a UDP channel between players that the game server never sees; the server only relays each player's address (§2.9). [bin] (protocol/gserv-1999.md#udp-128-beta-2-on); [2.05] (protocol/udp-p2p.md) The strongest evidence in this Part is the 2.05 rev 2 client read against GServer-v2's source and lab captures; later rows say which build and which kind of evidence they rest on, and an exact-build reading holds for that build only. [srv][2.05] (protocol/packet-layouts.md)

## Chapters

- → §2.1 Framing and encodings (`01-framing.md`)
- → §2.2 Ciphers and compression (`02-ciphers.md`)
- → §2.3 Login and handshake by generation (`03-login.md`)
- → §2.4 PLI message reference (client to server) (`04-pli.md`)
- → §2.5 PLO message reference (server to client) (`05-plo.md`)
- → §2.6 Props (`06-props.md`)
- → §2.7 File transfer (`07-file-transfer.md`)
- → §2.8 Chat and private messages (`08-chat-pm.md`)
- → §2.9 UDP peer-to-peer (`09-udp.md`)
- → §2.10 The 6.11 server-defined protocol (`10-server-defined.md`)
