# Appendix E lab runs on lab host A, fifth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. The lab host A: the debian-lab446 Linux VM, on loopback
only. No public service was contacted. The earlier batches are
[`lab-appe-hosta-2026-11-20.md`](lab-appe-hosta-2026-11-20.md) to
[`lab-appe-hosta-2026-11-20d.md`](lab-appe-hosta-2026-11-20d.md).

## Windows 4.04r2 pickup in offline mode under Wine (E#611)

**Setup.** No Windows XP or 32-bit Windows 7 VM exists on lab host A, so the client ran under Wine 10
(32-bit loader, 32-bit prefix) inside the debian-lab446 VM, on a headless X server, in a network
namespace with only loopback. The client was the extracted 4.04r2 install (the same build as the
single-file 4.04r2 exe of the earlier labs); the executable and engine DLL were checked unchanged
against the originals. The login screen's "Offline Test" button starts offline mode in the tutorial
map, at the level `offlinetutorial_b-2`, with the player at x 30.5, y 40, facing down. A work copy
of that level got four 2 x 2 bushes on plain grass beside the start (one directly below the
player, three to the right). The tutorial loads its own tileset image, which has water where the
classic bush tiles sit, so the work copy also gained one script line that overlays a 32 x 32 bush
picture from the classic tileset onto those tiles. Faked time was not needed.

**Keys.** The tutorial level script calls `disableweapons`. With that in force, D (item) and S
(sword) did nothing when pressed facing a bush: no animation and no tile change. A, the action key
in the default key set, is the pickup key.

**Lift.** Facing down at the bush, one tap of A removed the bush at once: its four tiles changed to
the "picked up" tiles, which in this tutorial show as white placeholder squares because the
tutorial tileset has no picture there. With the stock offline files nothing else happened on
screen. The offline install has only the tutorial's `human2` animations (idle, walk, grab, push,
pull, swim, sit) and no lift or carry animation, so the player stayed in the idle pose and no bush
was drawn above the head. In a second run with the classic lift and carry animations added to the
work copy, the same A press played the lift animation and then held the carry pose. The head and
hair drew but the body did not, because the tutorial's body image has a different layout from the
classic one. In neither run was the carried bush drawn above the player.

**Carry.** Walking while carrying moved the player normally in both runs, and with the added
animations the carry walk played (with the same partial drawing). Nothing was left at the old spot
except the placeholder tiles, and the bush did not grow back during the roughly two minutes of each
run.

**Throw.** A second tap of A (facing left in the first run, up in the second) ended the carry at
once, and the player went straight back to the idle pose. No flying bush, landing or leaf burst was
drawn in any frame (frames every quarter second for about two and a half seconds). Whether the
object was thrown unseen or simply dropped cannot be told from the screen.

**Console and log output.** None for any of the actions. The console log held only the start-up
lines (DirectDraw and Direct3D 7 set up, "Graal has been activated!", the sound driver line). With
the single-file exe it also logged that it could not open the offline tile-definitions file in its
levels folder for writing.

**Pickup-bound field and carried category.** Not recorded: no debugger or memory reader is set up
for 4.04r2 on this machine.

**What did not work.**
- The first three starts failed with "DirectX couldn't be initialized" and looped through DirectDraw
  set-up, because the first Wine prefix used Wine's GDI renderer. A prefix on the default OpenGL
  renderer fixed it for both the single-file exe and the extracted install. Seven starts in all, two
  of them used for the actions.
- The stock offline files cannot show the lift or carry at all, and even with added animations the
  carried and thrown object is never drawn, so the throw itself is not visible.
- Only the bush below the player was used; the three to the right sat partly under a palm's leaves.

Compared with the Win10 guest runs (→ [`lab-appe-hostb-2026-11-20d.md`](lab-appe-hostb-2026-11-20d.md)),
Wine with the OpenGL renderer gives a repeatable offline scene for 4.04r2.

**State afterwards.** In debian-lab446 the Wine client, wineserver and X display were stopped and
the work folder deleted; the VM was left running for other work. The work level, added files,
frames, logs and run scripts are kept on lab host A outside any repository. The client files are
unchanged.
