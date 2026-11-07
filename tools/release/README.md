# Document release build

`build_book.py` writes `release/0.0.1/` from the markdown notes in this
checkout. Standard library only. Install `pandoc`, a weasyprint binary on
`PATH` (pandoc's `--pdf-engine=weasyprint`), and `pdfinfo` (poppler).

From the repository root:

```
python3 tools/release/build_book.py
```

The script's pandoc invocation is:

```
pandoc INPUT.md -o OUTPUT.pdf \
  --pdf-engine=weasyprint \
  --css tools/release/book.css \
  --metadata title="TITLE" \
  --no-highlight \
  --resource-path=. \
  -f markdown-raw_html-smart-tex_math_dollars
```

`pdfinfo` measures each PDF. The script refuses a part over 100 pages and
writes the measured counts into `release/0.0.1/README.md`.
