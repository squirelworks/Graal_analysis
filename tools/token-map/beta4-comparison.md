# Beta4 documentary version list versus the canonical token reference

## Scope and source

Compared 2026-11-15 against GServer-v2 beta4 commit
[`365bbd2`, documentary version list](https://github.com/squirelworks/seihai-gserver-v2/blob/365bbd29a3e0e57495a02267a4b3f27839ad2ec6/server/src/versions.txt).
The pinned tree's content agrees with the retained comparison copy. This is
the actual beta4 reference, not an assumption based on a working branch name.
It is a human-readable list of version labels and tokens, with headings and
comments; it is not itself an executable's identity or a captured login.

The canonical catalogue at this comparison has 175 associations and 115 known
identifier values. The documentary list has 38 distinct raw values: 26 match
canonical bytes exactly, while 12 use shortened prefixes. No other raw values
are unmatched. Of the 115 canonical identifiers, 89 are absent from the raw
list; twelve of those are the full-prefix corrections below, leaving 77 other
identifier values beyond this list. These totals include roles beyond game
login and are not 77 newly compatible clients. **[doc]**

## Raw-prefix discrepancies

The documentary list spells five early values as `SERV009`, `SERV011`,
`SERV013`, `SERV016` and `SERV018`. The inspected clients use the corresponding
`GSERV` spellings. It spells seven later values as `NW20020`, `NW22030`,
`NW13040`, `NW10050`, `NW21050`, `NW22060` and `NW07080`; recovered client
values retain the leading `G`. The catalogue's static reads, not an automatic
repair rule, support the full bytes. The source records retain these raw list
discrepancies as conflicts rather than counting them as confirmation of the
exact token. **[bin][doc]**

`compare_beta4.py` reports suggested prefix counterparts separately. It never
normalizes the input before matching or silently creates evidence. Missing
captures do not establish missing tokens. The documentary entry describing a
corrupt package does not yield a token. **[doc]**

## Ambiguities and consumer compatibility

Three exactly matching values already have multiple canonical associations:
`GNW03081`, `GNW31101` and `GNW28015`. The list's broad version labels and
historical comments cannot select an exact public/world build or transfer
features, static findings or captures between siblings. Its similarly named
Windows labels do not establish a Linux or Mac executable's identity. **[doc]**

The canonical reference adds platform-specific values, early families,
mobile/tool associations, connector-supplied identities and non-login roles.
Unresolved production values and documented no-token families remain explicit.
They must not be imported into a game-server allow-list as if each row were a
fixed game-client token. The generated TSV is a research-association schema,
not the beta4 text layout. No drop-in format or runtime compatibility is
established; an importer must select the intended role/platform and preserve
ambiguity rather than inventing a feature profile from a shared token. **[inf]**

To repeat the exact-value comparison, supply the pinned public text to
`python tools/token-map/compare_beta4.py <versions-text-file>`. The tool reads
text only and prints exact matches, prefix discrepancies, unmatched values,
canonical additions and ambiguous associations. Public source citations and
the canonical category records remain the authority for evidence. **[doc]**
