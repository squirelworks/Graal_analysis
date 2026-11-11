# Early Windows client timer configuration (E#300)

## Scope and evidence

This static correction covers three Windows x86 clients identified below. Build identities, observations and the private evidence digest are researcher-supplied. The publication editor reviewed only the sanitized handoff; underlying executables and evidence were not independently inspected. Evidence ID: `GRAAL-E300-20261109-01`, registered in [the evidence index](../docs/evidence-index.tsv).

| Build | Bytes | MD5 | SHA-256 |
| --- | --- | --- | --- |
| 4th Graal alpha | 711680 | 8cae23a58e1b1b10f3149bdbe53d0431 | 013478713aa325e07de2e114e6f584ed20903f8aeb81096f77b9c3e19b82010b |
| 5th Graal | 723968 | 0e7c3573f0a916f8b2376060e768fe96 | fd50cff1358c9d6144c24c62332252a970355317f6096962879840524ef72289 |
| 5th Graal alpha | 739840 | e54397e7d4f59d30b77d5cf0475335a1 | 8c5b1f98d948a12f15586f68cfa6a6b2c63f043253d0ce19015b93b4eca8dff5 |

The editor matched the supplied MD5 and size pairs against the existing [build catalogue](build-catalogue.md) and [static survey](../version-profiles/matrix/builds-static-survey.tsv). This checks correspondence with published identities, not the private files themselves.

## Stored configuration

`[bin]` Each of the three main adventure forms declares an enabled DelphiX timer with an interval of 50 milliseconds, active-only disabled, maximum lag ten, and a bound timer callback. The declared callback has a corresponding published executable method in the researcher's metadata check. This establishes static binding only.

`[bin]` The researcher reports the same serialized settings in four controls: 1st Graal, 3rd Graal, 4th Graal and 6th Graal. All seven inspected forms also declare a separate ordinary timer without serialized interval or enabled values. No idle-handler property was present in those forms.

`[inf]` The three survey cells formerly reading “none (idle loop)” therefore cannot describe timer absence in these exact inputs. They now record the configured 50 ms interval. The correction does not establish the absence of programmatically installed idle code.

## Validation and remaining questions

`[bin]` The researcher extracted owner-supplied archives, hashed the executable inputs, decoded complete binary forms with no trailing bytes, read settings from component trees, and matched callbacks against validated published-method metadata. No client or installer was executed.

- [x] ~~Determine whether the three disputed forms contain a configured timer.~~ All three declare the configuration above.
- [x] ~~Measure callback execution.~~ The callbacks run; see [callback execution](#callback-execution).
- [ ] Measure actual elapsed tick duration (cadence).
- [ ] Check runtime changes to timer settings and programmatic idle-handler installation.

A configured interval is not an observed runtime cadence. Appendix E#300 remains open for the timing questions.

## Callback execution

`[lab]` Evidence ID `GRAAL-E300-RUNTIME-20261109-01`. A debugger breakpoint on the bound timer callback counted hits over a requested 3000 ms capture of each client:

| Build | Hits in 3 s |
| --- | ---: |
| 4th Graal alpha | 61 |
| 5th Graal | 61 |
| 5th Graal alpha | 60 |

The 5th Graal alpha run used the 5th Graal assets and level as donors, so it did not show an original alpha world. Every run restored the original byte and memory protection, had no trap-flag cleanup failures, detached cleanly and left the client running.

`[lab]` This proves that the configured callbacks execute. About 20 hits per second is consistent with the serialized 50 ms timer, but it is not a cadence measurement: a breakpoint adds overhead, and three seconds is a short window. It is not a general 50 ms or 20 Hz claim. Runtime changes to timer settings and idle callbacks were not tested.

`[lab]` The same campaign recorded 60 timer hits in 3 s for the 1st Graal, with the player starting at (24.5, 30); a held Right reached (29.5, 30) and Left returned to the start, over 700 valid player-state snapshots. That run is reported in the same source summary and was not repackaged separately.
