# Version ID map

Date: 2026-10-14

## Protocol token → version

| Token | Version | Source |
|-------|---------|--------|
| `GNW07080` | 1.39 (CLVER_1_39) | version-token pack / gs2lib |
| `GNW13110` | 1.41r1 | allowedversions.txt |
| `GNW03081` | 2.05 (CLVER_2_052) | version-token pack; hardcoded in v2.05 constructor |
| `GNW24011` | 2.0 | version-token pack (v2.0 equivalent) |
| `GNW22122` | 2.1.7.x | allowedversions.txt |
| `GNW03014` | 2.2.2.0 | allowedversions.txt |
| `GNW28015` | 2.3.1.0 | allowedversions.txt |
| `GNW30123` | unmapped (reads as 30 Dec 200x by the date rule below) | seen on listserver port 14922 |
| `GSERV007` | 1.21 | build catalogue |
| `GSERV013` | 1.28 beta2 | build catalogue |
| `GSERV014` | 1.3 test | build catalogue |
| `GSERV016` | 1.31 | build catalogue |
| `GSERV018` | 1.32 | build catalogue |
| `GNW20020` | 1.33 | build catalogue |
| `GNW22030` | 1.34 | build catalogue |
| `GNW13040` | 1.35 | build catalogue |
| `GNW10050` | 1.36 | build catalogue |
| `GNW21050` | 1.37 | build catalogue |
| `GNW22060` | 1.38 | build catalogue |
| `GNW08011` | NewMain client (1.42 notes) | build catalogue |
| `GNW23021` | 2.01, 2.01 rev1 | build catalogue |
| `GNW15041` | 2.02, 2.02 rev1 | build catalogue |
| `GNW20041` | 2.02 rev2 | build catalogue |
| `GNW06051` | 2.03 | build catalogue |
| `GNW24061` | 2.04 | build catalogue |
| `G2N15041` | NewWorld betas 1 and 2 | build catalogue |
| `G3D03014` | Linux 3.04 | 3.x client binary (GNW03014 with a G3D prefix) |
| `G3D28015` | Mac OS X 3.153 | 3.x client binary (GNW28015 with a G3D prefix) |
| `G3D30123` | 3.x listserver login | 3.x client binary |

GNW tokens are `GNW` + build date as DDMMY (GNW03081 = 3 Aug 2001). The 2.1 test builds (Sep 2001) still send GNW03081.
Per-build hashes, dates and the rest are in `build-catalogue.md`.

## Filename → build

| Binary | Build |
|--------|-------|
| `Graal_2171.exe` | 2.171 |
| `Graal_222.exe` | 2.22 |
| `Graal_231.exe` | 2.31 |

## Construction (v2.05)
Token is eight `_LStrFromChar` immediates in `TAdventureClient_Create`, not a string literal. Random prefix `(rand & 0x7F) + 0x20` precedes it.

## Confirmed in Graal 139.exe.c
FUN_004c7208 builds the token as char immediates: G N W 0 7 0 8 0 → GNW07080.
Connects to port 14900 (PTR_s_14900).

## 1st Graal.exe.c
No GNW token construction found. Uses .zelda level files (level33.zelda, house19.zelda). Has socket code but no version-token immediates. Predates the GNW scheme.

## Dhrake-improved 1.39 export
Same binary, better symbols. ~390 recovered names. Token still built as char immediates (line ~128320). Preferred corpus in shdecompiling/graal-139-dhrake.
