# Graal 6.x clients: Windows 6.00–6.03, Linux 6.01 and 6.03, Mac OS X 6.11

Date: 2026-10-29

Sources: nine uploads, read statically. Nothing was run. The Linux and Mac builds are unpacked native binaries, so this page is built from them. Tags: **[bin]** read from the client binaries · **[inf]** inferred.

## What the uploads are

| Upload | What it is | Build stamp |
|---|---|---|
| 6.00 beta1, beta2 (Windows) | `GraalSetup.exe` is the game itself, behind an obfuscating packer: every section has the same name (`.PATCH` / `.debug`), the only imports are LoadLibraryA and VirtualAlloc, the entry point is junk-jump code, and a ~430 KB payload sits in the overlay. Authenticode-signed (Thawte, Paris). | Jan 2010 |
| 6.00r2, 6.00r4, 6.03r7 (Windows) | Themida / WinLicense 2.x (blank and random 8-letter section names, one import, Themida entry stub). VERSIONINFO says `Graal.exe` 6.002, 6.004, 6.037, "Linux Cyberjoueurs". | Jun 2011, Jun 2011, Nov 2012 |
| 6.01r1 Linux x64 and x86 | ELF, stripped, not packed | 18 Sep 2011 |
| 6.03r7 Linux x64 | ELF, stripped, not packed | 11 Nov 2012 |
| 6.11r1 Mac OS X | HFS+ disk image, `Graal.app`, Mach-O x86_64, CFBundleVersion 6.111, "©2014 Eurocenter", Developer ID signed. About 1,660 C++ symbols survive (mostly inline and template methods). | 25 Mar 2014 |

Both Windows wrappers need to run to unpack, so the Windows builds are only identified here. 6.01r1 and 6.03r7 Linux are the same releases as Windows 6.01/6.03, so they stand in for them. **[bin][inf]**

## Architecture

- One native C++ program per platform. The 4.x/5.x split into a Delphi launcher and a `GraalEngine.dll` is gone. The class names come from the same `graallib` code base as 5.x (`TGraalVar`, `TGraalConnection`, `TGaniObject`, `TServerPlayer`, `GuiGraalCtrl`, `TSecureVar<T>`, `TEncodedFileKey`), but there is no Torque layer left. **[bin]**
- Linux links SDL_mixer, X11 (Xcursor, XF86VidMode), OpenGL and avahi (LAN service discovery). 6.03 moves zlib from 1.2.3 to 1.2.5 and adds PEM/RSA/DSA key handling and `/dev/urandom` use. 6.11 adds TLS, LibTomCrypt (DES, AES, RC4, RSA) and an RTMP/video path. No bzip2 library strings show, but the type-6 frame compressor keeps the bzip2 call shape (block size 5). **[bin]**
- Many short strings (hosts, ports, tokens, URL parts) are stored scrambled and only decoded at run time, so a plain `strings` search does not find them. A per-byte decoder that depends on the string length and the position does the decoding; it is the same in 6.01, 6.03 and 6.11. **[bin]**

## Login server

- **No `license.graal` any more.** The 3.x–5.x RSA-signed license file is not read. The login hosts are compiled in, scrambled. **[bin]**
- 6.01r1: `loginserver.graalonline.com`, `loginserver2.graalonline.com`, `loginserver3.graalonline.com`, port **14900**, as four scrambled strings. **[bin]**
- 6.03r7: the same three hosts, each stored as `host:14900`, in a list the client walks on failure. A host without a port gets 14900. **[bin]**
- As in 5.x, the client opens a normal game connection to a server named **`Login`**. The server list and account screens then come from that server (S→C 190 raises `onServerListerConnect`). **[bin]**
- 6.11 replaces this with an HTTP "connector", see below. **[bin]**

## Login message (6.01 and 6.03)

Id **5**, sent in the mode-3 login frame (zlib, no cipher, no type byte), with the key byte first as before:

1. key byte (random & 0x7F)
2. version token, 8 characters
3. `GCHAR len` + account
4. `GCHAR len` + password (0xFF + the first 0xDF bytes when the length is 0xE0 or more)
5. a comma list: `linux`, then four machine ids

Then id **37** (language), as in 3.x–5.x. **[bin]**

| Build | Token | How it is stored |
|---|---|---|
| 5.00r7 (for comparison) | `G3D22067` | eight one-character globals |
| 6.01r1 Linux | **`G3D0108A`** | `G` plus seven one-character strings, concatenated |
| 6.03r7 Linux | **`G3D0511C`** | one scrambled string `g3d0511c`, decoded and upper-cased |
| 6.11 Mac | set by the server's connector script | — |

The Linux machine ids replace 5.x's Windows ones (DigitalProductId, MAC, C:\ serial): MD5 hex of the `eth0` MAC address, MD5 hex of the inode number of `/etc`, an empty field, and the kernel release + version string. **[bin]**

Guest logins send account `guest` with a password decrypted at run time from 8 compiled-in bytes (DES-style call). **[bin][inf]**

## Cipher and framing (classic mode)

- **Gen 5, unchanged.** Both directions are seeded `0x04A80B38`, the LCG is `it = it*0x08088405 + key`, key = rand & 0x7F. Frame type by size: 2 raw (short), 4 zlib, 6 bzip2. XOR at most 12 dwords for type 2 and 4 dwords for types 4/6. Login frame mode 3, then mode 0. **[bin]**
- New since 5.x: a frame of 0xFFFF bytes or more is sent as length `0xFFFF` followed by a 4-byte big-endian length. Buffers flush at 0x1000. **[bin]**
- Packets are still `id+32`, body, `\n`; an outgoing packet that contains a newline is refused with "Illegal characters in the outgoing data". **[bin]**

