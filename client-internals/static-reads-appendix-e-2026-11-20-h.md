# Static reads for Appendix E, ninth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (the existing decompiler output of the Mac OS X 3.153 client,
`Graal.app`, PowerPC; no client run). Only behaviour is given here. Covers App. E#208.

## The 3.153 script container (E#208)

3.153 (February 2005, the first Torque-based client that handles `PLO_NPCBYTECODE`, 131) reads
compiled scripts in the **same four-segment container** as 4.2.0.8, 5.0.0.7 and 6.x (→ §8.4.2). It
does not read the OpenGS1 layout. 3.153 also has a routine that writes that container.

### The reader

- The body is a run of segments. Each segment is a 32-bit big-endian type and a 32-bit big-endian
  length, then that many bytes. The reader stops at the first type outside 1 to 4.
- **Type 1:** one 32-bit big-endian number, stored as the script's event mask. A segment shorter
  than 4 bytes gives 0.
- **Type 2:** the function table. Each entry is a 32-bit big-endian code position, then a name
  ending in a zero byte. A name starting with `public.` loses those seven characters and is marked
  public.
- **Type 3:** the string table, as zero-terminated strings one after another.
- **Type 4:** the instruction stream. Each byte is an opcode, except the operand markers. `F0`,
  `F1` and `F2` take a one-, two- or four-byte string-table index, and an index past the table is
  ignored. `F3`, `F4` and `F5` take a one-, two- or four-byte signed number. `F6` takes a number
  written as zero-terminated text. An operand fills in the instruction just before it.
- Two script-setting routines call the reader. One of them is the class path.

### The writer

3.153 also has the reverse routine, which turns a script held in memory into the same container:

- **Segment 1:** the event mask.
- **Segment 2:** each function's code position and name, with `public.` put back in front of
  public names. Joined-class entries go in as the class name, a dot and the function name.
- **Segment 3:** every string operand, each stored once.
- **Segment 4:** each instruction's opcode. A string operand is written as an `F0`, `F1` or `F2`
  index, using the smallest form that fits. A whole number is written as `F3`, `F4` or `F5`, again
  the smallest form that fits. Any other number is written as `F6` text.

Its caller was not traced, so this note does not say whether 3.153 compiles source or only
re-saves a script it received.

### What this settles

- OpenGS1's layout (a body offset, counted constant tables and 4-byte packed values, → §8.4.3)
  matches none of the official readers. That now includes 3.153 as well as 4.2.0.8, 5.0.0.7, 6.x
  and the 6.113 server bodies. OpenGS1 describes only itself.
- The four-segment container, its operand markers and the `public.` convention are already in place
  in 3.153. So they date from the first bytecode client, not from 4.x.

## Not covered

- The 3.153 opcode switch (the case set and the effects), and whether it has the folds 200 and up.
- What calls the writer.
