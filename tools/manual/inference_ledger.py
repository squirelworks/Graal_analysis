#!/usr/bin/env python3
"""List the manual's table rows that rest on inference alone.

    python tools/manual/inference_ledger.py          # rewrite the ledger
    python tools/manual/inference_ledger.py --check  # fail if it is stale

A row counts when its last cell (the source column) carries `[inf]` and no
stronger tag: no `[bin]`, `[cap]`, `[live]`, `[lab]`, `[wire]`, `[src]`,
`[shot]`, `[doc]`, `[file]`, `[srv]` and no build tag such as `[2.05]`.
Those are the claims a reader can't check against an artifact. The ledger
is `manual/inference-ledger.tsv`: one row per claim, with the manual file,
the row's first cell, the cited notes, and the row's text, so that each
one can be settled by a read or a lab run, or kept as a labelled guess.
Appendix E (open questions) is left out; its rows are open by design.
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MANUAL = ROOT / "manual"
OUT = MANUAL / "inference-ledger.tsv"
SKIP = {"app-e-open-questions.md"}
TAG = re.compile(r"\[([^\]\s]+)\]")
STRONG = {"bin", "cap", "live", "lab", "wire", "src", "shot", "doc", "file", "srv", "test", "checked"}
BUILD = re.compile(r"^\d+(\.\d+)+")
CITE = re.compile(r"\(([\w./#-]+\.md[\w#-]*)\)")


def tags(cell):
    out = set()
    for t in TAG.findall(cell):
        for part in t.split("]["):
            out.add(part)
    return out


def rows():
    for path in sorted(MANUAL.rglob("*.md")):
        if path.name in SKIP:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if not (s.startswith("|") and s.endswith("|")) or set(s) <= set("|-: "):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 2:
                continue
            src = cells[-1]
            t = tags(src)
            if "inf" not in t:
                continue
            if t & STRONG or any(BUILD.match(x) for x in t):
                continue
            key = re.sub(r"\s+", " ", cells[0])[:80]
            text = re.sub(r"\s+", " ", " | ".join(cells[1:-1]))[:240]
            cites = ", ".join(dict.fromkeys(CITE.findall(src)))
            yield rel, key, cites, text


def render():
    lines = ["file\trow\tcited\ttext"]
    for r in rows():
        lines.append("\t".join(x.replace("\t", " ") for x in r))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = render()
    if a.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("manual/inference-ledger.tsv is stale: run tools/manual/inference_ledger.py")
            return 1
        print(f"inference ledger up to date ({text.count(chr(10)) - 1} rows)")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({text.count(chr(10)) - 1} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
