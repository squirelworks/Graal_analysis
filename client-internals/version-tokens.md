# Version tokens

Date: 2026-10-14

Internal version strings recovered from the public version list. No decompile material.

| Token | Build notes |
|-------|-------------|
| GNW07080 | 1.39 |
| GNW03081 | 2.05 rev 2 (= 2002ver9 leak build); gen-3 cipher, pre-2.1 code paths |
| GNW31101 | 2.1.0.0–2.1.0.3 (version string not updated) |
| GNW30042 | 2.1.4.0 (first with server-list tabs) |
| GNW15053 | 2.1.9.0 (bz2 + new encryption, new server-list gfx) |
| GNW01113 | 2.2.1.1 (plaintext and zlib; extra compression byte) |
| GNW14015 | 2.3.0.0 |
| GNW28015 | 2.3.1.0 |
| G3D03014 | Linux 3.04 (Torque rewrite; 2.22 protocol, see `protocol/v3x-clients.md`) |
| G3D28015 | Mac OS X 3.153 (2.31 protocol) |
| G3D30123 | 3.x listserver token (the 3.x form of GNW30123) |

Filename builds in the client tree: Graal_2171 = 2.171, Graal_222 = 2.22, Graal_231 = 2.31.

From 2.3 the editor and the online client are separate executables. PE FileVersion is authoritative for the editor (2.3.1.1).

The early-client transition (14801 → 14900 → length+zlib) is the protocol-side counterpart of the same era.
