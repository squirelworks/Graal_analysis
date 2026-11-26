# Batch W, fifth pass: Tiger Mac clients on our server (2026-11-26)

Date: 2026-11-26. Follows [3d-batch-w-rows-part3-2026-11-26.md](3d-batch-w-rows-part3-2026-11-26.md).
Captures, logs and screenshots stay in the owner-held lab kit. **[lab]**

## Setup

- **Server VM:** an offline Debian 13 QEMU guest (512 MB) runs seihai-listserver 0.1.1 (`d542419`)
  and seihai-gserver 0.1.0. The gserver is a Linux build of `5daf3b9`, from the #206 era, so it
  predates main at `8800c2b`. The guest also runs DHCP and a DNS that answers only the login and
  listserver names (everything else gets NXDOMAIN).
- **Client VM:** a Tiger PPC QEMU guest (1 GB) joined to the server only by a QEMU socket link. It
  has no user-net and no route out.
- **Clients:** both run unchanged under the gdb render shim:
  - Mac 3.153 (`G3D28015`), protocol 19.
  - Mac 4.20r6 (`G3D27076`), protocol 21.
- **World:** a Sun, a Sky with 6 entries and two `.3ds` cubes. Run A gives the client Camera
  control. Runs C and D give it Player control, with the `tgeplayershape` set to `octahedron.dts`.
- **Capture:** one capture on the server NIC covers every run (18,351 frames).

## T3D-089 Part B: 3.153 against seihai-gserver

What works:

- The listserver lists the server, and the generation-5 login works.
- The client links at protocol 19. With Camera control it is ghosted a Sky and a Camera; with
  Player control, a Sky and a Player.
- The mission start finishes and the control object is acked.
- Moves flow: one client sent 15,400 in run C.
- **No crash.** Against gs2emu the client crashed on its first frame (EXC_BAD_ACCESS; see
  [live-3153-and-404r2-sessions-2026-11-25.md](live-3153-and-404r2-sessions-2026-11-25.md)).
  Against our server it stays up.

What does not work yet:

- **No 3D frame is seen.** The window stays on the loading bitmap, with only a sky gradient across
  the top.
- The client logs `zero-scale not allowed` in phase 2.
- The world's `.3ds` objects are not ghosted to protocol 19 at all.
- **Sky textures go out twice.**
  - The server answers bare-name requests first.
  - Each `.gif` request then gets both a "sent" and a "not sent" for the same name.
  - `conf_sky4.gif` and `conf_sky5.gif` go out twice, first at 135/137 bytes and then at 232.
- **Chat is unverified.** Tab opens the chat bar and takes text, but Enter sent through the VM's
  input channel did not submit it.

**Verdict:** partial. Against our server, 3.153 logs in, links, holds and sends moves without the
gs2emu crash. Nothing is drawn past the loading screen. The next things to fix are the zero-scale
object and the doubled sky file sends.

## T3D-067: two 3.153 clients at once

There was not enough host RAM for a second VM, so both clients ran as two instances in one guest,
from two copied folders.

- Both log in, as players 1 and 2, link at the same time and hold. In run C they sent 15,400 and
  5,303 moves.
- **How the other player appears:**
  1. When the second client logs in over TCP, the first is sent a 2D placeholder ghost for it.
  2. About 0.3 s later, the second client's 3D link comes up and the placeholder is replaced by a
     **Player** ghost: the stock TGE Player.
  3. The second client is sent the first one's Player ghost at mission start.
- The second client's 3D link request reaches the server before its TCP login is matched. The
  server logs that no TCP login matches it yet, then pairs the two correctly.

**Verdict:** answered at link level. 3.153 is shown another player as a stock TGE Player ghost, and
two 3.153 clients share a world cleanly. It could not be checked on screen, because neither client
draws past the loading bitmap (T3D-089).

## T3D-072: the protocol-21 leg (Mac 4.20r6)

- The client logs in through the built-in lobby and links at protocol 21.
- It is ghosted a Sun, a Sky, the two cube GameObjects, its own GameObject and a Camera.
- The control object arrives and the client logs `Graal has been activated!`.
- **It draws its first 3D frame with no crash,** even though the Sky has only 6 entries. So this
  server build already sends a Sky that protocol 21 accepts.
- The view is sky over a flat red fill. This comes from the guest's software GL, the same as in the
  2026-11-20 lab.
- The client answers pings every 30 s.
- **The server got 0 moves.** The client sent only 5- and 21-byte UDP payloads: 475 up and 304
  down in about 3 minutes. Holding the arrow keys made no difference. No chat UI was found.

**Verdict:** a protocol-21 client links and draws on our server. Together with the 19/24/24 run in
[3d-multiclient-coexistence-066-072-211-512-2026-11-26.md](3d-multiclient-coexistence-066-072-211-512-2026-11-26.md),
all three protocols now link to the same server code. This run did not have a 21 and a 19 or 24 in
one world at once. That, and why 4.20r6 sends no moves, are still open.

## Open

- 3.153: the zero-scale object, the doubled sky sends, and `.3ds` objects not ghosted to protocol
  19. Then retry for a first frame.
- 4.20r6: why no moves are sent, and one world that holds 19, 21 and 24 together.
- Re-run on gserver main, since this run used `5daf3b9`.
