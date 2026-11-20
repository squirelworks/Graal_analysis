<!-- manual: kind=reference status=draft -->
# Appendix E. Open questions and disagreements

> Status: draft. Rewritten on 2026-11-19 as a discussion of each unknown: what it is, what has been tried, the best current guess, what would settle it, and how likely it is to be settled. Entry numbers are permanent. Answered entries no longer live here: each settled answer, with the record of how it was settled, now sits in the chapter section it belongs to, and → §E.12 lists where each one went.

## E.0 How to read this appendix

This appendix is where the manual keeps everything it does not know. The other Parts state what was measured or read and mark the rest `unmeasured` or `disputed → App. E#n`; each such cell points here (→ §0.4).
Entries are grouped by subject in the order of the Parts (→ §E.2 to §E.10), and only open questions are kept here. When a question is answered, its answer and the record of how it was settled move into the chapter section it belongs to, and → §E.12 lists where each one went.
An entry number is permanent. The hundreds give the Part where the question was first raised: E#1–99 front matter, Part I and Part II; E#100s Part III; E#200s Part VIII; E#300s Part IV; E#400s Parts V to VII; E#500s Parts IX and X; E#600s Part XI and the seed taken from CONSOLIDATED.md [doc] (CONSOLIDATED.md).

Each entry has the same parts, in this order:

- **Question.** One sentence that says what is unknown and why it matters. (→ §0.3)
- **Evidence.** The claims on record, each with its source. When two notes disagree, both are quoted as Claim A and Claim B. (→ §0.3)
- **Tried.** What has already been done to answer it, so the same step is not repeated blind. (→ §0.3)
- **Best guess.** The reading the evidence favours today, tagged `[inf]`. A best guess is a working assumption for a reader who must build something now. It is never used to fill a table cell elsewhere in the manual, which still says `unmeasured` or `disputed` (→ §0.4).
- **Settles it.** The specific read, lab run or capture that would answer the question, with the client and setup it needs. (→ §0.3)
- **Outlook.** One of the five words in the table below. (→ §0.3)

The outlook says what stands between the question and its answer. It is the most useful single word for deciding what to work on next:

