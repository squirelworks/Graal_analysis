# Default listserver endpoint per profile

Date: 2026-10-25

This is what a reimplementation should dial first for each profile. It is **not** what the binary carries. The binary's own host and port are kept as history in `built_in_host` and `built_in_port`.

Rule (written in Seihai `documentation/port-rule.md`, from the public checks of 2026-10-25):

- Host is always `listserver.graal.in`.
- **14921 is dead.** The public service resets it. No profile defaults to it.
- **Legacy** profiles (classic login) default to **14923**: 2.00 and everything earlier that has a listserver. 2.01 to 2.04 are treated as legacy until a check shows otherwise.
- **Supported** profiles default to **14922**: 2.05 and later.
- `kind` is `legacy` or `supported`. `port_status` is `confirmed` (a public check of that profile's login got a list on that port) or `assumed` (the rule applied to a profile nobody ran).

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
| 1.41 | listserver.graal.in | 14923 | legacy | assumed | listserver.graal.in | 14923 |
| 1.42 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.00 | listserver.graal.in | 14923 | legacy | confirmed | www.graalonline.com | 14921 |
| 2.01 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.02 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.02 rev2 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.03 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.04 | listserver.graal.in | 14923 | legacy | assumed | www.graalonline.com | 14921 |
| 2.05 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14921 |
| 2.1 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.12 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.13 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.14 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.15 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.16 | listserver.graal.in | 14922 | supported | assumed | www.graalonline.com | 14922 |
| 2.17 | listserver.graal.in | 14922 | supported | assumed | - | - |
| 2.22 | listserver.graal.in | 14922 | supported | confirmed | - | - |
| 2.3 | listserver.graal.in | 14922 | supported | assumed | - | - |
| 2.31 | listserver.graal.in | 14922 | supported | confirmed | - | - |

What the status means per profile:

| status | profiles | evidence |
|---|---|---|
| confirmed | 2.00 | a classic login on 14923 got the legacy list (4 rows) in both runs of 2026-10-25 |
| confirmed | 2.22, 2.31 | the gen-5 login on 14922 got the current list (8 rows, welcome, site and upgrade lines) in both runs |
| assumed | 1.41, 1.42, 2.01 to 2.04 | rule only: legacy. Not run on the public service. 1.41's 14923 is also the port its patched copy carries |
| assumed | 2.05 | the user's 2.05 binary, which sent the gen-5 login, got the current list on 14922. Seihai's own 2.05 profile sends the classic login and was not run on 14922 |
| assumed | 2.1 to 2.16 | rule only; no binaries (2.1's built-in values come from the 2.1 test 2 and 3 builds) |
| assumed | 2.17 | rule only. A **classic** login on 14922 got no reply for 5 s (twice). How a real 2.17 client logs in to the listserver is unobserved, so 14922 is the rule's port, not a port a 2.17 login is known to work on |
| assumed | 2.3 | no binary; 2.31 is confirmed |

Open: a classic (2.05-style) login on 14922, and the 2.17 flow, need a public check before those rows can move to confirmed, or to a different port.
