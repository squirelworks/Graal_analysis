# v3 — engine surface (Torque)

Date: 2026-11-08 · Tags: **[bin]**

## Torque is the host · **high**

`graalexe 3.0.4` links a full Torque tree: `SimObject`, `NetConnection`, `BitStream`, `TSShape`, console (`Con::`), OpenGL, telnet remote console, master-server queries. Banner string: `Torque Game Engine Demo`. Graal is a set of `graal/*.cpp` types on that host (`TClient`, `TGraalConnection`, `TServerPlayer`, `TServerNPC`, `TBaddy`, `TShowImg`, `TLevelObject`).

This is not the v4 split (Delphi exe + custom Engine, Torque only inside the 3D DLL).

## UDP · **high**

Torque brings up UDP (`UDP initialized on port %d`). Graal prefs can pin or disable it (`fixedport`, `fixedudpport`, `noudp`). If UDP fails, the client tells the user to disable UDP in options. `UDP send error` exists on the Graal side as well.

## Sockets vs Torque packets · **medium**

libc `send`/`recv` show up on the Torque telnet/net path. Graal’s own objects sit above that (connection + GCHAR payload). Exact byte layout of the Torque packet that carries a Graal line was not fully walked.

## Diff vs v4

v4: custom Engine for 2D/net, Torque residual in `Graal3DEngine.dll`. v3: one Torque binary, Graal compiled in.
