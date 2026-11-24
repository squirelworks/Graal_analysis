# Mac 6.004 beta date gate (E#618)

Date: 2026-11-24. Tags: **[bin]** for the static read of the held Mac 6.004
`Graal.app` x86_64 slice; **[lab]** for earlier Lion / Sequoia runs cited below;
**[inf]** for what a clock-held live frame still needs.

This is the Protection follow-up for Appendix E **E#618** / board **G029**: whether
Mac 6.004 and 6.015 draw a game frame once 6.004's clock is held before its beta
limit. It does not replace the slice study in
[mac-6004-6015-slices.md](mac-6004-6015-slices.md) or the guest runs in
[lab-mac-v6-6015-lion-2026-11-16.md](../version-profiles/lab-mac-v6-6015-lion-2026-11-16.md)
and [lab-appe-hosta-2026-11-20d.md](../protocol/lab-appe-hosta-2026-11-20d.md#mac-6004-and-6015-with-working-opengl-e618).

## What was already known from lab

| Build | Guest | Result |
| --- | --- | --- |
| 6.015 | Lion 10.7.5, no OpenGL accel | Graal window opens; content stays white; process stays up **[lab]** |
| 6.015 | macOS 15 with software OpenGL | OpenGL initialises; client logs in, enters the start level and asks for its files; main window stays blank system grey; a small "Select File" window draws the GUI skin **[lab]** |
| 6.004 | macOS 15 (current date) | Prints the "This is a beta release of Graal…" notice and quits at once; no window, no connection **[lab]** |

Both clients report `MacOS version: 10.9.0`. A 10.9-era guest with OpenGL was not
held for a clock-held 6.004 run. **[lab][inf]**

## Static beta gate on Mac 6.004

The Mac 6.004 x86_64 image carries the same beta-notice string the Sequoia run
printed. Mac 6.015's image does **not** carry that string and has no matching
fixed cutoff constant. **[bin]**

On the 6.004 x86_64 slice, the start path that emits the beta notice also reads
the wall clock and compares it to a fixed unix cutoff. If the clock is **after**
that cutoff, the path returns failure (no window / no connection), matching the
Sequoia observation. The cutoff is **2011-09-08 19:22:31 UTC** (2011-09-09
04:22:31 Asia/Tokyo). At day resolution that is the same stop day as Windows
6.00r4 from the E#14 / G148 clock search (last pass day 2011-09-08, first stop
day 2011-09-09). **[bin]**

So a clock-held Mac 6.004 run needs the guest clock set **on or before** that
cutoff for the whole session (a mid-2011 date in the Windows 6.00r4 pass window
is enough). **[bin][inf]**

## Frame / login / level — answer with limits

- **6.015:** logs in and reaches level-file requests on both Lion (wire) and
  Sequoia (OpenGL + wire). The **main** Cocoa game view does **not** draw a
  playable frame on those guests; only auxiliary GUI (Sequoia "Select File")
  showed the skin. **[lab]**
- **6.004:** the beta quit on a current-date Sequoia run is explained by the
  static date gate above. The lab-host-A experiments list (L1) calls for a
  clock-held Mac 6.004 run on the Sequoia guest, noting a full main-view answer
  still wants a 10.9-era OpenGL guest. Owner confirmed Lion and Sequoia guests
  exist on lab host A for this pass; Lion is preferred for the old binary.
  From the Windows lab host used here, guest control (start / QMP / VNC / SSH
  into the Mac guests) was not reachable — shared-folder sync only — so the
  clock-held live frame was **not** observed on this pass. **[lab][inf]**
- The residual settler remains a **clock-held Mac 6.004** on a reachable lab
  host A Lion (preferred) or Sequoia guest, and ideally a 10.9-era OpenGL
  guest for the main-view draw. **[inf]**

## Open

- [x] Confirm Mac 6.004's beta quit is a compiled-in wall-clock cutoff (and give
  the day). **Done 2026-11-24 [bin]**
- [x] Confirm Mac 6.015 has no matching beta-notice / cutoff constant. **Done
  2026-11-24 [bin]**
- [ ] Clock-held Mac 6.004 on a Lion / Sequoia / 10.9 guest: does the main view
  draw a game frame after the gate passes?
- [ ] 10.9-era guest with OpenGL for both builds' main-view draw.
