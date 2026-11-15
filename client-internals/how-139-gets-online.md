# How 1.39 gets online (no listserver path)

Date: 2026-11-16. Research-list rank **#8** (focus 1.39).

**Answer:** 1.39 (and the other gen-2 GNW builds 1.33–1.38) has **no listserver or server-list path**. The player edits a host:port in the connect dialog and dials the game server directly. seihai-listserver’s client table correctly starts at **1.41 rev 1**.

Tags: **[bin]** static catalogue and login construction; **[lab]** Wine loopback against GServer-v2 beta4; **[doc]** existing notes cross-linked below. No new binary session in this pass.

## What 1.39 does

| Step | Behaviour | Evidence |
|---|---|---|
| Discover servers | None. No list name, no list ports, no server-list window. | `build-catalogue.md` (“1.39 and earlier have no listserver”); `versions-133-139.md` (“There is no listserver”) **[bin]** |
| Connect dialog | Pre-filled with a classic host:port and the `guest` / `guest` account; the player may edit the address. | `versions-133-139.md` **[bin]**; lab harness uses loopback **[lab]** |
| First game frame | Login message id 0: eight-byte token (`GNW07080` for the catalogued 1.39), then account and password. Gen-2 framing (u16be length + zlib, no cipher). | `versions-133-139.md`; `VERSION-TOKENS.md` `GNW07080` **[bin][lab]** |
| After login | Board / props / files as for other 1.3x builds. No 178 lobby warp (that is a 4.x–6.x Login-mode path). | `versions-133-139.md` live check; `tools/lab-servers/README.md` **[lab]** |

## What it does not do

- It does **not** open a TCP list session (no shape A/B/C list login).
- It does **not** parse a multi-server list reply (ids 0/1/2 as used from 1.41 onward).
- It does **not** need seihai-listserver for an end-to-end play path: point the connect dialog at the gserver (lab classic port **14803** for 1.x on the beta4 pack).

1.41 rev 1 is the first focus build that goes online through a list (`silent_list_after_ms` / shape S). That is a separate open item (research-list **#13**), not a 1.39 gap.

## Lab practice

- Loopback only. 1.39 under Wine against a local classic-generation gserver is enough to confirm walk/chat once the world has the 1.x art set.
- Do not expect a listserver registration or list refresh from this client.

## Open

- None for the list-vs-direct question. Residual 1.39 play gaps (props, combat, etc.) live under other ranks and the version-profile matrix.
