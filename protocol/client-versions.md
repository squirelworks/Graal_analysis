# Client versions side by side: 2.05, 2.17, 2.22, 2.31

Date: 2026-10-21

Sources: the four client executables in the Graal Reborn 2.2.2.0 folder (`Graal.exe` = 2.05 rev 2, `Graal_2171.exe`, `Graal_222.exe`, `Graal_231.exe`), read statically. Server-side names are from gs2lib. Tags: **[bin]** read from the client binaries · **[srv]** server source only · **[doc]** `newfeatures*.txt` · **[inf]** inferred.

All four clients are Delphi builds with the same network classes: one base socket class, a game-server subclass, and a listserver subclass. They also share the same cipher LCG, `it = it * 0x08088405 + key` with seed `0x04A80B38`. It uses the Borland `Random` multiplier, but adds the key where Borland adds 1. **[bin]**

## Game-server login

| | 2.05 rev 2 | 2.17 (2.1.7.1) | 2.22 | 2.31 |
|---|---|---|---|---|
| Login type (first GCHAR) | 0 | 0 | **5** | **5** |
| Key | GCHAR `rand & 0x7F` | same | same | same |
| Token | `GNW03081` | `GNW22122` | `GNW03014` | `GNW28015` |
| Then | `str account`, `str password` | same | same | same |
| Identity string after password | no | no | no | no |
| Cipher (client → server) | gen 3 insertion | **gen 3 insertion** | gen 5 partial XOR | gen 5 partial XOR |
| Frame (client → server) | `u16be len` + zlib | same | `u16be len` + compression byte + body | same |
| Sent right after login | `PLI_LANGUAGE` (37) | 37, then `PLI_TAMPERCHECK` (39) | 37, 39 | 37, 39 |

**[bin]**

- The token is assembled one character at a time in every build, so none of them has it as a string literal. **[bin]**
- **2.17 still uses the 2.05 cipher.** Its game-server send path is the same gen-3 code: a junk byte at `(it & 0xFFFF) mod len` from the second message on, then zlib over the buffer. The out-buffer limits are the same (flush at 0x1000, drop at 0x40000 queued). The gs2lib numbering puts type 4 (gen 4) at 2.19–2.21, which fits 2.17 still being type 0. **[bin][srv]**
- 2.22 and 2.31 send the login message in a fixed "zlib, no cipher, no compression byte" mode, flush it, and only then switch the socket to the dynamic gen-5 mode. So the login frame has no compression byte, and every later frame has one. **[bin]**
- The 2.22+ login line ends at the password. The guess in `login-and-walk.md` that 2.22+ appends an identity string does not hold for 2.22 or 2.31. **[bin]**
- `PLI_TAMPERCHECK` (39) carries **10 raw bytes**, not two GINT5 words: the bytes include values below 0x20, which a GINT5 byte can never be, and none is 0x0a, so the payload survives line framing unescaped. The 10 bytes are a constant per client build, identical across accounts and login keys (2.17 `2a7bad195e231243d82c`, 2.22 `250e4d0f962b03ede631`, 2.31 `291655b7602e87c9eb82`; see `version-profiles/tampercheck-values.tsv`). It is new in 2.17 and absent from 2.05. What the bytes are computed from is not traced. **[bin][cap]**
- From 2.17 on, the account name is kept obfuscated in memory and decoded only to build the login line. 2.31 does the same for the password. The obfuscation is the same byte map used for hidden strings, `dec(b) = (~b − 10) & 0xFF`. **[bin]** The 2.18 note "new password encryption" refers to the saved-password store, not to this. **[doc][inf]**

## Gen-5 send on the client (2.22, 2.31, RemoteControl) **[bin]**

The server-side description in `codec-and-framing.md` is the receive half. On the client, each flush of the out buffer (`n` bytes) picks its own compression:

| Buffer size | Type byte | Body |
|---|---:|---|
| `n < 0x30` | 2, or 4 if zlib is actually shorter | raw (or zlib) |
| `0x30 ≤ n < 0x1000` | 4 | zlib |
| `n ≥ 0x1000` | 6 | bz2 |

Then:

1. Partial XOR over the (compressed) body: `min(ceil(n/4), 12)` dwords for type 2 and `min(ceil(n/4), 4)` dwords for types 4 and 6, that is one LCG step per 4-byte group present, up to 12 groups uncompressed or 4 groups compressed. Each dword advances the LCG once and XORs with it, little-endian. A short last group still steps the LCG and XORs byte by byte with the iterator's low bytes. *(An earlier version of this note had `floor(n/4)` for types 4 and 6; that was wrong, see `codec-and-framing.md` for the evidence and which side it covers. The client's own send helper has not been re-read for this correction, and no real-client send of a short compressed frame has been captured.)*
2. The frame is `u16be (len + 1)`, then the type byte, then the body.

