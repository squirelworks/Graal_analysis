# Default listserver endpoint per profile

Date: 2026-10-25 (updated after the login-type matrix)

This is what a reimplementation should dial first for each profile. It is **not** what the binary carries. The binary's own host and port are kept as history in `built_in_host` and `built_in_port`.

Rule (written in Seihai `documentation/port-rule.md`; evidence in `../../protocol/listserver-login-type-matrix-2026-10-25.md`):

- Host is always `<list-host-reborn>`.
- **14921 is dead.** The public service resets it. No profile defaults to it.
- The public listserver answers by **login type**, not by version or token. A classic login (one plain zlib frame, id 0 then id 1) gets a list on **14923** (and, as of 2026-11-24, also on 14922 — see G019). A gen-5 login (id 7 with `GNW30123`) gets a list on 14922 and on 14923.
- **Legacy** profiles send the classic login and default to **14923**: 1.41 to 2.17, including 2.05 (Seihai's 2.05 profile sends the classic login).
- **Supported** profiles send the gen-5 login and default to **14922**: 2.22, 2.3, 2.31, and the 3.x builds 3.04 and 3.153 (`G3D30123`).
- `kind` is `legacy` or `supported`. `port_status` is `confirmed` (a public check of Seihai's login for that profile got a list on that port; a real client of that version was not captured) or `assumed` (not run with that login).

The table is produced by `python3 list_ports.py` (this directory) from the three profile files. `python3 list_ports.py --check` fails if a profile breaks the rule, so a later edit to a TOML cannot quietly bring 14921 back.

| version | host | port | kind | port status | built-in host | built-in port |
|---|---|---|---|---|---|---|
| 1.33 | - | - | no listserver | - | - | - |
| 1.34 | - | - | no listserver | - | - | - |
| 1.35 | - | - | no listserver | - | - | - |
| 1.36 | - | - | no listserver | - | - | - |
| 1.37 | - | - | no listserver | - | - | - |
| 1.38 | - | - | no listserver | - | - | - |
| 1.39 | - | - | no listserver | - | - | - |
| 1.41 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-reborn> | 14923 |
| 1.42 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.00 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.01 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.02 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.02 rev2 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.03 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.04 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.05 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14921 |
| 2.1 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.12 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.13 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.14 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.15 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.16 | <list-host-reborn> | 14923 | legacy | confirmed | <list-host-classic> | 14922 |
| 2.17 | <list-host-reborn> | 14923 | legacy | confirmed | - | - |
| 2.22 | <list-host-reborn> | 14922 | supported | confirmed | - | - |
| 2.3 | <list-host-reborn> | 14922 | supported | confirmed | - | - |
| 2.31 | <list-host-reborn> | 14922 | supported | confirmed | - | - |
| 3.04 | <list-host-reborn> | 14922 | supported | confirmed | <list-host-3x> | 14922 |
| 3.153 | <list-host-reborn> | 14922 | supported | confirmed | <list-host-3x> | 14922 |

What the status means per profile (matrix of 2026-10-25, one list-only login per profile and port; 3.x added 2026-11-24):

| status | profiles | evidence |
|---|---|---|
| confirmed | 1.41, 1.42, 2.00 to 2.04 (with 2.02 rev 2), 2.1, 2.12 to 2.16, 2.17 | Seihai's classic login got a legacy list on 14923 (2 or 4 rows) and no reply for about 5.5 s on 14922, in every case. Real clients of these builds were not captured; 2.1 to 2.16 have no binary at all |
| confirmed | 2.22, 2.3, 2.31 | the gen-5 login got the modern list on 14922 (8 rows, welcome, site and upgrade lines) and on 14923 (12 rows, 2.31: 17) |
| confirmed | 3.04, 3.153 | 2026-11-24: Seihai's `G3D30123` one-frame list login got a modern list on 14922 and on 14923 (legacy list then modern list). 2026-11-25: a stock 3.04 Linux client draws the list on 14922, but on 14923 the server's plain-zlib legacy frame comes first and the client disconnects ([`g428-stock-304-public-list-2026-11-25.md`](../../protocol/g428-stock-304-public-list-2026-11-25.md)); 3.153 untested. See [`g3d30123-public-listserver-2026-11-24.md`](../../protocol/g3d30123-public-listserver-2026-11-24.md) |
| confirmed | 2.05 | 2026-11-24 (G020): Seihai's classic shape-B login (the shape the 2.05 profile sends) got two id-0 lists plus status on 14923. The 2026-10-25 matrix binary had sent gen-5 for 2.05; both ports answered that. Real 2.05 clients were not captured against the public service; see [`g020-classic-login-14923-2026-11-24.md`](../../protocol/g020-classic-login-14923-2026-11-24.md) |

Open: how a real 2.17 (or stock 2.05) client logs in to the listserver.
