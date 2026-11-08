# Link a recovered Linux 4.04r2 script to live loading

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../workingpapers/sources.tsv).

## Recovered corpus and structural checks

`[bin]` A bounded embedded-zlib scan identified fourteen valid four-segment script
candidates. Together they contain 129 named function entries and 15,799 decoded
instructions. Decoded instruction bytes round-trip exactly; function entries
and string references are in range. Source: `L404-EMBEDDED-INDEX`.

`[bin]` Native container reader and writer operations were recovered for focused
review. Their recovery is not, by itself, a complete specification or an execution
result. Sources: `L404-CONTAINER-READER` and `L404-CONTAINER-WRITER`.

## One payload linked to execution

`[cap]` The live profile-script input was 9,530 bytes. Its digest matched the
recovered profile payload, and the same run then entered the native executor.
This links one recovered script to actual loading and an executor entry; it does
not establish execution of all fourteen streams or completion of that whole
profile script. Sources: `L404-PROFILE-PAYLOAD` and `L404-LIVE-LOAD`.

`[cap]` An initial reader used the wrong string representation and returned the
wrong digest. That attempt remains superseded. Reading through the corrected data
pointer produced the match; the extraction was not altered to manufacture it.
Source: `L404-LIVE-LOAD`.

`[cap]` This corrected live-load run used normal profile-script initialization;
no script input was substituted. Before the read, the original executable was
stopped in the native container reader. The debugger read the actual payload,
recorded its digest, allowed the reader to return and continued to executor entry.
The inferior was then explicitly terminated. Server and server commit were none;
the owned run used an isolated Linux guest and private network namespace.

`[cap]` The researcher reported debugger exit zero, no truncation, temporary-state
removal and verified owned-group cleanup. Two permission-denied process observations
were separately identified as kernel workers and were not treated as experiment
children or termination targets. The cleanup claim is limited to the owned group.
Source: `L404-LIVE-LOAD`.

The approved redacted record name is `L404-LIVE-LOAD.json`. It is an alias for
the owner-held original carrier, not a published JSON export; its indexed digest
does not describe hypothetical renamed-file contents.

## Boundary

The corpus is not a recovery of historical server-delivered Login or connector
content. It neither proves Windows/Linux component equivalence nor establishes
tested 3D gameplay. A Torque-facing surface remains a comparison lead rather
than a demonstrated common implementation.

- [x] ~~Connect one recovered payload to a live loader/executor path.~~ The corrected match does so.
- [ ] Test the remaining streams before claiming corpus-wide execution.
- [ ] Recover loader/writer semantics separately from round-trip counts.
- [ ] Compare components by exact identities before asserting cross-platform equivalence.
