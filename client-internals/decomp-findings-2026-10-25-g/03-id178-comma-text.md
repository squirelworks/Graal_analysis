# Id 178 (`PLO_SERVERWARP`)

Read in the 2.17.1, 2.22 and 2.31 clients (the handler, the text splitter and the connect routine were compared and match in all three).

## The handler

Build a string list from the text with the client's comma-text setter, require at least 4 items, and call the "connect to another server" routine with items 1, 2 and 3. Item 0 is not read. Anything shorter does nothing (lab: no reaction, connection stays open).

## The splitter

The same code as the standard list class of the toolchain the clients are built with. Rules in `comma-text-rules.tsv`. The ones that matter for 178:

- White space (bytes 1 to 0x20) before an item is skipped.
- A quoted item ends at its closing quote; two quotes in a row are one quote; an unclosed quote runs to the end of the text.
- An unquoted item ends at a byte of 0x20 or less or at a comma. A space inside an unquoted name therefore ends the item and the rest of the name starts the next one.
- After an item: white space, then one comma, then white space. A comma at the very end adds no empty item; an empty item between two commas is kept.
- A NUL ends the text.

Consequence: a server name that contains a space must be quoted by the sender. `x,Main Server,h,1` reads as five items and the client would connect to the host `Server`.

## The connect routine

- Item 1 is the server name. If its second character is a space the first two characters are dropped (type prefix, as in `P Name`). The result is stored as the current server's name. In 2.31 it is also put in the window caption: the caption is the name alone if the name already contains "graal" (any case), otherwise `Graal: ` plus the name.
- Items 2 and 3 are stored as the host and the port, both as text first.
- The routine then reconnects to the host and port. The name is not used to connect, which agrees with the lab (a made-up name connected normally; reordered host and port failed to connect).

## Selected 2.22 port-conversion boundary

The selected follow-up uses the 2.22 image with embedded version 2.2.2.0, distinguished from its separately modified sibling. Its receive-178 case requires at least four comma-text items and passes items 1, 2 and 3 onward. The selected server-switch routine copies item 3 into the stored port string. A guarded connection-construction path reads that same string; it requires the host and port strings to be nonempty before calling the lower-level connection routine. These are static data-flow and branch observations, not a connection test. **[bin]**

In the lower-level routine, the selected normal sequence calls an integer-conversion wrapper with the port string, passes its returned integer directly to the imported `htons` boundary, and writes the returned word into the socket-address port field. There is no intervening application-level comparison against a port range such as 1 through 65535 in that sequence. The underlying 32-bit integer parser has parse-error and overflow checks; those are not a separate validation of the 16-bit port domain. The wrapper's successful integer return was checked in the return-tail instructions as well as at its caller. **[bin]**

The conversion/store sequence has a local exception frame. This follow-up does not establish the resulting port value or recovery outcome when conversion fails, the complete accepted text grammar, or the behavior of the external networking implementation. No malformed port was submitted, no connection was attempted, and no wraparound or runtime-acceptance result is claimed. **[bin]**

G050 remains partial: this answers the selected 2.22 normal conversion/range-check question, not the real service's text or item 0, the other two historical inputs, all paths or runtime behavior. The static receipt is indexed as `V222-SERVERWARP-PORT-BOUNDARY-20261128` in the [evidence index](../../docs/evidence-index.tsv). **[bin]**

## What the writers send

- GServer-v2: forwards the listserver's answer to `PLI_SERVERWARP` (41) as 178, unchanged, and only to clients from 2.1 on. The server's own code calls this a hack to let the new clients serverwarp.
- graal-serverlist: for a request it answers with the server name twice, the host and the port, as one comma text made by its tokenizer (each item quoted, quotes doubled). A commented-out older line in the same function builds `playerworld` plus a number, then the name in quotes, then the host and the port: item 0 is a tag of that kind there. That is source-comment evidence only.
- A real service's text has never been captured.

Seihai reads the text with the same rules (`delphi_comma_text`) and shows the name without the type prefix.
