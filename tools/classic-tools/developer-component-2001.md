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
selected writer and merge behavior of this executable remain unverified.
**[doc]** Evidence: `DEV-COMPONENT-DOC`.

Its thirteen colour rows include light green (181, 239, 189) for green trees or
forest, and dark red (196, 0, 0) for red trees. The red-tree row is absent from
the twelve-row December 2000 contract in
[`graal-level-gen.md`](graal-level-gen.md#what-the-operator-does). The help change
does not prove that the generator implements a distinct red-tree branch or
establish its tiles, stamps or colour tolerance. Preserve the older contract
when implementing the older build. **[doc]**

The embedded form declares a Generate World action, map-image and output-folder
controls, and an image chooser advertising PNG, MNG and GIF. MNG is an interface
declaration beyond the help's stated input formats; successful MNG decoding or
generation has not been established. Form resources identify a Delphi/VCL
interface, without establishing the compiler version or architecture of any main
client. **[bin]** Evidence: `DEV-COMPONENT-STATIC`.

## Limits and implementation use

- [ ] Trace the Generate World action through palette selection to the selected
  level writer; distinguish advertised input from decoded input and emitted data.
- [ ] Establish the red-tree mapping and output signature for this executable.
- [ ] Establish exact-build animation-editor format behavior. No movie grammar
  from a later editor is attributed to this component.

The package identity is useful when choosing version-specific evidence. The
generator help and interface are candidates for the image-to-world tool contract,
with the source grades above. They do not justify changing an existing generator
implementation or client wire profile without the missing behavior evidence.
