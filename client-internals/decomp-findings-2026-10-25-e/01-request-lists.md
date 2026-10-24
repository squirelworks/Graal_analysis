# Request lists

## Lists
Each client keeps three lists of file names:
- A (wanted): names asked for with `PLI_WANTFILE` (23, name only).
- B (update asked): names asked about with `PLI_UPDATEFILE` (34: GINT5 time, then name).
- C (settled): every name a reply came back for.

## Asking
- No local copy: if the name is not in A, append it; send the request when A now holds at most four names.
- A local copy: if the name is in neither B nor C, append it to B; send when B holds at most four. A name in C is skipped, so each local file is checked once per connection.
- The time sent is the last-write time of the local file, Unix seconds. Lab: it matched the file's mtime for the sword, shield and body images at login.
- Builds whose packet set has no id 34 (1.33 to 1.41) never check a local copy.

## Replies
A reply (file, up to date, send failed, or the end of a large file) removes the name from A and B. If the removed position was among the first four and names are still waiting, the one now in fourth place goes out. Then the name is added to C. The pair A/B releases independently.

## Who asks
- Image loaders and animation loaders: local file, use it and check it; no file, ask for it.
- Sound loader: ask only when missing. The lab shows no check for a sound that exists.
- Levels: no file transfer; board packets and the level modtime exchange, plus the persistent web-level cache.
- A gmap file: checked like an image when present (lab, 2.22 gmap runs); asked for when missing (lab).

## Failed names
A name answered with "send failed" is not asked for again on the same connection (lab: a missing step sound is asked for once however often the player walks). What the client stores for it beyond that is not known.

## Cross-build
The list code is the same in 2.00, 2.05 rev 2, 2.17.1, 2.22 and 2.31. In 2.05 rev 2 and 2.22 the request-side function bodies were hard to read in the export; the request rules for those two come from the matching reply-side code and the lab, and are marked inferred in the tsv.