## Server → client ids (6.01, 6.03)

From the game connection's receive dispatcher.

- **6.03r7 (92 ids):** 0–25, 27–40, 42, 43, 45–49, 67, 68, 69, 74, 82, 84, 101, 102, 104–107, 109, 111, 131, 134, 140, 150, 151, 153–156, 166, 168, 170, 172–174, 176, 178–180, 182, 183, 185–187, 189, 190, 191, 194, 195, 197, 198. **[bin]**
- **6.01r1 (91 ids):** the same without 111. **[bin]**
- Against 5.00r7: drops 41, 75, 132, 133, 165, 169, 171, 175, 181, 184, 193; adds 109, 111 and 198. **[bin]**
  - 109: a GINT5 time plus two strings, handed to the file layer (probably a file redirect; the 6.11 native handler list has `setfileredirect(u,s,s)`). **[inf]**
  - 111: writes `creationtime.dat`. **[bin]**
  - 198: a GINT5 value stored on the connection. **[bin]**

Client → server: only 5 (login) and 37 (language) are confirmed as constant ids; the rest go through a virtual send call and were not tabulated.

## 6.11 Mac: the connector and a server-defined protocol

This is the big change in 6.x. In 6.11 the client no longer has a fixed protocol.

### Connector request

- On login the client sets the server name to `Login` and requests, in order, `https://con.quattroplay.com/con.png`, `https://con.quattroplay.com/con.gs`, `http://con.quattroplay.com/conf.gs`. Each step is retried up to twice, and retries use the host `con2` instead of `con`. After three failures it shows a warning. All URL parts are scrambled strings. **[bin]**
- The query is `?p=` + a comma-joined list `g=<client id>,p=mac,v=<version>,b=<build date and time>`, encrypted with DES-ECB under a compiled-in 8-character key (whole 8-byte blocks only), base64-encoded with the client's own alphabet, then URL-encoded. **[bin]**
- The HTTPS connection checks the server against a certificate bundle compiled into the client (base64, itself DES-encrypted with a second key). The request sends `User-Agent: Graal/<version>`. **[bin]**

### Connector reply

The reply is loaded as a script object, `StartScript_Connector`, and its `onCreated` runs. Before that the client sets `scriptip`, `scriptsslcipher`, `scriptsslsubject` and `scriptsslissuer` on it, so the script can check where it came from. If no connector script loads, a built-in `StartScript_Fail` is used. **[bin]**

### What the script controls

The connection object gives the script these methods: `connecttogameserver`, `setprotocol`, `sendraw`, `senddata(id, data)`, `flush`, `setsslparameters`, `getsslcipher`/`subject`/`issuer`, `setencryptionparsekey`, `setencryptionout(type, key, iv)`, `getpassword`, `setloginaccount`, `requestbasefiles`, `setoutdatahandlers`, `clearindatahandlers`, `setindatahandlers`, `defaultinhandler(id, data)`, plus `tclient_setencryptionin(type, key, iv)`. **[bin]**

- **Framing.** `setprotocol(template)` switches from classic gen-5 framing to a header the template describes. The header is as long as the template. Each letter marks a field and repeating it sets the width (max 4 bytes, big-endian): `I` packet counter (starts at 1), `L` length, `T` packet id, `E` another field. **[bin]**
- **Encryption.** In that mode the stream can be wrapped in **RC4** or **AES-CBC** (blocks padded with 0xFF), set separately for each direction (`setencryptionout`, `tclient_setencryptionin`). Other names turn it off. TLS is also possible (`setsslparameters`). **[bin]**
- **Client → server ids.** `setoutdatahandlers` loads a 256-entry table: internal message number → wire id. A value of 0xFE sends the message to a script event instead of the wire. **[bin]**
- **Server → client ids.** `setindatahandlers` takes (wire id, handler) pairs. A handler below 0x5F is one of 95 native handlers. 0xFE sends the packet to the script, 0xFF ignores it, and 0xFC/0xFD set two special ids. The native handlers are also exposed to script by name (about 90 `tclient_*` functions, from `tclient_setplayerprops` and `tclient_setlevelboard` to `tclient_setghostsnear` and `tclient_setpackageend`). **[bin]**
- **Login.** The script builds and sends the login itself (`getpassword`, `senddata`). So the token, packet ids, header layout and cipher for 6.11 live in the server's script, not in the client. **[bin][inf]**

The gen-5 code path is still in 6.11 and is the default before a script calls `setprotocol`. **[bin]**

None of this exists in 6.01 or 6.03 (no connector, no RC4/AES, no script-set id tables). **[bin]**

## File formats

All three builds carry the 5.x set: `GR-V1.03`–`GR-V1.05` levels, `GWEBL001` web-level cache, `GRMAP001` gmaps, `GRPKG001` update packages and `GRESCR01` script cache. No new magic was found. The text-level keywords are not in plain strings in 6.x (probably scrambled like the hosts). **[bin]**

## Still open

- ~~Unpacking the Windows builds~~ Done 2026-10-29, see `v5v6-windows-unpacked.md`.
- The full client → server id table for 6.01/6.03.
- The payload layouts of the new ids 109, 111 and 198.
- A live 6.11 connector script, to recover the real 6.11 token, header and id tables.
