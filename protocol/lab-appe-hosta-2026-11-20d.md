# Appendix E lab runs on lab host A, fourth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. The lab host A: the Debian VM, its Win10 guest and a macOS
15 guest, on loopback only. No public service was contacted. The earlier batches are
[`lab-appe-hosta-2026-11-20.md`](lab-appe-hosta-2026-11-20.md),
[`lab-appe-hosta-2026-11-20b.md`](lab-appe-hosta-2026-11-20b.md) and
[`lab-appe-hosta-2026-11-20c.md`](lab-appe-hosta-2026-11-20c.md).

## RC2 2.05's list of other RCs (E#424)

Client: `RC2_2.05.exe` (title "Remote Control 2006/12/20", token `GSERV025`), run natively in the
Win10 guest. Server: the seihai GServer-v2 fork (4.0.0-beta of 2026-11-20, with the same RC list
code as the 2026-11-14 build) and its listserver, with a second RC (the Seihai RC command-line
client).

- RC2's Players window is a flat list under group header rows, not an indented tree. A row belongs
  to the header above it. The counts shown on the headers stay 0 in every case, so they mean
  nothing.
- With the fork's one-space level, the other RC was listed under "Players" with an empty Level
  column, whichever RC logged in first. This is Claim B.
- Then, with the account files untouched, the gen-5 probe proxy injected three RC entries (add-player
  message 55) into RC2's live session that differed only in their level:

| Level sent | Where RC2 lists it |
| --- | --- |
| empty (length 0) | under "Admins" |
| one space | under "Players", with a blank Level column |
| `gs1lab.nw` | under "Players", with the level shown |

- So RC2 2.05 sorts on whether the level string is empty, with no trimming. Claim A (an empty level
  goes to Admins) and Claim B (the fork's one space goes to Players) both hold.
- Side note: the listserver counted the online RC as one player.

## The 6.03r7 HUD on Windows (E#326)

Build: the packed Windows 6.03r7 ("Graal 6.0.3.7", token `G3D0311C`) in the Win10 guest, against the
fork gserver with a server-warp NPC, through the Seihai listserver, with the built-in guest account.
It runs with the guest's current clock (2026-11-20); no clock hold is needed. Measured at 640 × 480,
800 × 600 and 1024 × 768 (`windowmode` in `game_config.txt`), in client-area pixels.

- The tab letters have the same boxes (x, y, width, height) at all three sizes: "A" (17, 37, 15,
  16), "S" (82, 37, 13, 16), "D" (148, 35, 14, 18). Each letter sits about 2 px right of its tab's
  left edge (the tabs start at x 15, 80 and 145) and 7 px below the tab's top. So Windows text is
  anchored top-left, as on Linux.
- Two items the chapter did not list: a blue "1" beside the sword at (122, 37, 7, 15), probably the
  sword power, and a small white mark above the D tab at (147, 29, 6, 6). Neither moves with the
  window size.
- The hearts stay anchored top-right: the red right edge is 70 px in from the right edge at 640 and
  at 800 wide, which fits the 68 px three-heart margin plus anti-aliasing. The 1024 window ran off
  the 1024-wide guest desktop, so it was not measured.
- Not covered: 1280 × 1024 and other heart counts.

## Mac 6.004 and 6.015 with working OpenGL (E#618)

Guest: macOS 15.8.3 Sequoia, with working software OpenGL (6.11r1 draws there). Its network card was
restricted, and the guest's hosts file pointed the login host names at the guest's own loopback for
the run (restored afterwards). Server: the Seihai gserver inside the guest, on loopback. Clients:
the x86_64 slices of the held Mac builds, started from Terminal in the logged-in session.

- **6.015** (`G3D3107A`) logged "Initialized OpenGL. Maximum texture size: 16384", then logged in,
  entered the start level and asked for its files (`idle.gani`, `pics1.png` and others), the same
  login as on Lion. The main "Graal" window stayed blank, plain system grey rather than white, for
  the whole run, also when brought to the front. A separate small "Select File" window did draw
  Graal's blue GUI skin, though its controls had no text.
- So the 6.0x main view stays empty on Sequoia even with OpenGL. Lion's white window was not only
  the missing OpenGL: something in how the 6.0x Cocoa view draws on a modern macOS is involved too.
  6.11r1 behaves differently.
- **6.004** printed its "This is a beta release of Graal…" notice and quit at once, with no window
  and no connection. That looks like a beta time limit against today's date, but no clock-held run
  was possible on that guest.
- Both clients report "MacOS version: 10.9.0". A 10.9-era guest was not run.

## Android Classic 1.8 on an emulator (E#18)

Setup: Android-x86 9.0-r2 x86_64 (the official image, size and checksum checked), booted live in
QEMU/KVM inside a loopback-only namespace. A lab DNS answered every name with the lab host. The
setup wizard was switched off at boot, so no terms were accepted. Client: GraalOnline Classic 1.8
for Android (version name 1.8). It ships x86_64 native libraries, so it ran natively.

- The client started and initialised OpenGL ("GraalClassic has been activated!", maximum texture
  size 8192). It made no game connection.
- Its first network step is a connector fetch, the same pattern as Mac 6.11r1: a name lookup for
  the publisher's connector host, then HTTPS on port 443 (a TLS 1.2 hello with no server name and an
  old RSA-only cipher list). When that failed it fell back to plain HTTP, asking for `conf.gs` with
  a long token in the query, with the user agent "Graal/6.15401". The token stays in the lab
  capture.
