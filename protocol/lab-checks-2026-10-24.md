# Lab checks, 2026-10-24

Derived facts from real-client runs against a local lab only. No public server was contacted. Placeholder accounts. Captures stay off the repo.

## Tampercheck (client PLI 39)

Every build sends the same 10 raw bytes at every login, regardless of account and login key. It is a per-build constant, not two GINT5 words (bytes below 0x20 occur; GINT5 bytes cannot be below 0x20). No byte is 0x0a, so it survives line framing unescaped.

| Build | Token | Constant |
|---|---|---|
| 2.17 | `GNW22122` | `2a7bad195e231243d82c` |
| 2.22 | `GNW03014` | `250e4d0f962b03ede631` |
| 2.31 | `GNW28015` | `291655b7602e87c9eb82` |

Position: second message of the first client frame, right after PLI 37 (language).

Re-send:
- 2.17: once, at login.
- 2.22: at login, and again once for every gmap-edge crossing. No periodic send.
- 2.31: at login, then about every 3.2 s. 2.31 also sends PLI 24 (1 byte, value 9) about every 5.1 s, and PLI 46 (1 byte, value 1) once at login. These are 2.31-only.

GServer-v2 accepted all three and did not log an invalid packet.

How the 10 bytes are built (two chained CRC-32 words over the client's own memory image) and why 2.31 repeats them every 3.2 s: `client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md` and `client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md`. The two words per build are in `version-profiles/tampercheck-words.tsv`.

## 2.17 listserver login

One TCP connection to port 14922. Plain zlib framing (u16be length + zlib body). No gen-5, no version token.

Client sends one frame holding two messages: `GCHAR 0` + `newmain`, then `GCHAR 1` + GSTRING account + GSTRING password.

Server answers with two plain zlib frames: frame 1 = id 0 server list; frame 2 = id 2 status text, id 3 site URL, id 5 donation URL. The client then closes.

After the list, the gserver login is type 0, key, `GNW22122`, account, password, then gen-3. The junk-byte rule decoded 100% of the 2.17 messages.

## 2.22 gmap edge crossing (2x2 gmap)

Crossing uses only normal props. No level-warp packet.

- A client flag `gr.x` / `gr.y` is set on every half-tile step (PLI 18). It carries the global position (local + 64 × cell), so it runs past 63.5.
- When the global position wraps, the same props message carries the wrapped local coordinate and the cell prop (GMAPLEVELX = prop 43, GMAPLEVELY = prop 44).
- East: at global x 64.0 the client sends PLI 39 (tamper constant), `gr.x=64`, and props with local X = 0 and prop 43 = 1.
- South: the frame at global y 64.0 carries PLI 39 and the flag; the props with local Y = 0.5 and prop 44 = 1 follow in the next half-step frame (position props go out only on whole-tile steps).
- West and north follow the same pattern with the wrapped coordinate and the cell prop set back to 0.
- Rule: local = global − 64 × cell. The cell prop changes in the same props message as the wrapped coordinate.

Server answer to each crossing (one frame): id 6 new level name, id 39 level mod time (only when not cached), id 0 empty board, id 6 gmap name, 174, 10, 156 gmap name. A second visit omits the server's 39.

Login on a gmap: server sends PLO_PLAYERWARP2 (49) with x×2, y×2, z+50, gmap cell x, gmap cell y, then the gmap name. It follows with PLO_LEVELNAME (6) = the level, then 6 = the gmap file name. The client asks for the gmap file. The first big server frame also carries the neighbour levels' boards. The client sends PLI_ADJACENTLEVEL (35) at login for the three neighbour levels (GINT5 modtime + name; modtime is 0 on a cold cache).

## Buddy, ignore, mute (2.22)

- Buddy add and delete: no network traffic. The client writes and deletes `buddyaccounts.txt` locally (deletes the file when empty). `verifybuddies` / `addbuddy` / `deletebuddy` were not sent in this lab, so the listserver-side token layout is still unseen.
- Ignore: local too (`ignoredaccounts.txt`, one account per line). No packet.
- Mute: PLI 43 with GSHORT playerId + GCHAR 1 (mute) or 0 (unmute). One message per click. GServer-v2 has no handler (falls into the invalid-packet counter), but two sends did not disconnect.
- Player-list window sections: Staff, Buddies, Guild, Normal, Ignore. Right-click: Message, History, Buddy, Ignore, Mute, Profile.

## Gen-5 XOR confirmation

Client-originated frames in the 2.22 sessions: ctype 0x02 uncompressed (580) and ctype 0x04 zlib (17). No ctype 0x06 (bz2) was sent; the bz2 path stays unseen (needs a send over 0x1000 bytes).

The 17 zlib frames have compressed bodies whose lengths mod 4 are 1, 2 or 3, never 0. All 17 decode and decompress with the one-step-per-group rule (partial last group steps, cap 4 for zlib). The old floor rule fails on them. So the corrected rule matches a real client, including short frames.

## Missing binaries

No 2.1.x (2.1 through 2.16) or 2.3 binaries are recoverable. Those rows stay inferred from neighbours and release notes. Practical treatment: alias 2.1–2.16 to 2.05 or 2.17, and 2.3 to 2.31.
