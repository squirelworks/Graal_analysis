#!/usr/bin/env python3
"""The full typed GS2 3D member sweep (T3D-150): probes, cases and the
derived per-build table.

The 5.12 typed surface (torque/gs2-3d-typed-surface-512-2026-11-26.md, T3D-096)
lists every class, property and function the 3D engine registers, with
declared types. This tool turns that list into lab probes that touch every
member on a live client, one weapon3d per group of classes, and reads the
reports back into a derived table.

    python3 tools/conformance/gen_sweep.py gen          # (re)write scripts/sweep_*.gs2, cases/c049..c055, sweep/manifest.tsv
    python3 tools/conformance/gen_sweep.py check        # fail if the generated files are stale
    python3 tools/conformance/gen_sweep.py extract --build 5.12 <work>/out/5.12 [--build 4.20r8 <dir>] ...
                                                        # write torque/conformance/sweep/results.tsv and RESULTS.md

What each probe does, per member, on an instance of the member's class:

- property: read it (`d`), and if it is writable assign a value of its type
  and read it back (`w`); a numeric or bool property is then assigned the word
  `zz` and read back (`j`): a registered property coerces it (0, false, a
  number), an unregistered name is just a dynamic variable and gives `zz` back.
- function: call it once with arguments of the declared types and report the
  return (`r`); a void call reports `r=` once it returns.

Before each class the probe reports `at <Class>` and which instance it got
(`inst`: `new`, a fallback such as the player, or `none`). A client that dies
mid-class is found from the last member reported: the next member in
manifest order is the one that took it down. Members known to crash a client
from earlier board rows are not called (`skip`, with the row).

Python 3.11+ standard library only. Derived data only: the extractor writes
values, never logs or captures.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SURFACE = REPO / "torque" / "gs2-3d-typed-surface-512-2026-11-26.md"
SUITE = REPO / "torque" / "conformance"
SCRIPTS = SUITE / "scripts"
CASES = SUITE / "cases"
SWEEP = SUITE / "sweep"

sys.path.insert(0, str(HERE))
import conformance as cf  # noqa: E402

# ------------------------------------------------------------------ the surface

PROP = re.compile(r"^- `([A-Za-z0-9_]+)` — \*([a-z]+), (writable|read-only)\*\s*$")
FUNC = re.compile(r"^- `([A-Za-z0-9_]+)\(([a-z,]*)\)` → ([a-z]+)\s*$")
CLASS = re.compile(r"^### `([A-Za-z0-9_]+)` → `([A-Za-z0-9_]+)` \((\d+) members?\)")


@dataclass
class Member:
    cls: str
    name: str
    kind: str          # prop | func
    type: str          # property type, or the function's return type
    writable: bool = False
    args: tuple = ()

    @property
    def key(self) -> str:
        return f"{self.cls}.{self.name}"

    @property
    def decl(self) -> str:
        if self.kind == "prop":
            return f"{self.type} {'rw' if self.writable else 'ro'}"
        return f"({','.join(self.args)}) -> {self.type}"


def read_surface(path: Path = SURFACE) -> tuple[dict[str, str], dict[str, list[Member]]]:
    """Classes (name -> parent) and their members, in the document's order,
    from the 5.12 model section (the 4.04r2 comparison is not read)."""
    parents: dict[str, str] = {}
    members: dict[str, list[Member]] = {}
    declared: dict[str, int] = {}
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and cur:
            break      # the model section ends at the next level-2 heading
        m = CLASS.match(line)
        if m:
            cur = m.group(1)
            parents[cur] = m.group(2)
            members[cur] = []
            declared[cur] = int(m.group(3))
            continue
        if not cur:
            continue
        m = PROP.match(line)
        if m:
            members[cur].append(Member(cur, m.group(1), "prop", m.group(2), m.group(3) == "writable"))
            continue
        m = FUNC.match(line)
        if m:
            args = tuple(a for a in m.group(2).split(",") if a)
            members[cur].append(Member(cur, m.group(1), "func", m.group(3), args=args))
    for c, n in declared.items():
        if len(members[c]) != n:
            raise ValueError(f"{c}: {len(members[c])} members read, heading says {n}")
    return parents, members


# ------------------------------------------------------------------ the probes

# Groups of classes, one probe and one case each, so that a crash in one group
# does not hide the rest. The scene objects that may touch the renderer
# (TerrainBlock, Terraformer) go last and alone.
GROUPS = [
    ("C049", "sweep-gameobject", "GameObject, SceneObject, SimObject, SimGroup, Camera",
     ["SimObject", "SimGroup", "SceneObject", "GameObject", "Camera", "TGameObjectAttr"]),
    ("C050", "sweep-shape-anim", "shapes, animation threads, materials and movement",
     ["GameShape", "GameShapeDTS", "GameShapeDIF", "GameShapeFT", "DTSAniThread", "TShapeMaterial",
      "GameMovementInterpolate", "GameMovementList", "GameMovementRigid", "TMovementRigid",
      "GameConnection", "ActionMap"]),
    ("C051", "sweep-sky-sun-water", "Sky, Sun, fxSunLight and WaterBlock",
     ["Sky", "Sun", "fxSunLight", "WaterBlock"]),
    ("C052", "sweep-replicators-gui", "the shape replicators and the 3D GUI controls",
     ["DynamicShapeReplicator", "DynamicGrass", "DynamicGrassReplicator", "GuiGraal3DCtrl",
      "GuiInputCtrl", "GuiMapOverviewCtrl", "GuiPlayerView", "GuiShapeNameHud"]),
    ("C053", "sweep-worldeditor", "WorldEditor and EditManager",
     ["EditManager", "WorldEditor"]),
    ("C054", "sweep-terraineditor", "TerrainEditor",
     ["TerrainEditor"]),
    ("C055", "sweep-terrain-globals", "TerrainBlock, Terraformer and the global 3D functions",
     ["TerrainBlock", "Terraformer", "@globals"]),
]

# Where an instance comes from when `new <Class>` gives nothing: GS2
# expressions tried in order (the player's own object, the client's server
# connection, a shape or thread hanging off a GameObject).
FALLBACK = {
    "SimObject": ["this.go"],
    "SceneObject": ["this.go"],
    "GameObject": ["player"],
    "Camera": ["ServerConnection.camera", "player.camera"],
    "GameConnection": ["ServerConnection"],
    "SimGroup": ["ServerConnection"],
    "GameShape": ["this.go.shapeobject", "player.shapeobject"],
    "GameShapeDTS": ["this.go.shapeobject", "player.shapeobject"],
    "GameShapeDIF": ["this.go.shapeobject"],
    "GameShapeFT": ["this.go.shapeobject"],
    "DTSAniThread": ["this.go.playAnimation(\"conf\")", "player.playAnimation(\"conf\")"],
    "TShapeMaterial": ["this.go.shapeobject.getMaterial(0)"],
    "GameMovementInterpolate": ["this.go.movement", "player.movement"],
    "GameMovementList": ["this.go.movement", "player.movement"],
    "GameMovementRigid": ["this.go.movement", "player.movement"],
    "TMovementRigid": ["this.go.movement", "player.movement"],
    "TGameObjectAttr": ["this.go.attrobjects[0]"],
    "Sky": ["findobject(\"Sky\")"],
    "Sun": ["findobject(\"Sun\")"],
}

# Members not called, from earlier board answers that they end the client.
SKIP = {
    "Terraformer.loadGreyscale": "T3D-050: crashes the client without a TerrainBlock",
    "Terraformer.loadGrayscale": "T3D-050: the same handler as loadGreyscale",
    # `Class.@inst`: getting an instance at all ends the client; the class is not touched
    "TGameObjectAttr.@inst": "T3D-150 sweep: ends the 5.12 client",
    "TerrainEditor.@inst": "T3D-150 sweep: ends the 5.12 client",
}

# Arguments for particular functions where the declared type alone would make
# a pointless call; GS2 literals.
ARGS = {
    "ActionMap.bind": ['"keyboard"', '"f9"', '"conf_bind"'],
    "ActionMap.getBinding": ['"conf_bind"'],
    "ActionMap.getCommand": ['"keyboard"', '"f9"'],
    "ActionMap.unbind": ['"keyboard"', '"f9"'],
    "WorldEditor.setMode": ['"move"'],
    "GameObject.playAnimation": ['"conf"'],
    "GameObject.playAnimation2": ['"conf"'],
    "GameObject.getdropz": ['"0 0 50"'],
    "GameObject.checkCollision": ['"0 0 1"', '"0 8 1"'],
    "GameObject.checkCollisionByBox": ['"-0.5 -0.5 0"', '"0.5 0.5 2"', '"0 4 1"'],
    "GameObject.move3d": ['"0 1 0"', "1", "0"],
}

GLOBALS = [
    # name, GS2 call (returns are reported), what it is
    ("castRay", 'castRay("0 0 50", "0 0 -50", -1)'),
    ("get3Dobjectsbybox", 'get3Dobjectsbybox("-20 -20 -20", "20 20 20")'),
    ("get3Dobjectsbyradius", 'get3Dobjectsbyradius("0 0 0", 20)'),
    ("getz", "getz(0, 0)"),
    ("getTerrainTexture", "getTerrainTexture(0, 0)"),
    ("getTerrainTextureIndex", "getTerrainTextureIndex(0, 0)"),
    ("setSunColors", "setSunColors({0, 1, 0.5, 0.5, 12, 1, 1, 1})"),
    ("setFogColors", "setFogColors({0, 0.5, 0.5, 0.5, 12, 0.6, 0.6, 0.6})"),
    ("setSkyBandColors", "setSkyBandColors({0, 0.2, 0.3, 0.9, 12, 0.3, 0.5, 1})"),
    ("setSkyBandSizes", "setSkyBandSizes({0, 0.3, 12, 0.5})"),
    ("syncTimeOfDay", "syncTimeOfDay()"),
    ("updateVisibleDistance", "updateVisibleDistance()"),
    ("lightScene", "lightScene()"),
]


def arg_literal(t: str, m: Member, i: int) -> str:
    if t in ("i",):
        return "1"
    if t == "int":
        return "1"
    if t in ("float", "num", "double"):
        return "1.5"
    if t == "bool":
        return "true"
    if t == "object":
        return "this.go2"
    # a string: most string arguments in this table are vectors or boxes
    return '"1 2 3"'


def call_args(m: Member) -> str:
    if m.key in ARGS:
        return ", ".join(ARGS[m.key])
    return ", ".join(arg_literal(t, m, i) for i, t in enumerate(m.args))


def set_literal(m: Member) -> str:
    """A value of the property's type to assign."""
    return {"int": "2", "float": "0.5", "bool": "true", "object": "this.go2"}.get(m.type, "")


