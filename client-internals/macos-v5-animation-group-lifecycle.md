# Shared Mac v5 animation-group acceptance and cleanup

[bin] A focused static review on 2026-11-09 opened the GANI consumer in the
shared PowerPC v5 executable identity (exact digest owner-held)
`owner-held SHA-256 (not published)`.
Five archive copies share this executable, including one labelled 5.12;
the review does not authenticate those release labels. No native loader run
or animation playback was observed for this finding.

## Group acceptance and abandonment

[bin] Within ANI state, comma-delimited placement records are collected into a
group whose required count is four. SINGLEDIRECTION changes that count to one.
At ANIEND, the loader accepts a sufficiently populated group and discards an
incomplete one. End of input destroys a still-current group. Thus reaching
end of input is not evidence that an unterminated group was committed.

These are native construction/cleanup observations. They extend the general
directive inventory in [the GANI reference](../formats/gani.txt); they do
not establish full placement grammar or safe rejection of every malformed input.

## Stored duration and sound metadata

[bin] WAIT adds duration to an existing group. PLAYSOUND stores a resource
reference, the current duration and two default fields; both optional numeric
arguments must exist for those defaults to be replaced. Stored duration and
sound fields do not prove scheduling, units, audible playback or rendering.

[bin] SCRIPT collects source lines through SCRIPTEND or end of input and
returns text. The opened loader body does not execute an interpreter.
This is not evidence that GS1 or GS2 ran successfully.

## Limits and decisive next test

- [ ] Observe one unchanged-loader positive control reach consumption and a
  successful return before testing incomplete groups with authored fixtures.
- [ ] Compare a complete one-direction group with one missing its terminator,
  keeping loader return, retained group state and rendering as separate results.
- [ ] Trace tokenizer and numeric helpers before defining quoting, comments,
  exact numeric conversions or malformed-input compatibility.

The original placement grammar, actor tables, timing/playback consumers and v6
implementation remain outside this result. No reproduction implementation,
shipped animation source, asset or native code is included.

## Evidence

MAC-PPC-V5-GMAP-GANI-20261109-R1 is a sanitized researcher-held static summary;
its public evidence identifier is registered in [the evidence registry](../docs/evidence-index.tsv); the exact digest remains owner-held.
The original export remains owner-held. Other gmap observations in that source
are deliberately excluded from this animation scope.

- `MAC-PPC-V5-GMAP-GANI-20261109-R1`.
