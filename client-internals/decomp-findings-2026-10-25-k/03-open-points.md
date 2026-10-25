# Open points

- Bomb, arrow and baddy hurt powers: the object-kind mapping was not traced. A capture of a real client hit by a server bomb and by an arrow, reading the power byte, would settle it.
- The per-player field of packet 40: inferred to be always equal for ordinary players. A real client hit by packet 40 from a player that owns a horse or similar would show whether it differs.
- End of respawn: the respawn routine calls the entry save once more after asking for the warp; whether the next respawn point is then the death spot online needs two respawns on a server that delays the level reply.
- CURPOWER after damage: needs a real client at full hearts hit by an injected packet 40 and a look for a props message with the hearts byte.
- Default weapon ids against images: see 02. A run that names the ids and the images together would settle it.
- Level cache format (GWEBL001): not part of this batch. A real client run twice against the same level with the cache folder inspected would show the key handling.
- File-index scan order for two files with the same name in different folders: a capture with different bytes in `levels/webgifs` and `levels/bodies` and a look at which is drawn.
- Whether pre-2.1 clients re-send the file check for a settled name: a 2.05 run against a server that answers every check with "send failed".
- When the maps folder rule arrived (2.1 to 2.16): no binaries.
