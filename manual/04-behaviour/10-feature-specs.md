<!-- manual: kind=reference status=draft -->
# 4.10 Other client features

This chapter collects the client features that sit outside the core game loop: the integrity checks, animation state as other players see it, key emotes, the player list and its social lists, and what the client does with the server's start message and disconnect texts. The message layouts are in → §2.4 and §2.5.

> Status: draft. The 2.05 parts are read from 2.05 rev 2; the 2.17 to 2.31 parts come from lab captures and reads of those clients. Open points are App. E#320 to E#322.

## 4.10.1 Integrity checks

### 4.10.1.1 The tamper check (2.17 to 2.31)

From 2.17 the client proves to the server that its code is unchanged. The rules below give the message, how its bytes are laid out and what the CRC words cover [bin][cap] (client-internals/feature-specs/08-tampercheck.md#what-it-is-bincap).

| Rule | Detail | Source |
| --- | --- | --- |
| builds | new in 2.17; absent from 2.05 and 1.x | [bin][cap] (client-internals/feature-specs/08-tampercheck.md#what-it-is-bincap) |
| message | `PLI_TAMPERCHECK` (39), 10 raw bytes, sent right after `PLI_LANGUAGE` (37) in the first frame after login; the per-build values are in → §2.4.9 | [cap] (client-internals/feature-specs/08-tampercheck.md#what-it-is-bincap) |
| what the bytes are | two 32-bit words A then B, each written as 5 bytes in a form that is neither `GINT5` nor masked: only the first and last byte are range-limited, so the middle three can fall below 0x20 | [bin] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md#what-the-10-bytes-are) |
| the words | both are standard reflected CRC-32 values over the client's own image in memory, chained across ranges; A covers 8 or 9 ranges of the code, B one large code range and one block of static data | [bin] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md#what-the-10-bytes-are) |
| constant | nothing depends on the login key, account, level or time, so the value is a constant per build and changes only if the executable's bytes change; all six lab values were reproduced offline from the executables | [bin][cap] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md) |
| 2.17 | sent once at login; nothing more in about 90 s | [cap] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md#when-it-is-sent) |
| 2.22 | re-sent by the level-change routine, so on every gmap edge crossing and after every link request the client starts, but not after a server-side warp; no timer | [cap][bin] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md#when-it-is-sent); [cap] (client-internals/feature-specs/08-tampercheck.md#what-it-is-bincap) |
| 2.31 | re-sent every 3.2 s by the 64-tick integrity cycle of → §4.1.3; not re-sent on level entry | [bin][cap] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md#pli-39-re-send-every-32-s) |
| client check | the clients only send it; nothing on their receive side checks it | [bin] (client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md#does-the-server-verify-it) |
| servers | the open-source server reads and discards it; four public servers accepted a 2.22 login without it for at least 20 s, which shows only that they do not enforce it at login (→ App. E#320) | [srv] (client-internals/feature-specs/08-tampercheck.md#exact-server-behaviour-srv); [cap] (client-internals/feature-specs/08-tampercheck.md#public-servers) |

### 4.10.1.2 Process list and window scan

The server can also ask for a process list, and 2.31 scans windows on its own. The rules below give both checks and when they run [srv][inf] (client-internals/feature-specs/08-tampercheck.md#exact-server-behaviour-srv).

| Rule | Detail | Source |
| --- | --- | --- |
| process list | the server sends `PLO_LISTPROCESSES` (182) once during login to 2.17 and later; the client can answer `PLI_PROCESSLIST` (44) with its running programs (→ §2.4.9) | [srv][inf] (client-internals/feature-specs/08-tampercheck.md#exact-server-behaviour-srv) |
| 2.31 window scan | tick 20 of the 64-tick cycle compares the titles and classes of top-level windows with an obfuscated blacklist; the list is not decoded and what the client does on a match is unknown (→ App. E#321) | [bin] (client-internals/feature-specs/08-tampercheck.md#what-it-is-bincap); [doc] (client-internals/feature-specs/README.md#settled-index-cross-cutting-items-status-as-of-the-lab-batch-c-2026-10-24) |
| 2.31 debugger probe | tick 1 of the cycle probes for a debugger and arms a 5000 ms timer | [bin] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md#pli-39-re-send-every-32-s) |

### 4.10.1.3 What outside input tools look like

The recovered trainers of the period are summarised here only for what the client's checks could see of them:

| Rule | Detail | Source |
| --- | --- | --- |
| how they act | every recovered sample types keys into a classic client window or writes text into it through window messages; none speaks the game protocol | [bin] (recovered-hacks/behaviour-models.md#what-a-server-can-see) |
| memory | no memory-writing or remote-thread imports were found in the unpacked samples, so none of them changes the client's image; the tamper check of → §4.10.1.1 cannot see them | [bin] (recovered-hacks/TRAINER_RE_NOTES.md); [inf] (recovered-hacks/THREAT_TAXONOMY.md) |
| what the server sees | only the resulting actions (dig, use, walk, chat), at the rates the tool's waits allow | [inf] (recovered-hacks/behaviour-models.md#what-a-server-can-see); [inf] (recovered-hacks/static-2026-11-01/README.md#what-a-checker-can-use) |
| window titles | some tools look for the client window by title, and some show their own named window; such a window is the kind of thing the 2.31 scan compares, but whether its list names any of them is unknown (→ App. E#321) | [bin] (recovered-hacks/behaviour-models.md); [inf] (recovered-hacks/TRAINER_RE_NOTES.md) |

### 4.10.1.4 The recovered trainers, tool by tool

The trainers fall into four groups: AFK chat bots, AutoIt input macros, chat and costume script spam, and one archive blocked as malware and never opened; a caps-lock utility filed with them is not a Graal tool [bin] (recovered-hacks/THREAT_TAXONOMY.md#attack-class-overview). Their loops were read statically and none was run; the waits are client-side waits, not server cooldowns, so they are the rates a server would see [bin] (recovered-hacks/behaviour-models.md#what-a-server-can-see).

| Tool | What it sends | Rate and waits | Window check | Source |
| --- | --- | --- | --- | --- |
| AutoD (2001) | `d` | every 1 ms, forever | none | [bin] (recovered-hacks/behaviour-models.md#autod-bin) |
| AutoS | `s#` | no delay, forever | none | [bin] (recovered-hacks/behaviour-models.md#autos-bin) |
| AutoIdle | a fixed pass of 48 left and right arrow taps | no sleep | none | [bin] (recovered-hacks/behaviour-models.md#autoidle-bin) |
| Graal Auto Key | nothing to the game: renames the active window to `Graal Auto` after 2 s, then exits; the other RpgWarrior tools look for that title | once | renames | [bin] (recovered-hacks/behaviour-models.md#graal-auto-key-bin) |
| WaterGet v1.1 | Down twice, `a` | key delay 300 ms, then 2000 ms per pass | none | [bin] (recovered-hacks/behaviour-models.md#waterget-v11-bin) |
| WaterGet v1.0 | `S` nineteen times 1000 ms apart, then two idle directions twice each | 2000 ms, 500 ms between directions | `Graal Auto` must be active | [bin] (recovered-hacks/behaviour-models.md#waterget-v10-bin) |
| Random Walker | one of: nothing, Up, Down, Left or Right five times, or `S` five times, drawn at random | key delay 200 ms | `Graal Auto` | [bin] (recovered-hacks/behaviour-models.md#random-walker-bin) |
| Graal Prayer | Tab, then the chat text `/use_skill praying` and Enter three times 2000 ms apart, a weapon shortcut, `s` ten times, another shortcut and the idle direction; a helper sends Up ten times | key delays 0 to 100 ms, sleeps of 500 to 2000 ms | `Graal Auto` (the helper none) | [bin] (recovered-hacks/behaviour-models.md#prayer-bin) |
| Graal Load | each line of a chosen text file written into the client window, then Return; the bundled `bomb.txt` is 164 lines of costume commands and a countdown | 150 ms per line | finds the window by its text | [bin] (recovered-hacks/behaviour-models.md#graal-load-bin) |
| AFK Bot | three phrases in turn (`I am AFK` and two more) into the focused chat box | one every 3000 ms | none; 3 s to click the chat box or it stops | [bin] (recovered-hacks/behaviour-models.md#afk-bot-bin) |
| AFK Scroll Bot | one phrase scrolled across chat, first character moved to the end each tick | 100 ms tick | none | [bin] (recovered-hacks/behaviour-models.md#afk-scroll-bot-bin) |
| Graal Text Sender 1.3.5 | operator text in six modes (word scroller, middle in-out letters, word stay, two words repeat, letter-by-letter to-alls and shout-outs) | 100 ms timer, per-mode waits set by the operator | looks up the client window; declares `GetAsyncKeyState` but never calls it, so it is not a key logger | [bin] (recovered-hacks/behaviour-models.md#graal-text-sender-bin) |

The trainers recovered from the period were read one by one. Each rule is one tool or archive and what it turned out to be [bin] (recovered-hacks/THREAT_TAXONOMY.md#group-2--rpgwarrior--selzar-autoit-input-macros-gameplay-automation).

| Rule | Source |
| --- | --- |
| The AutoIt tools are compiled AutoIt 2.60 to 2.64 scripts packed with UPX, using only input and window-message calls (`keybd_event`, `mouse_event`, `SendMessageA`, `PostMessageA`, `FindWindowA`, `BlockInput`); the VB6 tools import only the VB runtime | [bin] (recovered-hacks/THREAT_TAXONOMY.md#group-2--rpgwarrior--selzar-autoit-input-macros-gameplay-automation); [bin] (recovered-hacks/TRAINER_RE_NOTES.md) |
| Digger's archive is truncated (36,111 of 41,893 bytes of a UPX image), so its loop is lost; its howto says to equip a shovel, stand on grass and focus the client | [bin] (recovered-hacks/behaviour-models.md#not-recovered) |
| The miner archive is blocked by the file host as malware and was never downloaded, so nothing is known of it beyond its size | [file] (recovered-hacks/THREAT_TAXONOMY.md#group-4--suspected-malware-download-blocked) |
| A static pass over the remaining images found the same input-only pattern and nothing that speaks the game protocol | [bin] (recovered-hacks/static-2026-11-01/README.md) |

## 4.10.2 Animation state as others see it

### 4.10.2.1 2.05: the sprite prop

In 2.05 the sprite prop carries a step number as well as the direction. The rules below give its form, when the step changes and the table from step to value [2.05] (client-internals/feature-specs/11-emotes-ganis.md#205-sprite-prop-205dec).

| Rule | Detail | Source |
| --- | --- | --- |
| form | prop 17 (→ §2.6.2) is direction + 4 × S | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#205-sprite-prop-205dec); [2.05] (client-internals/decomp-findings-2026-10-24/02-sprites-poses-emotes.md#how-the-sprite-prop-17-is-built) |
| when S changes | only while the active gani is the default `def` gani and the step is 38 or lower; other ganis leave S alone, and a name the sender does not know gives 0; read from the sender, not confirmed on the wire | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#205-sprite-prop-205dec) |
| hurt | S = 32, so the prop is 0x80 + direction | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#205-sprite-prop-205dec) |
| step to S, steps 0 to 38 | 0, 4, 5, 4, 3, 2, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 11, 12, 14, 15, 16, 17, 23, 18, 19, 20, 19, 18, 21, 22, 21, 18, 24, 25, 26, 27, 28, 29; steps 9 to 13 are the sword swing (→ §4.3) | [2.05] (client-internals/decomp-findings-2026-10-24/sprite-step-table.tsv) |
| gani to step | idle and def: frame; walk and walkslow: frame + 1; kick 9; sword, ridesword and spin: 9 + (frame mod 5); push 14 + frame; grab 19; pull 20 + frame; lift 23; carrystill and hiddenstill 24; carry and hidden 25 + frame; shoot 33; ridestill 34; ridefire 35; rideeat 36; ride 35 + (frame and 1); sit 37; sleep 38; hurt and ridehurt 39; dead 40, not sent | [2.05] (client-internals/decomp-findings-2026-10-24/gani-to-step.tsv) |
| built-in ganis | 31 names, index 0 to 30: idle, walk, walkslow, kick, sword, ridesword, spin, push, grab, pull, lift, carrystill, hiddenstill, carry, hidden, shoot, ridestill, ridefire, rideeat, ride, sit, sleep, hurt, ridehurt, dead, maps1, maps2, maps3, swim, lava, carried | [2.05] (client-internals/decomp-findings-2026-10-24/gani-name-table.tsv) |
| not on the wire | swimming, lava and death are sent as S 0 plus direction; death travels only as the STATUS dead bit (→ §2.6.2.1, §4.4); there is no swim sprite, so another 2.05 client cannot tell a swimmer from an idle player | [2.05] (client-internals/decomp-findings-2026-10-24/02-sprites-poses-emotes.md#swim-lava-and-dead-on-the-wire) |
| STATUS as 2.05 sets it | 0x01 editor or paused; 0x02 hidden (mode 14 or the hidden timer); 0x04 male; 0x08 dead, only once the death timer reaches 28 ticks; 0x10 weapons allowed; 0x20 sword hidden while the `hidesword` timer runs; 0x40 has the charged spin (→ §2.6.2.1) | [2.05] (client-internals/decomp-findings-2026-10-24/status-bits-prop18.tsv) |
| short codes | the client maps gani-name parts to one letter (attack A, carry C, dead D, hurt H, idle I, kick K, lift L, ride R, sit T, spin U, swim V, sword S, walk W, def X and others) to shorten cached gani file names | [2.05] (client-internals/decomp-findings-2026-10-24/gani-short-codes.tsv) |

### 4.10.2.2 2.1 and later

From 2.1 the gani travels as a name. The rules below give that prop and where its cadence is measured [srv][cap] (client-internals/feature-specs/11-emotes-ganis.md#a-animation-state).

| Rule | Detail | Source |
| --- | --- | --- |
| gani prop | prop 10 is the gani name as a string; a receiver that lacks `<name>.gani` asks the server for it | [srv][cap] (client-internals/feature-specs/11-emotes-ganis.md#a-animation-state) |
| 2.22 cadence | → §4.1.4 | [cap] (live-runs/2gta-222-2026-10-30/README.md) |

## 4.10.3 Key emotes (2.05 rev 2, same routine in 1.39)

Ctrl and a letter shows an emote. The rules below give the keys, how the image is found, where it is drawn and that nothing is sent [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes).

| Rule | Detail | Source |
| --- | --- | --- |
| keys | Ctrl+A to Ctrl+Z, with no text field focused and the player neither dead nor locked | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| lookup | the letter is lowercased and the client takes the first loaded file whose name starts with `emoticon_<letter>` and ends in png, mng or gif; there is no letter-to-name table, so the mapping is whatever files exist | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes); [2.05] (client-internals/decomp-findings-2026-10-24/02-sprites-poses-emotes.md#emotes-ctrlletter) |
| drawing | at the player's x + 2, y − 5 (a little lower when a second flag is set) for 50 ticks (2.5 s) | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| network | the key path sends nothing; `PLI_SHOWIMG` (24) is sent only by the script command `showimg` (→ §8.2) | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| others seeing it | unmeasured: captured SHOWIMG frames re-sending an AFK image about every 3 s are not explained by the key path (→ App. E#322) | [cap][inf] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| earlier builds | 1.38 introduced Ctrl+letter emotes, and 1.39 added letters | [doc] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |

## 4.10.4 Picking up and dropping items online

Items are picked up and dropped through four messages. The rules below give each one and what the server does with it [cap][srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap).

| Rule | Detail | Source |
| --- | --- | --- |
| 2.05 pickup | sends `PLI_ITEMDEL` (13) with the item's half-tile position and changes its own props itself; the server only removes the item and tells the others | [cap][srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| the other form | `PLI_ITEMTAKE` (32) also removes the item, and the server applies it to the player's props and echoes them | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| drop | `PLI_ITEMADD` (12) with the position and item | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| chest | `PLI_OPENCHEST` (20) with whole-tile x and y; the opened state is per account (→ §4.5.4) | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |

## 4.10.5 The player list and social lists

### 4.10.5.1 2.05 (F7)

The 2.05 player list is opened with F7. The rules below describe its window, its popup and what each action does [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#player-list-window).

| Rule | Detail | Source |
| --- | --- | --- |
| window | a stay-on-top form with a multi-select list, a caption "--- N online ---" and Profile and Options buttons; the Options window has 5 check boxes and the profile edit window 10 fields | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#player-list-window) |
| popup | right-click selects the row under the cursor and shows Message (default), History, Buddy, Ignore, Profile; Buddy and Ignore are checked when every selected player is in that list | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#player-list-window) |
| open | double-click or Enter opens the read window if a PM from that player is waiting, otherwise the compose window | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#player-list-window) |
| Message | one PM to all selected rows, reusing an open window for the same set; at most 50 recipients (→ §2.8) | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#actions) |
| Profile | the first selected player only; online it sends `PLI_PROFILEGET` (80), which the listserver answers (→ §6) | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#actions); [srv] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf) |
| Ignore | toggles each selected account in `ignoredaccounts.txt` and saves the buddy list too; local only; ignored players' chat and PMs are dropped | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#actions); [2.05] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf) |
| Buddy | toggles `buddyaccounts.txt`; Buddy and Ignore exclude each other | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#actions) |
| auto reply | the client holds the text "Your messages are ignored."; when it is sent was not traced | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#actions) |
| world click | there is no right-click handler on a player in the game view; the only player popup is the list's | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#not-found) |
| no player action form | the person-action form is the editor's NPC script editor (→ §4.9), not a trade or duel menu | [2.05] (client-internals/decomp-findings-2026-10-24/03-player-list-popup.md#person-action-is-not-a-player-menu) |

### 4.10.5.2 By build

The player list grew one feature at a time. Each row gives the build where a feature arrived [bin] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf).

| Builds | Change | Source |
| --- | --- | --- |
| 1.33 | popup Message, Ignore, History; sections GPs, Guild, Normal, Ignore | [bin] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf) |
| 1.34 | ignore by account name; ignored players drawn red | [bin] (client-internals/feature-specs/14-friends-ignore.md#what-it-is) |
| 1.35 | Buddy, kept in `buddyaccounts.txt` | [bin] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf) |
| 1.39 | Profile and the Player List Options window | [bin] (client-internals/feature-specs/10-right-click-menu.md#what-is-known-205inf) |
| 2.14 and later | a Staff section named from `PLO_STAFFGUILDS` (47); the status list `PLO_STATUSLIST` (180) with the player's own index in prop 53 | [srv] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |
| 2.22 | sections Staff, Buddies, Guild, Normal, Ignore; popup Message, History, Buddy, Ignore, Mute, Profile | [cap] (client-internals/feature-specs/14-friends-ignore.md#lab-findings-from-a-real-222-client-2026-10-24-cap) |
| 2.22 Buddy and Ignore | local only: they write `buddyaccounts.txt` or `ignoredaccounts.txt`, one account per line, delete an empty buddy file, move the entry in the list, and send nothing | [cap] (client-internals/feature-specs/14-friends-ignore.md#lab-findings-from-a-real-222-client-2026-10-24-cap) |
| 2.22 Mute | sends `PLI_MUTEPLAYER` (43) with the player id and 1 or 0, one message per click; the entry does not move | [cap] (client-internals/feature-specs/14-friends-ignore.md#lab-findings-from-a-real-222-client-2026-10-24-cap) |

## 4.10.6 Start message and disconnects

The rules below cover the messages a server sends around login and logout: the start message, the RPG window, their order, and how a disconnect is explained [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv).

| Rule | Detail | Source |
| --- | --- | --- |
| start message | `PLO_STARTMESSAGE` (41) carries the server message as one line of HTML; 2.05 has a form for it; whether it shows at once or on request is unmeasured | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| RPG window | `PLO_RPGWINDOW` (179), 2.1 and later: quoted, comma-separated lines naming the server and its software | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| login order | level data, big map, minimap, RPG window, start message, an empty `PLO_SERVERTEXT` (82) | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| disconnects | every refusal, kick and ban reaches the client as `PLO_DISCMESSAGE` (16) with the text, `\r` for a line break, then the socket closes; the client then shows the reconnect dialog (→ §4.8.2.1) | [srv] (client-internals/feature-specs/13-ban-kick.md#what-it-is) |
| upgrade | from 2.14, `PLO_UPGRADEURL` (169) with a disconnect turns Reconnect into an Upgrade button | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| server texts | the refusal texts and the order of the server's login checks are server behaviour (→ §5) | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
