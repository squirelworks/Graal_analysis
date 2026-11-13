# Late v5 (5.303 / 5.314) — identity

Date: 2026-11-08  
Targets: unpacked **5.30r3** (FileVersion **5.303**) and **5.31r4** (**5.314**). Tags: **[bin]**.

---

## Product · **high**

| Field | 5.303 | 5.314 |
|---|---|---|
| Ship | Scylla dump of Themida-era setup/client | Same class of dump |
| CompanyName | Linux Cyberjoueurs | Linux Cyberjoueurs |
| ProductName | Graal | Graal |
| FileVersion | **5.303** | **5.314** |
| Diag label | `Client-version: ` (+ OS/CPU/Time) | Same |
| Engine | `quattro_lib` (e.g. `…\quattro_lib\crypto\sha1.c`, des/3des) | Same |

No `GRAALRELOADED-version`. No Eurocenter rebrand yet (that appears on Windows 6.113).

---

## Version / login token · **medium** (absence **high**)

| Probe | Result |
|---|---|
| Cleartext eight-char `G3D` / `GNW` / `GNP` | **Absent** in both dumps |
| `guest` / `-guestaccount` | Present |
| ASCII FileVersion outside resources | Not used as a free-standing token string |

**Reading:** Same family as Windows 6.0x dumps — do **not** invent a baked GNW/G3D/GNP literal. Token assembly site for late 5.x is still open (no `StartScript_Connector` in these images).

---

## Host / port defaults · **high**

Both builds embed adjacent cleartext:

| Field | Value |
|---|---|
| Login host | **`<login-host>`** |
| Port | **`14900`** |
| Related | `<public-host>`, account signup/translate URLs, `logins…` |

A long hex fingerprint string sits next to the host/port cluster (integrity / list fingerprint — not fully named here).

This is a clear **diff vs Windows 6.037/6.113 dumps**, which do **not** carry these ASCII host/port constants.

---

## Guest / connect surface · **high**

CLI/script flags include `-guestaccount`, `-connect`, `graal://` / `graal3://`, `-rtmp`, `-opengl`. UX: `Connecting to the login server...`, `serverlist` / `ServerList`-family strings.

---

## vs 6.x (identity) · **high**

| | Late 5.x | 6.037 | 6.113 |
|---|---|---|---|
| FileVersion style | 5.303 / 5.314 | 6.037 | 6.113 |
| Company | Cyberjoueurs | Cyberjoueurs | Eurocenter Games |
| Baked login host:port | **yes** | no | no |
| Connector script | no | no | **yes** |
