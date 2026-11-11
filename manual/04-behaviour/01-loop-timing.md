<!-- manual: kind=reference status=draft -->
# 4.1 Frame loop and timing

This chapter fixes the tick that every count in Part IV uses, how each build drives it, and the periodic work that runs off it. Durations of individual actions are in the chapter for each action (→ §4.1.5).

> Status: draft. The notes cover configured intervals and runtime timing separately; the three early builds in App. E#300 have static configuration and a callback-execution count, not a measured cadence; the 3.x and 4.x Torque-era loops are not in the notes (→ App. E#301).

## 4.1.1 The tick

Everything in Part IV is counted in ticks. The rules below fix the tick's length and show that it holds from the first Delphi build to 6.x [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules).

| Rule | Detail | Source |
| --- | --- | --- |
| length | one game tick is 50 ms (20 ticks per second) | [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules); [2.05] (client-internals/decomp-findings-2026-10-24/constants-205.tsv) |
| same in every Delphi build | the static survey of all 57 Delphi executables finds a 50 ms frame interval wherever a frame timer is present | [bin] (version-profiles/matrix/builds-static-survey.tsv) |
| tick counter | 2.05 and 2.22 keep a per-player tick counter that rises by one every 50 ms whatever the player does | [live][2.22] (live-runs/2gta-222-2026-10-30/README.md) |
| 5.x and 6.x | a moving 5.24r4, 5.30r3 or 6.03r7 client sends its position every 50 ms; their walk, push, lift and sword timings equal 2.05's in ticks | [wire] (protocol/v5v6-lab-play.md) |
| Graal3D | driven by a 50 ms DelphiX timer | [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |

## 4.1.2 What drives the tick, by build

The tick is the same everywhere, but what drives it changes. Each row gives a group of builds and the timer or loop that runs its frame [bin] (version-profiles/matrix/builds-static-survey.tsv).

| Builds | Driver | Source |
| --- | --- | --- |
| 1st Graal to 4th Graal | a DelphiX timer on the main form, interval 50 ms | [bin] (version-profiles/matrix/builds-static-survey.tsv) |
| 4th Graal alpha, 5th Graal, 5th Graal alpha | main adventure form declares an enabled DelphiX timer, interval 50 ms, active-only disabled, maximum lag ten, with a statically bound callback. A debugger count shows the callback runs (61, 61 and 60 hits in 3 s); actual cadence and runtime idle installation remain unmeasured → App. E#300 | [bin] (client-internals/early-form-timers-2026-11-09.md#stored-configuration) [lab] (client-internals/early-form-timers-2026-11-09.md#callback-execution) |
| 6th Graal (beta5) to 1.41 rev1, and Graal3D | a DelphiX timer on the main form, interval 50 ms | [bin] (version-profiles/matrix/builds-static-survey.tsv) |
| NewMain 1.42 to 2.31 (every 2.0x, NewWorld betas 1 and 2, the 2.1 tests, 2.17.1, 2.22, 2.31) | no form timer; the frame runs from the application's idle handler behind a 50 ms gate | [bin] (version-profiles/matrix/builds-static-survey.tsv); [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| 2.31 | in addition, the main form carries a 50 ms timer that runs the 64-tick integrity cycle (→ §4.1.3) | [2.31] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md) |
| 3.x, 4.x | unmeasured | [doc] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| Windows 4.04r2 | still unmeasured, but the core's clocks are traced: `getTicks` is `GetTickCount` and `timevar2` scales it by 0.001; legacy `timeout` counts service passes (set ×20 + 0.0001 floored, read ×0.05); a GS2-style pass advances its script clock 0.05 per pass and drives `istimeout` and scheduled events → App. E#301 | [bin][cap] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-clocks) |
| Mac PowerPC 4.04r2, 4.20r6 and v5 | a Carbon event-loop timer calls the engine entry once; it runs an initialize method, then an update method repeatedly while it returns non-zero, then shutdown, and quits the event loop. The pump sleeps 1 ms when idle. The update rate is not measured | [bin] (client-internals/mac-ppc-startup-input-2026-11-09.md#start-up-one-timer-that-runs-the-whole-engine) |

### 4.1.2.1 The frame function (idle-driven builds)

In the idle-driven builds one function runs each frame. The rules below give its order and two consequences a remake must copy: no catch-up after a stall, and input read once per tick [live] (client-internals/rendering-observations.md#frame-loop).

| Rule | Detail | Source |
| --- | --- | --- |
| order | after the 50 ms gate opens, one frame handles clock skew, network traffic, then drawing | [live] (client-internals/rendering-observations.md#frame-loop) |
| no catch-up | a stall costs one frame; the client does not run extra ticks to catch up, and ignores any step count its pacer supplies | [live] (client-internals/rendering-observations.md#frame-loop) |
| input sampling | key state is read once per tick: a key released and pressed again inside one tick is not seen as a new press, and a tap shorter than a tick can be lost | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |

## 4.1.3 Periodic work

Some work runs every tick and some on a longer cycle. Each row gives the period, the work and the builds it was read in [live][2.05] (client-internals/player-mannerisms-live.md).

| Period | Work | Builds | Source |
| --- | --- | --- | --- |
| every tick | the player state machine steps (walk, push, hurt, death and other counters in §4.2 to §4.4) | all measured builds | [live][2.05] (client-internals/player-mannerisms-live.md) |
| every tick | the tile under the player is checked for water and lava, except while the sword swings, while riding, and when the player is not under local control | 2.05 | [2.05] (client-internals/water-and-ganis.md#water) |
| every tick | the probe point for links is taken and each link of the level is tested (→ §4.2.11) | 2.05 | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| 64 ticks (3.2 s) | a counter modulo 64 runs the integrity cycle: tick 1 a debugger probe and a 5000 ms timer armed, tick 10 the first tamper-check word, tick 20 a scan of top-level window titles and classes against a blacklist, tick 30 the second word, tick 31 `PLI_TAMPERCHECK` sent (→ §2.4, §4.10) | 2.31 only; 2.17.1 and 2.22 have no such timer | [2.31] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md#pli-39-re-send-every-32-s) |
| about 5.1 s | a one-byte id 24 message (→ §2.4); tying it to the 5000 ms timer above is an inference | 2.31; 2.22 only while another player is in the level | [2.31][inf] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md#pli-24-about-every-51-s-1-byte-lab-value-9) |
| 5.0 s | the server's `PLO_NEWWORLDTIME`, seen alongside the client's id 24 | 2.22 against a public server | [cap] (live-runs/2gta-222-2026-10-30/README.md) |

## 4.1.4 Movement updates on the wire

How often a moving client reports itself; the message layouts are in → §2.4.

| Builds | What is sent while a key is held | Source |
| --- | --- | --- |
| 1.1.9 (relay) | a `D` line of type `P` on the level connection every 100 ms: x and y in half-tiles, then frame·4 + direction (→ §2.3) | [cap] (client-internals/live-trace-early.md#119-gserver-with-two-119-clients-relay) |
| 1.21 | one id 2 (player props) message every 100 ms with X, Y and SPRITE | [cap] (client-internals/live-trace-early.md#gserver-121-with-121-gserv007) |
| 1.28 beta 2 | UDP id 0 to each peer every 100 ms: X, Y, SPRITE, STATUS and CARRYSPRITE (→ §2.9) | [cap] (client-internals/live-trace-early.md#gserver-128-with-128-beta-2-gserv013) |
| 1.3 test against GServer13 | one id 2 message every 100 ms with X and SPRITE; speed 0.5 tile per tick | [cap] (client-internals/live-trace-early.md#gserver13-with-13-test-gserv014); [live] (client-internals/live-gserver13.md) |
| 2.22 | the X prop only on whole tiles (every other tick), plus the final half-tile when the player stops; the gani prop switches to the walk gani with the first step and back to idle 100 ms after the last | [cap] (live-runs/2gta-222-2026-10-30/README.md) |
| 2.22 | a script that changes a client flag every tick makes the client send that flag every tick, one message each, uncoalesced | [cap] (live-runs/2gta-222-2026-10-30/README.md) |
| NewWorld beta | the idle gani is re-sent about every 100 ms, because the control NPC sets it each tick; 2.05 sends it only now and then | [cap] (client-internals/newworld-betas.md) |
| 5.24r4, 5.30r3, 6.03r7 | the position (x2/y2) every 50 ms | [wire] (protocol/v5v6-lab-play.md) |
| 2.05 | unmeasured as a rate; a hit sends one props message with CURPOWER, GANI and SPRITE in the hit's tick, then the knockback positions | [cap] (client-internals/live-trace-205.md) |

## 4.1.5 Durations in ticks

The canonical place of each tick count:

- → §4.2.5 blocked steps before the push pose (18) and the push cycle (20)
- → §4.2.6 the ledge jump (8 ticks)
- → §4.2.8 the pull cycle (18 ticks)
- → §4.2.10 swimming and the lava burn (101 ticks)
- → §4.3 sword, spin, hurt and knockback
- → §4.4 the death timer

## 4.1.6 Clocks in the later engines

These are exact-build static and debugger readings of how a later engine advances its clock. None of them is a measured frame cadence (→ App. E#301). [cap] (client-internals/linux-420r6-clock-property.md)

#### Linux 4.20r6: clock updates and the `isgraal3d` predicate

[cap] Six unchanged-startup updater returns in Linux 4.20r6 have a zero branch byte. The initial zero clock is seeded within the observer's wall-clock interval; the next five values each match binary-double previous value plus 0.05. Debugger pauses prevent inferring a 50 ms frame period, 20 Hz rendering, movement timing or sleep latency. [cap] (client-internals/linux-420r6-clock-property.md)


[bin] Registration directly binds global read-only `isgraal3d` to the getter for that predicate byte, whose ELF default is zero. Three direct-reference writer owners are identified; the set-to-one branch follows a `3 ` input prefix. Indirect/alias/module writes remain possible. With the byte zero and the clock nonzero, it adds 0.05 per call; if the clock is zero, or the byte is nonzero, it refreshes from the wall-clock helper. The probe observed one seed and five increments; it does not prove that the clock can never be reset or reseeded. No live nonzero branch, 3D connection or rendering is observed. [cap] Inputs/signatures/executable/mode byte stay unchanged; the untruncated capture retains executable equality and verifies cleanup, with no server. E#301 remains open for frame-driver and walk measurements. [bin][inf] Separate callback adapters provide no complete ABI, module activation or Windows reader result. [bin] (client-internals/linux-420r6-clock-property.md); [cap] (client-internals/linux-420r6-clock-property.md); [inf] (client-internals/linux-420r6-clock-property.md)

#### Windows x64 v7, input 701750: managed and native update

The separately identified Windows x64 recovered inputs show managed Update calling native QuattroUpdate and conditional FixedUpdate forwarding. QuattroUpdate increments a counter, calls a wrapper bound to GetTickCount and stores the return as 32 bits; an inferred void pseudocode type does not override caller dataflow. Guarded QuattroFixedUpdate iterates a registered collection and dispatches onFixedUpdate with an empty argument string. Update3D wraps a one-byte state getter rather than establishing scene simulation. These are selected-range static observations: no measured cadence, wrap/catch-up policy, complete collection/lifecycle/indirect-call semantics, build-614/v6 equivalence, authenticated release provenance or independent original-to-recovered derivation. Exact image identities remain owner-held. E#301’s older-client driver question remains open. [bin] (client-internals/v7-701750-bridge-clock.md)