def gs2_class(cls: str, ms: list[Member]) -> str:
    """One function that gets an instance of `cls` and touches every member."""
    if f"{cls}.@inst" in SKIP:
        # getting an instance ends the client: report the class and its members as skipped
        out = [f"function s_{cls}() {{", f'  cf("at", "{cls}");', f'  cf("{cls}.@inst", "skip");']
        out += [f'  cf("{m.key}", "skip");' for m in ms]
        out.append("}")
        return "\n".join(out)
    out = [f"function s_{cls}() {{", f'  cf("at", "{cls}");', f'  temp.o = new {cls}("sw_{cls.lower()}");',
           '  temp.how = "new";']
    for fb in FALLBACK.get(cls, []):
        out += ["  if (temp.o == NULL) {", f"    temp.o = {fb};", f'    temp.how = "{fb.replace(chr(34), "")}";', "  }"]
    out += ['  if (temp.o == NULL) temp.how = "none";',
            f'  cf("{cls}.@inst", temp.how @ "|" @ temp.o.objecttype());',
            "  if (temp.o == NULL) return;"]
    for m in ms:
        k = m.key
        if k in SKIP:
            out.append(f'  cf("{k}", "skip");')
            continue
        if m.kind == "prop":
            out.append(f"  temp.d = temp.o.{m.name};")
            if m.writable:
                lit = set_literal(m)
                if lit:
                    out.append(f"  temp.o.{m.name} = {lit};")
                else:
                    # a string: keep the shape of the default (a vector, a colour, a word)
                    out += ["  temp.n = temp.d.tokenize().size();",
                            '  if (temp.n == 3) temp.v = "1 2 3";',
                            '  else if (temp.n == 4) temp.v = "0.1 0.2 0.3 1";',
                            '  else if (temp.n == 6) temp.v = "-1 -2 -3 1 2 3";',
                            '  else if (temp.n == 7) temp.v = "1 2 3 0 0 1 0";',
                            '  else temp.v = "conf";',
                            f"  temp.o.{m.name} = temp.v;"]
                out.append(f"  temp.w = temp.o.{m.name};")
                if m.type in ("int", "float", "bool"):
                    out += [f'  temp.o.{m.name} = "zz";', f"  temp.j = temp.o.{m.name};",
                            f"  temp.o.{m.name} = temp.d;",
                            f'  cf("{k}", "d=" @ temp.d @ "|w=" @ temp.w @ "|j=" @ temp.j);']
                else:
                    out.append(f'  cf("{k}", "d=" @ temp.d @ "|w=" @ temp.w);')
            else:
                out.append(f'  cf("{k}", "d=" @ temp.d);')
        else:
            call = f"temp.o.{m.name}({call_args(m)})"
            if m.type == "void":
                out += [f"  {call};", f'  cf("{k}", "r=");']
            elif m.type == "object":
                out += [f"  temp.r = {call};", f'  cf("{k}", "r=" @ ov(temp.r));']
            else:
                out += [f"  temp.r = {call};", f'  cf("{k}", "r=" @ temp.r);']
    out.append("}")
    return "\n".join(out)


