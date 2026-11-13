# Mac OS X 6.11r1: the named send slots

Date: 2026-11-14. Static read of the Mac OS X 6.11r1 client executable (Mach-O, x86_64; the same input as [mac-611r1-gs2-runner.md](mac-611r1-gs2-runner.md)). Nothing was run. Tags: **[bin]** read from the executable · **[inf]** inferred.

[`protocol/v6x-clients.md`](../protocol/v6x-clients.md#the-611-named-send-slots) describes the Windows 6.11 mechanism. Each outgoing message has a slot in a script-loaded table, and a slot holding 0xFE makes the client call an `onSend…` script event instead of sending. The Mac build uses the same mechanism and the same slot numbers.

## The table and the test

**[bin]** Each sender begins the same way, hand-decoded for slots 44 and 45:

1. It loads a 32-bit entry from one global table. Entries are 4 bytes apart, and both senders address the same table base.
2. `test` / `js`: a **negative entry returns** without sending or calling an event.
3. `cmp eax, 0xFE`: an entry of **254 takes the event path**. The sender builds the event name, picks the supplied payload if there is one or a shared fallback otherwise, and hands both to a common helper.
4. Any other non-negative value takes the remaining path, which was not followed here.

**[bin]** All 56 `onSend…` names from the Windows table are present in the Mac binary, and each has a code reference. For 52 of them, the table entry loaded just before the 254 test is exactly the slot number in the published Windows table. Examples:
- `onSendWantWeaponScript`: slot 0
- `onSendToAllChat`: slot 3
- `onSendTriggerAction`: slot 11
- `onSendPlayerProperties`: slot 44
- `onSendNPCProperties`: slot 45
- `onSendWindowList`: slot 56

So the slot numbering is shared between the Windows and Mac 6.11 builds. **[inf]**

**[bin]** For four names my pattern scan did not give a clean result:
- `onSendShot`, `onSendProjectile` and `onSendPrivateMessage`: no slot load matched the pattern before the test.
- `onSendImageUpdate`: the scan picked up an unrelated earlier load.

These four are unconfirmed, not contradicted.

## Notes

- Unlike the unpacked Windows 6.1.1.3 image described in `../manual/01-builds.md`, where `onSendNPCProperties` is absent, this Mac build **does** contain `onSendNPCProperties` and uses it for slot 45. **[bin]**
- The table holds 32-bit entries, one per slot. Whether the script side fills it as a 256-entry table, as described for Windows, was not checked on Mac. **[bin]** **[inf]**
- Load commands for this build: minimum macOS 10.7.0. It links OpenGL, OpenAL, AudioToolbox, AudioUnit, AppKit, Foundation, CoreFoundation, IOKit, CoreServices, ApplicationServices, `libstdc++.6` and `libobjc`. **[bin]**

## How this was checked

Static read with a small Mach-O reader. For every `onSend…` string in `__cstring` it finds each RIP-relative reference, the nearest preceding `cmp eax, 0xFE` and the 32-bit table load before that. The player-property and NPC-property senders were also decoded by hand from their first bytes. No decompiler was used and nothing was run.

## Still open

- Follow the non-254 path (the ordinary send) for one slot, to confirm it reaches the packet writer with the original payload.
- Resolve the four unconfirmed slots with a real disassembler.
- Confirm where the table is filled from script on Mac.
