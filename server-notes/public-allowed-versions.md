# Which client versions public Reborn game servers allow

Date: 2026-10-31. These are the two "Allowed:" lists seen from public game servers, read against gs2lib's version table. No v5 or v6 client has logged in to a public server yet. Everything below about v5/v6 comes from these two lists and the server code.

Tags: **[cap]** seen in a public run's output · **[src]** read in GServer-v2 or gs2lib source · **[inf]** inferred.

## The refusals on record

| Date | Server | Software | Client sent | Reply |
|---|---|---|---|---|
| 2026-10-29 | Graal the Adventure, `2gta.home.eevul.net:14913` | GServer-v2, listed as "Beta Version: 4.0.0" | Seihai, 2.3 profile (`GNW14015`) | `Your client version is not allowed on this server.` / `Allowed: 2.22, 5.07` |
| 2026-10-30 | "S2" (host not recorded) | gs2, signature 73 | Seihai, 2.05 profile (`GNW03081`) | `Your client version is not allowed on this server. Allowed: 2.22, 1.41r1 - iPhone Belote 1.5` |

- The 2gta line is from the user's terminal on a personal lab host (hostname redacted), run `debug-20261029-101954`. The same server took the 2.22 profile (`GNW03014`) in every other run that day. **[cap]** The packet logs of that run hold only ids and lengths, so the terminal is the only record of the text.
- The S2 line is from the public game-server check, `public-checks/public-gserver-2026-10-30.md` in the project folder (also `documentation/public-gserver-2026-10-30.md` in Seihai). **[cap]**
- GServer-RS ("S1") closed a 2.05 login with no message, so it gave no list. **[cap]**

## How the server builds the list **[src]**

Read in GServer-v2 `TServer::loadAllowedVersions` and `TPlayer` (the login check), and in gs2lib `5c36ab8` `src/IUtil.cpp`:

- Each line of `config/allowedversions.txt` is either a token or a range `A:B`. The message prints each token through gs2lib's version string table, and prints a range as `A - B`.
- A range allows every token whose **position** in `clientVersions[]` lies between A's and B's, both ends included (`versionID >= a && versionID <= b`). A token that is not in the table gets `CLVER_UNKNOWN` (0), which lies in no range.
- The stock `allowedversions.txt` that comes with GServer-v2 enables only `GNW03014` (2.22). Every other line, including all the 5.x and 6.x tokens, is commented out.

## What that means for 5.x and 6.x

**Graal the Adventure** (`2.22, 5.07`): "5.07" is gs2lib's name for `G3D22067`, which is **5.00r7**. That is the only 5.x or 6.x build it allows. 5.12, 5.24, 5.30/5.31 and every 6.x would be refused. **[cap]** for the list, **[src]** for the name.

**S2** (`2.22, 1.41r1 - iPhone Belote 1.5`): the range runs from `GNW13110` to `G3D2504D`, which in gs2lib `5c36ab8` covers every 2.x, 3.x, 4.x, 5.x and 6.x entry in the table. **[inf]** The server's own table was not seen, and it refused 2.05 (`GNW03081`), which sits inside that range in `5c36ab8`. So S2's table differs from `5c36ab8`, most likely an older gs2lib with no 2.05 entry. The table below assumes S2's table has the 5.x and 6.x entries in the same order as `5c36ab8`. If it does, S2 should take these builds:

| Build | Token | gs2lib name | In S2's range |
|---|---|---|---|
| 5.00r7 | `G3D22067` | 5.07 | yes |
| 5.12 | `G3D14097` | 5.12 | yes |
| 5.30r3, 5.31r4, 6.00r2, 6.00r4 | `G3D26090` | 5.31x | yes |
| 6.01x | `G3D3007A` | 6.015 | yes |
| 6.034, 6.035 | `G3D2505C` | 6.034/6.035 | yes |
| 6.03r7 Windows / Linux | `G3D0311C` / `G3D0511C` | 6.037 / 6.037 (Linux) | yes |
| 5.24r3, 5.24r4, 6.00 beta2 | `G3D15010` | not in the table | **no**: unknown tokens are 0 |
| 6.00 beta1 | `G3D03048` | not in the table | **no** |

**The listserver does not check the version.** The 2026-10-25 runs (`protocol/listserver-login-type-matrix-2026-10-25.md`) show it chooses its reply by login type, not by version or token. Whether a 5.x or 6.x build gets in is up to each game server's `allowedversions.txt`.

## Best picks

- **5.00r7** is the only 5.x or 6.x build both servers allow.
- If S2's range is read correctly, **6.03r7** is the 6.x build to try there. It is also the build that played best in the lab (`protocol/v5v6-lab-play.md`).
- **5.24 is refused everywhere** until a server's gs2lib adds `G3D15010` (see `protocol/file-transfer.md`).

## Open

- No v5 or v6 login has been made to a public server. A single 5.00r7 or 6.03r7 login to S2 would test the range reading.
- The allowed lists of the other public servers are unknown. A server only prints its list to a client it refuses.
