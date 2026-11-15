# The 2001 Windows developer component

The installer describes Developer `1.0.0-3` as a component alongside separate
Executable `2.0.3-0`, Main, Levels and Sounds components. The developer component
version therefore does not identify a main client executable version. The level
generator in this component declares executable version `1.0.0.0`. These are
embedded declarations, not authenticated release dates. **[doc][bin]**
Evidence: `DEV-COMPONENT-DOC`, `DEV-COMPONENT-STATIC` in
[`docs/evidence-index.tsv`](../../docs/evidence-index.tsv).

## Contents and purpose

Two container representations have the same eight regular-file payloads by
complete size and digest comparison. They contain an animation editor, an image
converter, NPC-programming documentation, and an image-to-level generator with
help and example images. Neither complete inventory contains a main client, RC
or NC executable. This establishes the component's tool-and-document composition;
it does not establish undocumented behavior of its programs. **[file]**

All three executables are Windows PE32 images for x86. Their complete standard
import tables contain no socket-library imports and have no delay-import entries.
Dynamic library loading is present, so this observation does not establish that
the programs never access a network. No runtime network behavior is established
by this reading. **[bin]** Evidence: `DEV-COMPONENT-STATIC`.

## Generator help and interface

The bundled help identifies its revision as 6 May 2001. It specifies GIF or
8-bit PNG input, with width and height each 64 times the desired level count.
It describes generating linked levels and an editor map, and reading existing
levels to add objects on a later pass. These are documentation claims; the
help alone does not establish the selected writer or merge behavior of this executable.
**[doc]** Evidence: `DEV-COMPONENT-DOC`.

Its thirteen colour rows include light green (181, 239, 189) for green trees or
forest, and dark red (196, 0, 0) for red trees. The red-tree row is absent from
the twelve-row December 2000 contract in
[`graal-level-gen.md`](graal-level-gen.md#what-the-operator-does). The help change
alone does not prove that the generator implements a distinct red-tree branch or
establish its tiles, stamps or colour tolerance. Preserve the older contract
when implementing the older build. **[doc]**

The embedded form declares a Generate World action, map-image and output-folder
controls, and an image chooser advertising PNG, MNG and GIF. MNG is an interface
declaration beyond the help's stated input formats; successful MNG decoding or
generation has not been established. Form resources identify a Delphi/VCL
interface, without establishing the compiler version or architecture of any main
client. **[bin]** Evidence: `DEV-COMPONENT-STATIC`.

## Selected static generation path

The form event and a four-entry published-method table agree on the Generate
World handler. Its selected instructions read three form fields, append a
backslash to one nonempty string value when needed, and call a generation
routine. This is a static action path, not an observed button press or successful
generation. **[bin]** Evidence: `DEV-GENERATOR-PATH-STATIC`.

The generation routine derives level counts from two loaded image dimensions
divided by 64. It calls the same colour-mask stage separately with the forest
selector and the red-tree selector. The mask stage calls a classifier with a
thirteen-entry colour table. Its forest entry is (181, 239, 189); its red-tree
entry is (196, 0, 0). The classifier sums the absolute differences in the three
colour channels and accepts totals strictly below 32. A negative pixel index is
rejected. This establishes a reachable red-tree colour-classification path;
the complete neighbor-to-stamp and tile mapping remains unresolved. **[bin]**
Evidence: `DEV-GENERATOR-PATH-STATIC`.

The selected initializer assigns constructed names ending in `.graal` to level
objects. The generation routine later enumerates those objects into a serializer.
That serializer branches on the `.nw` extension; its other branch writes the
eight-byte `GR-V1.03` signature to the supplied stream. Thus the generated-name
path selects the classic signature branch, subject to the level name remaining
unchanged. Existing-level loading and name preservation are not fully traced.
This distinguishes the selected writer from the other format strings in the
image; it does not establish successful file output or runtime acceptance.
**[bin]** Evidence: `DEV-GENERATOR-PATH-STATIC`.

These are selected instruction and data-flow reads, not a whole-program control
flow proof. Dynamic stream dispatch and unresolved helpers limit the reading.
Successful MNG loading remains unverified. The older twelve-colour build contract
is unchanged by this evidence about the developer component's generator.

A separate caller-seeded analysis of the generation routine corroborates its
dimension scaling and staged call order, including the two colour-mask calls.
The routine boundary was supplied from the independently validated direct call
and instruction body; it was not automatically discovered or recovered as an
original symbol. This analysis covers the generation routine, not the internal
classifier or serializer bodies read above. **[bin]** Evidence:
`DEV-GENERATOR-SEEDED-ROOT`.

That function body excludes an exception-handler region and contains one
unresolved indirect call. Its recovered call relationships are therefore partial.
Untruncated value-flow within the selected body does not establish cross-function
effects, exception behavior, successful image loading or native generation.
**[bin]** Evidence: `DEV-GENERATOR-SEEDED-ROOT`.

## Limits and implementation use

- [x] Trace the selected Generate World action to the colour classifier and
  serializer branch; [static path](#selected-static-generation-path).
- [ ] Establish the complete red-tree stamp/tile mapping and native output.
- [ ] Trace existing-level loading and name preservation, dynamic stream helpers,
  and successful MNG decoding before claiming those behaviors.
- [ ] Establish exact-build animation-editor format behavior. No movie grammar
  from a later editor is attributed to this component.

The package identity is useful when choosing version-specific evidence. The
generator help and interface are candidates for the image-to-world tool contract,
with the source grades above. They do not justify changing an existing generator
implementation or client wire profile without the missing behavior evidence.
