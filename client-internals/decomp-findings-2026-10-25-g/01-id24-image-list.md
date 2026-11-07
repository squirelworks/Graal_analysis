# Id 24 (`PLI_SHOWIMGPLAYER`) and its relay (`PLO_SHOWIMG`, 32)

Read in the 2.17.1, 2.22 and 2.31 clients. The sender routine is the same in all three (same structure, same constants); the receiver was read in 2.31.

## What the text is

A list of the images that the sender's weapon scripts currently show (`showimg` and the `changeimg*` commands), one record per image. A record starts with a byte that is 0x2a plus the image's index (0 to 199). Fields follow, each a tag byte (0x20 plus the tag number) and its data. See `image-text-format.tsv`.

A tag byte of 0x2a or more starts the next record, so tags run 0 to 8. An unknown tag skips its one data byte. A tag byte with no data byte after it ends the whole text.

The first byte of a text may be the marker 0x29 (a closing parenthesis). As a GCHAR that is the value 9, which is the one byte every real client was seen to send. It means "this is the full list"; here the list is empty.

## Sender

- It collects the images of the player's weapons (index 0 to 199) and compares them with the list it sent last. Changed images are sent with the fields that changed; an image that is gone is sent with an empty name.
- A counter runs from 100 down; at a wrap the text starts with the marker and every image goes out in full. The wrap is the 101st call of a periodic handler. The call after a send is skipped, so a wrap is 102 ticks. The lab period of about 5.1 s fits a tick of 50 ms; that interval was inferred from the period, not read from the client's form resource.
- Nothing is sent when the text is empty. With no images the only text that ever exists is the marker alone at a wrap, one byte: GCHAR 9. The first tick after login is a wrap.
- The client sends a UDP copy when it can (the 2.05 UDP id 15 form for older builds). The TCP copy goes out only when its test says so.

## The TCP test

- 2.31: the test is a constant true. The TCP copy goes out at every wrap, alone or not, in any level.
- 2.22 and 2.17.1: the same test in both. It is true when UDP does not reach some player in the client's level; with nobody else in the level there is nothing to find and it is false. This fits the lab: 2.22 sent only with a second player present (no sends in three solo sessions), and the 90 s solo 2.17 capture saw no id 24.
- A wrap that finds the test false is lost. The next wrap is a full period later.

## Receiver

- The relay is `GSHORT sender id`, then the sender's text unchanged (GServer-v2 does not look inside it).
- The 2.31 handler reads the sender's id, finds that player in the client's active level and hands the rest to the routine that applies the text. Nothing else reads the byte.
- Per record the image is looked up by index. Name: an empty name removes the image; a non-empty name creates it if missing (defaults: layer 1, colours 200 each, zoom 10, mode 0) and sets the name. Other fields are applied only to an image that exists.
- Part: 0x20 means the whole image. 0x21 is followed by left and top as two 7-bit bytes each, then width and height as one byte each; the values are clamped (left and top 0 to 16000, width and height 0 to 220).
- After a marked text, every image of that player that the text did not name is removed.

## What is not known

- The sender's own value formatting for each field. The units above are the receiver's reading, so the units of x, y, colours and zoom are unconfirmed.
- What the per-player "UDP reaches this player" flag in the 2.22 test is and how it is set.
- How the client draws the images (layers, the screen-unit mode of layer 10 and over, colour and zoom).
- 2.05 uses the same tagged form (tags 0 to 6) with a 60-call full-list countdown: `../id24-205.md`. Builds before 2.05 were not read.
