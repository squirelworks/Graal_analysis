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
| `GNW30123` | unmapped | seen on listserver port 14922 |

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
