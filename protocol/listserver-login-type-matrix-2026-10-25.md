# Public listserver: the reply depends on the login type (matrix, 2026-10-25)

Derived note. The data is one run of the read-only list check made by the user on their own Linux machine on 2026-10-25 (started 22:43 JST): 19 Seihai version profiles, each tried once on port 14922 and once on port 14923 of `listserver.graal.in`, one list-only login per run (no game-server login, no chat, no warp), 38 runs in all. Each run was captured with `tcpdump`. The account name is masked, and no login frame bytes, credentials or keys appear here; the captures stay private. Per-run table: `listserver-login-type-matrix-2026-10-25.tsv`.

This extends `public-listserver-2026-10-25.md` (first two runs: 2.00, 2.05, 2.17, 2.22, 2.31) to every profile that has a listserver.

## Result

The listserver chooses its reply by the **login type** the client sends, not by the version number or the token.

| login sent | profiles in the matrix | port 14922 | port 14923 |
|---|---|---|---|
| classic: one plain zlib frame holding id 0 `newmain` and the id 1 account and password message (36 bytes of TCP payload) | 1.41, 1.42, 2.00, 2.01, 2.02, 2.02 rev 2, 2.03, 2.04, 2.1, 2.12, 2.13, 2.14, 2.15, 2.16, 2.17 (15 runs per port) | connection accepted, **no reply** for the 5 s read timeout (5.3 to 5.8 s per run) in all 15 | **legacy list** in all 15: one plain zlib id 0 frame, 2 or 4 rows, no status, site or upgrade lines |
| gen-5: id 7 with the key byte and token `GNW30123` and `newmain` in one plain zlib frame (28 bytes of TCP payload), then a gen-5 frame with id 1 (20 bytes) | 2.05 (see below), 2.22, 2.3, 2.31 | **modern list** in all 4: 8 rows plus status, site and upgrade lines | **modern list** in all 4: the legacy list first (2.05, 2.22, 2.3: 12 rows in all; 2.31: 17 rows), then the status, site and upgrade lines |

So 14923 answers both login types, and 14922 answers only the gen-5 login. For a default port that gets a list: classic login to 14923, gen-5 login to 14922 (14923 also works for it).

- The version number and the token do not decide it. 1.41 to 2.17 differ in version and token, and all got the same reply to the same login type. 2.17 (`GNW22122`) was silent on 14922 like 1.41.
- The silent case keeps the connection open; nothing is sent, and nothing closes it before the client's timeout. A classic login on 14922 is never refused, just unanswered.
- The row counts of the legacy list varied between runs (2 rows in 4 classic runs, 4 rows in 11) without following version order, and the 14923 modern list had 12 rows in three runs and 17 in one. The cause was not tested; the list changes between runs, not with the version.
- This fits the 2001 server tools' `settings.ini` (`tools/server-tools-2001.md`): clients connect on 14922 and older clients on 14923 (`clientPortOld`). The public service today answers the classic login only on 14923; the 2001 setting does not say what the current service does for each login type, so that is a reading of the two, not something tested.
- 14921 was not part of this run. It was refused at once in the earlier run.

## What this does not show

- A real client of any of these versions was not captured. Every login here was sent by the Seihai reimplementation for the named profile; the result tells which login type the service answers on which port, and says nothing about what a real 1.41 to 2.17 client sends. Whether a real 2.17 client sends the classic frame is still unobserved.
- For 2.05, the binary that made the runs sent the **gen-5** login (28-byte frame, same shape as 2.22's), while the current Seihai main sends the classic login for the 2.05 profile. The 2.05 rows above are therefore the gen-5 case. A classic 2.05 login was not run; by the table above it would be answered on 14923 only.
- No game-server login was made, so nothing here says anything about game-server traffic.

## Defaults that follow

`client-internals/version-profiles/` now gives the profiles the port of the login type the Seihai profile sends: 14923 for 1.41 to 2.17 (classic), 14922 for 2.22, 2.3 and 2.31 (gen-5). The ports are marked `confirmed` for every profile whose own login type was run on its port: the 15 classic profiles on 14923 and 2.22, 2.3 and 2.31 on 14922. 2.05 is `assumed` on 14923, because its classic login was not run. `list-ports.md` has the table.
