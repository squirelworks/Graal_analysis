# RemoteControl

Delphi staff client, predecessor of the GTK `RC2_2.05`. One process, 25 auto-created forms. Live console holds two `TGraalClient` sockets:

- RC / game socket at console +0x38c.
- NPC-server socket at console +0x390.

## Codec

Classic Graal text codec (not the later binary RC framing):

- Logical id sent as `id + 0x20`.
- Strings length-prefixed the same way.
- 14-bit and 21-bit integers with the same offset.
- First line of a session carries the XOR increment.
- Buffer flushed at 0x1000 bytes or immediately for large files.
- Compression mode chosen once (raw / zlib / second compressor); even modes XOR-encrypted with Borland LCG (seed `0x04A80B38`).

NPC login is type 3 starting with the literal `NCL11012`.

## Player list

Packet 0x37 creates or updates a `TServerPlayer`. The body is a property stream walked by the property parser. Id is a 14-bit integer. Constructor defaults include hearts = 3, sword = `sword1.gif`, body = `body.png`, level = `onlinestartlocal.graal`.

## File and account operations

- Folder change: 0x5a.
- Upload framed by 0x9b / 0x5d / 0x9c.
- Delete requires the rights string to contain `w`.
- Account list and property get/set use the matching PLI_RC_* ids from gs2lib.

Local settings live in `controlconfig.txt`. RC2 later wrote the same family to `control2config.txt`.