def gs2_globals() -> str:
    out = ["function s_globals() {", '  cf("at", "@globals");']
    for name, call in GLOBALS:
        out += [f"  temp.r = {call};", f'  cf("@globals.{name}", "r=" @ temp.r @ "|n=" @ temp.r.size());']
    out.append("}")
    return "\n".join(out)


def probe(gid: str, title: str, classes: list[str], members: dict[str, list[Member]]) -> str:
    steps = [c for c in classes]
    head = f"""// Generated by tools/conformance/gen_sweep.py; do not edit by hand.
// Conformance sweep {gid} (T3D-150): {title}. Every typed member of these
// classes from the 5.12 surface (T3D-096), touched once on a live client:
// properties read, written with a value of their type and read back (numeric
// and bool ones also given the word zz, which a registered property coerces);
// functions called with arguments of the declared types. One class a timer
// tick; reports go back as cf(<Class.member>, <value>).
//#CLIENTSIDE
function onCreated() {{
  setTimer(4);
}}
function onTimeout() {{
  this.n++;
  if (this.n == 1) {{
    this.go = new GameObject("sw_go");
    this.go2 = new GameObject("sw_go2");
    cf("made", (this.go != NULL) @ "");
  }}"""
    body = [head]
    for i, c in enumerate(steps, start=2):
        fn = "s_globals" if c == "@globals" else f"s_{c}"
        body.append(f"  else if (this.n == {i}) {fn}();")
    last = len(steps) + 2
    body.append(f'  else if (this.n == {last}) cf("done", "1");')
    body.append(f"  if (this.n < {last}) setTimer(1);")
    body.append("}")
    for c in steps:
        body.append(gs2_globals() if c == "@globals" else gs2_class(c, members[c]))
    body.append("""function ov(o) {
  if (o == NULL) return "null";
  return "obj:" @ o.name;
}
function cf(k, v) {
  triggerserver("gui", "ConfProbe", "cf", k, v);
}""")
    return "\n".join(body) + "\n"


