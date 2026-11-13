# Late v5 (5.303 / 5.314) — login and framing

Date: 2026-11-08 · Tags: **[bin][ghidra]** · raw under `repro-letsgo2/v5/raw/`.

---

## Framing family · **high**

Both late-5 dumps sit in the **classic Graal gen-5** family:

| Signal | 5.303 / 5.314 |
|---|---|
| `Illegal characters in the outgoing data` | yes |
| `Received illegal data (1\|2) from …` | yes (wording **illegal**, not 6.113’s **invalid**) |
| `Cannot send data, socket is not initialized yet.` | **absent** |
| `Received invalid data (3)` / template path | **absent** |
| `StartScript_Connector` / `DOQLHRbY` / AES selector | **absent** |
| `onSend*` FE remapper table | **absent** |

**Reading:** Dual-mode template + AES cipher select is a **6.113** cut, not late 5.x.

### Exact wire layout (5.314 Ghidra) · **high**

Outbound:

- Packet id as GCHAR: `id + 0x20`
- Body must not contain newline (`Illegal characters…`)
- Special internal ids **`0x5D`** / **`0xA3`**: length-wrap path
- Flush when outbound buffer **> `0xFFF`**

Inbound:

- **2-byte big-endian** length (`CONCAT` of first two payload bytes)
- If length **`0xFFFF`**: extended header path; failure → `Received illegal data (1)`
- Other failures → `Received illegal data (2)`; socket kill flag set

Same classic shape as proven 6.037 send/recv. Trailing `0x0A` terminator is the family default; confirm in assembly excerpt under `repro-letsgo2/v5/raw/` if a repro needs the exact push.

---

## Cipher · **medium**

| Signal | Note |
|---|---|
| `RC4` | Present inside a crypto-algorithm catalog (libtomcrypt-style list with CFB/OFB/ECB/CBC…) — **not** proof of the 6.113 `DOQLHRbY` Arc4/AES socket selector |
| `Arc4Process` export-style name | **Absent** (unlike 6.037+) |
| DES / 3des | Named under `quattro_lib` crypto sources (GRESCR / asset path family) |

Default post-login game socket: expect **classic framing**; do not require AES template negotiation for a late-5 repro.

---

## Login · **high** (endpoints) · **medium** (first bytes)

| Step | Client | Server |
|---|---|---|
| Resolve | `<login-host>`:**14900** (baked) | Accept TCP |
| Auth | account/password or `-guestaccount` / `guest` | Accept/reject; return list/session |
| Game | Connect to chosen game server | Speak classic gen-5 PLI/PLO |
| Steady | No FE `onSend*` table | Native/classic packet ids |

HTTP account URLs exist (`…/accounts/signup.php`) — account-site, not the game framing path.

---

## UDP · **high** (presence)

`onReceiveUDPData` present in both, with bind/connect socket script surface (`onBind`, `onConnect`, “received UDP”). Scripted datagram path exists; not proof of a mandatory peer mesh.

---

## vs 6.x framing cut · **high**

| Feature | Late 5.x | 6.037 | 6.113 |
|---|---|---|---|
| Classic Illegal-characters | yes | yes | yes |
| illegal vs invalid wording | **illegal (1\|2)** | (6.037 lacks invalid(3) cluster) | **invalid (1\|2\|3)** |
| Template + AES + connector | no | no | **yes** |
| Baked login host:14900 | **yes** | no | no |
