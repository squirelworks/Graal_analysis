# Login and walk frames

Date: 2026-10-14, revised 2026-10-21

Tags: **[2.05]** confirmed in 2.05 rev 2 · **[srv]** GServer-v2/gs2lib only · **[cap]** captures · **[inf]** inferred.

## Login line (first message, sent clean)

```
GCHAR client_type      ; 0 = PLTYPE_CLIENT           [2.05][srv]
GCHAR key              ; rand & 0x7F, gen-3 key       [2.05]
char[8] token          ; "GNW03081" for 2.05          [2.05]
GSTRING account                                       [2.05]
GSTRING password                                      [2.05]
"\n"
```

- The old "random prefix `(rand & 0x7F) + 0x20`" is the encryption key, not padding. **[2.05]**
- Each login byte is a GCHAR, so the line opens with `0x20` (type 0) and the key follows. **[2.05]**
- The token is built one character at a time in code, so there is no string literal to search for. **[2.05]**
- Right after the login line the client sends `PLI_LANGUAGE` (37, wire `0x45`) with the language string (`English` observed). **[2.05][cap]**

### How the server parses it **[srv]**

1. Read the type GCHAR. `type = 1 << value`. 0 → client, 1 → RC, 2 → NPC-server, 3 → NC, 4 → client 2.19–2.21, 5 → client 2.22+, 6 → RC2, 8 → web.
2. For type 0, read 8 bytes as a token. 2.05 puts the key first, so these bytes are not a known token. The server rewinds one byte, switches to gen 3, reads the key, then reads the real 8-byte token.
3. Read the account and password GSTRINGs. The login line ends there for 2.05, and also for 2.22 and 2.31 (a static read of those clients' login routines finds no identity string after the password). The server's optional identity-string read is for later clients. **[2.05][bin]**
4. `GNW03081` maps to `CLVER_2_052` in current gs2lib. That enum sits **below** `CLVER_2_1`, so the server takes every pre-2.1 code path for 2.05. These include no file modtimes, `PLPROP_GANI` sent as the bow slot, the `sendLevel141` level sequence, and `gr.x`/`gr.y` movement forwarding.

Other login tokens from gs2lib: NC `NCL11012`/`NCL21075`, RC `GSERV023`–`GSERV025`, NPC-server `GRNS0000`/`LNX00001`. **[srv]**

## "Walk" frames are PLI_PLAYERPROPS

The short client frames headed `"` are message id 2 (`0x22 = 2 + 0x20`), **PLI_PLAYERPROPS**. They are not a dedicated walk packet. **[srv][2.05]** The body is a property stream of `GCHAR(prop id)` + value, using the `PLPROP_*` table in `player-props.md`.

Decoding the 2026-10-04 examples **[cap][inf]**:

| Frame | Props |
|-------|-------|
| `"1-` | `0x31-0x20 = 17` SPRITE = 13 |
| `"/[` | 15 X = 59 → 29.5 tiles |
| `"0f` | 16 Y = 70 → 35.0 tiles |
| `"0[14` | Y = 59 → 29.5, then SPRITE = 20 |
| `"*$walk/I…` | 10 GANI = `walk` (length 4), then X = 41 → 20.5 |

- X and Y are GCHAR of `tiles * 2` (half-tile steps). SPRITE is the classic sprite index. `sprite % 4` is the direction **[srv]**.
- Direction numbering: **0 up, 1 left, 2 down, 3 right** (2.22 `commands.rtf`; GServer agrees). The "0 south / 1 west / 2 east / 3 north" mapping in the older notes is wrong.
- 2.05 builds these frames through a get-prop helper keyed by prop id. Observed groupings: {0, 11, 13, 18, 31, 33} at session start, {42, 15, 16} on attach or position, and a per-tick diff of changed props. **[2.05]**
- In 2.05 (pre-2.1), prop 10 is the **bow** slot, not GANI. The `"*$walk` frame comes from the 2.17 capture, where 10 is GANI. **[srv]**

## Offline wiring

`OfflineSession::try_move` still returns `Option<PlayerUpdate>`. To put it on the wire, write `PLI_PLAYERPROPS` with X/Y/SPRITE. Drop the provisional `PacketId::Login 0x01`, `LevelRequest 0x10`, and `PlayerUpdate 0x20` ids. The real ids are type-0 login, `PLI_LEVELWARP` 0, and `PLI_PLAYERPROPS` 2.
