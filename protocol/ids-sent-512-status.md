# Ids sent by 5.12; 2.31 id-44 disagreement — status

Date: 2026-11-16. Research-list rank **#17**. Consolidates E#4 / profile rows; **no new send-wrapper walk or throw capture**.

Reconciled 2026-11-22 against the already published November 20 throw lab; no new execution.

Tags: **[bin]** send floors; **[cap]** partial 5.12 / 2.31 labs; **[inf]** open disagreements.

## 5.12 client→server send floor

| Source | What it lists | Limits |
|---|---|---|
| Genuine 5.12 **S→C** handled set | Identical to 5.00r7 (100 ids incl. 132/133/193/197) | [`v5v6-windows-unpacked.md`](v5v6-windows-unpacked.md) **[bin]** — receive side |
| Original 5.00r7 send-wrapper scan (connection) | Scan omitted **11**; combined floor now includes the separately traced throw path. Includes **44** as process-list reply | [`v5x-clients.md`](v5x-clients.md#client--server-ids-500r7) **[bin]** |
| 5.00r7 throw path (backup engine) | **Does** send **11** (`PLI_THROWCARRIED`) empty body — wrapper list missed it | E#4 static resolution; [`windows-404r2-500r7-static-2026-11-09.md`](../client-internals/windows-404r2-500r7-static-2026-11-09.md) **[bin]** |
| Unchanged 5.00r7 throw lab | Empty-body **11** on both completed throws; separate from the backup-engine static input | [`November 20 lab`](lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4) **[lab]** |
| Profile `5.00-6.03.toml` 5.12 row | Cap-only sample: `1, 2, 11, 23, 24, 34, 37, 38, 44, 47, 157` — **send code not read** | `pli_sent_src = "cap only"` **[cap]** |

**Status for #17 (5.12 half):** superseded by the [complete send sets below](#full-send-sets-500r7-and-genuine-512-g255-2026-11-25). Earlier text: treat the **5.00r7 floor + id 11** as the best proxy until a genuine **5.12 `Graal3DEngine.dll` send-wrapper pass** lands. Cap sample proves 5.12 can emit 11 and 44 on the wire; it is not a complete set. Do not use the “5.12 untouched” tree (it is 5.00r7 — F01 / #53).

## Full send sets, 5.00r7 and genuine 5.12 (G255, 2026-11-25)

Static read of the unpatched 5.00r7 engine and a memory image of the genuine 5.12 engine; nothing run. **[bin]**

**How.** The game connection has one send routine, `SEND(id, body)`, reached through the connection object's method table.
It either encodes the packet at once (id + 32, body, newline) or queues it for the worker thread, whose flush calls the same
encoder; for id 93 it first sends a 50 carrying the length. Every call through that method and every direct call to `SEND` in the
code section was traced back to the id it pushes, and a raw byte scan found no call the disassembly missed. The encoder has only
those two callers, the queue only `SEND`, the connection pointer is not handed to any other object, and the only other socket
sender is the HTTP file downloader. **[bin]**

**Every send site uses a fixed id.** The only variable ids are `SEND` passing its own argument on to the encoder or queue, and
the queue replaying them. No script can send an arbitrary id: the send-related built-ins (`sendServerText`, `sendtorc`, and in
5.00r7 `sendtonc`) all use fixed ids, scripts only supply bodies, and the encoder refuses a body containing a newline (except 93,
which is length-prefixed). **[bin]**

| Build | Ids sent (complete static set) | Count |
|---|---|---|
| 5.00r7 | 0, 1, 2, 4–24, 26–30, 32–38, 40, 41, 43–47, 50, 79, 80, 81, 92, 93, 96, 97, 98, 130, 152, 154–159, 161, 162 | 62 |
| 5.12 | the same, minus 21 and 40, plus 48 | 61 |

The difference, with every other wrapper matching one for one:

- **21 (`PUTNPC`), 5.00r7 only.** Its one wrapper is called only from the GS1 command executor (`putnpc2`); 5.12 has neither
  ([GS1 is gone in 5.12](../npc-library/gs1-commands-by-version.md#512-no-gs1-command-table-2026-11-24)). **[bin]**
- **40 (`SHOOT`) becomes 48 (`SHOOT2`).** The same wrapper slot on the shoot / `setshootparams` path sends 48 in 5.12, with a
  larger body builder; no send of 40 is left. This matches 5.12's S→C 191 (`PLO_SHOOT2`). **[bin]**

Other points:

- **38 (`TRIGGERACTION`)** is sent by both builds, from the `triggeraction` / `triggerserver` built-ins, mouse clicks and
  pushed/pulled events; 5.12 only loses the GS1 executor as a caller. The original 5.00r7 wrapper list missed it. **[bin]**
- **11** is confirmed in both, from the throw path. **[bin]**
- **5** has two uses: the bomb-removal wrapper, and the login packet's type byte, sent by the connect routine before 37
  (language). **[bin]**
- **162** is sent from the receive dispatcher's S→C 108 branch, which both builds test before the main switch, so 162 is reachable ([v5x-clients](v5x-clients.md#server--client-ids-500r7)). 43, 45, 46, 79, 92, 96–98, 130 and 162 were not named from the
  code here; their labels in the profile are the server's. **[bin][inf]**
- The original 5.00r7 floor is fully reproduced; it had missed 0, 11, 20, 27, 30, 38, 40, 43, 45, 46 and 162. Every id of the
  5.12 capture sample (`1, 2, 11, 23, 24, 34, 37, 38, 44, 47, 157`) is in the 5.12 set. **[bin][cap]**
- Reachability is static: every wrapper has a caller, but not every caller was shown to run. **[inf]**

`version-profiles/5.00-6.03.toml` now carries both sets with `pli_sent_complete = true`.

## 2.31 “id 44” — two different messages

| Direction | Id 44 | 2.22 | 2.31 | Verdict |
|---|---|---|---|---|
| **S→C** | `HASNPCSERVER` | handled | **dropped** (adds 84, 189) | **Settled** [`2.22-2.31.md`](../version-profiles/2.22-2.31.md) **[bin]** |
| **C→S** | process-list reply to S→C 182 | sent | still sent (lab answered process-list) | **Settled** as still present **[bin][cap]** |

There is no remaining “does 2.31 send 44?” disagreement once S→C vs C→S are separated. Profile `pli_sent` for 2.31 still lists C→S 44.

## Lab: controlled 5.12 throw (G256, 2026-11-25)

Loopback lab in the headless Debian lab VM: Windows 5.12 (`G3D14097`) under Wine, the lab's `gs2emu-73` world (commit unrecorded) behind `gen5probe.py`, run `thr512-a`. The plan injected a bush below the player and held A for 0.3 s to lift and again to throw; no level file, glove or flag was changed, and the start level was unchanged afterwards. Captures stay in the VM. **[lab]**

| Step | C→S ids |
|---|---|
| Idle, 10 s | only 24 (one byte), about every 5.1 s |
| Lift 1 | 1 (board change, 2×2 bush tiles); 2 (gani `lift`, prop 19 = 1, gani `carrystill`); 34, 157, 23 for the lift gani, carry gani and lift sound |
| Carrying, 4 s | only 24 |
| Throw 1 | **11** with an empty body, in the same bundle as props (gani `idle`, prop 19 = −1); then 23 for the crush sound |
| Lift 2 | as lift 1, without 34/157/23 (files cached) |
| Throw 2 | **11** with an empty body, with the same props |
| Idle after | only 24 |

Id 11 appears exactly once per throw and never while idle, lifting or carrying, matching the 2026-11-20 5.00r7 result.

## Still open

- [x] ~~Full **5.12** send-wrapper / variable-send floor on genuine engine (**S**).~~ Complete for both 5.00r7 and 5.12; no variable-id sends ([above](#full-send-sets-500r7-and-genuine-512-g255-2026-11-25)).
- [x] ~~Wire-confirm id 11 on a 5.00r7 throw.~~ The published November 20 lab records two throws; this does not supply a controlled 5.12 throw comparison.
- [x] ~~A controlled **5.12 throw capture** tying id 11 to the throw action.~~ [Lab 2026-11-25](#lab-controlled-512-throw-g256-2026-11-25): one empty-body 11 per throw, none at idle, lift or carry. **[lab]**
- [x] ~~Align `v5x-clients.md` wrapper-list text with the separately traced throw path.~~ The original scan and combined floor are now distinguished, with the later lab cited separately.
