# Server notes (from decommissioned local workspace)

These files are extracts from the Ember atlas that lived in the local Graal research workspace. They document the server side of the protocol, the lineage of the dumps, and the algorithms used by gs2emu / Ash / Phoenix.

They are provided here so that server-side understanding is versioned alongside the client analysis already in this repository. The full original materials (including ATLAS.html, all Ember markdown, the complete GServerStory, source dumps, Phoenix, and Ash) are in the Google Drive archive linked from `../ARCHIVAL.md`.

Nothing in these notes was invented about the protocol. Identifiers and behavior match the dumps and the Ash rewrite.

## Our own servers (2026-10-30)

`lab-servers-2026-10-30.md`: what the project's lab gserver (GServer-v2 `efb5b90` + a gs2lib patch) and listserver are, real 2.05 / 2.17.1 / 2.22 runs against them, and a comparison with GServer-v2 beta4, graal-serverlist, Guthius's graal-listserver, glauncher and gs2-parser.
