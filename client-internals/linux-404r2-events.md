# Record Linux 4.04r2 event ordering and deferred delivery

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../docs/evidence-index.tsv).

## Observed dispatch sequence

`[cap]` A self-authored compiled fixture was substituted for the owned process's
profile-script input. Its top-level statements ran before the creation handler.
That handler queued another event and continued to its following statement;
the queued handler did not run inline. Top-level statements ran again before
the queued handler. A second control reproduced the same ordering. Sources:
`L404-EVENT-FIXTURE`, `L404-EVENT-CONTROL` and `L404-EVENT-REPEAT`.

`[cap]` In a preserved earlier attempt, an event-name-only invocation was rejected
for too few arguments. An invocation with an additional value allowed delivery.
This qualifies the tested fixture call; it does not define every variadic API.
Source: `L404-TRIGGER-ARITY`.

## Experiment boundary

`[cap]` The run began with stock initialization up to the script loader. Only
the owned process's input buffer and length were replaced; executable files
and signature checks were not patched. The fixture events completed before
explicit inferior termination and owned-group cleanup. The researcher checked
fixture identity, ordered output, debugger completion and capture completeness.
Server and server commit were none; the network namespace was isolated.

Redacted evidence record names are `L404-EVENT-CONTROL.json`,
`L404-EVENT-REPEAT.json` and `L404-TRIGGER-ARITY.json`. These approved aliases
identify owner-held carriers; they are not published JSON exports. The source
index digests identify the original carriers rather than hypothetical renamed files.

This measures two event dispatches in one object lifecycle. It does not establish
all-version event scheduling, joined-class lookup, public calls, networking or
full GS2 conformance. It is an instrumented script-input experiment, not an
untouched GUI-startup result.

## Relationship to earlier notes

The [earlier third-party lead](../docs/preagonal-gs2-clean-room-2026-11-07.md)
left repeated top-level execution unconfirmed. This client experiment supplies
a narrow result without using that other VM's implementation as evidence.
The [later Windows engine study](gs2-vm-from-engines.md) retains its own build
scope; its unmeasured event questions are not all closed by this result.

- [x] ~~Test top-level ordering and deferred delivery in this fixture.~~ Two runs agree.
- [ ] Measure other object lifecycles, joined classes and event sources separately.
- [ ] Establish complete invocation signatures before generalizing the arity result.
