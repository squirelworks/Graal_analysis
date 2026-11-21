# Appendix E lab runs on lab host A, third batch (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. The lab host A Debian lab VM (`debian-lab446`), on loopback
only. No public service was contacted. The earlier batches are
[`lab-appe-hosta-2026-11-20.md`](lab-appe-hosta-2026-11-20.md) and
[`lab-appe-hosta-2026-11-20b.md`](lab-appe-hosta-2026-11-20b.md).

## RC logins on the GServer-v2 fork (E#424)

Server: the seihai GServer-v2 fork (4.0.0-beta of 2026-11-14), with two RC logins, one of them
through the probe proxy.

- A new RC logging in while another RC is online sees that RC listed with the level " " (one
  space).
- The RC already online gets add-player message 55 for the new RC, with a one-space level, and a
  "New RC: name" chat line.
- Both held with and without a `LEVEL` line in the account.
- This is Claim B's server side.
- RC2 2.05 itself was not run to the list. Under Wine 10, after a Pango font fix, its login dialog
  draws, but OK crashes inside the GTK GDK library before it connects. A virtual desktop and XP mode
  did not help. So whether RC2 shows the one-space RC under Players or under Admins is still open.
- Lab note: an empty `LEVEL ` line in the fork's flat-file accounts makes the login fail ("no RC
  rights") and rewrites the account. Leave the line out instead.

## Protocol 19 and 3.153 (E#506)

- The 3.153 half could not be run here. The only real 3.153 held is the Mac PowerPC build, which
  needs the Tiger guest on lab host B. The Linux 3.15r1 installer is a truncated self-extracting bundle
  with no client binary in it, and no Windows 3.153 is held.
- The 4.04r2 half from the first batch stands.

## Mobile clients (E#16, E#18)

- No Android emulator or Android-x86 image is on the lab. Lab host A has `adb` and `fastboot` only.
- Classic+ 1.13 is an iPhone build, so an Android emulator would not cover E#16 in any case.