| Outlook | Meaning | Source |
| --- | --- | --- |
| **Lab** | A loopback lab run with clients and servers already held would answer it. Nothing else is missing | [doc] (AGENTS.md#labs) |
| **Read** | A static read of a binary already held would answer it, possibly followed by one confirming lab run | [doc] (AGENTS.md#decompile-and-pyreborn-material-stays-here) |
| **Owner** | The only clean answer touches a public server or service, so it waits for the owner's written permission | [doc] (AGENTS.md#labs) |
| **Missing** | It needs a binary, app, host or document that is not held. It becomes Lab or Read if that material turns up | [doc] (client-internals/build-catalogue.md) |
| **Maybe never** | The evidence that would settle it probably no longer exists (lost builds, the official servers' own source and data). The entry is kept so that a later find can be recognised | [inf] (client-internals/build-catalogue.md) |

## E.1 The unknowns at a glance

The table lists every open entry with its outlook and a one-line best guess, so a reader can choose work without reading each entry. Settled entries and where their answers now sit are listed in → §E.12, and the closing discussion of what may stay unknown is in → §E.11.

| Entry | Question | Outlook | Best guess | Source |
| --- | --- | --- | --- | --- |
| E#1 | Compiler of the early Delphi builds | Maybe never | a pre-release Delphi 3 compiler; not Delphi 2 or C++Builder 1 | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| E#3 | What a public 5.x or 6.x `Login` server sends | Owner | a GUI-script lobby built from `basepackage.gupd` and S→C 190 | [inf] (protocol/login-session-known.md#still-unobserved) |
| E#10 | When downloads moved to `maps` | Missing | after 2.1.0.4, by 2.17.1, with the gmap work | [inf] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md) |
| E#12 | Whether the `GNW` digits are a build date | Maybe never | yes, DDMMY | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| E#15 | Graal 2002 and 1.40 send sets and default routes | Lab | each build follows its token's neighbour; 1.40 and v22 logins captured | [inf] (client-internals/graal2002-and-140-builds.md#open-points) |
| E#16 | Classic+ 1.13 login wire layout | Missing | the desktop gen-5 login (type 5, key, token, two strings, trailer); trailer and native run open | [bin] (protocol/ios-classic-plus-113-framing.md#login) |
| E#18 | Mobile clients' outer framing and cipher | Read | iPhone settled (desktop generation 5); Android unread | [bin] (protocol/ios-classic-plus-113-framing.md) |
| E#19 | Generation 4 (2.19 to 2.21) on the wire | Missing | the server source's bz2 plus partial XOR | [inf] (protocol/codec-and-framing.md) |
| E#101 | Size of the type-0 allow lists | Read | the earlier mask came from another sheet or table | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| E#103 | 2.22 signature verifier variants | Read | a cracked or debug variant, not an official one | [inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions) |
| E#203 | The rest of the 2.05 `#` code set | Lab | `#E` is an empty placeholder (read); bare `#5`/`#6` is a 2.17 scanner change | [inf] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls) |
| E#207 | GS2 language, library and event model | Read | the official compiler's grammar matches the published GS2 syntax | [inf] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written) |
| E#209 | GS2 VM details left open by the per-build read | Read | 48, 49 and 54 settled on 5.00r7; unread builds remain | [inf] (client-internals/gs2-vm-loader-diff.md#still-open) |
| E#210 | Particle emitter and `format` details | Lab | `%d` truncates, `indexof` is case-sensitive | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| E#211 | Which objects make 6.00 fuse fold 241 | Read | objects resolved once and safe to cache, such as weapons and globals | [inf] (protocol/gs2-fold-241-2026-11-16.md#still-open) |
| E#214 | Why some official bodies do not end in a return | Owner | a separate emitter path for one kind of script | [inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#still-open) |
| E#304 | Stopping positions and wire rounding | Lab | stopping measured; the wire value is truncated to the half tile | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| E#320 | Whether any server checks the tamper check | Owner | no server rejects a missing or wrong value | [inf] (client-internals/feature-specs/08-tampercheck.md#public-servers) |
| E#323 | 2.22 level-object routines | Read | as in 2.05; the throw is now read and matches 2.05's table | [inf] (client-internals/static-reads-appendix-e-2026-11-20-f.md#the-222-throw-e323) |
| E#324 | Combat live checks still open | Lab | 1.21 gives a direct reward, not a drop | [inf] (live-runs/open-issues-2026-11-19/README.md) |
| E#325 | Sound census and playback limits | Read | one file counted twice in the format split | [inf] (client-internals/sound-files-6x.md#what-the-files-are) |
| E#400 | Two projects called Ash | Missing | two projects that share a name | [inf] (ash/ARCHIVAL-NOTE.md) |
| E#401 | Listserver reply ids 1 and 2 | Maybe never | the 2002 listserver used them as the RC reads them | [inf] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| E#402 | The 2000-era listserver reply | Maybe never | today's legacy reply is the old one unchanged | [inf] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| E#403 | Classic logins on port 14922 | Owner | 14922 answered classic logins in 2001 and stopped later | [inf] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| E#404 | A public server refusing 2.05 | Owner | an older version table with no 2.05 entry | [inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| E#406 | How the official listserver assigns PC ids | Maybe never | a row number in a machine table | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| E#422 | Quoting of folder rights | Maybe never | the original server stored the CSV form | [inf] (protocol/rc-capture-2026-11-04.md#rights) |
| E#507 | 3.04 sheet type 5 and server tile definitions | Lab | type 5 is a walk rule (read); servers sent no tile definitions | [inf] (torque/304-tile-types.md#not-settled) |
| E#610 | 4.04r2 offline gameplay | Lab | it plays like 4.20r6 offline | [inf] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| E#611 | 4.04r2 pickup semantics | Lab | the bound field is the carried object's kind | [inf] (client-internals/404r2-carry-state.md#open-questions) |
| E#612 | GraalShop movie editor attribution | Missing | the 2006 editor wrote the movie format | [inf] (tools/graaleditor-vs-205.md#workflow) |
| E#615 | v7 Worlds login token and quit reason | Owner | the connector supplies a `G3D2204D`-family token | [inf] (client-internals/v7-il2cpp-names-and-startup-gate.md#still-open) |
| E#616 | v7 connector script plaintext | Maybe never | the RSA block wraps an AES key for the payload | [inf] (protocol/v7-connector-live-20261111.md#5-open) |
| E#618 | Whether Mac 6.004 and 6.015 draw a game frame | Lab | 6.015 logs in and plays (lab); the white frame is the guest's missing OpenGL | [lab] (protocol/probe-mac-6015-2026-11-19.md) |

## E.2 Builds, identity and protection

These questions are about which build is which, who built it and how it protects itself. They matter because every other Part keys its rows to an exact build (→ §1.1), and a wrong identity moves a finding to the wrong row [doc] (client-internals/build-catalogue.md).

### E#1 Compiler of the early Delphi builds

**Question.** Which compiler built 1st Graal, 3rd Graal to 1.1.9 and 1.21. It matters for reading their runtime library correctly, not for their behaviour [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The builds use the Delphi 2 class-metadata layout: self pointer 64, class name 32 bytes before the VMT | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Claim B | The same builds carry the runtime-library copyright "1983,97 Borland", a year late for Delphi 2 | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Tried | Nothing beyond reading the two clues; no runtime library has been matched against candidates | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Tried (2026-11-20) | 1st Graal, 3rd to 15th Graal, 1.1 and 1.1.9 keep the 64-byte self pointer but carry the `SysInit` unit, language interfaces and a package-information resource, which are Delphi 3 features; none has C++ start-up code, so C++Builder 1 is ruled out. 2nd Graal, 1.3 beta and later use shipping Delphi 3's 76-byte layout | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#compiler-of-the-early-delphi-builds-e1) |
| Best guess | A pre-release Delphi 3 compiler, whose class table is 12 bytes shorter than the shipping one's, with the 1997 runtime library. Confidence: moderate | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#compiler-of-the-early-delphi-builds-e1) |
| Settles it | That pre-release compiler's own runtime library, matched function by function | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#compiler-of-the-early-delphi-builds-e1) |
| Outlook | Maybe never, since Delphi 3 pre-release kits are unlikely to turn up; low priority, since no behaviour depends on it | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#compiler-of-the-early-delphi-builds-e1) |

### E#12 Whether the token digits are a build date

**Question.** Whether the five digits of a `GNW` login token are the build date (DDMMY). The reading is used to place builds with no other date [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Read as DDMMY, the digits fall on or a few days before each build's link date | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Evidence | The dates fit the change-log order of 2.01 to 2.05, but nothing in a binary names the format | [inf] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#open) |
| Tried | Every held `GNW` build was compared with its link date; none contradicts the reading | [inf] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#reading-the-digits-inferred) |
| Best guess | The digits are a build date. Confidence: high. The manual uses the reading for ordering only, never to date a build that has its own link date | [inf] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#reading-the-digits-inferred) |
| Settles it | A vendor note, a server source or a version table that decodes the token | [inf] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#open) |
| Outlook | Maybe never. The format was never published, and the official server source is not held | [inf] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#open) |

### E#15 Graal 2002 and 1.40 exact-input validation

**Question.** How the Graal 2002 builds and the checked 1.40 behave at login and in play, each on its own evidence. The static inputs in §1.1.5 establish tokens, command names and receive-route differences, not exact-input login or gameplay [bin] (client-internals/graal2002-and-140-builds.md#open-points).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Exact ver10 is wire-captured at login, and its normal list and game entry has been observed with mixed supporting data | [bin] (client-internals/graal2002-and-140-builds.md#ver10-list-entry-and-connection-boundary) |
| Settled part (2026-11-20) | 1.40 (`GNW23090`) captured in the lab: a start form with no host field, a server list from its built-in list host on port 14910 (1.41 rev 1 uses 14923), then login type 0, generation 3; the server's level name and one full board are drawn and walkable; the client's first messages are four file requests, its own props and three NPC-prop messages | [lab] (protocol/lab-appe-mirae-2026-11-20b.md#login-of-the-140-build-e15) |
| Tried (2026-11-20) | Graal 2002 v22 (`GNW31101`) fetches its list (list name `graal2002`) from port 14922 but never opens a game connection from it against the lab listserver | [lab] (protocol/lab-appe-mirae-2026-11-20b.md#graal-2002-v22-gnw31101-not-completed) |
| Settled part (2026-11-20) | Graal 2002 v22 (`GNW31101`) logged in once a Wine virtual desktop cleared a stale dialog: list name `graal2002`, an 8-field list row, then login type 0, generation 3, key 36; first sends 37 and 39; it ran the level's GS1 NPC and a GS1 weapon and stayed online | [lab] (protocol/lab-appe-mirae-2026-11-20c.md#graal-2002-v22-login-e15) |
| Open | The ver7 to ver13 default routes for 2, 4, 17, 18, 154 and 155 need an identified baddy, chest or horse fixture with a visible result, not a count of dispatch entries | [bin] (client-internals/graal2002-and-140-builds.md#open-points) |
| Open | Exact ver10's first properties update: the no-reply arm is confounded by a timer, and the reply arms are bounded; static gate clearing does not prove emission | [bin] (client-internals/graal2002-and-140-builds.md#method-and-remaining-limits) |
| Open | The six Graal 2002 client-to-server id sets need their own send-site reads | [bin] (client-internals/graal2002-and-140-builds.md#open-points) |
| Best guess | Each build behaves like the neighbour that shares its token. The manual does not borrow those rows, because the 2002 builds were patched in places the token does not show | [inf] (client-internals/graal2002-and-140-builds.md#open-points) |
| Settles it | Send-site reads for each id set, and a fixture per default route | [inf] (client-internals/graal2002-and-140-builds.md#open-points) |
| Outlook | Lab and Read: all inputs are held | [inf] (client-internals/graal2002-and-140-builds.md#open-points) |

### E#615 v7 Worlds login identity, start-up quit and date gate

**Question.** What login token a v7 Worlds client sends, and which reason its expiry path gives. The clients carry no baked token, quit after one frame when started standalone, and only dial the connector inside each build's 180-day window (→ §1.8.10) [bin][doc] (protocol/v7-connector-live-20261111.md#1-self-identification-labbin).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | No cleartext token in 548 to 71243; the connector script builds the login; gs2lib names `G3D2204D` as Worlds | [bin][doc] (protocol/v7-connector-live-20261111.md#1-self-identification-labbin) |
| Evidence | The managed quit entry takes a reason string; the managed side has no date gate; the unpacked engine imports calendar-to-timestamp functions | [bin] (client-internals/v7-il2cpp-names-and-startup-gate.md#still-open) |
| Settled part | The date gate is `now − reference > 180 days` with a compiled-in reference date per release, active in every build except 610; the instant-quit reason literal is `QuitInstant` (→ §1.8.10) | [bin] (client-internals/v7-il2cpp-names-and-startup-gate.md#the-date-gate-is-an-n-days-after-a-reference-date-check-wired-to-the-boot-quit); [bin][inf] (client-internals/v7-il2cpp-names-and-startup-gate.md#the-quit-reason-is-native-and-the-instant-quit-literal-is-quitinstant) |
| Tried | The Unity 6000 build's gate values and both verdicts were confirmed live from outside a QEMU guest: inside the window it passes and disarms itself; after it the client stays on a black window without crashing (→ §1.8.10) | [cap] (client-internals/v7-il2cpp-names-and-startup-gate.md#for-a-live-debugger-where-to-break-and-what-to-read) |
| Tried (2026-11-20) | 614 standalone with no network: on 2024-10-12 it reaches OpenGL init; on 2024-10-13 it stalls before graphics init. Neither date quits within minutes or logs a reason | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#v7-worlds-614-at-the-date-boundary-e615) |
| Best guess | The production connector sends a `G3D`-family token of the `G3D2204D` kind, and past the gate the client stalls before graphics init rather than quitting with a reason, at least standalone. Confidence: moderate for the stall, moderate for the token family | [inf] (client-internals/v7-il2cpp-names-and-startup-gate.md#still-open) |
| Settles it | A decrypted connector script for the token (→ App. E#616); a boundary-date boot of 614 (2024-10-12 boots, 2024-10-13 quits, by the table) for the reason | [inf] (client-internals/v7-il2cpp-names-and-startup-gate.md#still-open) |
| Outlook | Lab for the expiry reason; Owner or Maybe never for the token, which depends on E#616 | [inf] (client-internals/v7-il2cpp-names-and-startup-gate.md#still-open) |

### E#618 Whether Mac 6.004 and 6.015 draw a game frame

**Question.** Whether the Mac 6.004 and 6.015 clients get past a white window to a rendered frame, a login and a level (→ §1.8.7) [lab] (version-profiles/lab-mac-v6-6015-lion-2026-11-16.md#lion-guest-run-6015).

| Part | Discussion | Source |
| --- | --- | --- |
| Tried | Mac 6.015 on Mac OS X 10.7.5 in an emulator, offline: once the executable bit was restored, the app came up with a Graal menu and a window titled Graal whose content stayed white; no crash | [lab] (version-profiles/lab-mac-v6-6015-lion-2026-11-16.md#lion-guest-run-6015) |
| Evidence | Mac 6.11r1 showed the same white window on the same guest, which has no OpenGL acceleration; both 6.0x builds use a Cocoa OpenGL view | [lab][bin] (version-profiles/lab-mac-v6-6015-lion-2026-11-16.md#static-surface-used-to-choose-the-live-build) |
| Tried (2026-11-19) | The x86_64 slice of Mac 6.015 in the same Lion guest logged in through the probe proxy (generation 5, token `G3D3107A`), stayed connected through the whole core probe plan and ran a clientside GS1 NPC whose chat came back; the canary read the wire, not the screen | [lab] (protocol/probe-mac-6015-2026-11-19.md) |
| Tried (2026-11-20) | On a macOS 15 guest with working software OpenGL, 6.015 initialised OpenGL, logged in, entered the start level and asked for its files, but its main window stayed blank grey; a small "Select File" window drew the GUI skin. 6.004 printed its beta notice and quit at once, probably a time limit | [lab] (protocol/lab-appe-gwentea2-2026-11-20d.md#mac-6004-and-6015-with-working-opengl-e618) |
| Best guess | The 6.0x Cocoa main view draws only on the macOS versions it was built for (around 10.9, the version it reports), not on Lion without OpenGL or on Sequoia; 6.004 needs its clock held before its beta limit. Confidence: low | [inf] (protocol/lab-appe-gwentea2-2026-11-20d.md#mac-6004-and-6015-with-working-opengl-e618) |
| Settles it | A 10.9-era macOS guest with OpenGL, with the clock held for 6.004 | [inf] (protocol/lab-appe-gwentea2-2026-11-20d.md#mac-6004-and-6015-with-working-opengl-e618) |
| Outlook | Lab. A Mac 6.03r7 is not held, so that build stays Missing | [inf] (version-profiles/lab-mac-v6-6015-lion-2026-11-16.md#open-points) |

## E.3 Transport: frames, ciphers and logins

These questions are about the layer under the messages: how a frame is cut, ciphered and compressed, and what the first exchange looks like. They come first among the protocol questions because a wrong frame rule makes every later byte unreadable (→ §2.1, → §2.2, → §2.3) [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering).

### E#3 Public `Login` server session (5.x, 6.x)

**Question.** What a public 5.x or 6.x `Login` server sends after the handshake: the lobby that every later client sees before it reaches a game server [doc] (protocol/login-session-known.md#still-unobserved).

| Part | Discussion | Source |
| --- | --- | --- |
| Unobserved | The bytes the server sends, including the payload of S→C 190 | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | The GUI script text for the server list, the account screens and the `ChatBar` control | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | The file list inside `basepackage.gupd` and any later update package, and the backdrop level the server chooses | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | The 6.11 connector script body, and with it the framing, cipher and login token a 6.11 client uses on the public service (the lab path is in → §2.10.8) | [doc] (protocol/login-session-known.md#still-unobserved) |
| Tried | A real Windows 4.20r8 to 6.03r7 run reached a lab `Login` server, so the client side of the lobby is known; the server side is what a lab server chooses to send | [lab] (live-runs/real-win10-2026-11-18/README.md) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | The lobby is a set of GUI scripts delivered in the update package and driven by S→C 190, with no lobby logic in the client beyond the script runtime. Confidence: moderate | [inf] (protocol/login-session-known.md#still-unobserved) |
| Settles it | A capture of a real `Login` session; it touches a public server, so it needs the owner's written permission | [doc] (AGENTS.md#labs) |
| Outlook | Owner. If the service has changed since these clients shipped, part of the period behaviour may be lost for good | [doc] (AGENTS.md#labs) |

### E#16 Classic+ 1.13 caller contract versus mobile wire layout

**Question.** What Classic+ 1.13 actually puts on the wire at login. The static follow-up established one-byte prefix construction and the selected positive byte-copy count, not a captured mobile login [bin] (client-internals/classic-113-login-construction.md#prefix-and-copy-helper-follow-up); [bin] (client-internals/classic-113-login-construction.md#forwarding-boundary).

| Part | Discussion | Source |
| --- | --- | --- |
| Open | The short-path object append and the remaining field cases, before any claim of a complete codec, character semantics or size limits | [bin] (client-internals/classic-113-login-construction.md#prefix-and-copy-helper-follow-up) |
| Open | String identities and the vector format: the getters and serializer must be bound to their consumers before fields are named | [bin] (client-internals/classic-113-login-construction.md#caller-observations) |
| Settled part | Framing: selector 5 is the login message id (client type 5); the sender adds the key byte after it on the first message, and the login goes out as one zlib frame with no compression byte and no XOR | [bin] (protocol/ios-classic-plus-113-framing.md#login) |
| Open | Native acceptance: no run yet | [bin] (protocol/ios-classic-plus-113-framing.md#open) |
| Tried (2026-11-20) | No Android emulator or Android-x86 image is on the lab machines (GwenTea2 has adb and fastboot only), and Classic+ 1.13 is an iPhone build, so an Android emulator would not cover it | [lab] (protocol/lab-appe-gwentea2-2026-11-20c.md#mobile-clients-e16-e18) |
| Best guess | The two strings are account and password, as on desktop. Confidence: moderate | [inf] (protocol/ios-classic-plus-113-framing.md#login) |
| Settles it | Tracing the lower sender, then a qualified native run with a capture | [inf] (client-internals/classic-113-login-construction.md#forwarding-boundary) |
| Outlook | Missing: no iPhone device or simulator is held; the static trace is Read | [inf] (client-internals/classic-113-login-construction.md#forwarding-boundary) |

### E#18 Mobile clients: outer framing and cipher

**Question.** How the Android and iPhone clients frame, compress and cipher their stream. Without it no mobile client can be probed, even on a lab server [bin] (client-internals/android-login-token-boundary.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The held Android Classic and Era reading covers the Java host, the frame gate, collision, board, render, chat builder and the Classic 1.8 GS2 machine across seven packages; it did not recover the connect and token builders | [bin] (client-internals/android-classic.md); [bin] (client-internals/android-login-token-boundary.md) |
| Evidence | The native engine libraries are not encrypted, so the connect and token builders are within reach of a static pass | [bin] (client-internals/android-login-token-boundary.md) |
| Tried | No device, emulator or capture. The lab Linux VM has no nested KVM, and no Android or iPhone app is installed on a lab host | [doc] (protocol/unknowns-ledger.md) |
| Settled part | iPhone Classic+ 1.13 uses the desktop generation-5 frame: two-byte length (or `FF FF` and four bytes), compression byte, partial XOR with round-down for compressed bodies, and a type-5 login with a key byte in one zlib frame | [bin] (protocol/ios-classic-plus-113-framing.md) |
| Tried (2026-11-20) | Android Classic 1.8 ran natively on an Android-x86 9.0 emulator on loopback: it fetches a signed connector script first (HTTPS, then plain HTTP for `conf.gs`, user agent "Graal/6.15401") and, with no valid reply, never opens a game connection. So it is on the 6.1x connector line, and its game framing can't be captured without a genuine connector reply | [lab] (protocol/lab-appe-gwentea2-2026-11-20d.md#android-classic-18-on-an-emulator-e18) |
| Best guess | Android uses the 6.1x connector front end and then the same game frame as the 6.1x desktop clients, since it reports the same engine line. Confidence: moderate | [inf] (protocol/lab-appe-gwentea2-2026-11-20d.md#android-classic-18-on-an-emulator-e18) |
| Settles it | A static read of the Android native socket layer after the connector step | [inf] (protocol/lab-appe-gwentea2-2026-11-20d.md#android-classic-18-on-an-emulator-e18) |
| Outlook | Read (Android); a run is blocked by the signed connector reply | [doc] (protocol/unknowns-ledger.md) |

### E#19 Generation 4 on the wire (2.19 to 2.21)

**Question.** Whether the generation-4 codec in the server source (bz2, then XOR over the first dwords) is what 2.19, 2.2 and 2.21 actually sent [srv] (protocol/codec-and-framing.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Everything known about generation 4 comes from the server source; no type-4 login or frame has been captured | [srv] (protocol/codec-and-framing.md) |
| Tried | The probe proxy has a generation-4 codec from the server source, but no client to point it at | [doc] (protocol/unknowns-ledger.md) |
| Lead | Server tables list Linux 3.0beta (`G3D16053`) and 3.01 (`G3D27063`) as client type 4, generation 4, and clean installers of both are held (→ §1.8.4). A lab login with either would show a generation-4 frame from a real client, even though they are not 2.19 to 2.21 | [bin][inf] (version-profiles/batch-linux-3x-clean-installers-2026-11-16.md#open-still) |
| Best guess | The server source is right: it was written against those clients, and generations 3 and 5 on either side match their source. Confidence: moderate to high | [inf] (protocol/codec-and-framing.md) |
| Settles it | Any 2.19 to 2.21 binary, read statically or run against the proxy; meanwhile, a Linux 3.0beta or 3.01 login against the proxy tests the codec itself | [inf] (protocol/codec-and-framing.md); [inf] (version-profiles/batch-linux-3x-clean-installers-2026-11-16.md#open-still) |
| Outlook | Missing. If no build of these versions survives, Maybe never | [inf] (protocol/codec-and-framing.md) |

### E#616 v7 connector script plaintext

**Question.** What the decrypted v7 connector script says: the game host it names, the framing and cipher it sets and the login it builds. The reply container and its per-launch signature are known (→ §2.10.7) [lab][bin] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Container layout, an RSA-2048 signature bound to the per-launch request, and both AES-CBC and RC4 exported | [lab][bin] (protocol/v7-connector-live-20261111.md#3-the-real-reply-container-lab) |
| Open | The payload cipher and whether the RSA block also wraps its key; the plaintext; the `?p=` DES key | [inf] (protocol/v7-connector-live-20261111.md#5-open) |
| Tried | The live date gate was read from outside a QEMU guest without tripping the anti-tamper layer (→ App. E#615); the script buffers were not read | [cap] (client-internals/v7-il2cpp-names-and-startup-gate.md#for-a-live-debugger-where-to-break-and-what-to-read) |
| Method (2026-11-18) | Host-side debugging through QEMU/KVM's gdb server reads a running packed client with nothing inside the guest; it stopped the v7 date gate at entry and read its inputs live. Bochs was assessed and not used | [lab] (client-internals/hypervisor-live-debug.md#short-answer); [lab] (client-internals/hypervisor-live-debug.md#what-was-done-on-v7-lab) |
| Evidence (6.1.1.3, 2026-11-19) | The 6.1.1.3 request is deterministic across launches, and its connector gate can be passed in a lab only by a lab trust anchor; the joined login and connector chain has not been run (→ §2.10.8) | [lab][inf] (protocol/v6113-login-lab-method.md#replay-forge-and-the-only-lab-bypass); [lab] (protocol/v6113-login-lab-method.md#still-open-carried-not-closed) |
| Tried (2026-11-19) | On 6.1.1.3 the trust-anchor bypass named above was tried and is a NO-GO: the key the signature check uses never appears in a patchable form, and the reply's payload decrypt is inside the same protector machine. Container fuzzing of the stock client fails closed on every malformation | [lab] (protocol/conf-gs-fuzzing.md) |
| Best guess | The RSA block wraps an AES key for the payload, and the script follows the 6.11 script's structure (→ §2.10): set protocol, set ciphers, id tables, connect, login. Confidence: moderate | [inf] (protocol/v7-connector-live-20261111.md#5-open) |
| Settles it | A read of the live script buffers after decryption, by a method the anti-tamper layer tolerates, on a client whose baked public key is replaced | [inf] (protocol/v7-connector-live-20261111.md#5-open) |
| Outlook | Maybe never for the production script, which only the operator's service produces for a live launch; Lab for the structure, using a lab-signed script | [inf] (protocol/v7-connector-live-20261111.md#5-open) |

## E.4 Messages, props and what they do

These questions are about single messages and props: which builds send or handle an id, how wide a field is, and what a message changes on the screen. Each one leaves a `unmeasured` or `disputed` cell in → §2.4, → §2.5, → §2.6 or App. A, and most of them are within reach of the probe proxy, which injects a message into a live loopback session and watches the client's reaction [lab] (protocol/probe-targets-2026-11-18.md).

### E#10 When the `maps` download folder arrived

**Question.** Which build started saving downloads into a `maps` folder [bin] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The 2.1 test builds save downloads with no `maps` rule, and 2.17.1 has one; no client between them has been read | [bin] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md) |
| Tried | The Windows 2.1.0.0 to 2.1.0.4 images are now identified, so the question no longer waits on a binary for that range; 2.12 to 2.16 have none | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md) |
| Tried (2026-11-19) | The gmap code, `loadgmaps.txt` included, is absent from 2.1.0.0 to 2.1.0.4 and present in 2.17.1 | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#gmap-code-in-the-21-builds-e10) |
| Best guess | The rule arrived with the gmap work, after 2.1.0.4 and by 2.17.1. Confidence: moderate | [inf] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md) |
| Settles it | The save routine of the 2.1.0.x images; for 2.12 to 2.16, any binary that turns up | [inf] (client-internals/decomp-findings-2026-10-25-e/03-open-points.md) |
| Outlook | Read for 2.1.0.x; Missing for 2.12 to 2.16, so the exact build may never be known | [inf] (client-internals/decomp-findings-2026-10-25-e/03-open-points.md) |

## E.5 File formats and tiles

These questions are about what is in a file and how a client reads it (→ Part III). Several of them look like format questions but are really questions about which client routine consumes a field, which a file alone cannot answer [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle).

### E#101 Size of the type-0 allow lists

**Question.** Whether an earlier mask count of walkable tiles describes the lists read from the exact file [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The exact-input lengths, overlap and union are in → §3.5.3.1; they do not reproduce the earlier count | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| Evidence | The earlier export counted 3195 non-blocking and 682 blocking tiles | [live] (formats/tile-walk.md#type-0-allow-lists) |
| Best guess | The earlier mask was made from another sheet or a later table, so the numbers describe a different input. Confidence: moderate | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Settles it | Link the original mask and the exact file to the producing client path and sheet before comparing | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Outlook | Read, if the mask's producer can be identified; otherwise the old count is simply retired | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |

### E#103 Verifier variant reachability and signature interpretation

**Question.** What the four unconditional guards in one 2.22 verifier variant mean for which signed files a client accepts. The bounded result in → §3.5.5.1 compares retained inputs; it does not measure startup acceptance [bin][inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Four conditional guards in one RSA-verification routine are unconditional in the compared variant; only A was deep-imported, B compared by full byte difference | [bin] (formats/windows-222-verifier-variants.md#evidence-and-method) |
| Evidence | The earlier three-branch community-control patch is a different comparison; the control is not authenticated as pristine official code | [bin][inf] (formats/windows-222-verifier-variants.md#relationship-to-the-earlier-signature-note) |
| Open | Broader lineage differences, startup caller reachability, the helper algorithm, the signature format and the inputs accepted | [bin][inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions) |
| Best guess | The variant with unconditional guards is a patched community build that accepts unsigned files, not an official release. Confidence: moderate. No PM or GS1 conclusion follows from the verifier | [inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions) |
| Settles it | Trace the callers and helper against identified inputs before interpreting runtime acceptance | [inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions) |
| Outlook | Read | [inf] (formats/windows-222-verifier-variants.md#coverage-and-remaining-questions) |



## E.6 Client behaviour

These questions are about what a client does in play: timing, walking, combat, items and the screen (→ Part IV). Most were raised by a static read that found a routine but not every input to it, so most are settled by one controlled lab scene on the exact build [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv).

### E#304 Stopping positions and the wire rounding of nudged positions

**Question.** Where a player stops after a blocked step, and how a position that is not on a half tile is rounded when sent [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The flush snap and the 0.1 nudges are read from the 2.05, 2.17.1, 2.22 and 2.31 walking routines | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| Open | The stopping positions on a live client, and the rounding of a nudged position on the wire | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settled part (2026-11-20) | On 2.22 a player walking into a wall from either half-tile alignment stops flush at the wall (y 25.0, wire 50), then the push gani starts | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#walking-into-a-wall-on-222-e304) |
| Settled part (2026-11-20) | On 2.22 a player walking up into a 2 × 2 rock stops flush at y 21.0 from both half-tile alignments; with 0.5 or 1.0 tiles of overlap it slides off the corner through half-tile x values only (28.5, 28.0, 27.5) and walks on; with 1.5 or more it stops | [lab] (protocol/lab-appe-mirae-2026-11-20c.md#walking-into-a-rock-on-222-e304) |
| Best guess | The wire value is the position in half tiles, truncated; every position seen was already on a half tile. Confidence: low | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | A finer capture of the corner slide (positions are sent at most every 0.1 s, so the step size is unseen), or a read of the position packer | [inf] (protocol/lab-appe-mirae-2026-11-20c.md#walking-into-a-rock-on-222-e304) |
| Outlook | Lab | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#320 Does any server check the tamper check

**Question.** Whether any server checks the value of `PLI_TAMPERCHECK` (39), or its periodic re-send from 2.31 [srv][cap] (client-internals/feature-specs/08-tampercheck.md#public-servers).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The clients only send it; the open-source server discards it; four public servers accepted a 2.22 login without it for 20 s | [srv][cap] (client-internals/feature-specs/08-tampercheck.md#public-servers) |
| Tried | Our GServer-v2 build (GS2Emu 4.0.0-beta) takes an empty 39 silently: no reply, no log line, and the session continues | [lab] (protocol/probe-targets-2026-11-18.md) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | No server rejects a missing or wrong value; at most an official server logged it for staff. Confidence: moderate | [inf] (client-internals/feature-specs/08-tampercheck.md#public-servers) |
| Settles it | A 2.31 session on a public server with the re-send withheld or altered, which needs the owner's written permission | [inf] (client-internals/feature-specs/08-tampercheck.md#needs) |
| Outlook | Owner | [inf] (client-internals/feature-specs/08-tampercheck.md#needs) |


### E#323 Level-object routines not read (2.22)

**Question.** How 2.22 throws a lifted object, what a cut or lift drops, and the rest of its level-object routines [bin] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv).

| Part | Discussion | Source |
| --- | --- | --- |
| Open | The carrying pose, the chest and sign probe points, the glove value the server sends, snapping after a step, and the swim and carry speed factors | [bin] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |
| Evidence | `PLI_THROWCARRIED` (11) and `PLI_HITOBJECTS` layouts wait on this read and a 2.22 carry and throw capture | [bin] (protocol/carry-shoot-hit-status.md) |
| Tried (2026-11-19) | 2.22's probe table is byte-identical to 2.05's; its carry, throw and take-player-carry logic sits in one large script action dispatcher; the routines were not compared one by one | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#222-level-object-code-e323) |
| Settled part (2026-11-20) | The throw sends UDP 18 and, when a TCP copy is needed, an empty `PLI_THROWCARRIED` (11); it flies 9 ticks at 1 tile per tick from (x + 0.5) with a shadow at y + 1, sinking 0.2 tile per tick, on the same step table as 2.05; it hits a wall, an NPC (`waspelt`), baddies, then the player within 2 tiles, and lands as a splash or a break effect (leaves for a bush), or sets a carried bomb or NPC back down; cut and lift roll no drop (→ §4.5.2). The x, y sender earlier taken for 11 is the bomb pickup, UDP 11 with `PLI_BOMBDEL` (5) | [bin] (client-internals/static-reads-appendix-e-2026-11-20-f.md#the-222-throw-e323) |
| Open (2026-11-20) | The read gives 9 tiles of flight where the 2.05 live note saw about 6; a 2.22 frame-by-frame throw in open ground would settle it | [bin] (client-internals/static-reads-appendix-e-2026-11-20-f.md#not-covered-1) |
| Best guess | The routines match 2.05's, since 2.22's walking rule does. Confidence: moderate | [inf] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |
| Settles it | Reading those routines in 2.22, or one lab run per item | [inf] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |
| Outlook | Read | [inf] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |

### E#324 Combat rules the 1.21 to 2.31 pass left open

**Question.** The live checks left after the static combat pass over 35 builds settled its four unidentified gates [bin] (client-internals/combat-baddy-tile-by-version.md#not-known).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled part | 1.39 and 1.41 rev 1 handle id 40; player mode 7 is attachment to another local player; the extra victim test is ghost mode (170), and from 2.17.1 Kingdoms or New World mode (176, 177); respawn AP bands match 2.05 from 1.41 rev 1 | [bin] (client-internals/combat-baddy-tile-by-version.md#hits-by-packet-ids-40-and-46); [bin] (client-internals/combat-baddy-tile-by-version.md#sword-judge-gates); [bin] (client-internals/combat-baddy-tile-by-version.md#death) |
| Settled part | The 2-tile sideways sword edge is included on both sides on 1.35, and half a tile further misses | [lab] (live-runs/sword-edge-2026-11-18/README.md) |
| Settled part | 2.05 rev 2 has no client-side drop roll offline: 17 archer and 8 soldier kills, no drop, against 9 drops in 12 archer kills on 1.39 | [lab] (live-runs/open-issues-2026-11-19/README.md) |
| Open | The extra fields 1.41 rev 1 reads from an id 40 body of 6 bytes or more | [bin] (client-internals/combat-baddy-tile-by-version.md#hits-by-packet-ids-40-and-46) |
| Open | 1.21 gave exactly one gralat in the frame of each of 12 archer kills, with no darts or hearts; the drop spot overlapped the player, so a dropped gralat picked up at once and a direct kill reward look the same | [lab] (live-runs/open-issues-2026-11-19/README.md) |
| Open | 2.17.1's drop behaviour, and the sword spark (no separate spark sprite was seen on 1.39 against a rock wall) | [lab] (live-runs/open-issues-2026-11-19/README.md) |
| Tried (2026-11-20) | Two 2.05 clients swinging at each other at once, 4 times: no spark sprite, and the victim took half a heart in 3, so no true sword-on-sword meeting was caught | [lab] (protocol/lab-appe-mirae-2026-11-20.md#sword-against-sword-on-205-e324-one-sub-check) |
| Tried (2026-11-20) | On 1.21 offline a thrown bush put a penned archer into its hurt state twice but did not kill it in four tries; lifting a bush left a drawn item (a gralat or hearts) on the spot, so 1.21 draws ground drops from bushes; 2.17.1 and the sword-against-sword scene were not run | [lab] (protocol/lab-appe-mirae-2026-11-20c.md#combat-checks-on-121-e324-tried-not-settled) |
| Tried (2026-11-20) | On 2.17.1 Training the sword never hurt or killed an archer in 12 levels, so no drop could be checked; on 2.05 rev 2 four shielded soldiers died to the sword with no drop, and no separate spark sprite could be told apart from the two swings | [lab] (protocol/lab-appe-mirae-2026-11-20d.md#combat-checks-on-2171-and-205-e324) |
| Best guess | 1.21 gives a direct kill reward of one gralat rather than rolling a drop; 2.17.1 has no drop roll, like 2.05; the spark appears only when a sword meets a sword or a shield. Confidence: moderate, low, low | [inf] (live-runs/open-issues-2026-11-19/README.md) |
| Settles it | A ranged kill on 1.21 (thrown bush or pot, or an arrow), the same archer scene on 2.17.1, and a sword against a sword or a baddy's shield | [inf] (live-runs/open-issues-2026-11-19/README.md) |
| Outlook | Lab | [inf] (client-internals/combat-baddy-tile-by-version.md#not-known) |

### E#325 Later sound census and playback limits

**Question.** How many distinct WAVs the 4.x to 6.x builds ship, and which formats each client really plays [file][doc] (client-internals/sound-files-6x.md#what-the-files-are).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The survey reports 255 distinct WAVs, but its format counts (202 + 43 + 6 + 3) and channel counts (193 + 61) each total 254 | [file][doc] (client-internals/sound-files-6x.md#what-the-files-are) |
| Evidence | Backend names, filter strings, file contents and script help do not establish exact-build playback, content sniffing, scheduling or failure behaviour; the survey ran no client (→ §3.10.5, → §4.7.5) | [file][bin] (client-internals/sound-files-6x.md) |
| Best guess | One file was dropped from both splits, so 255 is right and each split is one short. Confidence: moderate | [inf] (client-internals/sound-files-6x.md#what-the-files-are) |
| Settles it | Recount against the surveyed inputs, and test each format on each exact client and sound backend | [inf] (client-internals/sound-files-6x.md#what-the-files-are) |
| Outlook | Read for the count; Lab for playback | [inf] (client-internals/sound-files-6x.md#what-the-files-are) |

### E#610 Windows 4.04r2 offline initialization against gameplay

**Question.** Whether 4.04r2 plays offline. A harness drove its offline transition, but no gameplay was seen [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Instrumentation changes the offline-mode flag, allocates an adventure object and observes continued message-loop callbacks | [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Open | A rendered offline level, player movement, and cutting, lifting, carrying or hiding on that build | [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Settled part (2026-11-20) | On a Win10 guest with no network, and with its user-mode callback filter turned off, the unchanged packed 4.04r2 opened the offline tutorial level drawn, with the player in it; holding Right walked the player to the beach and the view scrolled. The next key hold closed the client, and four later starts closed within 5 s of Offline Test, so offline play works but not reliably there | [lab] (protocol/lab-appe-mirae-2026-11-20d.md#windows-404r2-offline-scene-on-win10-e610-e611-partly-run) |
| Best guess | It plays offline as 4.20r6 does, once the level files it expects are present. Confidence: low | [inf] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Settles it | A controlled scene with captured actions and the state before and after each one | [inf] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Outlook | Lab | [inf] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |

### E#611 Windows 4.04r2 pickup semantics and input qualification

**Question.** What 4.04r2's pickup-bound field means and which key reaches it. The pickup state is recovered statically, but no interaction was captured [bin][cap] (client-internals/404r2-carry-state.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Static recovery separates the pickup action, the carried category and the carrying flag | [bin][cap] (client-internals/404r2-carry-state.md) |
| Open | The meaning of the pickup-bound field, the asset behind a provisional second cut pattern, and whether the second A throws or drops (the key itself is now known: A) | [bin] (client-internals/404r2-carry-state.md#open-questions) |
| Evidence | The countdown cannot give elapsed timing without the clocks of → §4.1.7 | [bin] (client-internals/404r2-carry-state.md#timing-and-input-limits) |
| Tried (2026-11-20) | The same Win10 offline session never reached a liftable object before the client closed, so no lift, carry or throw was captured | [lab] (protocol/lab-appe-mirae-2026-11-20d.md#windows-404r2-offline-scene-on-win10-e610-e611-partly-run) |
| Tried again (2026-11-20) | About 13 more starts on the same guest, with bush tiles added beside the tutorial start, never reached the login window: each stopped at the start-up callback crash, so this guest gives no repeatable scene | [lab] (protocol/lab-appe-mirae-2026-11-20d.md#windows-404r2-offline-scene-on-win10-e610-e611-partly-run) |
| Evidence (2026-11-20) | Under Wine (OpenGL renderer) offline play is repeatable. A is the pickup key (D and S do nothing under the tutorial's `disableweapons`): one tap lifts a bush and changes its tiles, walking carries, and a second tap ends the carry. The stock offline files have no lift or carry animation, and the carried or thrown bush is never drawn, so a throw cannot be told from a drop on screen | [lab] (protocol/lab-appe-gwentea2-2026-11-20e.md#windows-404r2-pickup-in-offline-mode-under-wine-e611) |
| Best guess | The bound field is the carried object's kind, set when the lift starts. Confidence: low | [inf] (client-internals/404r2-carry-state.md#open-questions) |
| Settles it | A semantic read of the field, then a debugger or memory read of it around each action in the Wine scene | [inf] (client-internals/404r2-carry-state.md#open-questions) |
| Outlook | Read, then Lab | [inf] (client-internals/404r2-carry-state.md#open-questions) |

## E.7 Servers, listserver, RC and NC

These questions are about the programs on the other side of the connection (→ Parts V to VII). They split cleanly in two: the lab servers and staff tools that are held can answer theirs, while questions about what the official servers of 1999 to 2010 did depend on a capture of a public service or on source that is not held [doc] (AGENTS.md#labs).

### E#400 Two projects called Ash

**Question.** Whether the two things the notes call Ash are one project at two stages or two projects that share a name [src] (server-notes/01-lineage.md#what-is-binary--world-only).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | Ash is a Python rewrite of the gs2emu protocol with its own world and default port 14812; it is not the Reborn 2.4 binary | [src] (server-notes/01-lineage.md#what-is-binary--world-only); [src] (server-notes/ash-overview.md) |
| Claim B | Ash is the blueprint pack of the 2006 39ster 2.1 GServer, describing that server as written; default port 14822 | [src] (ash/INDEX.md); [src] (ash/ARCHIVAL-NOTE.md) |
| Best guess | Two projects that share a name: the ports, languages and subjects differ. Confidence: moderate. The manual keeps them apart (→ §5.2, → §5.3.1) | [inf] (ash/ARCHIVAL-NOTE.md) |
| Settles it | The Drive archives of both, compared by date and content | [doc] (ash/ARCHIVAL-NOTE.md#full-archive) |
| Outlook | Missing: the full archives are owner-held | [doc] (ash/ARCHIVAL-NOTE.md#full-archive) |

### E#401 Listserver reply ids 1 and 2

**Question.** What listserver reply ids 1 and 2 meant in 2002. The 1.41 game client, RC 1.41 and later clients read them differently [srv] (protocol/listserver.md#listserver--client; protocol/listserver-141r1-silent-list.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | Id 1 is empty and id 2 is status text with `\r` as a line break; 2.17, 2.22 and the public service send status text as id 2 | [srv] (protocol/listserver.md#listserver--client); [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| Claim B | RC 1.41 (2002) reads id 1 as one more server entry and id 2 as the end of the list, then disconnects | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Claim C | Game client 1.41 rev 1 reads id 1 as one more server entry and ignores 2, 3 and 4; it never sends a list login | [bin][lab] (protocol/listserver.md#141-rev1-no-login-the-server-speaks-first-binlab; protocol/listserver-141r1-silent-list.md) |
| Best guess | The 2002 listserver used 1 as "one more server" and 2 as "end of list", as both 1.41 programs read; the meanings changed when the later listserver took over. Confidence: moderate | [inf] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Settles it | A 2002-era listserver binary or capture, or a re-read of the 2.05 handler for id 1 | [inf] (protocol/listserver.md#205-specifics-205) |
| Outlook | Read for 2.05's handler; Maybe never for the 2002 service itself | [inf] (protocol/listserver.md#205-specifics-205) |

### E#402 The 2000-era listserver reply

**Question.** Whether today's legacy listserver reply is what the service sent in 2000 to 2002 [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | A real 2.00-era reply is observed: one plain zlib frame, id 0 only, 4 rows, no status, site or upgrade lines (the public 14923 reply to a classic login) | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| Claim B | What a real 2.00-era listserver sent is unobserved; the two-frame list 2.00 accepted in the lab came from a lab forwarder | [lab] (protocol/listserver.md#205-specifics-205) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | Today's legacy reply is a kept copy of the old path and matches it in shape, though not in content. Confidence: moderate | [inf] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| Settles it | A capture of a real 2.00 or 2.05 against the 14923 service, or a 2000-era listserver binary | [inf] (protocol/login-frames-by-version-2026-10-25.md#captures-that-would-settle-it-all-read-only-list-requests) |
| Outlook | Owner for today's service; Maybe never for the service of 2000 | [doc] (AGENTS.md#labs) |

### E#403 Classic logins on port 14922

**Question.** Why a real 2.17.1 sends a classic login to a port that does not answer it today [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | A real 2.17.1 sends a classic login (shape B) to port 14922, the port in its signed `arrays2.dat` | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Claim B | The public 14922 accepts a classic login and never answers it; the 2001-era tools put pre-2.2 clients on 14923 | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result); [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |
| Open | Whether the 2001 service answered classic logins on 14922, whether 2.17.1 was built for another listserver, and whether the zlib header (`78 DA` against `78 9C`) matters | [inf] (server-notes/lab-servers-2026-10-30.md#real-clients-against-it-today-lab); [inf] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | 14922 answered classic logins when 2.17.1 shipped and stopped when the service moved them to 14923; the zlib header does not matter. Confidence: moderate | [inf] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| Settles it | A list-only capture of a pristine 2.17.1 against the public service, with the owner's written permission | [doc] (AGENTS.md#labs) |
| Outlook | Owner; even then, today's service may not show what 2001's did | [doc] (AGENTS.md#labs) |

### E#404 A public server refusing 2.05 inside its own range

**Question.** Why a public server refused 2.05 although its printed range seems to include it [src][inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The printed range runs from 1.41r1 to iPhone Belote 1.5, which in the current version table covers every 2.x to 6.x entry | [src][inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Claim B | The same server refused 2.05 (`GNW03081`) | [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | The server runs an older version table with no 2.05 entry, so 2.05's token falls outside the range by lookup. Confidence: moderate | [inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Settles it | One 5.00r7 or 6.03r7 login to that server, with the owner's written permission | [inf] (server-notes/public-allowed-versions.md#open) |
| Outlook | Owner | [inf] (server-notes/public-allowed-versions.md#open) |

### E#406 How the official listserver assigns PC ids

**Question.** The rule by which the official listserver turns a client's machine fields into a PC id [src] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The id is a signed 64-bit decimal from `SVI_ASSIGNPCID`; the listserver's inputs are the identity string, account, password and the game server | [src] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| Also open | Whether 5.12 reads the product id as 5.24 and later do; what `getlockcomputer` compares; what 6.11 and later connector scripts send as machine fields; the empty product id under 64-bit Windows | [inf] (protocol/pcid.md#open) |
| Tried (2026-11-20) | The owner approved the public captures, but no lab device holds an account for the public service, so none was run; the project leaves this entry open rather than contact the service again | [doc] (AGENTS.md#labs) |
| Best guess | A row number in a listserver table of machines matched on the hardware hashes; a truncated hash of the fields would fit too. Confidence: low | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| Settles it | The official listserver, or captures of its `ASSIGNPCID` replies for known inputs (public servers need the owner's written permission) | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| Outlook | Maybe never for the rule, which lives only in the operator's database; a clean-room server can pick its own rule, since clients only store the number | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |

### E#422 Quoting of folder rights

**Question.** Whether the original server stored folder rights in the RC's CSV form [cap] (protocol/rc-capture-2026-11-04.md#rights).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The 2004 RC sends folder-rights lines as CSV, so `rw levels/*` goes out quoted, and splits what it reads back the same way | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| Claim B | A GServer-v2 fork returned the line unquoted, and the RC showed it as two lines | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| Evidence | In RC script text, trailing empty fields are kept and the GServer-v2 fork doubles backslashes inside quoted lines; the original RC2 and RC3 rule is unread | [cap][doc] (protocol/rc-text-escaping-status.md) |
| Best guess | The original server stored and returned the CSV form, so the fork's reply is a fork bug. Confidence: moderate to high, because the RC was built against that server | [inf] (protocol/rc-capture-2026-11-04.md#rights) |
| Settles it | A capture of 62 from an original 2.x GServer, or a static read of its rights reply | [inf] (protocol/rc-capture-2026-11-04.md#rights) |
| Outlook | Maybe never for the original server; a clean-room server should follow the RC | [inf] (protocol/rc-capture-2026-11-04.md#rights) |

## E.8 NPC scripting

These questions are about GS1 and GS2 (→ Part VIII). GS1 is read one build at a time, so its open points are mostly "does the 2.05 result hold elsewhere". GS2 is the largest open area in the manual: the bytecode container and the opcode sets are read, but the language, its library and its event model are known only in part [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting).

### E#203 The 2.05 `#` message-code set

**Question.** The full set of 2.05 `#` message codes, what each field holds, and how other builds differ [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled part | Original 2.05r2's outer dispatch has 44 selector bytes, 53 family-expanded spellings, including preserved display codes and an empty `#7` (→ §8.1.11); thirty outputs from three usable offline scenes bound the expansion | [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage); [lab] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls) |
| Settled part | `#a` is the account and `#L` the recorded level name; `#6` held the carried NPC's lowercased image name in a pickup and drop control; the shared `#p` list is made by dispatch splitting the actor's pending text, with `callnpc` and `callweapon` using empty-parameter queue wrappers | [2.05][bin][lab] (npc-library/gs1-message-codes-205r2.md#field-identities-a-l-e-and-a-positive-carry-control); [bin] (npc-library/gs1-message-codes-205r2.md#independent-carried-npc-association-checkpoint); [bin][lab] (npc-library/gs1-event-parameters-205r2.md#producer-and-consumer-linkage; npc-library/gs1-event-parameters-205r2.md#new-end-to-end-original-client-controls) |
| Settled part | Other builds: `#F`, `#S`, `#I` and `#P6` to `#P9` hold values from 2.17.1, `#R` from 2.22, `#D` exists from 2.17.1 (empty in the context tested), and `#C6` and `#C7` stay empty everywhere; `##` is a one-pass escape on 2.05r2 and 2.17.1 and an empty code on 1.33 (→ §8.2.12) | [lab] (live-runs/open-issues-2026-11-14/README.md#1c-f-s-d-i-r-p6p9-c6c7-in-a-populated-context) |
| Settled part | 2.17.1 names 46 codes; 2.22 and 2.31 add `R(S)`; Linux 3.04 drops `C5`, `C6` and `C7`; 1.41r1 has no `#e` or `#K` | [bin][lab] (npc-library/gs1-message-codes-by-build.md#registered-names) |
| Boundary | Reading `C5` from storage does not prove a sixth clothing colour or change the five-byte wire colour prop; prop setters have a separate grammar | [bin] (npc-library/gs1-message-codes-205r2.md#character-selectors) |
| Open | The writer of `#E` (a space in one context), quoted scanners, exact number formatting and renderer semantics in 2.05; why a bare `#5` or `#6` on 2.17.1, 2.22 and 2.31 is replaced by the label text in front of it while 2.05r2 shows it empty | [bin][lab] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls); [lab] (npc-library/gs1-message-codes-by-build.md#bare-5-and-6) |
| Settled part (2026-11-20) | In 2.05 rev 2 `#E` always expands to a single space, a placeholder no feature fills | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#the-e-message-code-in-205-e203) |
| Best guess | `#E` is a field no 2.05 feature fills, left from an earlier design; the bare `#5` and `#6` effect is a scanner change in 2.17 that backs up over the label when the code has no index. Confidence: low | [inf] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls) |
| Settles it | A 2.17.1 trace of the bare-code scanner (its expander was not found by the 2026-11-20 read) | [inf] (npc-library/gs1-message-codes-by-build.md#bare-5-and-6) |
| Outlook | Read | [inf] (npc-library/gs1-message-codes-by-build.md#bare-5-and-6) |

### E#207 GS2 language and bytecode format

**Question.** GS2's syntax, standard library and event model, enough to write a compatible compiler and VM. Each result below closes part of it [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | 4.x and later clients run GS2 and receive it compiled; 3.153 already handles the NPC bytecode ids | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| Container | 4.2.0.8, 5.0.0.7 and unpacked 6.00 parse one four-segment container unlike OpenGS1's and run the switch in → §8.4.2 and → §8.3.3; the value stack caps at 10000, opcode 9 stops past 10000, and opcode 10 stores the stack height without jumping | [bin] (protocol/gs2-client-vm.md#container-the-client-reads); [bin] (client-internals/gs2-vm-from-engines.md#opcodes) |
| Official output | 19 server-compiled bodies from 6.113 caches walk with the 4.2 to 6.00 reader: segments 1 to 4 in order, segment 1 zero, `F0` to `F6` operands in range, no trailing newline, no opcode at or above 200; the official compiler emits 190 `loadparams`, which the third-party compiler does not | [cap] (protocol/gs2-official-bytecode-6113.md#container-what-all-19-bodies-show) |
| Opcode sets | Case sets for 4.03r3 to 7.12.43, Linux 6.x x64 and Android 1.8 and 2.2: 119, 154, 158, 165 and 167 cases; the dispatcher stops changing at 5.30r3; four portability rules for a compiler (→ §8.4.4) | [bin] (protocol/gs2-opcode-table.md#case-sets) |
| Events | 221 distinct engine `on…` names across nine builds, with 55 `onSend…` hooks new in 6.1.1.3 (→ §8.3.4) | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| Linux 4.04r2 | Two instrumented dispatches repeat top-level execution and queued delivery follows the running handler; a positive-sleep snapshot keeps the next instruction through restore; correct grouping gives 176 types and 332 globals; dispatch ends at 190 and slot 11 selects a common skip path; fourteen script candidates include one profile payload matched to live input (→ §8.3.4, → §8.3.5, → §8.4.4, → §8.4.7) | [cap] (client-internals/linux-404r2-events.md); [cap] (client-internals/linux-404r2-sleep.md); [test] (client-internals/linux-404r2-api-ownership.md); [bin][cap] (client-internals/linux-404r2-vm-dispatch.md); [bin][cap] (client-internals/linux-404r2-embedded-scripts.md) |
| Cross-version | The Linux follow-ups separate static selector classes, executor-entry stops and three observed startup cached jumps; record static state saving and first-match pending-record replacement; and explain serialized tags against fused internal selectors, each without claiming a wider result (→ §8.3.4, → §8.4.4, → §8.4.6, → §8.4.7) | [bin] (client-internals/linux-cross-version-embedded-controls.md); [bin] [cap] (client-internals/linux-cross-version-dispatch.md); [bin] (client-internals/linux-420r6-selector11.md); [bin] (client-internals/linux-420r6-reader-fusion.md) |
| Other builds | Windows 5.00 queues named and enum delivery separately from service, with limit-before-dedup and named lifecycle priority bounded statically; Linux 6.01 x86 separates reader, post-pass and executor preparation; the Mac OS X 6.11r1 runner decodes 40-byte records with cached handlers, an end marker 164, a per-record loop check with default limit 10000, snapshot-based sleep and waitfor, and calls that can suspend on `classesdownloaded` (→ §8.3.4, → §8.4.4) | [bin][inf] (client-internals/windows-500-event-queue.md); [bin] (client-internals/linux-601-x86-program-state.md); [bin] (client-internals/mac-611r1-gs2-runner.md) |
| Language use | Three owner-held script sets rank the GS2 constructs real 2007 to 2008 scripts use (joins, methods, for-each, `switch`, GUI `new`, code outside functions) and the GS1 commands a port must replace; no message code sits inside a GS2 string literal | [lab] (npc-library/gs2-world-corpus-2026-11-12.md) |
| Open | The built-in command table's semantics and the source grammar the official compiler accepts; which gameplay site fires each event name; packet 140's own framing; the Linux x86 and ARM Android dispatchers; handler effects on 5.30r3 and 7.12.43; 5.00r7 and 5.12 from the shipped DLLs; table extent, opcode 7 and arithmetic handlers on the Mac runner | [bin] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written); [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation); [bin] (protocol/gs2-opcode-table.md#still-open); [inf] (client-internals/gs2-engine-event-names.md#still-open) |
| Best guess | The official compiler accepts the GS2 syntax the archived scripting pages and the world corpus show, and the clients' opcode semantics are stable from 5.30r3 on, so one compiler targeting 5.30r3 to 6.03r7 is realistic; the event model is a per-object queue drained once per 50 ms step. Confidence: moderate | [inf] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written) |
| Settles it | A decoded bytecode message from a 4.x lab session, a reading of the built-in command table and the compiler's grammar, and a note on the GS2 documentation in the archived websites | [bin] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written); [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Outlook | Read and Lab for the client side; Maybe never for the official compiler's own source, so its grammar must be inferred from its output | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

### E#209 GS2 VM: what the per-build reading left open

**Question.** The VM details the six-VM reading of 3.153 to 6.03r7 left open. The cross-version table settles some and names the builds still unread [bin][doc] (client-internals/gs2-vm-loader-diff.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Opcode 54 | On unpacked 6.1.1.3 it is a member store: drop two values, convert the value then on top, store as opcode 50. 5.00r7's pop count still has two descriptions (two values, or value plus name plus object) | [bin] (protocol/gs2-unpacked-6113.md#cases-54-and-121); [doc] (client-internals/gs2-vm-loader-diff.md#500r7-and-512) |
| Opcodes 48, 49 | Operand order unread | [bin] (client-internals/gs2-vm-by-version.md#not-known) |
| `waitfor` timeout | Followed on 5.12 and 6.00r2: the wait is saved with 1 and resumed with 0 after the deadline; not followed on 4.20r8 | [doc] (client-internals/gs2-vm-loader-diff.md#500r7-and-512) |
| 6.x loop limit | 5.24r4 to 5.31r4 still name the property `maxlooplimit`; 6.00r2 and 6.00r4 keep the field under a scrambled name | [bin] (client-internals/gs2-vm-by-version.md#limits); [doc] (client-internals/gs2-vm-loader-diff.md#524r4-530r3-531r4-600r2-and-600r4-windows) |
| Unread builds | Windows 4.04r2, 5.12 and 5.24r4 to 6.00r4 are now read; still unread are Mac 4.04r2, Mac 5.12, the December 2006 Mac 4.20r6, 6.015, 6.034, Android Era, Classic other than 1.8, and 7.x (out of scope) | [doc] (client-internals/gs2-vm-loader-diff.md#still-open) |
| Tried (2026-11-19) | Script fuzz on 6.03r7, 5.24r4 and 4.20r8: setting `maxlooplimit` works on 6.03r7 and 5.24r4 (50 reads back as 100; 2000000 lets a 20000-pass loop stop as expected), so 6.03r7 still takes the property by that name; opcode 54 on 6.03r7 and 5.24r4 matches the two-value prediction for every push order and is not dispatched on 4.20r8; opcodes 48 and 49 give an empty value on 4.20r8 and 5.24r4 and crash 6.03r7, so their operand order still needs 5.00r7 or 5.12, which dispatch them | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Settled (2026-11-20) | On 5.00r7, 54 consumes three values, pushed as object, member name, value, then runs the opcode-50 store. 49 pops up to its clamped count and appends in pop order, so the list is in reverse push order. 48 builds an object from pairs pushed name then value, but its loop counter counts up, so with a positive count it takes pairs until two or fewer values remain | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#gs2-opcodes-48-49-and-54-on-500r7-e209) |
| Best guess | The 6.x property is still `maxlooplimit` under the scrambling, as the fuzz run shows for 6.03r7. The remaining items are the unread builds. Confidence: moderate | [inf] (client-internals/gs2-vm-loader-diff.md#still-open) |
| Outlook | Read | [doc] (client-internals/gs2-vm-loader-diff.md#still-open) |

The work list carried from the difference table:

- [x] ~~Prove opcodes 48 and 49's operand order on 5.00r7.~~ Settled by the 2026-11-20 read [doc] (client-internals/gs2-vm-loader-diff.md#still-open)
- [x] ~~Pick one pop count for opcode 54 on 5.00r7.~~ Three values [doc] (client-internals/gs2-vm-loader-diff.md#still-open)
- [ ] Recover the 6.x loop-limit property name. [doc] (client-internals/gs2-vm-loader-diff.md#still-open)
- [ ] Read the VMs still marked open in the difference table, including event-name case (`onTimeout` / `onTimeOut`) and the client match for `onActionServerSide`. [doc] (client-internals/gs2-vm-loader-diff.md#still-open)

### E#210 Particle emitter and `format` details

**Question.** The details of the particle emitter and of opcodes 82 and 84 (`format`, `indexof`) that the static read left open [bin] (client-internals/showimg-particles-and-gs2-format.md#not-settled).

| Part | Discussion | Source |
| --- | --- | --- |
| Open | Whether `removemodifiers()` clears the emit list as well as the local and global lists | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Open | When a global modifier's clock starts; the read suggests time zero, so a global `once` fires on the first frame | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Open | The exact particle kinds; "store its own data (good for text emitters)" shows that a text kind exists | [doc] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Open | Case handling in `indexof`, and whether `%d` truncates or floors | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Tried (2026-11-19) | `%f` and `%5.2f` follow C printf on 4.20r8, 5.24r4 and 6.03r7, and a string that is not a number formats as −1; `%d`, `indexof` case and the particle points were not in the fuzz set | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Settled part (2026-11-20) | On 4.20r8 and 5.12, `%d` floors (−3.7 → −4), `%i` truncates 3.7 to 3, `%x` and widths follow C, and position and index lookups are case-sensitive | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#format-and-indexof-e210) |
| Settled part (2026-11-20) | On 4.20r8, 5.12, 5.24r4 and 6.03r7, `removemodifiers()` clears the emit list and the live particles while emission goes on; a global "once" modifier fires on the first frame after it is added, and a global "impulse" runs on its own interval | [lab] (protocol/lab-appe-gwentea2-2026-11-20b.md#particle-modifiers-e210) |
| Best guess | The particle kinds are as read; `%d` truncates and `indexof` is case-sensitive as read. Confidence: low to moderate | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Settles it | A run that changes the property that picks the particle kind, and the `format` checks, on a 4.x or 6.x client | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
| Outlook | Lab | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |

### E#211 Which objects make 6.00 fuse fold 241

**Question.** Stock 6.00 makes fold 241 when a name load resolves to an object carrying a flag and a store or resolve follows. Which objects carry that flag (→ §8.4.6) [bin] (protocol/gs2-fold-241-2026-11-16.md#234242-600).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Every other fold from 200 to 242 matches between stock 4.20r8, 5.00r7 and 6.00 and the open reimplementation; 241 is the one left out, on purpose, until the flag is known | [bin][doc] (protocol/gs2-fold-241-2026-11-16.md#verdict) |
| Best guess | The flag marks objects that resolve once and can be cached on the instruction, such as weapons and globals; running the sequence unfused gives the same result, more slowly. Confidence: low for the flag, moderate for "same result" | [inf] (protocol/gs2-fold-241-2026-11-16.md#still-open) |
| Settles it | A deeper static read of the 6.00 fusion stage at the flag test | [inf] (protocol/gs2-fold-241-2026-11-16.md#still-open) |
| Outlook | Read | [inf] (protocol/gs2-fold-241-2026-11-16.md#still-open) |

### E#214 Why some official bodies do not end in a return

**Question.** 18 of 660 official bodies do not end in a return instruction. Whether that is intended, truncation, or a separate emitter path (→ §8.4.10) [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#enlarged-residual-bodies-that-do-not-end-in-a-return).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | The other 642 end in a return; the 18 are a real residual, and the official compiler is not held | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#enlarged-residual-bodies-that-do-not-end-in-a-return) |
| Best guess | A separate emitter path for one kind of script, since the bodies otherwise look clean; a client that stops at the end of the stream handles both. Confidence: low | [inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#still-open) |
| Settles it | Grouping the 18 by what they are, from the private bodies; or the official compiler | [inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#still-open) |
| Outlook | Owner, since the bodies stay private; Maybe never for the compiler's reason | [inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#still-open) |

## E.9 Graal3D and the Torque-era 3D

These questions are about the 3D side: the 2000 Graal3D client and the Torque-based plug-in of the 3.x and 4.x clients (→ Parts IX and X). They matter less to a 2D server, and most are answerable from the held plug-ins [bin] (graal3d/torque-engine-4x.md#not-done).

### E#507 3.04 sheet type 5 and server tile definitions

**Question.** What a `tiledefs` entry of type 5 changes in 3.04, and whether a 3.04-era server sent `addtiledef` lines at login (→ §10.7.8) [bin] (torque/304-tile-types.md#not-settled).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | Type 5 is accepted when picking an entry and sets a flag of its own; the package ships only the offline tutorial's line | [bin][file] (torque/304-tile-types.md#how-the-sheet-type-is-chosen) |
| Settled part (2026-11-20) | A read of 3.04: type 5 comes from a per-level tile-type table and is a walk rule, with its own path in the walk classifier and a ground height of 0; it is not only a drawing variant | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#sheet-type-5-on-304-e507) |
| Best guess | Type 5 is a walk rule (now read); ordinary servers sent no tile definitions, so the per-level table was filled by the client's own defaults. Confidence: low | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#sheet-type-5-on-304-e507) |
| Settles it | A read of what fills the per-level tile-type table; any 3.04-era server capture | [inf] (client-internals/static-reads-appendix-e-2026-11-20-d.md#sheet-type-5-on-304-e507) |
| Outlook | Read for the flag; Missing for the server side | [inf] (torque/304-tile-types.md#not-settled) |

## E.10 Tools

This question is about the period's editors and the formats they wrote (→ Part XI) [doc] (tools/graalshop.md#movie-mode-file-grammar).

### E#612 GraalShop movie editor attribution and sample limits

**Question.** Which editor wrote the movie format, and how a movie plays [doc] (tools/graalshop.md#movie-mode-file-grammar); [doc] (tools/graaleditor-vs-205.md#workflow).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The movie-grammar note attributes its read to a 2002-05-01 editor | [doc] (tools/graalshop.md#movie-mode-file-grammar) |
| Claim B | The comparison describes the old 2002 editor as sprite-only and ties movie support to the 2006 editor | [doc] (tools/graaleditor-vs-205.md#workflow) |
| Evidence | The Classic+ 1.13 and Era+ 1.0 sample confirms lowercase boolean spellings for its `SPRITE` and `TEXT` declarations only (→ §3.3.6); a packaged mobile movie cannot say which editor wrote it | [file][doc] (tools/graalshop.md#shipped-movie-sample-and-remaining-limits) |
| Open | Indexed `CHAR`-key spelling, coordinate units, frame duration and native interpolation and playback | [file][doc] (tools/graalshop.md#shipped-movie-sample-and-remaining-limits) |
| Best guess | The 2006 editor wrote the movie format, and the 2002 attribution names the wrong input. Confidence: low to moderate | [inf] (tools/graaleditor-vs-205.md#workflow) |
| Settles it | The exact editor inputs and their reader and writer evidence reconciled, then a controlled playback test on a client that plays movies | [inf] (tools/graalshop.md#shipped-movie-sample-and-remaining-limits) |
| Outlook | Missing for the editor identity; Lab for playback | [inf] (tools/graalshop.md#shipped-movie-sample-and-remaining-limits) |

## E.11 What may never be known

The project's aim is to be as complete as the surviving evidence allows. Some questions have a clear path to an answer, and the outlook column of → §E.1 marks them Lab or Read. Others depend on material that may no longer exist, and it is better to say so than to let a guess harden into a fact [inf] (client-internals/build-catalogue.md).

Three kinds of evidence are missing for good, or nearly so:

- **Lost builds.** No binary of 2.12 to 2.16 or of 2.19 to 2.21 is held, so the first build of the `maps` folder (→ App. E#10) and the generation-4 wire (→ App. E#19) rest on neighbours and on server source. A build that turns up in an old archive would reopen them at once; the build catalogue lists what to look for. [bin] (client-internals/build-catalogue.md)
- **The official servers' own code and data.** The 1999 to 2010 official game servers, listservers and RC backends were never published. Their rules can only be inferred from what the clients expect, from open-source servers written to match them, and from today's services, which may have changed. This limits E#401, E#402, E#406 and E#422, and the meaning of the `GNW` digits (→ App. E#12). [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields)
- **Signed or server-held scripts.** From 6.11 on, the protocol itself lives in a script the operator signs (→ §2.10). The structure can be learned with a lab-signed script, but the production script's exact content can only come from the live service (→ App. E#616). [inf] (protocol/v7-connector-live-20261111.md#5-open)

For these, the manual's rule is the same as everywhere else: state what is known, mark the rest, and keep the entry open. A clean-room server or client does not need most of these answers, because the client tolerates a range of server behaviour; where it does need one, the best guess in the entry is the starting point and the lab run in "Settles it" is the check. [inf] (protocol/probe-targets-2026-11-18.md)

## E.12 Settled questions

These questions were answered. Each answer, with the record of how it was settled, now sits in the chapter section named below, under a paragraph that starts "Settled question, formerly E#n". The numbers are kept so that older notes which cite them can still be followed (→ §E.0).

| Entry | Question | Answer now in |
| --- | --- | --- |
| E#2 | Generation-5 step count of 5.12 and 5.00r7 | → §2.2.3 |
| E#4 | Whether 5.00r7 sends id 11 | → §2.4.2 |
| E#5 | Meaning of id 162 from the client | → §2.4.9 |
| E#6 | Client-to-server constants of 1.21 and 1.32 | → §2.4.2 |
| E#7 | Receive-branch revision discrepancy | → §2.5.2 |
| E#8 | Prop parser ranges of 2.00 | → §2.6.6 |
| E#9 | Uploads from game clients | → §2.7.1 |
| E#11 | Client-to-server ids the NewWorld betas lack | → §2.4.2 |
| E#13 | Gmap neighbour overwrite on classic-login 2.x clients | → §2.5.3.2 |
| E#14 | Expiry dates of the Themida 5.x/6.00 builds | → §1.8.7 |
| E#17 | The 6.1.1.3 login after the RC4 switch | → §2.10.8 |
| E#20 | The 2.31 step on `PLO_SETACTIVELEVEL` (156) | → §2.5.3 |
| E#21 | Whether a compiled gani script (`PLO_GANISCRIPT`, 134) runs | → §2.5.6 |
| E#22 | `DEFAULT*` lines in `PLO_LOADGANI` (195) | → §2.5.6.1 |
| E#23 | What prop 81 changes in the player list | → §2.6.6 |
| E#24 | Baddy props 11 and up | → §2.6.6 |
| E#25 | The 2.22 start-up file checks: 13 against 17 | → §2.7.10 |
| E#100 | Collision of the Bush stamp tiles | → §3.5.2.2 |
| E#102 | Tile id to pixel position on pics1 | → §3.5.1 |
| E#200 | When a GS1 condition counts as true | → §8.1.3 |
| E#201 | Four GS1 argument signatures in 2.05 | → §8.2.1 |
| E#202 | Which message carries GS2 bytecode | → §8.4.1 |
| E#204 | Writing to GS1 object members | → §8.2.5 |
| E#205 | Index of the hare baddy | → §8.2.2 |
| E#206 | `move` option bits in 2.05 | → §8.2.9 |
| E#208 | What the OpenGS1 opcode set describes | → §8.4.3 |
| E#212 | Whether a function-only image skips the top-level pass | → §8.4.10 |
| E#213 | How GS2 text bytes draw on screen | → §8.4.10 |
| E#215 | When GS2-only names arrived, and what a missing name does | → §8.3.9 |
| E#300 | Frame driver of 4th Graal alpha, 5th Graal and 5th Graal alpha | → §4.1.2 |
| E#301 | Frame loop of the 3.x and 4.x clients | → §4.1.7 |
| E#302 | Walking speed factors other than 1.0, 1.2 and the hidden 0.2 | → §4.2.1.1 |
| E#303 | Two unidentified lists in the blocked-point test | → §4.2.3 |
| E#305 | The 2.22 push frame field | → §4.2.5 |
| E#306 | What picks `lift2.wav` for a pull | → §4.2.8 |
| E#307 | Probe, nudge and step tables of 1.39 | → §4.2.2.2 |
| E#308 | Link probe offsets and the neighbour-table flag | → §4.2.11 |
| E#309 | Knockback distance of 1.39 | → §4.3.7.2 |
| E#310 | Where the once-per-second hit stamp sits | → §4.3.3 |
| E#311 | Blast hit zone and the occasional full-heart hit | → §4.3.5 |
| E#312 | The last byte of a shot | → §4.3.5.2 |
| E#313 | Do arrows and fireballs pass walls | → §4.3.5.2 |
| E#314 | Gmap entry and the respawn save | → §4.4.4 |
| E#315 | The level-entry save in the 2.1 test builds | → §4.4.4 |
| E#316 | Glove power steps | → §4.5.2 |
| E#317 | The 1.x pickup box and item draw order | → §4.5.2 |
| E#318 | Level reload on re-entry offline | → §4.5.7 |
| E#319 | The single-player start levels | → §4.8.3 |
| E#321 | The 2.31 window blacklist | → §4.10.1.2 |
| E#322 | How others see a key emote | → §4.10.3 |
| E#326 | Remaining 6.03r7 HUD measurements | → §4.6.9 |
| E#327 | Missing chest art and menu skin in the 6.03r7 item run | → §4.5.8 |
| E#328 | What drives 2.22's tick | → §4.6.10 |
| E#405 | RC token `GSERV025` | → §7.1.1 |
| E#420 | Flag and chest counts in the RC props tail | → §7.1.8 |
| E#421 | The last byte of RC_PLAYERPROPSSET2 | → §7.1.8 |
| E#423 | The 1999 servers: what the static read left open | → §5.1.6 |
| E#424 | RC2's Admins folder against a one-space level | → §7.1.9 |
| E#425 | Standalone NC flag-action recipient and ranges | → §7.3.4 |
| E#500 | Back clipping plane of the Graal3D client | → §9.4 |
| E#501 | Class CRC of the 4.04r2 3D plug-in | → §10.3.2 |
| E#502 | Whether 4.04r2 loads `.mis` mission files | → §10.6 |
| E#503 | Whether 4.04r2 reads `.dso` compiled TorqueScript | → §10.6 |
| E#504 | The `GR3DV003` beta at run time | → §9.7.3 |
| E#505 | How a server makes a 5.12 player move in 3D | → §10.3.8 |
| E#506 | Protocol 19 against a real 3.153 or 4.04r2 client | → §10.3.9 |
| E#600 | Tile layer as GraalEditor writes it | → §11.1.2 |
| E#601 | Whether link arrival offsets are evaluated | → §11.6.4 |
| E#602 | Code width of `Z3-V1` boards | → §3.1.1.2 |
| E#603 | Whole tiles and fractions in level records | → §3.1.2.5 |
| E#604 | Where a binary sign list ends | → §3.1.2.6 |
| E#605 | Client listserver frames in two vocabularies | → §6.1.3 |
| E#606 | Whether a gmap carries `HEIGHTS` blocks | → §3.2.4 |
| E#607 | Leftover lines in the protocol cheat sheet | → §2.1.2 |
| E#608 | How many `arrays.dat` lists make a tile passable | → §3.5.3.1 |
| E#609 | macOS archive labels and application identity | → §1.9.1 |
| E#613 | Windows 2.22 remote PM roster and visible result | → §2.8.7 |
| E#614 | Tiledef type 4 consumer | → §3.5.2 |
| E#617 | Whether 1.41 rev 1 loads `.nw` levels online | → §1.5 |
| E#619 | Whether 5.30r3 and 5.31r4 use their built-in login host | → §1.9.4 |
| E#620 | What the 1.41 rev 1 program-check handler does | → §1.1.5 |
