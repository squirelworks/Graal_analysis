# Default listserver endpoint per profile

Date: 2026-10-25 (updated after the login-type matrix)

This is what a reimplementation should dial first for each profile. It is **not** what the binary carries. The binary's own host and port are kept as history in `built_in_host` and `built_in_port`.

Rule (written in Seihai `documentation/port-rule.md`; evidence in `../../protocol/listserver-login-type-matrix-2026-10-25.md`):

- Host is always `listserver.graal.in`.
- **14921 is dead.** The public service resets it. No profile defaults to it.
- The public listserver answers by **login type**, not by version or token. A classic login (one plain zlib frame, id 0 then id 1) gets a list on **14923** and nothing on 14922. A gen-5 login (id 7 with `GNW30123`) gets a list on 14922 and on 14923.
- **Legacy** profiles send the classic login and default to **14923**: 1.41 to 2.17, including 2.05 (Seihai's 2.05 profile sends the classic login).
- **Supported** profiles send the gen-5 login and default to **14922**: 2.22, 2.3, 2.31.
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
| 1.41 | listserver.graal.in | 14923 | legacy | confirmed | listserver.graal.in | 14923 |
| 1.42 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.00 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.01 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.02 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.02 rev2 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.03 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.04 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.05 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.1 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.12 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.13 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.14 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.15 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.16 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14922 |
| 2.17 | listserver.graal.in | 14923 | legacy | confirmed | - | - |
| 2.22 | listserver.graal.in | 14922 | supported | confirmed | - | - |
| 2.3 | listserver.graal.in | 14922 | supported | confirmed | - | - |
| 2.31 | listserver.graal.in | 14922 | supported | confirmed | - | - |
| 3.04 | listserver.graal.in | 14922 | supported | assumed | listserver.graalonline.com | 14922 |
| 3.153 | listserver.graal.in | 14922 | supported | assumed | listserver.graalonline.com | 14922 |

What the status means per profile (matrix of 2026-10-25, one list-only login per profile and port):

| status | profiles | evidence |
|---|---|---|
| confirmed | 1.41, 1.42, 2.00 to 2.04 (with 2.02 rev 2), 2.1, 2.12 to 2.16, 2.17 | Seihai's classic login got a legacy list on 14923 (2 or 4 rows) and no reply for about 5.5 s on 14922, in every case. Real clients of these builds were not captured; 2.1 to 2.16 have no binary at all |
| confirmed | 2.22, 2.3, 2.31 | the gen-5 login got the modern list on 14922 (8 rows, welcome, site and upgrade lines) and on 14923 (12 rows, 2.31: 17) |
| assumed | 2.05 | Seihai's 2.05 profile sends the classic login, which was not run for 2.05. The matrix binary sent the gen-5 login for 2.05; both ports answered it. 14923 answered the classic login of every other classic profile, so it is the port assumed here |
| assumed | 3.04, 3.153 | the 3.x clients send the gen-5 login with `G3D30123newmain` (`../../version-profiles/3.04-3.153.toml`). A G3D token was not tried against the public listserver; 14922 is assumed from the 2.22/2.31 result |

Open: a classic 2.05 login on 14923; how a real 2.17 client logs in to the listserver.
