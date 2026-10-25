# A public GServer-RS login, 2.22 profile (2026-10-25)

Counts and layouts only. The capture, screenshots, and the server's address
are not in this repository.

## Login burst

819 messages in the session. In order, the ones that matter: own player
props, flags, a weapon list of one weapon (`-gr_movement`, with its script),
`SETACTIVELEVEL`, the level board (64 x 64 tile ids, two bytes each),
three `PLO_LEVELCHEST` records, no `PLO_LEVELSIGN`, four `PLO_NPCPROPS`
records, then text and window messages. One file request in the session was
answered with a send-failed message.

## Why no chests were drawn

All three chest records are the short form (opened, x, y): the server says
the account had opened them. The board has none of the chest tile ids (closed
1784 1785 1800 1801 or open 829 830 845 846) and the three positions are plain
grass. The client draws nothing for a chest record, so nothing is drawn.

## Weapon scripts and line breaks

The server writes a line break in a weapon script as `§`. A latin-1 server
sends the byte A7; a UTF-8 server sends C2 A7. Decoded as latin-1 without
handling the pair, the script becomes one `//` comment line and does nothing.
With the break read as a newline the `-gr_movement` script parses with no
diagnostics. It sets two player strings from the position, rounded to half a
tile, and sets the chat property to a fixed word, every 0.05 s.

## Capture link type

A capture taken with `tcpdump -i any` uses Linux cooked v2 (pcap link type
276, a 20-byte pseudo-header whose first two bytes are the protocol type);
older cooked captures use type 113 with 16 bytes.