WORLD = """sun 0.57735 0.57735 -0.57735 0.8 0.8 0.8 1 0.3 0.3 0.35 1
sky conf_sky0,conf_sky1,conf_sky2,conf_sky3,conf_sky4,conf_sky5 500
skyoptions 1 0 0 0.4 0.6 0.9
object ConfCube conf_red.3ds 0 4 1
playershape conf_nomat.3ds
spawn 0 0 1
"""

BUILD_EXPECT = {
    "4.20r8": "unread: the typed table is read for 5.12; a 4.20r8 member may be absent",
    "5.12": "[bin] T3D-096 types every member called here; values unread before this sweep",
    "6.037F": "unread: our Frankenstein 6.037 (gcr) against the 5.12 surface",
}


def case_toml(gid: str, slug: str, title: str, classes: list[str]) -> str:
    n = len(classes) + 2
    checks = [("compiled", "server", 'pattern = "weapon3d ConfProbe: not compiled"'),
              ("made", "probe", 'key = "made"\nvalue = "1"'),
              ("done", "probe", 'key = "done"\nvalue = "1"\nnote = "every class step ran (no script stop, no crash)"'),
              ("alive", "alive", 'note = "the client was still running at the end"')]
    lines = [f'id = "{gid}"', f'slug = "{slug}"',
             f'title = "Every typed GS2 3D member of {title}, touched on a live client (full sweep)"',
             'rows = ["T3D-150", "T3D-096"]', "priority = 3", "",
             "# Generated by tools/conformance/gen_sweep.py; do not edit by hand.",
             "# Per-member values go to torque/conformance/sweep/results.tsv (gen_sweep.py extract).",
             "", "[world]", f'lines = """\n{WORLD}"""',
             'files = ["conf_red.3ds", "conf_nomat.3ds", "conf_sky*"]',
             f'scripts = ["sweep_{slug.split("-", 1)[1].replace("-", "_")}.gs2"]', "",
             "[run]", f"seconds = {max(45, 4 + n * 2 + 20)}", ""]
    for cid, kind, rest in checks:
        lines += ["[[check]]", f'id = "{cid}"', f'kind = "{kind}"'] + rest.splitlines() + [""]
    for b, src in BUILD_EXPECT.items():
        lines += [f'[expect."{b}"]', "compiled = false", 'made = "?"', 'done = "?"', 'alive = "?"',
                  f'source = "{src}"', ""]
    return "\n".join(lines)


