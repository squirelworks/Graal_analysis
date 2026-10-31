# Lab run: the real Mac 4.20r6 and 3.153 clients on Mac OS X 10.4 in qemu

Date: 2026-10-31. Tags as elsewhere: **[cap]** seen on the wire or on screen in this run. Raw captures (proxy logs, pcaps, screenshots, the qemu driving scripts and `aglshim.c`) are in the project files under `v4/lab-mac420r6-2026-10-31/` and `v3/lab-mac3153-2026-10-31/`.

## 4.20r6

The real `Graal.app` 4.20r6 (upload sha256 e1b60bcc…1d9d, executable unmodified) ran on
Mac OS X 10.4 Tiger (retail DVD, build 8A428, archive.org `macosx10.4tigerretaildvd`,
MD5 28b3352b8b125469f23ed9c3e386f4a3, matches archive.org) in `qemu-system-ppc 8.2.2 -M mac99,via=pmu`,
in the cloud container. Server: `seihai-lab/servers/seihai-lab-servers.tar.gz` (GServer-v2 efb5b90)
started with `./run-lab.sh stock`, `G3D27076` added to `allowedversions.txt`, the gserver's `listport` and
the lab listserver moved to 14899. `scripts/warpproxy.py` (the 6.x lab proxy, warp host changed to the
qemu host address 10.0.2.2) listened on 14900; the guest's `/etc/hosts` pointed
`loginserver{,2,3}.graalonline.com` at 10.0.2.2, as in the 4.04r2 Wine lab. Account `seihaimac`, throwaway password.

### Login line (captured, `run2.pcap`, `proxy.log`)

    %  <key>  G3D27076  )seihaimac  'labpass  mac,"",a87b712247c6c9068448ba8c2f68a24b,""\n

