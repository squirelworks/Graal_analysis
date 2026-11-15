"""Generate public token views from the sole canonical Markdown catalogue.

Usage: python tools/token-map/generate.py [--check]
No binary inputs, external packages or network access are used.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "client-internals/version-token-catalogue.md"
MAP = ROOT / "VERSION-TOKENS.md"
DATA = ROOT / "version-profiles/version-token-map.tsv"
CONFIDENCE = {
    "W": "captured in the cited context; not feature or stockness proof",
    "B": "static recovery in the cited exact-association scope",
    "B+": "static recovery plus accepted lab login; frame not decoded",
    "L": "server/table/report evidence in its cited scope",
    "S": "connector supplied; not a permanent per-build token",
    "C": "script constant in its cited scope",
    "U": "unresolved; not proof that networking or a token is absent",
    "-": "documented no-token family; not an unresolved scan",
}
HEADER = ["Build", "Token", "Grade", "Source", "Platform", "Role", "Repro", "Repro label"]
ORDER = "WBLSUC"
SOURCE_ITEM = re.compile(r"^\[(W|B\+?|L|S|U|C|-)@([a-z][a-z0-9-]*)(?:~([a-z][a-z0-9-]*)|(!conflict))?\] (.+)$")


def evidence_sources(text: str) -> list[dict[str, str]]:
    """Named citations preserve dependencies without counting copies as confirmation."""
    result = []
    for item in text.split("<br>"):
        match = SOURCE_ITEM.fullmatch(item.strip())
        if not match:
            raise ValueError("source must use [category@id] citation records")
        category, source_id, parent, conflict, citation = match.groups()
        result.append(dict(id=source_id, category=category, citation=citation,
                           depends_on=parent or "", status="conflict" if conflict else "support"))
    by_id = {item["id"]: item for item in result}
    if len(by_id) != len(result):
        raise ValueError("duplicate source id")
    for item in result:
        visited = {item["id"]}
        current = item
        while current["depends_on"]:
            parent = current["depends_on"]
            if parent not in by_id or parent in visited:
                raise ValueError("missing or cyclic source dependency")
            visited.add(parent)
            ancestor = by_id[parent]
            if current["category"] != ancestor["category"] or ancestor["status"] != "support":
                raise ValueError("dependent source cannot create a category or depend on a conflict")
            current = ancestor
    if not any(item["status"] == "support" for item in result):
        raise ValueError("association needs supporting evidence")
    return result


def signature(sources: list[dict[str, str]]) -> str:
    categories = {item["category"] for item in sources if item["status"] == "support"}
    if "-" in categories:
        if categories != {"-"}:
            raise ValueError("documented no-token cannot mix with token evidence")
        return "-"
    if "U" in categories and len(categories) > 1:
        if any("scope:" not in item["citation"].lower() for item in sources
               if item["category"] == "U" and item["status"] == "support"):
            raise ValueError("mixed unresolved evidence requires an explicit scope:")
    return "".join("B+" if c == "B" and "B+" in categories else c
                   for c in ORDER if c in categories or c == "B" and "B+" in categories)


def primary_grade(sources: list[dict[str, str]]) -> str:
    sig = signature(sources)
    if sig == "-":
        return "-"
    return next("B+" if c == "B" and "B+" in sig else c for c in ORDER if c in sig)


def anchor(text: str) -> str:
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


def parse(text: str) -> list[dict[str, str]]:
    records = []
    family = ""
    active = False
    seen = set()
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("##"):
            active = False
        if line.startswith("### "):
            family = line[4:]
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells == HEADER:
            active = True
            continue
        if not active or all(re.fullmatch(r"[-:]+", c) for c in cells):
            continue
        if len(cells) != 8:
            raise ValueError(f"catalogue line {number}: expected eight columns")
        build, raw_token, evidence, details, platform, role, _, _ = cells
        plain = raw_token.strip("`")
        state = "none" if plain == "none" else "unresolved" if plain == "unknown" else "known"
        token = plain if state == "known" else ""
        if token and (not token.isascii() or any(c.isspace() or c == "`" for c in token)):
            raise ValueError(f"catalogue line {number}: token must be one exact ASCII value")
        sources = evidence_sources(details)
        combined = signature(sources)
        grade = primary_grade(sources)
        if evidence != combined or not all((family, build, platform, role, details)):
            raise ValueError(f"catalogue line {number}: noncanonical signature or missing metadata")
        if state == "none" and combined != "-" or state == "unresolved" and "U" not in combined or state == "known" and combined == "-":
            raise ValueError(f"catalogue line {number}: unknown/none grade mismatch")
        key = (token, state, build, platform, role)
        if key in seen:
            raise ValueError(f"catalogue line {number}: duplicate association {key}")
        seen.add(key)
        records.append(dict(token=token, state=state, build=build, platform=platform,
                            role=role, family=family, evidence=evidence, grade=grade,
                            confidence="; ".join(CONFIDENCE[c] for c in re.findall(r"B\+|[WBLSUC-]", combined)),
                            source_records=json.dumps(sources, ensure_ascii=False, sort_keys=True),
                            source="client-internals/version-token-catalogue.md#" + anchor(family),
                            source_details=details))
    if not records:
        raise ValueError("no canonical rows found")
    return records


def root_links(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        if "://" in target or target.startswith("#"):
            return match.group(0)
        path, sep, fragment = target.partition("#")
        resolved = (SOURCE.parent / path).resolve()
        relative = resolved.relative_to(ROOT).as_posix()
        return f"[{label}]({relative}{sep}{fragment})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, text)


def render(records: list[dict[str, str]]) -> tuple[str, str]:
    unique = {r["token"] for r in records if r["state"] == "known"}
    groups = [
        ("Recovered or captured login associations", lambda r: r["state"] == "known" and r["grade"] not in {"L", "C"} and r["role"] in {"game-login", "rc-login", "nc-login", "list-login", "connector-game-login"}),
        ("Reported and server-recognized associations", lambda r: r["state"] == "known" and r["grade"] == "L"),
        ("Services, script constants and non-login identifiers", lambda r: r["state"] == "known" and (r["grade"] == "C" or r["role"] not in {"game-login", "rc-login", "nc-login", "list-login", "connector-game-login"}) and r["grade"] != "L"),
        ("Unresolved and documented no-token families", lambda r: r["state"] != "known"),
    ]
    out = ["# Version token map", "", "Coverage audited: **2026-11-15**. Generated from the [canonical catalogue](client-internals/version-token-catalogue.md); edit that source, then run `python tools/token-map/generate.py`. [Download the generated TSV](version-profiles/version-token-map.tsv).", "",
           f"**{len(records)} associations; {len(unique)} distinct known identifier values**, including service and non-login roles. This is known evidence across the published source set, not every historical build or completion of the research intake.", "",
           "**A token is not a unique client identifier.** Search the exact, case-sensitive bytes below and retain every build/platform/role association. A wire capture of one sibling does not upgrade the others. No token grants a feature profile or authenticates an unmodified release.", "",
           "Evidence signatures retain all supporting categories in **W B L S U C** order: **W** captured wire context; **B** static recovery; **L** server/table/report; **S** connector supplied; **U** explicitly unresolved scope; **C** script constant. **B+** remains one qualified B category (accepted lab login, frame not decoded), so **WB+L** is unambiguous. **-** means documented no token, never unknown. Source records/citations remain separate; copies and conflicts do not add supporting categories or promote siblings.", "",
           "Desktop/Mac/Linux/game, iOS, Graal3D, RC/NC and server-recognition sources are included; Android token coverage is explicitly unresolved. iOS: 27 packages / 26 unique executables, 23 token-bearing; no mobile wire capture is claimed. Shared package copies are not independent corroboration. The Worlds production game-login value remains unestablished despite known HTTP identification.", "",
           "## Find a token", ""]
    out += [f"- [{name}](#{anchor(name)})" for name, _ in groups]
    emitted = []
    for name, predicate in groups:
        selected = sorted((r for r in records if predicate(r)), key=lambda r: (r["token"], r["role"], r["build"]))
        emitted.extend(id(r) for r in selected)
        out += ["", f"## {name}", "", "| Exact value | Build / aliases | Platform · role | Evidence | Source and limits |", "|---|---|---|---|---|"]
        for r in selected:
            value = f'`{r["token"]}`' if r["token"] else r["state"]
            source = f'[Catalogue: {r["family"]}]({r["source"]}); ' + root_links(r["source_details"])
            out.append(f'| {value} | {r["build"]} | {r["platform"]} · {r["role"]} | {r["evidence"]} | {source} |')
    if Counter(emitted) != Counter(id(r) for r in records):
        raise ValueError("view groups must include every association exactly once")
    out += ["", "## Coverage and unresolved questions", "",
            "Known-only server labels remain separate from inspected clients. Do not assign `G3D29090` to encrypted Era+ 1.0 or `G3D2504D` to Belote 1.50 (whose recovered value is `G3D04048`). Alien Abuse 1.0/1.1 remain unresolved, not proven offline. A genuine 2.3 input and several list-only desktop builds remain missing.", "",
            "The legacy `newmain` and `graal2002` list identifiers are not game tokens. `GSERVL01`/`GLEVNW01` are level magics; `NW01`/`NW51` scan hits and stored lowercase `g3d…` intermediates are not alternate login values. The login builder uppercases the latter. No date, folder label or negative string search creates a token.", "",
            "Core's generated registry is a downstream, token-level consumer: it cannot represent every per-association role/grade and omits some reported/tool entries. Its support list is not feature evidence. See the [source catalogue's open points](client-internals/version-token-catalogue.md#open-points) and [generation/check instructions](tools/token-map/README.md).", ""]
    fields = ["token", "state", "build", "platform", "role", "family", "evidence", "confidence", "source", "source_details", "source_records"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(dict(r, source_details=root_links(r["source_details"]),
                         source_records=json.dumps([dict(item, citation=root_links(item["citation"]))
                                                    for item in json.loads(r["source_records"])],
                                                   ensure_ascii=False, sort_keys=True)) for r in records)
    return "\n".join(out), stream.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    records = parse(SOURCE.read_text(encoding="utf-8"))
    stale = []
    for path, content in zip((MAP, DATA), render(records)):
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("stale token views: " + ", ".join(stale))
    print(f"token map {'checked' if args.check else 'generated'}: {len(records)} associations")


if __name__ == "__main__":
    main()
