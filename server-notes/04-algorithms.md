# Algorithms and pseudocode

Faithful to `CEncryption.cpp`, `TPlayer.cpp`, `TPlayerLogin.cpp`,
`TServerList.cpp`, `TMap.cpp`, `TLevelBaddy.cpp`, `msgPLI_TRIGGERACTION`.
Identifiers match the dumps.

---

## 1. LCG step

```
function step(codec):
    codec.iterator ← (codec.iterator × 0x8088405 + codec.key) mod 2³²

ITERATOR_START = [0, 0, 0x04A80B38, 0x04A80B38, 0x04A80B38, 0]

function reset(codec, key):
    codec.key ← key
    codec.iterator ← ITERATOR_START[codec.gen]
    codec.limit ← -1
```

## 2. Gen-3 dummy byte (client → server packets only)

```
function gen3_insert(codec, buf):          # client encrypt
    step(codec)
    pos ← (codec.iterator ∧ 0xFFFF) mod length(buf)
    return buf[0..pos) + byte(')') + buf[pos..]

function gen3_remove(codec, buf):          # server decrypt
    step(codec)
    pos ← (codec.iterator ∧ 0xFFFF) mod length(buf)   # length is already +1
    delete buf[pos]
```

gs2emu outbound gen 3 does **not** insert. Only zlib + length.

## 3. Gen-4 / gen-5 XOR stream

```
function xor_stream(codec, buf):
    i ← 0
    while i < length(buf):
        if i mod 4 = 0:
            if codec.limit = 0: return buf
            step(codec)
            if codec.limit > 0: codec.limit ← codec.limit - 1
            word ← iterator as little-endian 4 bytes
        buf[i] ← buf[i] xor word[i mod 4]
        i ← i + 1
    return buf
```

Inbound gen 4: `limitFromType(0x06)`, xor, bz2-decompress.
Inbound gen 5: read type byte, `limitFromType(type)`, xor, then
decompress by type.

## 4. Inbound frame

```
function doMain(player):
    while recvbuf has ≥ 2 bytes:
        n ← u16be(recvbuf)
        if recvbuf shorter than 2+n: break
        payload ← recvbuf[2..2+n)
        consume 2+n
        case player.in_codec.gen of
            1: inner ← payload
            2,3: inner ← zlib_dec(payload)
            default: inner ← decryptPacket(payload)
        parsePacket(player, inner)

function parsePacket(player, inner):
    if player.type = AWAIT:
        line ← read through '\n'
        return msgPLI_LOGIN(line)
    for each line in inner split '\n':
        if gen = 3 and player.isClient:
            gen3_remove(player.in_codec, line)
        id ← gchar(line[0])
        TPLFunc[id](line[1..])
```

## 5. Login

```
function msgPLI_LOGIN(pkt):
    type ← 1 << gchar()
    choose gen from type          # CLIENT→3, CLIENT2→4, CLIENT3/RC2→5
    if client or new RC:
        key ← gchar(); reset(in_codec, key); out_codec matches
    version ← 8 bytes
    name ← pstring(); pass ← pstring()
    if version not in allowedversions: disc("not allowed"); return false
    if ip banned: disc(); return false
    if RC and name not in staff: disc("no RC rights"); return false
    if NPCSERVER:
        if pass ≠ ns_password: disc(); return false
        setNPCServer(this, gshort port)
        sendNC_Maps(); sendNC_Levels(); sendNC_Weapons()
        return true
    send listserver SVO_VERIACC2(name, pass, id, type)
    # continue in SVI_VERIACC2
```

(See the full file in the Drive archive for the complete set of sections: warp, gmap, baddies, trigger hacks, RC file browser, gtokenize, AP tick, etc.)

---
*Extracted from the Ember atlas in the decommissioned local workspace. Full algorithms are in the Google Drive archive.*
