# Appendix E lab runs on GwenTea2, second batch (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. Real clients in the GwenTea2 Debian lab VM (`debian-lab446`),
on loopback only, under Wine 10 or natively. No public service was contacted. Captures and
screenshots stay in the lab. The first batch is in
[`lab-appe-gwentea2-2026-11-20.md`](lab-appe-gwentea2-2026-11-20.md).

## The later Graal3D beta at run time (E#504)

Build: the "New Graal 3D Beta Version" `Graal3D.exe` (630,272 bytes, login version `GR3DV003`).
Server: the Graal_analysis reference server, changed in the lab only to accept `GR3DV003` beside
`GR3DV002`, with a fake player in the level as a UDP target.

- **The archive.** The RAR is a solid archive. It holds the exe, `Genesis.dll` (dated 1999-11-17),
  the D3D, Glide and software drivers, the art (a font, the chat bar, corona and shadow bitmaps and
  `startscreen.jpg`), `dema.act` and `genvs.bsp`. 7z on the lab cannot open it, and libarchive stops
  after the first entry because the archive is solid. That is probably why an earlier read saw only
  the exe.
- **The run.** A login form, then a Genesis3D driver picker (D3D HAL full screen and window,
  software window and full screen). With the software window driver it draws the `genvs.bsp` world
  and the `dema.act` player, with the nickname over the head and a chat bar (Tab opens it). It
  logged in, got its props and the level, and played.
- **The wire.** The TCP login is laid out as in `GR3DV002`: version, account, password. UDP position
  datagrams are a 0 byte and props 1 to 5 back to back (10 bytes), about every 50 ms while moving
  and only on a change, the `GR3DV002` shape. A chat line goes as a 1 byte and the text by UDP, and
  as prop 13 on TCP, also as in `GR3DV002`. Height is the second coordinate: the player falls on
  spawn, and a jump moves it.
- **Physics defaults.** With the ten physics and camera keys removed from `graal3dconfig.txt`, the
  walking speed (about 200 units a second) and the jump height (about 32 units) matched the shipped
  values. So the built-in walk, jump and gravity defaults match the shipped file. The run speed and
  the camera keys were not separated.
- Not checked: the D3D driver path, and whether this `Genesis.dll` is byte for byte a public SDK copy.

## A GS2 call to a name the client lacks (E#215)

Setup: GS2 bytecode from the Seihai compiler, delivered as a fresh NPC through the probe proxy.
Clients: Windows 4.20r8 (unpacked, Wine 10), Windows 5.12 and 5.24r4 (Wine), and the real Linux
6.03r7 x64. Results come from the chat the script set, the console log and screenshots.

- An unknown function called as a statement, as a value, as a method on the player, or twice in a
  row: the script went on with the next statement every time, and the next chat line arrived. The
  unknown call's value is 0, equal to `NULL`. Reading an unknown attribute of the player also gives
  0.
- The console logs one line per call: "Function NAME not found in script of …" on 4.20r8 and 5.12,
  and "Function NAME not found in function onTimeout in script of …" on 5.24r4. The method case
  names the object ("Function Player <account>.NAME not found"). Reading an unknown attribute logs
  nothing.
- Five of the eight GS2-only names were called on all four builds and worked: `md5("abc")` gave the
  right digest, `keydown2` returned 0, `findimg` returned an object, `findweapon` of a missing weapon
  returned `NULL`, and `onwall2` returned a value that depends on the level. `triggerserver`,
  `scheduleevent` and `cancelevents` were not called.
- Which build first has the names (4.04r2 or 4.11) is not answered by a run.

## Particle modifiers (E#210)

Same setup and clients as E#215.

- **`removemodifiers()`** clears the emit list. An emit-modifier impulse that grew the template's
  zoom by 0.25 every 0.5 s stopped at once, and the template kept its last value. It also removes
  the emitter's live particles: the live count read 0 in the same tick, then refilled. Emission goes
  on, and the running total of emitted particles keeps counting. The same on all four builds.
- **The global modifier clock.** A global "once" modifier fires on the first frame after it is
  added, whatever its time: 2, 3 and 6 s all fired within one 0.5 s step on 4.20r8, 5.12 and
  6.03r7. One added at creation, before any particle existed, changed nothing visible. A global
  "impulse" of 1.5 s grew the live particles in steps about 1.5 s apart, the first about 2 s after
  creation. So "fires on the first frame" holds for "once" even when it is added later, and an
  impulse runs on its interval.
- A global alpha replace of 0 hid the particles on 4.20r8 but not on 6.03r7, where the lab's
  software GL drew untextured particles as plain white squares. On 6.03r7, read the timing from the
  zoom, not the alpha.
- Not done: which property picks the particle kind.