- With no valid connector reply it waits on a black screen and never dials a login server or a
  listserver, so no game frame was seen. The connector reply is a server-signed script the lab
  cannot make (→ §2.10), so a loopback run cannot get past this step.
- So Android Classic 1.8 is on the 6.1x connector line (engine string 6.15401), not the older
  direct-login line.
- E#16 (Classic+ 1.13 for iPhone) is not covered: there is no iOS emulator here.

## How a server moves a 5.12 player in 3D (E#505)

Setup: the real Windows 5.12 (`G3D14097`) in the Win10 guest, in a loopback-only namespace, with a
lobby warp to a local copy of the Seihai gserver's Graal3D mode (the 2026-11-20 Camera build). The
copy was changed in the lab only, not in any repo: the player's own control object was given a
section-6 movetype and section-7 movement data (a position, an identity rotation, zero vectors and
a closing flag of 0), and every second the server moved that position 0.5 units along y. All of the
client's own updates were logged. One run per movetype, about 45 s each.

- **No movetype (baseline).** The client reports its control position in every packet (about once a
  second while idle) and sends no object section.
- **interpolate.** The client takes the movement data and glides toward each new target, reporting
  a position about 0.25 to 0.5 units behind it (target 28.0, reported 27.75). In its own update it
  echoes section 7 (movement data) every time, and once at the start sections 3 (shape), 5
  (transform), 6 (movetype "interpolate") and 13 (flags).
- **list.** The client jumps exactly onto each new position (target 25.0, reported 25.0). It echoes
  section 5 (transform) every time, plus the same one-time 3, 5, 6 and 13 at the start.
- **rigid.** The client follows the targets with the same small lag as interpolate, but echoes no
  object section, only the position in each packet.
- Sections 9 (chat) and 3 (shape) were not echoed after the first update. Nothing was typed or
  walked, so keyboard input together with a movetype was not tested.
- The movement-data layout was accepted as read: three 32-bit position values, four 8-bit rotation
  values, six 9-bit vectors and one flag for interpolate and rigid; for list, entries of a flag and
  eight 32-bit values, ending with a flag of 0. No run desynchronised. One early interpolate run
  ended with "The Graal3D server has dropped the connection"; an identical later run went the full
  45 s.
- The 3D view looked the same throughout, because the Camera ghost does not follow the player
  object, so the wire figures are the evidence.
