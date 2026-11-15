# Windows 4.20r8 engine: class / weapon surface (export names)

Date: 2026-11-16

Static string pass over the Batch-1 unpacked Windows 4.20r8 `GraalEngine.dll` (packet-logger companion tree). No disassembly is published. Tags: **[bin]**. Evidence id: `BATCH1-420R8-ENGINE-20261116`.

This is the clean-room counterpart to the prior REA lead on server → client class delivery (PLO **133** / `PLI_UPDATECLASS`): the engine exposes a class join/leave API by name, so a 4.20r8 client that never receives class bytecode cannot satisfy `this.join("class")`.

## Named exports / symbols observed

Class scripting:

- `addClassScript`
- `getClass`
- `joinClass` / `joinClassSimple`
- `leaveClass`
- `isInClass`
- `setClasses`
- `checkLeaveClasses` / `checkUpdatedClasses` / `classUpdateAction`
- `needEventWithoutClass`

Weapons / login hooks (same module):

- `addGraalPlayerWeapon` / `deleteGraalPlayerWeapon` / `setGraalPlayerWeaponScript` / `invokeWeaponEvent`
- `getGraalLoginInfo` / `graal_setOnServerLogin` / `onServerLogin` / `onPlayerLogin`
- Script words `getclass`, `getweapon`, `weapons`, `weapon`, `weaponfired`
- Package string `.gpake`

## Implication for seihai PARITY

- v4 wants the **193 / 132 / 133** weapon/class path, not the v6 **197 / 140** cache path (already recorded in prior REA leads and seihai notes).
- Closing “Classes… | no” still means implementing **133** on the server for `UPDATECLASS`, not discovering a second client API here.
- Do not send 132/133/193 to v6 profiles; do not send 197/140 to v4 profiles.

## Limits

Export and literal names only. No packet layouts, no RVAs, no decompiled bodies. Packet shapes stay in the protocol notes and in private working papers.
