# Entering a 3D server and the UDP ports (4.04r2, 5.12)

Static read of the 4.04r2 client (GraalEngine.dll and Graal4.exe) and the 5.12
client (Graal3DEngine.dll). Behaviour only. Board rows: T3D-028 and T3D-059.

## Where the logic lives

| Build | Server-list hand-over code | Options and UDP code |
|---|---|---|
| 4.04r2 | GraalEngine.dll (the 2D engine); Graal4.exe starts the 3D plug-in ("Starting Graal3D...", "You need to download Graal3D at") | GraalEngine.dll and Graal4.exe |
| 5.12 | Graal3DEngine.dll (one engine) | Graal3DEngine.dll |

The 4.04r2 Graal3DEngine.dll has no "3 " literal and no UDP options. It gets the
host and ports through the host callbacks (`graal_setConnectTo3DServer`,
`graal_setStartGraal3D`). The rule below is the same in both builds.

## Picking a server from the list (T3D-059)

When the player picks a list entry, the client gets three values: the listed
name, the host and the port (as text).

1. Name. If the second character of the name is a space, the first two
   characters are dropped from the stored name. Any one-character prefix is
   dropped this way, not only "3 ".
2. 3D test. The entry is a 3D server when the listed name, before stripping,
   starts with exactly `3 ` (digit three, then a space).
3. 3D entry while the client is in 2D mode. The client calls the host's
   StartGraal3D callback with the host and the port and stops there. The host
   switches to 3D mode and the pick is replayed. If the host refuses, the
   client falls through to the steps below.
4. 3D entry while the client is in 3D mode. The client marks itself as 3D,
   sets the minimum frame time to 1 tick, and calls the host's
   ConnectTo3DServer callback with three values:
   - the host,
   - the **listed port + 1**,
   - the local UDP port (see below).
5. Any other entry. The client marks itself as 2D, sets the minimum frame
   time back to the 2D value (4 × setting + 6; the shipped setting is 11, so
   50), and logs in over TCP to the listed host and port.

So a 3D server must list its TCP port in the server list and serve the 3D UDP
traffic on that port + 1. The "Offline" entry name is handled separately and
never connects.

Open:

- what happens when the 3D plug-in is missing on 4.04r2 (Graal4.exe has the
  download message). This needs a lab with the DLL removed.
- 4.20r8 and 5.00r7: same rule expected, not read yet.

## UDP ports (T3D-028)

- The 3D server's UDP port is always the listed port + 1. Nothing the server
  sends changes it, and no option overrides it.
- What the player can set is the client's own UDP port. There are three
  options, in the options file and as console prefs:

| Option | Console pref | Effect |
|---|---|---|
| `fixedport` | `$pref::Graal::fixedport` | off by default; when on, the client binds its UDP socket to `fixedudpport` |
| `fixedudpport` | `$pref::Graal::fixedudpport` | default 14899 |
| `noudp` | `$pref::Graal::noudp` | turns UDP off |

- With `fixedport` off, the client binds port 0, so the OS picks the port.
- Changing `fixedport`, `fixedudpport` or `noudp` while connected makes the
  client close and reopen its UDP socket.
- If UDP fails, the client shows "It seems that the UDP protocol is not
  working, it might be better to disable UDP in the options".

## What this means for our server

- seihai-gserver-v2 graal3d mode must answer on listed port + 1 for UDP.
- The client's source port is random unless the player sets `fixedport`. The
  server should reply to the packet's source address, not to 14899.
- A server-list entry needs the `3 ` prefix to start the 3D hand-over. The
  prefix is not shown in the stored name.
