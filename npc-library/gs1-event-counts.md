# GS1 event flags: how many scraped level scripts use each one

Date: 2026-11-13. Counted from the full script bodies of the scraped level scripts, which the owner keeps outside this repo
(see [README](README.md)). This note gives counts only. It quotes no script.

## Method

- The set is the 3,187 records of the owner's full page copies (the repo's `npcs.json` holds 3,172 of them). It is the set the older counts in [gs1-commands.md](gs1-commands.md#event-frequency-reminder) came from: the method
  below reproduces them (`playerenters` 2,268, `playertouchsme` 1,986, `playertouchsother` 1,074, `playerendsreading`
  1,123, `compusdied` 1,122, `wasshot` 728; `timeout` 1,455 against 1,456).
- A script counts once for an event if the event's name appears in it as a whole word. `wasshot` therefore does not count
  `wasshooted`, and `playersays` does not count `playersays2`.
- Every hit below 50 was read by hand. Almost all sit inside an `if (…)` condition. The exceptions are listed in the table.
- The stored bodies have their line breaks flattened, so a `//` comment's end cannot always be seen. Where a hit is plainly
  inside commented-out code it is noted; hits that only follow a comment on what was probably its own line are counted.

## Counts

| Event | Scripts | Note |
| --- | ---: | --- |
| `created` | 0 | the one whole-word hit is the English word in a comment |
| `playerchats` | 13 | one of them is commented-out test code, so 12 live |
| `playersays(…)` | 36 | one in the same commented-out block, so 35 live. Most are `playersays(text)`; five use a two-argument form `playersays(0, text)` |
| `playersays2(…)` | 7 | five use the two-argument form `playersays2(0, text)` |
| `wasshooted` | 215 | |
| `washit` | 1,048 | |
| `wasthrown` | 136 | |
| `waspelt` | 903 | |
| `peltwith…` | 5 | all five use it to weigh damage by what was thrown; names seen: `peltwithblackstone`, `peltwithbush`, `peltwithsign`, `peltwithstone`, `peltwithvase` |
| `exploded` | 1,144 | |
| `compsdead` | 2 | |
| `playerdies`, `playerhurt`, `playerhurted` | 0 each | |
| `playerlaysitem` | 1,134 | |
| `weaponfired` | 41 | |
| `action…` | 0 | the two hits are a script variable named `actionx`, not an event |
| `shotbyplayer`, `shotbybaddy` | 0 each | |
| `main` | 0 | |

## What it shows

- The events the 2.05 table holds but no scraped level uses (`created`, `playerdies`, `playerhurt`, `playerhurted`,
  `shotbyplayer`, `shotbybaddy`, `main` and any `action…` name) are newer than most of the scraped levels, or belong to
  weapons and server-side NPCs, which a level file does not hold. The scrape cannot tell which.
- `exploded`, `playerlaysitem`, `washit` and `waspelt` are as common as the core events. Many scripts test them in one
  catch-all block next to `playerenters` and `playertouchsme`.

## Limits

- Level scripts only. Weapon scripts and server-side NPC scripts are not in the set.
- A whole-word match also counts a name used outside a condition. The hand check covers counts under 50 only.