def manifest_rows(members: dict[str, list[Member]]) -> list[list[str]]:
    rows = []
    for gid, slug, _title, classes in GROUPS:
        for c in classes:
            if c == "@globals":
                for name, call in GLOBALS:
                    rows.append([gid, "@globals", name, "global", call.replace("\t", " ")])
                continue
            rows.append([gid, c, "@inst", "instance", "new " + " / ".join([c] + FALLBACK.get(c, []))])
            for m in members[c]:
                rows.append([gid, c, m.name, m.kind, m.decl])
    return rows


def generated() -> dict[Path, str]:
    _parents, members = read_surface()
    seen = [c for _g, _s, _t, cls in GROUPS for c in cls if c != "@globals"]
    missing = set(members) - set(seen)
    if missing or len(seen) != len(set(seen)):
        raise ValueError(f"GROUPS must name every class once; missing {sorted(missing)}")
    out: dict[Path, str] = {}
    for gid, slug, title, classes in GROUPS:
        script = f"sweep_{slug.split('-', 1)[1].replace('-', '_')}.gs2"
        out[SCRIPTS / script] = probe(gid, title, classes, members)
        out[CASES / f"{gid.lower()}-{slug}.toml"] = case_toml(gid, slug, title, classes)
    rows = manifest_rows(members)
    text = "group\tclass\tmember\tkind\tdeclared\n" + "".join("\t".join(r) + "\n" for r in rows)
    out[SWEEP / "manifest.tsv"] = text
    return out


# ------------------------------------------------------------------ results

def classify(kind: str, decl: str, value: str | None, crashed: bool) -> str:
    """One word per member and build, from its reported value:

    crash    the client died on this member (the next after the last report)
    skip     not called (a known crasher)
    noinst   no instance of the class could be had on this build
    works    a property that took a written value (or a function returning a
             non-empty typed value)
    readonly a read-only property with a typed (non-empty) value
    inert    registered (it coerced junk, or returned a typed default) but the
             write did not stick / the call returned the default
    absent   no sign it is registered: a numeric property gave the junk word
             back, or every read and return was empty
    ran      a void function that returned (no observable return)
    unrun    the probe never reached it (an earlier crash or a short run)
    """
    if crashed:
        return "crash"
    if value is None:
        return "unrun"
    if value == "skip":
        return "skip"
    if value == "noinst":
        return "noinst"
    f = dict(p.split("=", 1) if "=" in p else (p, "") for p in value.split("|"))
    if kind == "prop":
        d, w, j = f.get("d", ""), f.get("w"), f.get("j")
        if j is not None and j.strip() == "zz":
            return "absent"
        if w is None:
            return "readonly" if d.strip() else "absent"
        if w.strip() and w.strip() != d.strip():
            return "works"
        if j is not None or d.strip() or w.strip():
            return "inert" if w.strip() == d.strip() else "works"
        return "absent"
    if kind == "func":
        r = f.get("r", "")
        if decl.endswith("-> void"):
            return "ran"
        if r.strip() and r.strip() not in ("null",):
            return "works"
        return "inert" if r.strip() == "null" or decl.endswith(("-> object",)) else "absent"
    if kind == "global":
        return "works" if f.get("r", "").strip() or f.get("n", "0").strip() not in ("", "0") else "ran"
    if kind == "instance":
        return "noinst" if value.startswith("none") else value.split("|", 1)[0]
    return "?"