- id 5, then the key byte, the token `G3D27076`, account and password as GSTR, then the comma list.
- Four comma fields: `mac`, `""`, a 32-hex MD5, `""`. The same line was sent on both connections (Login server and after the 178 warp).
- Field 2 (the binary's hash of the primary Ethernet MAC from IOKit) came out **empty**, as `""`. The guest has a qemu `sungem` NIC with a MAC, so the client's IOKit lookup found nothing it accepts there. Whether a real Mac fills it is not shown by this run.
- Field 3 (hash of `stat("/etc")`) is a plain lowercase 32-hex string.
- Field 4 is `""`, as the static read said.
- Seihai's 4.20r6 row sends `mac,"","",""`. That matches the shape and the empty fourth field. The real client fills field 3.

### Client sends seen (C→S ids)

Session 1 (Login server, before the warp) and session 2 (after the 178 warp to `0,Lab Server,10.0.2.2,14900`):

| id | what | when |
|---|---|---|
| 37 | `English` | first, both sessions |
| 23 | `basepackage.gupd` twice, `bigmap.txt` (session 1 only), then gani/image/font names (`+.gani`, `wbomb1.png`, `wbowi1.png`, `chest.png`, `helveticabd.ttf`, `helvetica.ttf`, `arialbd.ttf`, `state.png`, `sword1.png`, `idle.gani`, `steps.wav`, `sword.gani`) | |
| 157 | `     +`, `     idle`, `     sword` (gani change) | |
| 46 | `!` | |
| 44 | empty (answer to 182) | |
| 2 | props: first `00 "" / 18=20 / 31=0 / 33=0 / 52 "English" / 75 "mac" / 76=0` (decoded with GServer-v2's prop sizes; raw in `proxy.log`); walking sends **78/79 (X2/Y2)**, prop 10 gani `walk`/`idle`/`sword`, chat prop 12 | |
| 34 | `&w6\x87$pics1.png`, `&w6\x87#defaulttextedit.png` | |
| 24 | `)` repeated | |

So the ids seen are 2, 23, 24, 34, 37, 44, 46, 157. Against `4.04-4.20.toml`'s 4.20r6 `pli_sent`
(4.20r8's list plus 162), **34 and 46 are missing from that list** but the real client sends both. Seihai's chain
already takes 34 and 46 as sent (from 3.153), so Seihai's set covers what was seen.

Not seen: id 18 (flag set). Seihai's 4.20r6 lab run sent `18 gr.x=30` / `gr.y=30.5` from the lab's `gr_movement`
weapon (`setstring gr.x,…`); the real client ran the same level and weapon and sent no 18 in either session.

Window title stayed empty; the level, HUD (A/S/D, AP) and chat text (white with a blue shadow) drew. The player sprite
did not draw: this server pack has no body/head art (the 4.04r2 lab copied 2.22 `graal_reborn` art for that).

### Server ids received (session 2)

4, 6, 7, 9, 10, 14, 25, 30, 33, 34, 39, 41, 42, 43, 47, 82, 100, 101, 168, 182, 190, 194. The client stayed connected
through all of them, including 41 (no case in the static read).

### Notes and caveats

- **qemu has no 3D**: the client asks AGL for `RGBA, DOUBLEBUFFER, ACCELERATED (0x49), NO_RECOVERY (0x48), DEPTH 32/16`
  (static: `FUN_0018acbc` in `mac420.c`) and stops with "Could not find valid pixel format" (`console-unshimmed-run.log`).
  `aglshim.c`, built in the guest with the DVD's gcc 4.0, is injected with `DYLD_INSERT_LIBRARIES` and drops only those
  two attributes, so Apple's software renderer is used. The executable and its signature files are untouched.
- First try was on the beta4 pack: GServer-v2 beta4 **segfaulted** (strlen on NULL in libc) on this login
  (`proxy-run1-beta4-crash.log`, `run1-beta4-crash.pcap`). The efb5b90 stock pack accepted it.
- One stray chat line (`curl …`, typed into the game by mistake) is in `proxy.log` at the end; ignore it.
- `scripts/` has the qemu driving scripts (monitor screendump, closed-loop mouse for Tiger's relative USB mouse, typing).

## 3.153

The real Mac `Graal.app` 3.153 (from the `GraalSetup.dmg` upload, executable sha256 6eb0a1f9…83fc, unmodified) ran on
the same Tiger 10.4 qemu guest as the 4.20r6 run (the 4.20r6 section above), with the same
`aglshim.dylib` (drops only AGL_ACCELERATED and AGL_NO_RECOVERY so the software renderer is used).
Servers: `seihai-lab-servers.tar.gz` (GServer-v2 efb5b90) with `./run-lab.sh stock`, `G3D28015` added to
`allowedversions.txt`. The lab listserver (`listserver-lab-qemu.py`) is the pack's, with two lab edits: its gserver port
moved to 14899, and the server entry's address is given as `10.0.2.2:14910` (the qemu host and the logging proxy) in
place of 127.0.0.1. The guest's `/etc/hosts` pointed `listserver{,2,3}.graalonline.com` at 10.0.2.2.
`warpproxy.py` ran with `NOWARP=1` on 14910 → 14802 (no 178 injection). Account `seihaimac`, throwaway password.

### Listserver

`listserver.log`: one connection to 14922, id 7 in gen 5 with token `G3D30123` and list `newmain`, then id 1 with the
account. The client showed the server list (tab "Hosted") and connected from it.

### Game login (captured)

First frame (plain zlib), four messages in one frame:

    5   %<key>G3D28015)seihaimac'labpass
    37  English
    34  #\x9dyO$bigmap.txt     34  #\x9dyO$minimap.txt     (then both again)

No platform/machine comma list on the login line (unlike 4.x). Same layout as the 3.04 Linux lab capture, with the
token `G3D28015`.

First props (id 2): `0 "unknown"` (the start window's nickname field), `18=20`, `31=0`, `33=0`, `52 "English"`,
**`75 "mac"`**, **`76 = 1250`** (GINT bytes `20 29 82`). Seihai's 3.153 row took OSTYPE mac from the binary and the code
page 1250 from 3.04; both are now seen on the wire.

### Walking: X2/Y2 confirmed

Walking sends props **78 (X2) and 79 (Y2)**, never 15/16 (old X/Y):

    2  *$walk1#n'p          (gani walk, sprite/dir, X2)
    2  n'\x80  n'\x90 ...    (X2 every ~150 ms)
    2  *$walk1"o)0  o)@ ...  (Y2)
    2  *$idle

So Seihai PR #294 (3.153 profile to X2/Y2) is right.

### Non-`client.` flags

The lab level has the `gr_movement` weapon (`//#CLIENTSIDE … setstring gr.x,…; setstring gr.y,…; timeout=0.05`).
In this session the client sent **no id 18 at all** (0 in `proxy.log`), while walking for several seconds.
The 3.04 Linux lab run did send 18 for this script, and Seihai's 4.20r6 lab run sent `18 gr.x=30`. The real 4.20r6 Mac
client also sent none. What this run cannot tell apart: 3.153 not sending non-`client.` flags, or the script not
setting them in this build. The real client shows the same nothing either way.

### Other sends

C→S ids seen: 2, 23, 24, 34, 46, 157 (plus 5 and 37 in the first frame).
- 34 UPDATEFILE for `wbomb1.png`, `wbowi1.png`, `defaultbutton.png`, `playerlist_icons.png`, `walk.gani`, `sword.gani`,
  `steps.wav`, `steps2.wav`, `sword.wav` (3.x uses 34 where 4.20r6 used 23 for ganis and sounds).
- 157 with the gani name (`     walk`, `     sword`), 46 `!`, 23 `chest.png` and others.
- 24 `)` about every 16 to 18 s (614.06, 632.99, 650.49, 666.74, 683.90).
- Sword: 34 `sword.gani`, 157 `sword`, prop 10 `%sword`, 34 `sword.wav`, then `idle` 0.75 s later.
- Chat: prop 12 (`,/hello from 3153`), drawn white with a blue shadow above the head.

Server ids received: 4, 6, 7, 9, 10, 14, 25, 30, 33, 34, 39, 41, 42, 43, 47, 82, 100, 101, 168, 182, 190, 194.
The player sprite drew (3.153 ships its own body/head art).
