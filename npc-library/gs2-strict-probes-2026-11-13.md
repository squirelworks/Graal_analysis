# What GS2 compilers tolerate: one-quirk probes

Date: 2026-11-13. Method: 34 authored one-quirk GS2 probes, each with a clean twin that differs
only in the quirk, were compiled as black boxes by two public GS2 compilers (Preagonal's
MPL-2.0 compiler and gs2-parser 4fa0a26, GPL-3.0). No code was taken from either. A quirk counts
as **tolerated** when both compilers accept it and emit the same bytes as the clean twin. The
result is used by squirelworks/seihai-core's strict GS2 mode (PR #26, release 0.0.25) **[doc]**.
Tags: **[test]** for the probe runs, **[inf]** where a reading goes beyond them.

The probes stand in for the engine's own server-side compiler, which this project does not
hold: the two compilers were written against it, so agreement between them is the best
available proxy **[inf]**. See [preagonal-gs2.md](preagonal-gs2.md) for the earlier clean-room
reading and [../docs/preagonal-gs2-clean-room-2026-11-07.md](../docs/preagonal-gs2-clean-room-2026-11-07.md).

## Tolerated: both accept, same bytes as the clean spelling

| Quirk | Example | Tag |
| --- | --- | --- |
| a function body without braces | `function f() a = 1;` | [test] |
| a call of a call's result | `f()(1);` | [test] |
| `elseif` written as one word | `if (a) … elseif (b) …` | [test] |
| a stray `;` after a block or a function, or an empty statement | `function f() { … };` | [test] |
| a function with no body | `function f();` | [test] |
| old operators `<>`, `=<`, `=>`, `:=` | `if (a <> b)` | [test] |
| an unterminated `/*` at the end of the file | `… /* note` | [test] |

## Accepted with different bytes

Both compilers accept these, but the output differs from the clean twin, so a strict reader
cannot treat them as spellings of the same thing **[test]**: an assignment inside a condition,
a bare expression statement, a declaration before the body, a duplicate function, a bare GS1 command with no arguments, an assignment to a
name built at run time, and a string as a parameter name.

## Rejected by both

Comma-separated statements, `enum` with text values, `global enum`, a GS1 command with
comma arguments (`setimgpart door.png,0,0,32,32;`), nested comments, a function declared
inside a block, a `;` missing before `else`, a missing `;` before `}` or at the end of the file,
a missing `;` mid-line, a `/word` outside a string, and an unclosed block **[test]**.

## Split

| Quirk | Preagonal | gs2-parser | Tag |
| --- | --- | --- | --- |
| a GS1 message code in an expression (`a = #a;`) | rejects | accepts, different bytes | [test] |
| a GS1 range test (`a in <1, 2>`) | rejects | accepts, same bytes | [test] |

## How common the quirks are

In four script corpora, the quirks that appear most are a brace-less function body, a bare
GS1 command, an assignment in a condition, `elseif`, an unterminated final comment and a bare
expression. Where a quirk is the only one in a script unit, Preagonal accepts nearly all units
with a brace-less body, `elseif` or an unterminated comment, and almost none with a GS1
command or message code **[test]**. The counts are aggregates only; no corpus text is
published here.

## What this means for a reader of old scripts

- A strict GS2 reader can accept the seven tolerated quirks with a warning and compile them
  to the clean bytes.
- A script with a GS1 command, a GS1 message code or a GS1 range is GS1 written in a GS2
  file, not loose GS2. Reading it as GS1 keeps its meaning; reading it as GS2 drops it
  (→ [../client-internals/gs1-on-5x-hud-and-flags.md](../client-internals/gs1-on-5x-hud-and-flags.md)) **[inf]**.

## Not known

- Whether the engine's own compiler accepts the two split quirks.
- The duplicate-function rule in the real client (which body runs).
