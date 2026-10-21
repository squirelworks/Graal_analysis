# Version ID map

Date: 2026-10-14

## Protocol token → version

| Token | Version | Source |
|-------|---------|--------|
| `GNW07080` | 1.39 (CLVER_1_39) | version-token pack / gs2lib |
| `GNW13110` | 1.41r1 | allowedversions.txt |
| `GNW03081` | 2.05 rev 2 / "2002ver9" leak (CLVER_2_052, sorts below CLVER_2_1) | gs2lib 2026; GServer versions.txt; built char-by-char in the 2.05 login |
| `GNW24011` | 2.0 | version-token pack (v2.0 equivalent) |
| `GNW22122` | 2.1.7.0–2.1.7.1 (CLVER_2_17) | allowedversions.txt; gs2lib; GServer versions.txt |
| `GNW03014` | 2.2.2.0 (CLVER_2_22) | allowedversions.txt; gs2lib |
| `GNW28015` | 2.3.1.0 (CLVER_2_31) | allowedversions.txt; gs2lib |
| `GNW30123` | unmapped; in no gs2lib table (2019–2026) and not in versions.txt. Probably a listserver-side or third-party token | seen on listserver port 14922 |

## Filename → build

| Binary | Build |
|--------|-------|
| `Graal_2171.exe` | 2.171 |
| `Graal_222.exe` | 2.22 |
| `Graal_231.exe` | 2.31 |

## Construction (v2.05)
Token is eight `_LStrFromChar` immediates in `TAdventureClient_Create`, not a string literal. Random prefix `(rand & 0x7F) + 0x20` precedes it.

Update 2026-10-21: the login line is GCHAR client type 0, then GCHAR key (`rand & 0x7F`), then the token. The "random prefix" is that key (see `protocol/login-and-walk.md`).

## Confirmed in Graal 139.exe.c
FUN_004c7208 builds the token as char immediates: G N W 0 7 0 8 0 → GNW07080.
Connects to port 14900 (PTR_s_14900).

## 1st Graal.exe.c
No GNW token construction found. Uses .zelda level files (level33.zelda, house19.zelda). Has socket code but no version-token immediates. Predates the GNW scheme.

## Dhrake-improved 1.39 export
Same binary, better symbols. ~390 recovered names. Token still built as char immediates (line ~128320). Preferred corpus in shdecompiling/graal-139-dhrake.

## Full gs2lib client token table (2026-10)

| Token | Build | Token | Build |
|-------|-------|-------|-------|
| `GSERV007` | 1.21 | `GNW20052` | 2.151 |
| `GSERV009` | 1.25 | `GNW12102` | 2.16 |
| `GSERV011` | 1.27 | `GNW22122` | 2.17 |
| `GSERV013` | 1.28 | `GNW21033` | 2.18 |
| `GSERV014` | 1.30 | `GNW15053` | 2.19 (bz2 + new encryption) |
| `GSERV016` | 1.31 | `GNW28063` | 2.2 |
| `GNW07080` | 1.39 | `GNW01113` | 2.21 (compression byte) |
| `GNW12080` | 1.391 | `GNW03014` | 2.22 |
| `GNW13110` | 1.41r1 | `GNW14015` | 2.3 |
| `GNW03081` | 2.05 rev 2 | `GNW28015` | 2.31 |
| `GNW31101` | 2.1 (2.1.0.0–2.1.0.3, also 2002ver10/13) | `G3D16053` | 3.0 |
| `GNW01012` | 2.12 | `G3D27063` | 3.01 |
| `GNW23012` | 2.13 | `G3D03014` | 3.041 |
| `GNW30042` | 2.14 | `G3D28095`… | 4.x+ |
| `GNW19052` | 2.15 | | |

The older GServer-v2 submodule lists 1.33–1.38 as `GNW20020`, `GNW22030`, `GNW13040`, `GNW10050`, `GNW21050`, and `GNW22060`. Its `versions.txt` writes them without the `G` (`NW20020`, …).
