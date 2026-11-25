# Graal 5.12 `.ft` tree shapes (procedural trees)

Date: 2026-11-25. Client: the real 5.12 `Graal3DEngine.dll` (SHA-256 `04f7a133…`), static read.
Tags as in `README.md`: **[bin]** read from that binary for behaviour, **[inf]** inferred,
**[lab]** seen live (none yet). Nothing here is decompiled text.

A `GameObject` whose shape file name ends in `.ft` gets a `GameShapeFT`: a tree grown at load time
from a small text grammar (an L-system), not a mesh. The other shape kinds are picked the same way
by extension: `.3ds`, `.dts` and `.dif`. **[bin]**

## Object properties

`GameShapeFT` adds two properties to the shape **[bin]**:

| Property | Meaning |
|---|---|
| `seed` | the random seed for growing the tree. Default when never set: a fixed built-in seed, so every tree from the same file looks the same. |
| `levels` | how many rewriting rounds to run, clamped to 1–15. Unset (0) uses the file's `defaultLevels`. |

Setting either one on an object that is already shown regrows it. Grown trees are cached by
(file, seed, levels), and the parsed file by name; the file is re-read when it changes on disk.
**[bin]** How a script or the server reaches these two properties on a `GameObject`'s shape is not
yet tested. **[inf]**

## File format

Plain text, read line by line (lines up to 127 characters). Blank lines and lines starting with
`//` are skipped, and `//` later on a line ends it. A line is split into words at spaces and tabs;
`"…"` keeps spaces inside one word. A line that is only `{` opens a block and a line that is only
`}` closes it; unknown blocks are skipped whole. **[bin]**

Top-level lines:

| Line | Meaning |
|---|---|
| `width <w0> <w1>` | the starting branch widths (the two ends of the trunk) |
| `length <l>` | the starting segment length |
| `defaultLevels <n>` | rounds to run when the object sets no `levels` |
| `billboard <name>` | a texture name for the far-away stand-in |
| `billboardsize <w> <h>` | the stand-in's size |
| `gramma` + block | the rewriting rules (spelled `gramma` in the file, not `grammar`) |
| `term <c> <type>` + optional block | what the one-character symbol `c` does when drawn |
| `texture <slot> <name>` + block | texture slot 0–7: a name, then a block of up to 4 rows of up to 8 numbers |

**[bin]** The client's own bounding size for a tree is half of `w0 + w1`, but never under 1.5.
**[bin]**

### `gramma` block

Each line is either `<c> <replacement>` (weight 1) or `<c> <weight> <replacement>`. Several lines
for the same symbol share its chance in proportion to their weights. The very first rule's symbol
is the starting string. **[bin]**

Growing: each round walks the current string. A symbol that has rules is replaced by one rule
picked at random by weight. A symbol with no rules is kept only if it has a `term`; any other
character is dropped. If the string grows past 512 characters it is cut to 512 and growing
stops. **[bin]**

### `term` types

| Type | Effect when drawn |
|---|---|
| `push` | save the current position, direction, length and widths |
| `pop` | restore the last saved state |
| `branch` | draw a segment with the branch texture and move to its end |
| `move` | move forward without drawing |
| `leaf` | draw a leaf |
| `rotate` | turn relative to the current direction |
| `absrotate` | turn to an absolute direction |
| `resize` | change length and widths without drawing or moving |

**[bin]**

Term block lines, all optional **[bin]**:

| Line | Meaning |
|---|---|
| `nobranch` | leaf flag (a leaf without its stalk) **[inf]** |
| `texBranch <n>`, `texLeaf <n>` | texture slot numbers |
| `coordLeaf <n>` | which texture-coordinate row a leaf uses **[inf]** |
| `size <s>` | scale for this term, clamped to 0.1–100 (default 1) |
| `widthRatio <r>` | width multiplier after this term (default 1) |
| `lengthRatio <r>` or `lengthRatio <min> <max>` | length multiplier, picked at random in the range |
| `yaw <a>` or `yaw <min> <max>` | turn angle in degrees, random in the range (also the leaf's angle) |
| `pitch <a>` or `pitch <min> <max>` | tilt angle in degrees, random in the range |

## A minimal file for a lab

Made up for testing, not taken from any game file:

```
// lab tree
width 0.4 0.3
length 2
defaultLevels 4
gramma
{
  A B[RA][LA]
  A 2 B[RA]
}
term B branch
{
  texBranch 0
  lengthRatio 0.7 0.9
  widthRatio 0.7
}
term [ push
term ] pop
term R rotate
{
  yaw 20 40
  pitch 25
}
term L rotate
{
  yaw -40 -20
  pitch 25
}
texture 0 bark.png
{
}
```

Open: a live run (render, `seed` and `levels` effects, texture rows) is queued for the lab Windows VM.
