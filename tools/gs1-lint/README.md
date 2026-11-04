# gs1-lint

A static checker for GS1 NPC scripts against the 2.05 rev 2 client's command
table. It reads the table from the reference manual (§8.2,
`manual/08-scripting/02-gs1-reference.md`), so it changes when the manual does.
Pure Python 3.10+, no dependencies, no network.

```
python tools/gs1-lint/gs1lint.py npc-library/scripts      # every *.gs1 below a folder
python tools/gs1-lint/gs1lint.py some.gs1 -q              # errors only
python -m pytest tools/gs1-lint -q                        # tests (also run in CI)
```

## What it reports

| Check | Level | From |
| --- | --- | --- |
| unclosed string, unbalanced bracket, missing `;` | error | §8.1.8 |
| a statement that is not a 2.05 command, keyword, assignment, increment or call of a script function | error | §8.2.4 |
| wrong argument count for the command's signature (a trailing `S`/`M` argument may hold commas) | error | §8.2.1 |
| a bare word that is not in the item, baddy, colour, carry-object or direction table | error | §8.2.2 |
| a command 2.05 parses but ignores (`setfocus`, `canwarp`, `setz`, ...) | error | §8.2.4.9 |
| a command only the 2.22 documentation has (`showtext`, `play2`, `addstring`, ...) | error | §8.2.7.3 |
| a call in an expression that is not a 2.05 expression function | error | §8.2.5 |
| a script function called but never defined | error | §8.1.3 |
| tests `timeout` but never sets `timeout` or calls `sleep` | warning | §8.1.4 |

The four disputed signatures of App. E#201 (`toinventory`, `puthorse`,
`showimg`, `replaceani`) accept either reading.

## What it does not do

It does not run the script. It cannot tell whether a flag name is spelt the
same in two scripts, whether an image file exists, or whether a condition
between 0 and 1 counts as true (App. E#200; write conditions that give 0 or 1).
`#` codes in strings are passed through unchecked (App. E#203).

The `Library` test lints every `*.gs1` file under `npc-library/scripts/`, the
original NPC library, so a script that does not parse fails CI.
