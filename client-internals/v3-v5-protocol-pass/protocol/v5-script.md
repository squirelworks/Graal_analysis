# v5 — script

Date: 2026-11-08 · Tags: **[bin]**

## Kind · **high**

Late 5 (5.303 and 5.314) is still a **GS1 verb** client. The token `GS2` is absent. `GRESCR01` and `.code` **are** present, next to a base64-style alphabet, so an encrypted `.code` container exists. That is not an opcode VM in this image.

5.0.0.7 `GraalEngine.dll` also has `GRESCR01`, `SCRIPTEND`, `showimg`, and, unlike late 5, the literal `setplayerprop` / `playerhp`.

## Level section tags · **high**

Present in both late-5 exes and in the 5.0.0.7 engine: `BOARD`, `NPC`, `SIGN` / `SIGNEND`, `CHEST`, `LINK`, `BADDY`, `GSERVL01`, `GRMAP001`, `GWEBL001`, plus `LEVELNAMES`, `HEIGHT`, `WIDTH`, `GENERATED`.

Gani-side tags in late 5 include `SCRIPTEND`, `PLAYSOUND`, `WAIT`, `ANIEND`, `ACTOR` / `ACTOREND`, `FRAME`.

## Builtins (late 5, sample) · **high** (names)

A contiguous verb run in 5.314 includes:

| Group | Names |
|---|---|
| Combat / items | `setsword`, `setshield`, `sethead`, `setgender`, `hidesword`, `explodebomb`, `hitplayer`, `hitnpc`, `spyfire` |
| Speech | `say`, `say2`, `sendtext`, `sendrpgmessage`, `sendtorc`, `requesttext` |
| Images | `showimg`, `showimg2` (elsewhere in the image), `setani`, `replaceani` |
| World | `updateboard`, `updateterrain`, `loadmap`, `loadclass`, `putleaps`, `addtiledef`, `addtiledef2` |
| Player | `takeplayerhorse`, `takeplayercarry`, `attachplayertoobj`, `detachplayer`, `freezeplayer`, `setplayerdir` |
| Files | `requestfilesmove`, `requestfilerename`, `requestfiledeletion` |
| Client | `graalversion`, `getPlatform`, `isopengl`, `switchToOpenGL`, `switchToDirectX`, `isDemoVersion`, `isPremiumVersion`, `isOfflineMode` |

Format-letter neighbors (`ssdd`, `iddd`, `siii`) sit between verbs. Full arity per verb was not decoded.

`showimg` help text in 5.314 still describes the old layer bias: removed objects, weapon showimgs (`+ 0x10`), daynight (`+ 0x20`).

## Events · **high**

`onPlayerLogin`, `onPlayerLogout`, `onRemotePlayerChats`, `onPlayerChanges`, `playerchats`. No `StartScript_Connector`. GUI starters are the ones already listed in the identity note (`StartScript_Profiles`, `StartScript_GraalGui`, dialogs).

## 5.0.0.7 · **medium**

Engine strings match the v4 GS1 set more than the late-5 verb run (`setplayerprop`, `playerhp`). This pass did not re-list every 5.0.0.7 builtin.