def extract(runs: list[tuple[str, Path]]) -> tuple[list[dict], dict]:
    """runs: (build, <work>/out/<build>) folders holding C049..C055 run dirs."""
    rows = list(csv.DictReader((SWEEP / "manifest.tsv").open(encoding="utf-8"), delimiter="\t"))
    results = []
    summary: dict[str, dict[str, int]] = {}
    for build, base in runs:
        per = {}
        for gid, _slug, _t, _c in GROUPS:
            log = base / gid / "gserver.log"
            text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""
            con = base / gid / "console.txt"
            per[gid] = (text, con.read_text(encoding="utf-8", errors="replace") if con.exists() else "")
        last_seen: dict[str, int] = {}
        vals: dict[int, str | None] = {}
        for i, r in enumerate(rows):
            text, _con = per[r["group"]]
            key = f'{r["class"]}.{r["member"]}'
            got = cf.probe_values(text, key)
            vals[i] = got[-1] if got else None
            if got:
                last_seen[r["group"]] = i
        dead = {}
        for gid, (text, _con) in per.items():
            done = cf.probe_values(text, "done")
            if text and not done and gid in last_seen:
                dead[gid] = last_seen[gid] + 1
            elif text and not done and cf.probe_values(text, "made"):
                # the probe started but died before its first member reported
                dead[gid] = next(i for i, r in enumerate(rows) if r["group"] == gid)
        noinst = set()
        for i, r in enumerate(rows):
            if r["member"] == "@inst" and (vals[i] or "").startswith("none"):
                noinst.add(r["class"])
        counts: dict[str, int] = {}
        for i, r in enumerate(rows):
            v = vals[i]
            if v is None and r["class"] in noinst and r["member"] != "@inst":
                v = "noinst"
            word = classify(r["kind"], r["declared"], v, dead.get(r["group"]) == i)
            if r["kind"] != "instance":
                counts[word] = counts.get(word, 0) + 1
            results.append({"build": build, "class": r["class"], "member": r["member"], "kind": r["kind"],
                            "declared": r["declared"], "verdict": word,
                            "value": (v or "").replace("\t", " ")[:160]})
        summary[build] = counts
    return results, summary


def write_results(results: list[dict], summary: dict, label: dict[str, str]) -> None:
    SWEEP.mkdir(parents=True, exist_ok=True)
    cols = ["build", "class", "member", "kind", "declared", "verdict", "value"]
    with (SWEEP / "results.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(results)
    builds = list(summary)
    words = ["works", "readonly", "ran", "inert", "absent", "noinst", "crash", "skip", "unrun"]
    md = ["# Typed GS2 3D member sweep: results by build (T3D-150)", "",
          "Generated by `tools/conformance/gen_sweep.py extract` from the C049 to C055 lab runs;",
          "do not edit by hand. One line per member and build is in [`results.tsv`](results.tsv);",
          "the verdict words are defined in `gen_sweep.classify`.", "",
          "| Build | Client | " + " | ".join(words) + " |", "|---|---|" + "---|" * len(words)]
    for b in builds:
        md.append(f"| {b} | {label.get(b, '')} | " + " | ".join(str(summary[b].get(x, 0)) for x in words) + " |")
    md += ["", "## By class", "", "| Class | Members | " + " | ".join(builds) + " |", "|---|---|" + "---|" * len(builds)]
    by: dict[tuple[str, str], dict[str, int]] = {}
    order: list[str] = []
    for r in results:
        if r["kind"] == "instance":
            continue
        if r["class"] not in order:
            order.append(r["class"])
        d = by.setdefault((r["class"], r["build"]), {})
        d[r["verdict"]] = d.get(r["verdict"], 0) + 1
    for c in order:
        n = sum(by.get((c, builds[0]), {}).values())
        cells = []
        for b in builds:
            d = by.get((c, b), {})
            cells.append(", ".join(f"{k} {v}" for k, v in sorted(d.items(), key=lambda kv: words.index(kv[0]))))
        md.append(f"| `{c}` | {n} | " + " | ".join(cells) + " |")
    (SWEEP / "RESULTS.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gen")
    sub.add_parser("check")
    ex = sub.add_parser("extract")
    ex.add_argument("--build", nargs=2, action="append", metavar=("BUILD", "OUTDIR"), required=True)
    ex.add_argument("--label", nargs=2, action="append", metavar=("BUILD", "TEXT"), default=[])
    a = ap.parse_args(argv)
    if a.cmd in ("gen", "check"):
        stale = []
        for p, text in generated().items():
            if a.cmd == "gen":
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8")
            elif not p.exists() or p.read_text(encoding="utf-8") != text:
                stale.append(str(p.relative_to(REPO)))
        if stale:
            print("stale (run gen_sweep.py gen):", *stale, sep="\n  ")
            return 1
        return 0
    results, summary = extract([(b, Path(d)) for b, d in a.build])
    write_results(results, summary, dict(a.label))
    for b, c in summary.items():
        print(b, " ".join(f"{k}={v}" for k, v in sorted(c.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
