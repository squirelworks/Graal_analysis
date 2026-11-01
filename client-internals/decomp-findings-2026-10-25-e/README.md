# Decompile mining, batch e: file-transfer request lists and save rules, 2026-10-25 (Asia/Tokyo)

Derived facts only. No raw decompile text, no addresses, no generated function names, no code, no paths. The raw exports stay private. Nothing was pushed to Graal_analysis, no public server was contacted, the lab was not touched. The lab facts quoted are from the 2026-10-24 captures that are already summarised in earlier notes.

Scope: what the real clients keep, what they re-request, and when a local file counts as up to date (Seihai queue item 9). Read in the 2.05 rev 2, 2.17.1, 2.22 and 2.31 clients; the 2.00 client only for the list code. Checked against the 2.17, 2.22 and 2.31 login and gmap captures.

## Files
| file | content |
|---|---|
| 01-request-lists.md | the three name lists, the window of four, which loaders ask for what, how replies settle names |
| 02-save-rules.md | whether and where a download is written, the folder table, the time of the saved file, name lookup |
| 03-open-points.md | what was not resolved and what would settle it |
| 04-name-index-case-link.md | which copy of a duplicated name is used, the A–Z case fold, and the packet 40 link (a horse does not change it) |
| request-rules.tsv | the request-side rules, one per row, with builds and evidence |
| name-index-rules.tsv | the index, fold and packet-40 link, one row each |
| download-folders.tsv | the save-folder decision table per build |
| open-questions.tsv | unresolved points |

## Top facts
1. A client holds three name lists: wanted, update-asked, settled. A file the client lacks is asked for with `PLI_WANTFILE`; a file it has is asked about with `PLI_UPDATEFILE` carrying the file's last-write time in Unix seconds.
2. Four requests of each kind are on the wire at once. More names wait in order; a reply for a name among the first four releases the name now in fourth place. The two kinds count separately. Identical in 2.00, 2.05 rev 2, 2.17.1, 2.22 and 2.31, and seen in the lab (four and four before the first reply).
3. A local file is checked once per name per connection. Any reply (file, up to date, send failed) puts the name in the settled list; a name in that list is not asked about again.
4. The client never compares times itself. The server decides, and answers with the file, "up to date" (45, 2.1+) or "send failed" (30, which before 2.1 also means up to date).
5. Image and animation loaders: local file means use it and send the check; none means ask for it. Sound loader: ask only when missing. Levels use no file transfer.
6. Downloads are kept as cached streams and written to disk only when the `saveimages` option is on (default on). A file the client already has is replaced where it is. A new file goes to `sounds`, `maps` (2.17.1 and later) or a folder under `levels` chosen by the name.
7. The saved file gets the server's time (2.1+) so the next check carries it. A lab 2.22 run saved a downloaded gmap under `maps` with the server's time.
8. A name the server could not send is not asked for again on the same connection (lab, 2.22).
