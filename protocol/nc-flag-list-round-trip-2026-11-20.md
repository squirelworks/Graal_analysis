# The 2001 NPC Control server-flag list, end to end (E#425)

Date: 2026-11-20. Evidence: **[bin]** (a linear disassembly of the two retained flag-list NPC
Control executables, plus a decompiler read on the lab host A; no program run). Only behaviour is
given here. It follows [nc-standalone-flag-action.md](nc-standalone-flag-action.md) and answers its
open questions for the client side.

Builds read: NPC Control 2001/05/21 (`NPCControl-leak2.exe`) and 2001/03/19
(`oldNPCControl-leak2.exe`), both NC token `NCL15031`, both with the `TFlagList` form ("Serverflag
List"). The July 2001 build (`nc7132001.exe`) has a weapons list in its place and was used only for
the comparison at the end.

## The round trip

1. The main window's **Server &Flags** button sends NC message **68** with an empty body.
2. The server answers with message **61**: a count, then the list. The NC clears the form's text
   box, adds each item as one line, and shows the form.
3. The user edits the lines. **&Send** sends message **69** with the whole list in the same layout
   as 61, then closes the form. **&Close** closes it without sending.

So the "flag action" sends the server's flag list back as a whole. The server's list is replaced by
the form's text, one flag per line.

## The list layout (61 and 69)

- The count is two characters: (count >> 7) + 32, then (count AND 127) + 32. The high character is
  taken as a byte with no mask.
- Then, for each line, one character with the line length + 32, followed by the line's text.
- The list is the `Lines` of a rich-edit box the form creates at start-up. On sending, the count is
  the number of lines, so a blank line goes out as a zero-length item.

### Ranges

- The count is correct up to 28,671 lines. From 28,672 the high character no longer fits in a byte
  and wraps.
- A line length is correct up to 223. A longer line's length byte wraps, and the server would read
  the wrong length.
- On receipt the NC reads each length as the byte − 32, treats a negative value as 0, and takes that
  many characters. It stops early if the body runs out.

## From message to socket

Every NC request goes through one send routine of the NC's single server connection. It has 22
callers, including 68 and 69.

- The message is the character (id + 32), then the body, then a line feed. It is appended to a text
  buffer.
- When the buffer reaches 4,096 bytes (checked before and after the append), it is flushed. The
  flush compresses the whole buffer with zlib (the program carries zlib 1.1.2). It then adds a
  two-byte big-endian length and appends the result to the raw output queue. This is the plain
  generation-2 frame: length and zlib, with no cipher.
- If the raw queue reaches 256 KiB, it is thrown away and the connection is marked as broken.
- The socket writer sends the raw queue in pieces of at most 256 bytes. If a send returns 0, it also
  marks the connection as broken. A later check then closes the socket and the NC window, and
  shows "You have been disconnected!" (or the server's own text, if one was received) under the
  title "Graal Remote Control".
- Smaller messages wait in the text buffer. The routine that writes the socket first flushes any
  pending text, so 69 is not held back until the buffer fills.

So 69 goes to the server the NC is logged into, the same peer as every other NC request.

## The two flag-list builds

The &Send routines of the March and May builds are the same instruction for instruction. Only the
address of the send routine they call differs. Both builds send 68 and 69 and handle 61 the same way.

## Against the July weapons list

The July build has a **Weapons** form instead. It sends one request per weapon: **116** to edit one
and **118** to delete one. It has no whole-list send. So the flag-list write is not "the weapons list
in another form". The weapons list edits single entries, while the flag list replaces the whole list.
The later NC layouts (`npc-control.md`) use 108 and 110 for an NPC's own flags, which is a different
thing.

## Not covered

- What the 2001 NPC server does with 69. No server of that date is held. The NC's view is that the
  server's flag list is replaced by the lines sent.
- Whether the server applies any limit of its own on the count or the line length.
