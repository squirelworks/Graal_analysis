# Graal Analysis 0.0.2 — release steps for Chiaki

These commands have **not** been run:

```
git tag -a v0.0.2 -m "Graal_analysis 0.0.2"
git push origin v0.0.2
```

After the tag is on `main`, open a GitHub release for `v0.0.2` whose body
points readers at `book/0.0.2/README.md` for the PDF list and measured page
counts.

The notes viewer is already on `main`. It is not a separate download. From a
checkout of the tagged source:

```
python3 tools/navigator/navigator.py
```

It serves on loopback port **8765**. No virtualenv is required.

The 0.0.1 PDF stitch in `release/0.0.1/` was not rebuilt and was not replaced.

Rebuild one chapter PDF from the repository root with pandoc and weasyprint.
`pdfinfo` measures the result. A file over 100 pages is split into parts and
measured again.

```
pandoc docs/book/01-a-level-and-a-session.md \
  -o book/0.0.2/01-a-level-and-a-session.pdf \
  --pdf-engine=weasyprint \
  --css tools/release/book.css \
  --metadata title="A level and a session" \
  --no-highlight \
  --resource-path=. \
  -f markdown-raw_html-smart-tex_math_dollars
```
