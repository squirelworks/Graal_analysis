# Graal Analysis 0.0.1 — release steps for Chiaki

These commands have **not** been run on this branch:

```
git tag -a v0.0.1 -m "Graal_analysis 0.0.1"
git push origin v0.0.1
```

After the tag is on `main`, open a GitHub release for `v0.0.1` whose body
points readers at `release/0.0.1/README.md` for the PDF list and measured page
counts.

The notes viewer is **not** a separate download. After `git pull` of the tagged
source:

```
python3 tools/navigator/navigator.py
```

It serves on loopback port **8765**. No virtualenv is required.

Rebuild the PDFs from the repository root with:

```
python3 tools/release/build_book.py
```

That needs pandoc, weasyprint, and pdfinfo. It uses no extra Python packages.
The pandoc invocation is documented in `tools/release/README.md`.

## What is in the PDF set

Chapter PDFs follow the repository `README.md` contents list: how to read the
notes, formats, protocol, client internals and version profiles, Graal3D and
Torque, tools and labs, and an NPC scripting overview (not every raw script
body). Appendix PDFs hold recovered tools, game-asset inventories, server and
other indexes, and NPC script image names only.

The four troff format notes `formats/gani.txt`, `formats/glevnw01.txt`,
`formats/grmap001.txt`, and `formats/tiletypes.txt` are converted into the
formats chapter.

## Drive links omitted in the PDF text

These source notes still appear in the book, but every Google Drive URL and
**File ID** line in them is replaced with a placeholder in the PDF text:

- `ARCHIVAL.md`
- `archive/ember-avelan-experimental.md`
- `npc-library/archival-scripting-notes.md`

Ember-atlas footer lines in `server-notes/01-lineage.md`,
`server-notes/03-protocol.md`, and `server-notes/04-algorithms.md` are rendered
as plain text without markdown emphasis so pandoc can merge those notes safely.
