# Login, framing and properties: unpacked 6.0.3.7 against 6.1.1.3

Date: 2026-11-07. Static read of both unpacked listings. Nothing was run. Only differences that are in both images are recorded. Tags: **[bin]**.

## Login token

Unpacked 6.0.3.7 stores one scrambled eight-byte string. The length-and-position decoder yields `g3d0311c`. The login constructor decodes it, upper-cases that buffer, and sends the result as packet id 5. **[bin]**

Unpacked 6.1.1.3 has no stored string that decodes to `g3d0311c`, `G3D0311C`, `gnp1905c` or `GNP1905C`. It has no constructor that loads an eight-byte token and sends id 5. The capture token `GNP1905C` is not in this image (`protocol/v6113-list-capture.md`). **[bin][cap]**

## Framing

6.0.3.7 keeps the generation-5 framer: the shared seed, the Borland step, and a key masked to 7 bits. The decoded string search finds no `setprotocol`, `sendraw` or `senddata`. **[bin]** (`client-internals/unpacked-6037.md#connection`)

6.1.1.3 still constructs a connection on that generation-5 framer, and it also has `setprotocol`, `sendraw` and `senddata`. `setprotocol` replaces the framer with an `I`/`L`/`T`/`E` header. `E` 1 is zlib and `E` 2 is bzip2 at block size 5. **[bin]**

## Property streams

6.1.1.3 registers script methods `tclient_setplayerprops`, `tclient_setotherplayerprops`, `tclient_setnpcprops` and `tclient_setbaddyprops`. A decoded-string search of 6.0.3.7 finds none of those names, and no `tclient_` name at all. **[bin]**

6.0.3.7's incoming game switch is the fixed id list in `client-internals/unpacked-6037.md`. That list includes the property messages. The field layout inside a player, NPC or baddy stream was not compared between the two images. A difference in those bytes: not found. **[bin]**
