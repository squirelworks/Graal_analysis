#!/usr/bin/env python3
"""The 3D client conformance suite: load cases, build their worlds, judge runs.

A case (torque/conformance/cases/*.toml) is one small world plus, where it
needs one, one GS2 probe script, the checks that read the run's artefacts,
and the expected value of every check for every client build. The board row
each expectation comes from is named in the case, so a failing case points
at the board, and an observed value ("?" expectations) feeds the board.

    conformance.py list                      cases, rows and builds
    conformance.py expected [--write]        the expected-results table (torque/conformance/EXPECTED.md)
    conformance.py build OUT [--case ID,..]  one world overlay per case (content generated, nothing copied)
    conformance.py judge RUNDIR CASE BUILD   verdict of one collected run (JSON on stdout)
    conformance.py table RESULTS.tsv [--write]  the derived results table (torque/conformance/RESULTS.md)

Run artefacts (what run.py collects into RUNDIR, and what `judge` reads):

    gserver.log   the seihai-gserver's stdout/stderr (run with --verbose)
    g3d.tsv       its graal3d_trace file
    console.txt   the client's console log(s), concatenated
    files.txt     a listing of the client folder after the run
    tasks.txt     the guest's process list just before the client is closed
    shot.ppm      the last screenshot (QMP screendump, binary PPM)

Python 3.11+ standard library only (tomllib).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SUITE = REPO / "torque" / "conformance"
CASES = SUITE / "cases"
SCRIPTS = SUITE / "scripts"
BOARD = REPO / "torque" / "3d-capability-board.tsv"

sys.path.insert(0, str(HERE))
import gen_content  # noqa: E402

# The five builds the suite is written for, in table order. A case may name
# others (e.g. "4.20r6L", the Linux 4.20 G3D22126); they get their own column.
CORE_BUILDS = ["3.153", "4.04r2", "4.20r8", "5.12", "6.037"]
CHECK_KINDS = {"trace", "server", "console", "files", "alive", "probe", "pixel", "blobs"}
# Expected value of a check: true, false, or "?" (observe and record only).
OBSERVE = "?"
PROBE_WEAPON = "ConfProbe"


@dataclass
class Check:
    id: str
    kind: str
    pattern: str = ""
    key: str = ""          # probe: the cf key
    value: str = ""        # probe: regex the reported value must match
    colour: tuple = ()     # pixel: RGB
    tol: int = 40          # pixel: per-channel tolerance
    min_fraction: float = 0.0
    min_pixels: int = 40   # blobs: the smallest region that counts (in sampled pixels)
    count: int = 1         # blobs: at least this many separate regions
    client: int = 1        # which client's artefacts (2: the second client of a two-client case)
    note: str = ""


@dataclass
class Case:
    id: str
    slug: str
    title: str
    rows: list[str]
    priority: int
    world: str
    files: list[str]
    scripts: list[str]
    server_options: list[str]
    server_flags: list[str]
    lobby_name: str
    seconds: int
    mid_action: str
    needs: list[str]
    terrain: list[str]
    derive: list[dict]
    clients: int
    checks: list[Check]
    expect: dict[str, dict]          # build -> {check id: True/False/"?", "source": str, "note": str}
    path: Path = field(default=Path())

    def builds(self) -> list[str]:
        extra = sorted(b for b in self.expect if b not in CORE_BUILDS)
        return [b for b in CORE_BUILDS if b in self.expect] + extra


class CaseError(ValueError):
    pass


def board_ids() -> set[str]:
    with BOARD.open(encoding="utf-8") as f:
        return {r["id"] for r in csv.DictReader(f, delimiter="\t")}


def load_case(path: Path) -> Case:
    d = tomllib.loads(path.read_text(encoding="utf-8"))
    try:
        checks = []
        for c in d.get("check", []):
            if c["kind"] not in CHECK_KINDS:
                raise CaseError(f"{path.name}: check {c['id']}: unknown kind {c['kind']}")
            checks.append(Check(
                id=c["id"], kind=c["kind"], pattern=c.get("pattern", ""),
                key=c.get("key", ""), value=c.get("value", ".*"),
                colour=tuple(c.get("colour", ())), tol=int(c.get("tol", 40)),
                min_fraction=float(c.get("min_fraction", 0.0)), note=c.get("note", ""),
                min_pixels=int(c.get("min_pixels", 40)), count=int(c.get("count", 1)),
                client=int(c.get("client", 1))))
        ids = [c.id for c in checks]
        if len(ids) != len(set(ids)):
            raise CaseError(f"{path.name}: duplicate check id")
        expect = {}
        for build, e in d.get("expect", {}).items():
            vals = {}
            for k, v in e.items():
                if k in ("source", "note"):
                    vals[k] = v
                    continue
                if k not in ids:
                    raise CaseError(f"{path.name}: expect.{build}: no check {k}")
                if v not in (True, False, OBSERVE):
                    raise CaseError(f"{path.name}: expect.{build}.{k}: true, false or \"?\"")
                vals[k] = v
            if "source" not in vals:
                raise CaseError(f"{path.name}: expect.{build}: no source")
            expect[build] = vals
        w = d.get("world", {})
        s = d.get("server", {})
        r = d.get("run", {})
        case = Case(
            id=d["id"], slug=d["slug"], title=d["title"], rows=list(d["rows"]),
            priority=int(d.get("priority", 2)), world=w.get("lines", ""),
            files=list(w.get("files", [])), scripts=list(w.get("scripts", [])),
            server_options=list(s.get("options", [])), server_flags=list(s.get("flags", [])),
            lobby_name=s.get("lobby_name", "3 Conformance"), seconds=int(r.get("seconds", 60)),
            mid_action=r.get("mid_action", ""), needs=list(d.get("needs", [])),
            terrain=list(w.get("terrain", [])), derive=list(w.get("derive", [])),
            clients=int(r.get("clients", 1)),
            checks=checks, expect=expect, path=path)
    except KeyError as e:
        raise CaseError(f"{path.name}: missing {e}") from None
    for dv in case.derive:
        if set(dv) != {"pack", "pick", "out", "version"} or dv["pack"] not in case.needs:
            raise CaseError(f"{path.name}: derive: pack (one of needs), pick, out, version")
    if case.clients not in (1, 2):
        raise CaseError(f"{path.name}: run.clients: 1 or 2")
    for c in case.checks:
        if c.client > case.clients:
            raise CaseError(f"{path.name}: check {c.id}: client {c.client} of {case.clients}")
    if case.mid_action not in ("", "stop-server"):
        raise CaseError(f"{path.name}: run.mid_action: '' or stop-server")
    return case


def load_cases(only: set[str] | None = None) -> list[Case]:
    cases = [load_case(p) for p in sorted(CASES.glob("*.toml"))]
    seen = set()
    for c in cases:
        if c.id in seen:
            raise CaseError(f"duplicate case id {c.id}")
        seen.add(c.id)
    if only:
        cases = [c for c in cases if c.id in only or c.slug in only]
    return cases


# ------------------------------------------------------------------ worlds

def build_world(case: Case, out: Path, packs: dict[str, Path] | None = None) -> Path:
    """Write the case's world overlay under out/<id>/: config/graal3dworld.txt,
    config/server.add (lines appended to the base world's server.txt),
    config/serverflags.txt, files/<content> and conf/<scripts>. The runner
    copies it over the lab's base world."""
    root = out / case.id
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "files").mkdir(exist_ok=True)
    world = case.world.strip() + "\n"
    for s in case.scripts:
        world += f"weapon3d {PROBE_WEAPON} conf/{s}\n"
    (root / "config" / "graal3dworld.txt").write_text(world, encoding="utf-8")
    opts = ["graal3d = true", "graal3d_trace = g3d.tsv", f"name = {case.lobby_name}"]
    (root / "config" / "server.add").write_text("\n".join(opts + case.server_options) + "\n", encoding="utf-8")
    if case.server_flags:
        (root / "config" / "serverflags.txt").write_text("\n".join(case.server_flags) + "\n", encoding="utf-8")
    content = gen_content.files()
    for name in case.files:
        matches = [n for n in content if re.fullmatch(name.replace(".", r"\.").replace("*", ".*"), n)]
        if not matches:
            raise CaseError(f"{case.id}: no generated file matches {name}")
        for n in matches:
            (root / "files" / n).write_bytes(content[n])
    for folder in case.terrain:
        for rel, data in gen_content.flat_terrain(folder).items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(data)
    for dv in case.derive:
        pack = (packs or {}).get(dv["pack"])
        if pack is None:
            raise CaseError(f"{case.id}: needs content pack {dv['pack']} (lab config [packs])")
        found = sorted(Path(pack).glob(dv["pick"]))
        if not found:
            raise CaseError(f"{case.id}: pack {dv['pack']} has no {dv['pick']}")
        (root / "files" / dv["out"]).write_bytes(
            gen_content.set_version(found[0].read_bytes(), int(dv["version"]), dv["out"]))
    if case.scripts:
        (root / "conf").mkdir(exist_ok=True)
        for s in case.scripts:
            (root / "conf" / s).write_bytes((SCRIPTS / s).read_bytes())
    meta = {"id": case.id, "slug": case.slug, "title": case.title, "rows": case.rows,
            "seconds": case.seconds, "mid_action": case.mid_action, "needs": case.needs,
            "lobby_name": case.lobby_name, "clients": case.clients}
    (root / "CASE.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return root


# ------------------------------------------------------------------ judging

def read_ppm(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    parts = []
    i = 0
    while len(parts) < 4:
        while data[i:i + 1].isspace():
            i += 1
        if data[i:i + 1] == b"#":
            i = data.index(b"\n", i) + 1
            continue
        j = i
        while not data[j:j + 1].isspace():
            j += 1
        parts.append(data[i:j])
        i = j
    if parts[0] != b"P6" or int(parts[3]) != 255:
        raise ValueError("not an 8-bit binary PPM")
    w, h = int(parts[1]), int(parts[2])
    pix = data[i + 1:i + 1 + w * h * 3]
    if len(pix) != w * h * 3:
        raise ValueError("short PPM")
    return w, h, pix


def colour_fraction(path: Path, rgb: tuple, tol: int) -> float:
    w, h, pix = read_ppm(path)
    r0, g0, b0 = rgb
    hit = 0
    n = 0
    # Every second pixel of every second row is plenty for a solid colour.
    for y in range(0, h, 2):
        row = y * w * 3
        for x in range(0, w * 3, 6):
            r, g, b = pix[row + x], pix[row + x + 1], pix[row + x + 2]
            n += 1
            if abs(r - r0) <= tol and abs(g - g0) <= tol and abs(b - b0) <= tol:
                hit += 1
    return hit / n if n else 0.0


def _read(rundir: Path, name: str) -> str | None:
    p = rundir / name
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def probe_values(server_log: str, key: str) -> list[str]:
    pat = re.compile(r"trigger ignored \(\"?gui\"?,\s*\"?" + PROBE_WEAPON + r"\"?,\s*\"?cf\"?,\s*\"?"
                     + re.escape(key) + r"\"?,\s*\"?([^,)\"]*)")
    return pat.findall(server_log)


def colour_blobs(path: Path, rgb: tuple, tol: int, min_pixels: int) -> list[int]:
    """Sizes of the separate regions of a colour (4-connected, on every second
    pixel of every second row), largest first, ignoring regions under min_pixels."""
    w, h, pix = read_ppm(path)
    sw, sh = (w + 1) // 2, (h + 1) // 2
    r0, g0, b0 = rgb
    hit = bytearray(sw * sh)
    for y in range(sh):
        for x in range(sw):
            i = ((2 * y) * w + 2 * x) * 3
            if abs(pix[i] - r0) <= tol and abs(pix[i + 1] - g0) <= tol and abs(pix[i + 2] - b0) <= tol:
                hit[y * sw + x] = 1
    sizes = []
    for start in range(sw * sh):
        if hit[start] != 1:
            continue
        hit[start] = 2
        stack, n = [start], 0
        while stack:
            k = stack.pop()
            n += 1
            y, x = divmod(k, sw)
            for nk, ok in ((k - 1, x > 0), (k + 1, x < sw - 1), (k - sw, y > 0), (k + sw, y < sh - 1)):
                if ok and hit[nk] == 1:
                    hit[nk] = 2
                    stack.append(nk)
        if n >= min_pixels:
            sizes.append(n)
    return sorted(sizes, reverse=True)


def observe(check: Check, rundir: Path, exe: str = "") -> tuple[bool | None, str]:
    """(value, detail). None: the artefact the check reads is missing."""
    if check.client == 2 and check.kind in ("console", "files", "alive", "pixel", "blobs"):
        rundir = rundir / "c2"   # the server log and trace are shared
    if check.kind == "blobs":
        shot = rundir / "shot.ppm"
        if not shot.exists():
            return None, "no screenshot"
        sizes = colour_blobs(shot, check.colour, check.tol, check.min_pixels)
        return len(sizes) >= check.count, f"{len(sizes)} regions of {check.colour} (sizes {sizes[:6]})"
    if check.kind == "pixel":
        shot = rundir / "shot.ppm"
        if not shot.exists():
            return None, "no screenshot"
        f = colour_fraction(shot, check.colour, check.tol)
        return f >= check.min_fraction, f"{f:.4f} of the screen within {check.tol} of {check.colour}"
    if check.kind == "alive":
        tasks = _read(rundir, "tasks.txt")
        if tasks is None:
            return None, "no process list"
        name = check.pattern or exe
        if not name:
            return None, "no client exe name"
        ok = re.search(re.escape(name), tasks, re.I) is not None
        return ok, f"{name} {'running' if ok else 'not running'} at the end"
    src = {"trace": "g3d.tsv", "server": "gserver.log", "probe": "gserver.log",
           "console": "console.txt", "files": "files.txt"}[check.kind]
    text = _read(rundir, src)
    if text is None:
        # No trace file at all means the server never traced a link.
        if check.kind == "trace" and _read(rundir, "gserver.log") is not None:
            text = ""
        else:
            return None, f"no {src}"
    if check.kind == "probe":
        vals = probe_values(text, check.key)
        if not vals:
            return False, f"probe {check.key}: no report"
        ok = any(re.fullmatch(check.value, v) for v in vals)
        return ok, f"probe {check.key} = {','.join(vals[:4])}"
    m = re.search(check.pattern, text, re.M)
    return m is not None, (f"matched: {m.group(0)[:80]!r}" if m else f"no match for {check.pattern!r}")


def judge(case: Case, build: str, rundir: Path, exe: str = "") -> dict:
    exp = case.expect.get(build)
    if exp is None:
        return {"case": case.id, "build": build, "verdict": "n/a", "checks": {}}
    out = {"case": case.id, "build": build, "checks": {}}
    mismatches = []
    missing = []
    for c in case.checks:
        want = exp.get(c.id, OBSERVE)
        got, detail = observe(c, rundir, exe)
        out["checks"][c.id] = {"expected": want, "observed": got, "detail": detail}
        if got is None:
            if want != OBSERVE:
                missing.append(c.id)
        elif want != OBSERVE and got != want:
            mismatches.append(c.id)
    if mismatches:
        out["verdict"] = "FAIL"
    elif missing:
        out["verdict"] = "ERROR"
    else:
        out["verdict"] = "PASS"
    out["mismatches"] = mismatches
    out["missing"] = missing
    return out


# ------------------------------------------------------------------ tables

def _fmt(v) -> str:
    return {True: "yes", False: "no", OBSERVE: "?"}.get(v, str(v))


def expected_table(cases: list[Case]) -> str:
    builds = list(CORE_BUILDS)
    for c in cases:
        for b in c.builds():
            if b not in builds:
                builds.append(b)
    lines = [
        "# 3D client conformance: expected results",
        "",
        "Generated by `tools/conformance/conformance.py expected --write` from",
        "[`cases/`](cases/); do not edit by hand. One row per case; each cell lists the",
        "case's checks as `check=yes/no/?` for that build (`?`: observed and recorded,",
        "not judged; blank: the build is not run for this case). Where each",
        "expectation comes from is in the case file's `source` lines.",
        "",
        "| Case | Rows | What | " + " | ".join(builds) + " |",
        "|---|---|---|" + "---|" * len(builds),
    ]
    for c in cases:
        cells = []
        for b in builds:
            e = c.expect.get(b)
            if e is None:
                cells.append("")
                continue
            cells.append("<br>".join(f"{k}={_fmt(e.get(k, OBSERVE))}" for k in (x.id for x in c.checks)))
        lines.append(f"| [{c.id}](cases/{c.path.name}) | {', '.join(c.rows)} | {c.title} | "
                     + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


RESULT_FIELDS = ["case", "build", "verdict", "date", "server", "client", "mismatches", "observed"]


def results_table(tsv: Path, cases: list[Case]) -> str:
    rows = []
    if tsv.exists():
        with tsv.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
    latest: dict[tuple[str, str], dict] = {}
    for r in rows:
        latest[(r["case"], r["build"])] = r   # the file is in run order: last wins
    builds = list(CORE_BUILDS)
    for (_, b) in latest:
        if b not in builds:
            builds.append(b)
    lines = [
        "# 3D client conformance: results",
        "",
        "Generated by `tools/conformance/conformance.py table results.tsv --write` from",
        "[`results.tsv`](results.tsv) (one line per run, appended by `run.py`); do not",
        "edit by hand. The latest run of each case and build: **PASS** (every judged",
        "check as expected), **FAIL** (the checks that differed), **ERROR** (an",
        "artefact was missing, e.g. no console log), `n/a` (not expected to run),",
        "blank (not run yet). Observed `?` values are listed under each run in",
        "`results.tsv`.",
        "",
        "| Case | What | " + " | ".join(builds) + " |",
        "|---|---|" + "---|" * len(builds),
    ]
    for c in cases:
        cells = []
        for b in builds:
            r = latest.get((c.id, b))
            if r is None:
                cells.append("n/a" if b not in c.expect else "")
            elif r["verdict"] == "FAIL":
                cells.append(f"FAIL: {r['mismatches']} ({r['date']})")
            else:
                cells.append(f"{r['verdict']} ({r['date']})")
        lines.append(f"| [{c.id}](cases/{c.path.name}) | {c.title} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def append_result(tsv: Path, verdict: dict, date: str, server: str, client: str) -> None:
    new = not tsv.exists()
    observed = ";".join(f"{k}={_fmt(v['observed'])}" for k, v in verdict["checks"].items()
                        if v["expected"] == OBSERVE and v["observed"] is not None)
    with tsv.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        if new:
            w.writerow(RESULT_FIELDS)
        w.writerow([verdict["case"], verdict["build"], verdict["verdict"], date, server, client,
                    ",".join(verdict.get("mismatches", [])), observed])


# ------------------------------------------------------------------ CLI

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    e = sub.add_parser("expected")
    e.add_argument("--write", action="store_true")
    b = sub.add_parser("build")
    b.add_argument("out", type=Path)
    b.add_argument("--case", default="")
    j = sub.add_parser("judge")
    j.add_argument("rundir", type=Path)
    j.add_argument("case")
    j.add_argument("build")
    j.add_argument("--exe", default="")
    t = sub.add_parser("table")
    t.add_argument("tsv", type=Path)
    t.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)

    only = set(a.case.split(",")) - {""} if getattr(a, "case", "") else None
    cases = load_cases(only)
    if a.cmd == "list":
        for c in cases:
            print(f"{c.id}  p{c.priority}  {','.join(c.rows):<28} {' '.join(c.builds()):<36} {c.title}")
    elif a.cmd == "expected":
        text = expected_table(cases)
        if a.write:
            (SUITE / "EXPECTED.md").write_text(text, encoding="utf-8")
        else:
            print(text)
    elif a.cmd == "build":
        for c in cases:
            print(build_world(c, a.out))
    elif a.cmd == "judge":
        case = next((c for c in cases if c.id == a.case or c.slug == a.case), None)
        if case is None:
            print(f"no case {a.case}", file=sys.stderr)
            return 2
        print(json.dumps(judge(case, a.build, a.rundir, a.exe), indent=1))
    elif a.cmd == "table":
        text = results_table(a.tsv, cases)
        if a.write:
            (SUITE / "RESULTS.md").write_text(text, encoding="utf-8")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