The receive side mirrors this with its own iterator. Both iterators start at `0x04A80B38` and use the same key. Type codes 1/2 mean raw, 3/4 zlib, and 5/6 bz2, and only the even codes are XORed. The odd code 3 is the fixed "zlib, no cipher" mode used for the login frame and for the whole NC session (see `tools/remotecontrol.md`). The client drops the connection once more than 0x40000 bytes are queued (RemoteControl: 0x800000).

## Server → client ids handled

Read from each client's main receive switch. ✔ = has a case. **[bin]**

| Ids | 2.05 | 2.17 | 2.22 | 2.31 | Notes |
|---|:-:|:-:|:-:|:-:|---|
| 0–25, 27–43, 45–48 | ✔ | ✔ | ✔ | ✔ | the 2.05 core set |
| 26 `NPCACTION` | · | · | · | · | never handled |
| 44 `HASNPCSERVER` | ✔ | ✔ | ✔ | **·** | dropped in 2.31 ("Classic switched to NPC-Server", v2.3) **[doc]** |
| 49 `PLAYERWARP2` | · | ✔ | ✔ | ✔ | gmap warp |
| 68 / 69 `LARGEFILESTART` / `END` | · | ✔ | ✔ | ✔ | "files bigger than 64k can be downloaded" (v2.14) **[doc]** |
| 75 `PROFILE` | ✔ | ✔ | ✔ | ✔ | |
| 84 `LARGEFILESIZE` | · | · | · | ✔ | `downloadsize` "correctly giving the size" (v2.3) **[doc]** |
| 100 `RAWDATA` | ✔ | ✔ | ✔ | ✔ | 101/102 arrive behind it |
| 150, 151, 153–156, 165, 166, 168 | ✔ | ✔ | ✔ | ✔ | |
| 169 `UPGRADEURL` … 185 `BOARDHEIGHTS` | · | ✔ | ✔ | ✔ | ghost mode (170, 173, 174), bigmap/minimap from the gserver (171, 172), Kingdoms and New World modes (176, 177), `serverwarp` (178), RPG window (179), status list (180), process list and screenshot (182–184), level heights (185) |
| 186 `BOARDMODIFY2` | · | · | ✔ | ✔ | |
| 189 `MOVE2` | · | · | · | ✔ | "full precision" positions and NPC moves (v2.3) **[doc]** |

Counts: 2.05 handles 59 ids, 2.17 handles 79, 2.22 handles 80, and 2.31 handles 81. All of them ignore unknown ids without error. The names come from gs2lib. That a client has a case for an id shows it handles it. Its payload is not traced here. **[bin][srv]**

## Listserver login

| | 2.05 | 2.17 | 2.22 | 2.31 |
|---|---|---|---|---|
| Host and port | built in, DES-hidden `www.graalonline.com`, `14921` | `arrays2.dat` | `arrays2.dat` | `arrays2.dat` |
| First message | id 0 `newmain` | id 0 `newmain` | id 7, key, `GNW30123newmain` | id 7, key, `GNW30123newmain` |
| Then | nothing: 2.05 sends only id 0 and waits for the list | id 1 `str account, str password` | id 1, now gen 5 | id 1, now gen 5 |
| Frame | `u16be` + zlib, no cipher | same | gen 5 after the first message | gen 5 after the first message |

**[bin]**

- **`GNW30123` is the 2.22/2.31 listserver token.** It travels inside listserver id 7 (`V2ENCRYPTKEYCL`), straight after the key, and is immediately followed by the list name `newmain`. So it is a listserver protocol token, not a game build, which is why no game-version table has it. **[bin][srv]**
- From 2.17 the listserver address comes from `arrays2.dat`, a CRLF text file checked against the 128-byte signature in `arrays2.sig`. The verification key is a long hex string hidden in the exe with the same `~b − 10` map. The signature algorithm is not verified here (RSA-1024 is a plausible reading of the key and signature sizes) **[inf]**. Lines: 0 = primary host, 1 = port, 2 = site domain, 3 = account-registration URL, 4 = translation URL, 5 and 6 = fallback hosts. The client tries up to three hosts in turn. **[bin]** The Graal Reborn copy reads `listserver.graal.in`, port `14922`, with fallbacks `listserver.graal.cc` and `listserver.graalonline.biz`. `graal.sig` is checked the same way against the executable itself, which is the "Graal.exe corrupted" check in `readme.txt`. **[bin][doc]**
- 2.05 has no `arrays2.dat` or `.sig` handling at all. **[bin]**

## Open

- Client → server id sets per version. The send helpers are virtual calls with the id in a register, so a full table needs per-version helper identification. 2.05's set is in `packet-ids.md`.
- What the two `PLI_TAMPERCHECK` words are.
- 2.19–2.21 (type 4, gen 4) are not in this folder, so the gen-4 client side is unverified.
