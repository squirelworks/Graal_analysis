# Mac PowerPC gmap readers and 4.04r2 board dispatch

[bin] This note extends [the Windows 4.04r2 gmap heights note](gmap-heights-404r2.md)
to the native gmap readers in four Mac PowerPC executables. That note already
covers two things: the Windows 4.04r2 reader, and a Mac 4.04r2 tutorial gmap as a
file. What is new here is the Mac readers themselves and how they store the data.
This note does not find new `HEIGHTS` syntax and says nothing about rendering.

The source is a focused static review dated 2026-11-09. It covers:
- the shared v3 executable (archive labels 3.04 and 3.15r2);
- label 4.04r2;
- label 4.20r6;
- the shared v5 executable (five copies, one labelled 5.12).

Each reader was opened in its own build. No result was carried over from another build. No client was run.

## The reader in all four builds

**[bin] Command handling.**
- A `GRMAP001` check on the first line gates all command handling.
- The commands are handled in a fixed order: `WIDTH`, `HEIGHT`, `GENERATED`, `LEVELNAMES`, `GENSEED`, `LEVHEIGHT`, `LEVCHAOS`, `MINIMAPIMG`, `NOAUTOMAPPING`, `HEIGHTMAP`, `RANDOMSEEDS` and `HEIGHTS`.
- In 4.04r2, width and height are converted when the reader meets them. `GENERATED` regenerates width × height level names.

**[bin] `HEIGHTMAP`.**
- The block is read line by line until `HEIGHTMAPEND` or the end of the input.
- Rows 0 to height and columns 0 to width are stored as floats. Both bounds are inclusive.
- Rows are laid out with a stride of width + 1.

**[bin] Named `HEIGHTS`.**
- Only the first header argument is used. It is matched against the current level names. The other header arguments are not read in the opened branch.
- Up to nine rows of nine floats are stored in that level's entry.
- If the name is not found, nothing is stored, but the rest of the block is still read.
- A named block can also end at the end of the input.

**[bin] Other behaviour.**
- Unknown commands fall through.
- The opened body returns nothing, so it reports no parse status.

**[bin] 4.04r2 allocations.**
- The height branches allocate their buffers lazily, when a buffer is still empty and the dimensions are positive.
- The map grid holds (width + 1) × (height + 1) floats.
- The seed buffer holds width × height integers.

**[bin] v5.** v5 moved this setup into a helper that was not opened. The 4.04r2 allocation sizes and guards cannot be assumed for v5.

**[bin] `RANDOMSEEDS` boundary (v3, 4.04r2 and 4.20r6).**
- Columns stop below width, so that bound is exclusive.
- The row condition allows row = height, so that bound is inclusive.
- The buffer holds only width × height integers.

[inf] The row bound and the allocation do not match. This needs checking against the callers and the assembly. It is recorded as an open boundary. It is not a confirmed defect and not a safe rejection.

**[bin] 4.20r6.** One input helper either moves a collection across or processes the input directly. Who owns the data afterwards was not traced.

## A v3 height writer

[bin] A second body in shared v3 writes height data. It does the following:
- builds a `weblevels` cache path;
- builds buffers that hold `GWEBL001` and, depending on a condition, `GR-V1.03` or `GR-V1.04`;
- for a level with active heights, writes `HEIGHTS`, nine comma-separated rows of nine samples, then `HEIGHTSEND`;
- below a threshold it writes a literal zero, otherwise it formats the number.

[inf] This is a candidate serializer, not a confirmed one. The exact layout, the threshold and the final write to disk are not established. The wrapper encoding and whether the output reads back correctly are also unknown.

## 4.04r2 board header dispatch

[bin] An opened 4.04r2 routine chooses how to load a board from the file header.

**How it chooses.**
- It returns early for null input or when a global gate is set.
- Otherwise it reads eight header bytes into a local buffer and compares that string.
- `GLEVNW01` goes to its own handler.
- Any other header takes a common path. That path passes a numeric argument of 12, or 13 for `GR-V1.02` and `GR-V1.03`.
- More helpers run for `GR-V1.00` through `GR-V1.03`, and one more is added for versions 1.01 through 1.03.

**What is not shown.**
- There is no `GR-V1.04` comparison in this routine.
- An unknown header that is not `GLEVNW01` also takes the common path.

[inf] So these comparisons are not a whitelist of accepted versions, and they do not show that 1.04 files are rejected. The value 12 or 13 is not proven to be a tile bit width. Its meaning needs the helper that receives it. This routine chooses a path; it is not a decoder.

## Limits

- Not established: tokenizer rules, case handling, quoting, numeric conversion, constructor defaults and finalization.
- Not established: behaviour on malformed input, safety on hostile files, rendering, and whether a server accepts the data.
- The packaged tutorial gmap is documented in [the Windows note](gmap-heights-404r2.md#file-fixture). This note does not run any reader on it.

## Remaining work

- [ ] Positive control: an unchanged reader, reached naturally, returns successfully on a known-good map. Then vary only the height data in a one-cell map written for the test. Record storage and rendering separately.
- [ ] Validate the `RANDOMSEEDS` row bound against the callers and the assembly.
- [ ] Open the board helper that receives 12 or 13, and the `GLEVNW01` handler.

## Evidence

These are sanitized static summaries held by the researcher. They are registered in
[the evidence index](../docs/evidence-index.tsv). Raw exports and digests are
owner-held.

- `MAC-PPC-V3-GMAP-SCRIPT-20261109-R1`
- `MAC-PPC-404-GMAP-BOARD-20261109-R1`
- `MAC-PPC-420-GMAP-SCRIPT-20261109-R1`
- `MAC-PPC-V5-GMAP-GANI-20261109-R1` (its gmap part; the animation part is in
  [the v5 animation-group note](../client-internals/macos-v5-animation-group-lifecycle.md))
