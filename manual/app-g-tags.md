<!-- manual: kind=front status=complete -->
# Appendix G. Evidence-tag legend

How tags are written and cited is fixed in → §0.3. This appendix lists every tag the manual uses.

## G.1 Kind-of-evidence tags

Each row gives one tag and the kind of evidence it marks.

| Tag | The claim comes from |
| --- | --- |
| `[bin]` | a static read of a program: headers, resources, strings, constants, code paths, described as behaviour |
| `[file]` | a file shipped with a build or found in an archive |
| `[doc]` | a readme, manual, release note, or a repository rule document |
| `[srv]` | server source, summarised through the notes |
| `[src]` | other source code, summarised through the notes |
| `[lab]` | a client this project ran in a loopback lab |
| `[live]` | a client this project ran and watched in play |
| `[cap]` | a packet capture |
| `[wire]` | bytes read on the wire during a loopback session |
| `[run]` | a loopback session log |
| `[shot]` | a screenshot or still from a run |
| `[test]` | a check of a reader or rule against real files |
| `[inf]` | an inference that the source note marked as one (→ §0.3) |
| `[GE]` | the GraalEditor notes |
| `[checked]` | a search of named builds for a script word or string |

Source of this legend: the reading guide [doc] (docs/book/00-how-to-read.md#what-a-source-tag-means) and the agent rules [doc] (AGENTS.md#no-real-servers-no-binary-addresses).

## G.2 Build tags

A build tag names the client build the claim was read from, written with the release number as the notes write it: `[2.05]`, `[2.22]`, `[2.31]`, `[1.39]`, `[5.12]` and so on. A build tag implies a static read or trace of that build unless another tag on the same claim says otherwise. The full list of builds and their names is → §1.1.

## G.3 Combining tags

A claim can carry more than one tag. Each row gives a form of combination and what it means.

| Form | Meaning |
| --- | --- |
| `[srv][2.05]` | both kinds of evidence agree on the claim |
| `[2.05][inf]` | read from 2.05, with an inference step the source marked |
| `[cap][inf]` | seen in a capture, with an inference step the source marked |
