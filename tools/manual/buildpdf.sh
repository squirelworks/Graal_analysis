#!/bin/bash
# Build the Technical Reference Manual as one PDF.
# usage: tools/manual/buildpdf.sh <repo-root> <out.pdf>
# needs: pandoc, node with the playwright package and its Chromium.
set -euo pipefail
R=$(cd "$1" && pwd); OUT=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
cd "$R/manual"
FILES="00-conventions.md 01-builds.md $(ls 02-protocol/*.md) $(ls 03-formats/*.md) $(ls 04-behaviour/*.md) 05-servers.md 06-listserver.md 07-rc-nc.md $(ls 08-scripting/*.md) 09-graal3d.md 10-torque.md 11-tools.md $(ls app-*.md)"
for f in $FILES; do sed '/^<!-- manual:/d' "$f"; printf '\n\n'; done > $W/all.md
cat > $W/style.css <<'CSS'
body{font-family:"DejaVu Sans",sans-serif;font-size:9pt;line-height:1.35;max-width:none;margin:0}
h1{page-break-before:always;font-size:18pt;border-bottom:2px solid #333}
h2{font-size:13pt;margin-top:1.4em} h3{font-size:11pt} h4{font-size:10pt}
table{border-collapse:collapse;width:100%;margin:.5em 0;font-size:8pt;page-break-inside:auto}
th,td{border:1px solid #999;padding:2px 4px;vertical-align:top;word-break:break-word}
th{background:#eee} tr{page-break-inside:avoid}
code{font-family:"DejaVu Sans Mono",monospace;font-size:8pt;background:#f4f4f4}
pre{background:#f4f4f4;padding:4px;font-size:8pt;white-space:pre-wrap}
#TOC{page-break-after:always} #TOC ul{list-style:none;padding-left:1em}
CSS
SHA=$(git -C "$R" rev-parse --short HEAD)
pandoc $W/all.md -f gfm -t html5 -s --toc --toc-depth=2 --metadata title="Graal Technical Reference Manual" --metadata subtitle="build of $SHA" -c $W/style.css --embed-resources -o $W/trm.html
node -e "
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://$W/trm.html');await p.pdf({path:'$OUT',format:'A4',margin:{top:'14mm',bottom:'14mm',left:'12mm',right:'12mm'},displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style=\"font-size:7pt;width:100%;text-align:center\"><span class=pageNumber></span> / <span class=totalPages></span></div>'});await b.close();})();"
echo "built $OUT from $SHA"
