<!-- manual: kind=reference status=draft -->
# 4.10 Other client features

This chapter collects the client features that sit outside the core game loop: the integrity checks, animation state as other players see it, key emotes, the player list and its social lists, and what the client does with the server's start message and disconnect texts. The message layouts are in → §2.4 and §2.5.

> Status: draft. The 2.05 parts are read from 2.05 rev 2; the 2.17 to 2.31 parts come from lab captures and reads of those clients. Open points are App. E#320 to E#322.

## 4.10.1 Integrity checks

### 4.10.1.1 The tamper check (2.17 to 2.31)

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

## 4.10.2 Animation state as others see it

### 4.10.2.1 2.05: the sprite prop

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

| Rule | Detail | Source |
| --- | --- | --- |
| gani prop | prop 10 is the gani name as a string; a receiver that lacks `<name>.gani` asks the server for it | [srv][cap] (client-internals/feature-specs/11-emotes-ganis.md#a-animation-state) |
| 2.22 cadence | → §4.1.4 | [cap] (live-runs/2gta-222-2026-10-30/README.md) |

## 4.10.3 Key emotes (2.05 rev 2, same routine in 1.39)

| Rule | Detail | Source |
| --- | --- | --- |
| keys | Ctrl+A to Ctrl+Z, with no text field focused and the player neither dead nor locked | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| lookup | the letter is lowercased and the client takes the first loaded file whose name starts with `emoticon_<letter>` and ends in png, mng or gif; there is no letter-to-name table, so the mapping is whatever files exist | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes); [2.05] (client-internals/decomp-findings-2026-10-24/02-sprites-poses-emotes.md#emotes-ctrlletter) |
| drawing | at the player's x + 2, y − 5 (a little lower when a second flag is set) for 50 ticks (2.5 s) | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| network | the key path sends nothing; `PLI_SHOWIMG` (24) is sent only by the script command `showimg` (→ §8.2) | [2.05] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| others seeing it | unmeasured: captured SHOWIMG frames re-sending an AFK image about every 3 s are not explained by the key path (→ App. E#322) | [cap][inf] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| earlier builds | 1.38 introduced Ctrl+letter emotes, and 1.39 added letters | [doc] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |

## 4.10.4 Picking up and dropping items online

| Rule | Detail | Source |
| --- | --- | --- |
| 2.05 pickup | sends `PLI_ITEMDEL` (13) with the item's half-tile position and changes its own props itself; the server only removes the item and tells the others | [cap][srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| the other form | `PLI_ITEMTAKE` (32) also removes the item, and the server applies it to the player's props and echoes them | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| drop | `PLI_ITEMADD` (12) with the position and item | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |
| chest | `PLI_OPENCHEST` (20) with whole-tile x and y; the opened state is per account (→ §4.5.4) | [srv] (client-internals/feature-specs/03-inventory.md#item-pickup-and-chests-srvcap) |

## 4.10.5 The player list and social lists

### 4.10.5.1 2.05 (F7)

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

| Rule | Detail | Source |
| --- | --- | --- |
| start message | `PLO_STARTMESSAGE` (41) carries the server message as one line of HTML; 2.05 has a form for it; whether it shows at once or on request is unmeasured | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| RPG window | `PLO_RPGWINDOW` (179), 2.1 and later: quoted, comma-separated lines naming the server and its software | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| login order | level data, big map, minimap, RPG window, start message, an empty `PLO_SERVERTEXT` (82) | [srv] (client-internals/feature-specs/12-motd-rules.md#packets-server-to-client-at-the-end-of-login-srv) |
| disconnects | every refusal, kick and ban reaches the client as `PLO_DISCMESSAGE` (16) with the text, `\r` for a line break, then the socket closes; the client then shows the reconnect dialog (→ §4.8.2.1) | [srv] (client-internals/feature-specs/13-ban-kick.md#what-it-is) |
| upgrade | from 2.14, `PLO_UPGRADEURL` (169) with a disconnect turns Reconnect into an Upgrade button | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| server texts | the refusal texts and the order of the server's login checks are server behaviour (→ §5) | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
