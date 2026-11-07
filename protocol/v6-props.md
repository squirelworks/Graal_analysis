# Property ids in unpacked 6.1.1.3 and 6.0.3.7

Static read of both listings. Nothing was run. [bin]

## What the receive methods do

In 6.1.1.3, `tclient_setplayerprops`, `tclient_setnpcprops`,
`tclient_setbaddyprops` and `tclient_setotherplayerprops` each take one
string and store it. None of those four functions switches on a property
id.

The id tables that are in the image are the outgoing encoders. Each walks
a fixed id range, and for an id whose flag is set it appends that id stored
plus 32, then the encoded value. 6.0.3.7 has no `tclient_set*` names. It
has the same two encoders, with the same ranges and the same case lists.

## Player

Both images loop ids 0 through 83. The encoder switch has a case for 72 of
them. These twelve are in the loop and have no case:

3, 25, 27, 28, 29, 30, 34, 36, 50, 51, 77, 83.

The case list is the same in 6.0.3.7 and 6.1.1.3. No player id is present
in one build and absent in the other.

The bytes stored for each id were not recovered. The search was the encoder
switch and the 0-through-83 loop in both listings. The switch body was not
split into a field width per id.

## Baddy

Both images loop ids 0 through 10, and the encoder switch has a case for
every one of those ids. The case list is the same in both builds.

What was visible inside the 6.1.1.3 cases, and matched by the same case
numbers in 6.0.3.7:

- Ids 1 and 2 each read one floating component and emit twice that value.
- Id 4 compares the image name `baddygray.png` and emits one biased byte.
- Ids 8, 9 and 10 each copy one of three neighbouring fields.
- Ids 0, 3, 5, 6 and 7 share one path that appends a string.

The per-id field widths beyond that were not recovered.

## NPC

No third loop of this shape is in either image. `tclient_setnpcprops` in
6.1.1.3 stores one string on the NPC. A numbered NPC property-id table was
not found. The search was the same id-plus-32 append loops and the
`tclient_setnpcprops` body.
