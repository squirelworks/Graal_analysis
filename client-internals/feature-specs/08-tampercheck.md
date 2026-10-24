# 08 Tampercheck (PLI 39) for 2.17+ and the process list

Snapshots read: Graal_analysis `8da6800` (`protocol/client-versions.md`, `version-profiles/2.22-2.31.md/.toml`), Seihai `06aacfd` (`protocol/profile.rs`), GServer-v2 (`TPlayer.cpp` `msgPLI_MAPINFO`, `msgPLI_PROCESSLIST`, `TPlayerLogin.cpp`), the public-server report.
Folded here: **PLO_LISTPROCESSES 182** and PLI 44/45 process list.

## Naming trap
GServer-v2's older header calls PLI 39 `PLI_MAPINFO` ("might be gmap related"). The Graal_analysis notes call it `PLI_TAMPERCHECK`. **Client to server 39** is not **server to client 39** (`PLO_LEVELMODTIME`, see 06). Never mix them.

## What it is **[bin][cap]**
- New in 2.17; absent in 2.05 and 1.x. Sent once right after `PLI_LANGUAGE` (37) at login.
- Payload: two GINT5 values (each a 32-bit word, top 4 bits first), 10 bytes. In two separate 2.22 lab sessions the bytes were identical, so they behave as a per-build constant. The lab value is stored in `version-profiles/2.22-2.31.toml` (`lab_value_hex`); do not paste it elsewhere. 2.31 also sends it; its value is not recorded.
- What the words hash is not traced (probably memory/code hashes of the client).

## Exact server behaviour **[srv]**
`TPlayer::msgPLI_MAPINFO` (id 39) reads the rest of the packet and returns. **GServer-v2 does not validate it.** The lab therefore cannot tell you whether a different value would be rejected. Real servers may check; unknown.
Process list: the server sends `PLO_LISTPROCESSES` (182) once during login (2.17+). The client can answer `PLI_PROCESSLIST` (44) with a list of running programs (inferred from the names and the server's parse, not captured); `msgPLI_PROCESSLIST` parses it into a vector and ignores it. A later copy of the server also has 45 (process running). Anti-cheat only.
Also relevant: `msgPLI_NULL` counts unknown ids and disconnects after more than 5, so never send ids that are not in the client's profile `pli` set.

## Public servers
The 2026-10-24 run logged in to 4 public servers with 2.22 and **no id 39**; none disconnected within 20 s (report in the lab dir). That shows presence is not enforced at login on those four, not that it is never enforced.

## Seihai today
- Profile flag `tampercheck` exists. `send_post_login` sends LANGUAGE only (no id 39), per the report.
- 182 and 44 are not handled.

## Steps for Claude
1. In the 2.22/2.31 profiles add `tampercheck_bytes: Option<[u8;10]>` read from the notes' value; send `PLI 39` right after LANGUAGE when the profile has `Some`. Keep `None` for 2.17 until a value exists.
2. Make it opt-in at first (`--send-tampercheck`) so the public-server default stays "same as the 4 servers that accepted us".
3. Handle 182 by sending nothing (or an empty `PLI_PROCESSLIST` if a server complains); log it.
4. Add a test asserting the frame decodes to two GINT5 values after the LANGUAGE frame.

## How to test
- Lab with GServer-v2: confirm the extra packet causes no error and no invalid-packet counter increase (the handler exists). Compare Seihai's frames with the 2.22 capture frame by frame (`examples/lab_replay`).
- Cannot test enforcement locally.

## NEEDS
- For enforcement only, and only if a server is seen to reject us: "the 2.22 id-39 value builder" (what the two 32-bit words are computed from). A decompile of that routine in the 2.22 client.
- For 2.17 and 2.31 values: a lab login capture with each client (no decompile; the 2.31 value is cheap, the 2.17 one needs the 2.17 build in the lab).
