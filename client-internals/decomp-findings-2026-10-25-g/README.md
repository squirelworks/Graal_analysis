# Decompile mining, batch g: ids 24, 46 and 178, 2026-10-25 (Asia/Tokyo)

Derived facts only. No raw decompile text, no addresses, no generated function names, no code, no paths. The raw exports stay private. Nothing was pushed from here to Graal_analysis directly, no public server was contacted, the lab was not touched. The lab facts quoted are from the 2026-10-24 captures that are already summarised in earlier notes.

Scope: the three fields earlier notes called unknown (Seihai queue item 12): the meaning of client id 24 (relayed as 32), the meaning of client id 46, and how the clients read server id 178. Read in the 2.17.1, 2.22 and 2.31 clients (all three read for 24 and 178; 46 in 2.31, with a negative check in 2.17.1 and 2.22), plus the GServer-v2 and graal-serverlist sources.

## Files
| file | content |
|---|---|
| 01-id24-image-list.md | what id 24 and its relay carry: the weapon-script image list, the full-list marker, the sender's rules, the receiver's rules |
| 02-id46-level-switch.md | where id 46 is sent and why its payload is a literal |
| 03-id178-comma-text.md | how the clients split the 178 text, what they do with each field, what the writers send |
| 04-open-points.md | what was not resolved and what would settle it |
| image-text-format.tsv | the image-record text, one row per tag |
| comma-text-rules.tsv | the clients' comma-text splitter, one rule per row |
| open-questions.tsv | unresolved points |

## Top facts
1. Id 24 is a list of the images that the sender's weapon scripts show (`showimg` and the `changeimg*` commands), not a heartbeat and not an emote. The one byte 9 that real 2.22 and 2.31 clients send is the list's first character on its own: a "full list follows" marker with no images after it.
2. The sender keeps the list it sent last and sends only changes, except that every 101st call of a periodic handler it sends the whole list, led by the marker. The call after a send is skipped, so a wrap is 102 ticks: the lab's 5.1 s if a tick is 50 ms (inferred from the period). With no images and no changes the only message is the marker.
3. The receiver (applies only for a player in its active level) creates an image when it gets a name, removes it on an empty name, changes the other fields only of an image that exists, and after a marked text removes every image the text did not name.
4. The 2.22 client sends its TCP copy only when UDP does not reach some player in the level; with nobody in the level that test is false. In 2.31 the test is a constant true. This explains the lab (2.22 only with a second player, 2.31 always). 2.17.1 has the same sender and test.
5. Id 46 is a content-free notice. One send site in 2.31 (none in 2.17.1 or 2.22): the start of the routine that switches the client's current level, when connected. The payload is a literal 1. GServer-v2 ignores it.
6. Id 178 is read by the clients' own comma-text reader, the same in all three builds: leading white space skipped, quotes with doubled quotes, an unquoted item ends at white space or a comma, at least 4 items, items 1 to 3 used. A name with a space must be quoted or it shifts the later items.
7. Item 1 of 178 is kept as the server's name: the first two characters are dropped when the second is a space (a listserver type prefix such as `P Name`). 2.31 shows it in the window title. It is not used to connect.
8. What a real list service sends for 178 has still never been captured. The open-source reimplementation sends four quoted items; a commented-out older line in its source shows a different shape with a tag in item 0.
