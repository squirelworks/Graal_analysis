# Offline lab for live captures

Date: 2026-10-21

This is how the 2.05 and 2.22 captures cited as **[cap]** in the protocol notes were made. Nothing here touches a public server.

## Isolation
- **Network:** everything runs inside a Linux network namespace with only loopback up (`unshare --net --mount`, then `ip link set lo up`). The clients have no route anywhere else, and DNS fails outside the hosts file.
- **Hosts file:** a private one is bind-mounted over `/etc/hosts` inside the mount namespace. It points `www.graalonline.com`, `listserver.graal.in`, `listserver.graal.cc` and `listserver.graalonline.biz` at 127.0.0.1.
- **Display:** each client gets its own Xvfb display, and Wine runs with a separate 32-bit prefix per client. Two copies of the same game folder let two clients run at once. Give them different `fixedudpport` values and set `noudp=false`, `fixedport=true`.
- **Capture:** `tcpdump -i lo` inside the namespace.

## Game server
- GServer-v2 built without the V8 NPC server.
- Stock GServer does not know `GNW03081`.
  - Mapped to a pre-2.1 version slot, the login sequence never finishes: the client sits on the loading screen.
  - Putting `GNW03081` in the **2.1** slot of the client version table and adding it to `allowedversions.txt` lets 2.05 log in and play.
- 2.22 (`GNW03014`) works unchanged.

## Listserver stub
A small script that speaks both sides:
- **Server side, port 14900:**
  1. Read the uncompressed `REGISTERV3` line, then zlib frames.
  2. Record `NEWSERVER`.
  3. Answer every `VERIACC2` with `SUCCESS`, echoing account, player id and type.
  4. Answer ping.
- **Client side, ports 14921/14922/14923:**
  - On id 0 (2.05 `newmain`) or id 1 (account/password), send id 0 with the server list and id 2 with a status line.
  - On id 7 (2.22), take the key and switch to post-2.2 framing.

Lab accounts are throwaway names with dummy passwords. This lab's stub accepts any password (other stubs may check accounts), and the logs print account names only. Captures still contain the dummy passwords in clear, so they stay out of the repo.

## Decoding
- **TCP:**
  1. Reassemble each direction.
  2. Split `u16be` frames and inflate (post-2.2 frames: undo the partial XOR first).
  3. Split lines on `\n`.
  4. For 2.05 client→server lines, replay the gen-3 iterator from the key in the login line and delete the byte at `(it & 0xFFFF) mod len(line)`.
- **UDP:** XOR each datagram with `recipientId XOR 1`, where the recipient is the player who owns the destination port. The first byte is then `seq`, the second the UDP id. See `protocol/udp-p2p.md`.

## Capture set
The **[cap]** tags in the protocol notes come from four runs in this lab, all on 2026-10-21:
1. 2.05 listserver exchange and one 2.05 game login.
2. 2.05 and 2.22 game logins, and the 2.22 listserver handshake.
3. Two 2.05 clients in one level with UDP enabled. This is the source for the UDP key and payloads.
4. Two 2.05 clients and a bomb next to bushes. This is the source for the board change, item drops and respawn.

The pcaps stay on the lab machine. Only the decoded text, with credentials removed, is kept outside it.
