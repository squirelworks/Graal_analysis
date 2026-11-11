<!-- manual: kind=reference status=draft -->
# 8 NPC scripting

> Status: draft. Each chapter carries its own status line.

## 8.0 Reading this Part

Graal has had two script languages, and they reach the client in different forms. GS1, the language of the 1.x and 2.x clients, arrives as source text in an NPC's script prop, and the client parses it itself. [2.05] (npc-library/gs1-reference-205.md#execution-model-205) GS2, the language of the 4.x and later clients, is compiled before it reaches the client and arrives as bytecode or a cached `.code` file. [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) The boundary is not a clean cut. 3.x still runs GS1 natively, 3.153 already handles the NPC bytecode ids, and 4.04 rev 2 still runs GS1 weapon scripts. [bin] (version-profiles/matrix/README.md#thinks-wire-and-scripting); [live] (client-internals/live-behaviour-404.md)

**GS1 is a client-side interpreter.** 2.05 does not compile GS1 to bytecode. It parses each script once, when the level loads, into a flat list of statement nodes, and every event runs that list from the top with the event's flag set. [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) There is no separate server VM for classic NPCs. A script that needs the server goes through flags, `triggeraction` and the few commands with online side effects, and a server announces an NPC server with PLO 44 to unlock the visual commands. [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client); [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) From 2.3 the classic client-side mode is gone and Classic moves to the NPC server. [doc] (client-internals/feature-timeline.md)

**GS1 is the best-read part of the Part.** §8.1 gives the language as 2.05 rev 2 runs it, and §8.2 gives every command, function and constant with its argument signature and the changes from build to build. [2.05] (npc-library/gs1-reference-205.md#execution-model-205) Some exact-build readings correct what the documentation implies. Constant numeric comparisons fold to zero in 2.05 rev 2, so `if (1==1)` is false while the same comparison on variables works. Message codes and event parameters follow byte-level rules that the 2000 documentation never states. [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#constant-comparison-folding); [bin] (npc-library/gs1-message-codes-205r2.md#processing-contract) The 3,172 scraped level scripts and the archived catalogue give the frequencies that show which commands and events matter in practice. [file] (npc-library/README.md)

**GS2 is known from its machine, not its source.** The 4.2.0.8, 5.0.0.7 and unpacked 6.00 engines parse one big-endian four-segment container and run it on one stack machine. That machine finds functions by name, treats events as functions, and keeps its own clock (§8.3.3, §8.4.2). [bin] (client-internals/gs2-vm-from-engines.md#which-binaries-contain-the-machine) GS2's syntax, its standard library and its full event model are still open, and so is which message id carries the compiled code (→ App. E#207, App. E#202). [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) A public third-party compiler and VM exist, but they are a lead for a clean-room machine, not a reading of the clients. [doc] (npc-library/preagonal-gs2.md#what-this-does-not-settle)

**Exact-build readings stay with their build.** Many sections below record one build's behaviour on one input: the 2.05 rev 2 readings in §8.1, the Linux 4.04r2, 4.20r6, 6.01 and 6.03 readings in §8.3.4 and §8.4.4 to §8.4.8, and the installed Windows 5.00 queue. Each states its own limit. A result there is not an all-version rule, and the 4.04r2 clock is not the 5.0 clock. [cap] (client-internals/linux-404r2-events.md#experiment-boundary); [bin] (client-internals/windows-500-event-queue.md)

## Chapters

- → §8.1 GS1 language (`01-gs1-language.md`)
- → §8.2 GS1 reference by version (`02-gs1-reference.md`)
- → §8.3 GS2 language (`03-gs2-language.md`)
- → §8.4 GS2 bytecode (`04-gs2-bytecode.md`)
