# PLO 181 — peer-UDP opt-out (`PLO_PLAYERNOUDP`)

Date: 2026-11-16

Server → client id **181** tells the receiving client not to send
**peer-to-peer UDP** to one named player. The TCP copy of that player's
actions still goes through the server as usual.

Tags: **[bin]** · **[srv]** (name / habit only) · **[inf]** where noted.
Canonical earlier write-up: `unknown-ids-2026-11-06.md` §PLO 181. Peer
channel itself: `udp-p2p.md`.

## Layout

| Field | Type | Notes |
|---|---|---|
| player id | `s` (GSHORT) | target other-player object |
| toggle | `c` (GCHAR) | flag set when `toggle > 0` |

Payload must be at least **3** bytes or the packet is dropped. **[bin]**

## What the client does

1. Looks up the player by id.
2. Sets a boolean on that player object from the toggle.
3. The **only** traced reader of that flag is the routine that builds the
   nearby-player list used for peer UDP (within 16 units on each axis;
   on a gmap, neighbouring boards as well). A flagged player is omitted
   from that list, so no peer datagram goes to them. **[bin]**
4. The client's own UDP socket must still be open for any peer send;
   `noudp` / no socket already means no peer UDP.

So 181 is **not** a TCP mute and **not** a disconnect. It only steers the
optional peer channel described in `udp-p2p.md`.

## Build range

| Span | Handle 181? |
|---|---|
| 2.17 through 5.24r4 | yes **[bin]** |
| 5.30r3 and later (incl. 6.x focus builds) | **no** receive case **[bin]** |

Others Work scope that called this "v4 only" is a lab focus, not a
conflict: our chain starts earlier (2.17) and ends at 5.24r4.

## Name

| Source | Name |
|---|---|
| This note / preferred | `PLO_PLAYERNOUDP` |
| Older tables | `PLO_UNKNOWN181` |
| GServer-v2 beta4 / pyReborn cite | `PLO_PLAYERNOUDP` **[srv]** |

`packet-ids.md` and the manual keep `UNKNOWN181` as the legacy label and
point here for behaviour.

## Server habit **[srv]** / **[inf]**

A server would send 181 when a player's UDP port is unusable (NAT,
`noudp`, dead peer port) so other clients stop spraying datagrams that
never arrive. No project capture of a **non-lab** server sending 181 is
on file; confidence on *why* a production host fires it stays medium.

## Open (do not block Seihai)

- Which neighbouring player flags (writers not traced) also drop a peer
  from the nearby list, and when a server sets those.
- Live loopback of 181 while two clients have UDP open (optional; static
  reader already settles the opt-out).
- Whether any post-5.24 build reintroduces an equivalent under another id
  (none seen on 6.03r7).

## Implications for Seihai / labs

- Safe to **name** 181 `PLO_PLAYERNOUDP` and document the layout.
- **Sending** 181 is low priority until a lab world uses peer UDP again;
  classic clients default `noudp=true` on some 2.x rows, and modern focus
  builds drop the id.
- Do not invent a keep/clear interaction with weapons or Login from this
  packet — that is PLO **194** (`plo` reset / CLEARWEAPONS leads), not 181.
