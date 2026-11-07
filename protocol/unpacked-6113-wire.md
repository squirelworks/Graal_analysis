# Unpacked Windows 6.1.1.3 on the wire

Date: 2026-11-07. Static read of the listing in `client-internals/unpacked-6113.md`. Nothing was run. Tags: **[bin]** this image · **[bin]** the neighbour notes cited below · **[cap]** the port 14900 capture.

The packed stub had no login builder (`protocol/v6113-wire.md`). This page is what the unpacked image actually contains.

## Generation-5 cipher

The generation-5 LCG is compiled in. A field is set to the seed `0x04A80B38`, and the step is that state times `0x08088405`, plus 1. That is the same pair the 6.00 through 6.03 notes call the shared cipher. This read did not recover the frame-type bytes (raw, zlib, bzip2) as a switch. **[bin]** (`protocol/v5v6-windows-unpacked.md#cipher-and-framing`)

Outgoing data that contains a newline is still refused with "Illegal characters in the outgoing data". The socket layer reports "winsocket startup failed" and "socket call failed". `TSocket` is present. An HTTP header `Connection: Keep-Alive` is present. `resolveHost` is not. **[bin]** (`client-internals/engine-600r4.md#what-changed-in-two-weeks`)

## No compiled-in token

There is no `G3D` string and no `GNP` string. The clear hello `GNP1905C` from the port 14900 capture is not a string in this image, so the capture's token is not a compiled-in literal here. Do not stamp this build with `G3D26090` or with either 6.03 token. **[bin][cap]** (`protocol/v6113-list-capture.md#the-clear-hello`)

## Script send slots

Each outgoing sender loads its own slot and compares it with `0xFE`. On a match it calls a script event instead of the wire. Otherwise it sends that slot's id. That is the 6.11 rule. The Mac note's slot numbers are not copied onto this image: the names are not stored in that order. **[bin]** (`protocol/v6x-clients.md#the-611-named-send-slots`)

The event names present are the Mac 6.11 set except `onSendNPCProperties`, which is not in this image. The other 55 names are here, including `onSendAddHorse`, `onSendDelHorse`, `onSendAddBomb`, `onSendDelBomb`, `onSendTriggerAction`, `onSendRemoveExtra`, `onSendShot`, `onSendLevelWarpModtime` and `onSendProjectile`. **[bin]**

## Connector names

Present as script objects and fields: `StartScript_Connector`, `StartScript_Fail`, `scriptsslcipher`, `scriptsslissuer`, `scriptsslsubject`, the server name `Login`, and `onConnectingToServer`. **[bin]**

Not present as plaintext: `setprotocol`, `setencryptionout`, `setindatahandlers`, `setoutdatahandlers`, `connecttogameserver`, `tclient_setplayerprops`, `con.png`, `con.gs`, `conf.gs`. The Mac method list is not a string table in this Windows image. CyaSSL cipher-suite names (RC4 with MD5, RC4 with SHA, AES-CBC, AES-GCM) are the TLS library. They are not, by themselves, a game-socket RC4 or AES setter. **[bin]** (`protocol/v6x-clients.md#what-the-script-controls`)

## Files the image names

| Name | In this image |
| --- | --- |
| `basepackage.gupd` | Used as a file name, including a comparison against a name being opened |
| `creationtime.dat` | Joined onto a directory path. No packet id was recovered for the write |
| `GR-V1.03`, `GR-V1.04`, `GR-V1.05` | Present |
| `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GLEVNW01` | Absent |
| `GWEBL001`, `GRMAP001`, `GRPKG001` | Present |
| `GRESCR01`, `.code` | Present. The reader is `protocol/gs2-unpacked-6113.md` |

**[bin]** (`protocol/v6x-clients.md#file-formats`, `protocol/v5v6-windows-unpacked.md#file-formats-and-bundled-files`)

`creationtime.dat` is the 6.03 name that unpacked 6.00r2 does not carry. The level magics match Windows 6.03r7's reduced set, not unpacked 6.00's `GR-V1.00` through `GR-V1.05`. **[bin]**
