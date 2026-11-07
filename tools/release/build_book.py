#!/usr/bin/env python3
"""Build the Graal Analysis 0.0.1 chapter and appendix PDFs.

From the repository root:

    python3 tools/release/build_book.py
    python3 tools/release/build_book.py --only 04

Each PDF is produced with:

    pandoc INPUT.md -o OUTPUT.pdf \
      --pdf-engine=weasyprint \
      --css tools/release/book.css \
      --metadata title="TITLE" \
      --no-highlight \
      --resource-path=. \
      -f markdown-raw_html-smart-tex_math_dollars

Requires pandoc, weasyprint, and pdfinfo. No third-party Python packages.
Page counts in release/0.0.1/README.md come from pdfinfo. A part over 100
pages is split and measured again.

`--only KEY` rebuilds one chapter (a CHAPTERS key such as `04`) and refreshes
that chapter's rows in the release README and contents from pdfinfo. Other
chapter PDFs stay as they are. The contents PDF is rebuilt so its page table
matches.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "release" / "0.0.1"
CSS = ROOT / "tools" / "release" / "book.css"
WORK = Path("/tmp/graal-book-build")
MAX_PAGES = 100
# Sum of separately measured piece lengths. The merged PDF is this long or
# shorter, because each piece was measured with its own closing page.
MERGE_CAP = 90
# Skip a single pandoc of a very large group; split by size first.
BYTE_SPLIT = 140_000
PANDOC_FROM = "markdown-raw_html-smart-tex_math_dollars"

CHAPTERS = (
    ("01", "ch-01-how-to-read", "How to read these notes", "Chapter", 1),
    ("02", "ch-02-formats", "Formats", "Chapter", 2),
    ("03", "ch-03-protocol", "Protocol", "Chapter", 3),
    (
        "04",
        "ch-04-client-internals-and-version-profiles",
        "Client internals and version profiles",
        "Chapter",
        4,
    ),
    ("05", "ch-05-graal3d-and-torque", "Graal3D and Torque", "Chapter", 5),
    (
        "06",
        "ch-06-tools-labs-and-level-conversion",
        "Tools, labs, and level conversion",
        "Chapter",
        6,
    ),
    ("07", "ch-07-npc-scripting-overview", "NPC scripting overview", "Chapter", 7),
    (
        "A-recovered",
        "ap-01-recovered-tools-and-trainers",
        "Recovered tools and trainers",
        "Appendix",
        1,
    ),
    ("A-assets", "ap-02-game-asset-inventories", "Game-asset inventories", "Appendix", 2),
    (
        "A-other",
        "ap-03-server-and-other-notes",
        "Server notes and other indexes",
        "Appendix",
        3,
    ),
    ("A-npc", "ap-04-npc-script-names", "NPC script names", "Appendix", 4),
)

CONTENTS_SLUG = "ch-00-contents"
CONTENTS_TITLE = "Graal Analysis 0.0.1 — contents"

DRIVE_LINK_SOURCES = (
    "ARCHIVAL.md",
    "archive/ember-avelan-experimental.md",
    "npc-library/archival-scripting-notes.md",
)

INTROS = {
    "02": (
        "Notes under `formats/`, in path order, followed by the troff format "
        "notes `formats/glevnw01.txt`, `formats/gani.txt`, `formats/grmap001.txt`, "
        "and `formats/tiletypes.txt` converted to markdown."
    ),
    "03": "Notes under `protocol/`, in path order.",
    "04": (
        "Reading order for the client notes, not directory order. "
        "Overview and architecture come first, including how a version id "
        "and a version profile are read. "
        "A version timeline follows: precursors and early clients, then 1.x, "
        "2.x, and later clients. "
        "Topic notes are grouped as movement, combat, the HUD and "
        "presentation, then files and the session. "
        "Dated decompile-finding batches are last, under Batch notes, each "
        "batch kept together and the batches in date order."
    ),
    "05": "Notes under `graal3d/`, then `torque/`, each in path order.",
    "06": (
        "Notes under `tools/` and `live-runs/`, in path order. "
        "`tools/navigator/README.md` describes the notes viewer. The viewer "
        "program stays in the source tree."
    ),
    "07": (
        "Narrative NPC notes under `npc-library/`, plus "
        "`server-notes/setcharprop-hash-n.md`. Script bodies stay in the "
        "`page.json` files. Image names are listed in the script-name appendix."
    ),
    "A-recovered": (
        "Behaviour notes under `recovered-hacks/` and `recovered-drive-tools/`."
    ),
    "A-assets": "Inventory notes under `archive/`.",
    "A-other": (
        "Server notes (except the setcharprop note, which is in the NPC "
        "volume), Ash notes, earlier archival notes, and the consolidated summary."
    ),
    "A-npc": (
        "Each bullet is one script in `npc-library/**/page.json`. The label is "
        "the script's image name. The script body is omitted. The path is the "
        "page file and the item number on that page."
    ),
}

FORMAT_MAN = (
    "formats/glevnw01.txt",
    "formats/gani.txt",
    "formats/grmap001.txt",
    "formats/tiletypes.txt",
)


@dataclass
class Unit:
    label: str
    body: str
    nbytes: int = field(init=False)

    def __post_init__(self) -> None:
        self.nbytes = len(self.body.encode("utf-8"))


@dataclass
class Piece:
    units: list[Unit]
    pages: int
    pdf: Path


def log(message: str) -> None:
    print(message, flush=True)


EMBER_FOOTER = re.compile(
    r"\*Extracted from the Ember atlas in the decommissioned local workspace\."
    r"(?: Full algorithms are in the Google Drive archive\.)?\*",
    re.I,
)
HORIZONTAL_RULE = re.compile(r"^---\s*$", re.M)
FILE_ID_LINE = re.compile(
    r"^(\s*(?:[-*•]\s+)?\*\*File ID:\*\*)\s*(?:`[^`]+`|\S+.*)$",
    re.M,
)


def redact(text: str) -> str:
    """Drop Drive URLs so the document release does not republish file ids."""
    host = "(?:drive|docs)." + "google.com"
    pattern = re.compile(r"https?://" + host + r"/\S+", re.I)
    text = pattern.sub("(Drive link omitted from the document release)", text)
    text = EMBER_FOOTER.sub(
        "(Extracted from the Ember atlas in the decommissioned local workspace.)",
        text,
    )
    text = re.sub(
        r"\n---\n\(Extracted from the Ember atlas",
        "\n\n(Extracted from the Ember atlas",
        text,
    )
    text = HORIZONTAL_RULE.sub("", text)
    text = FILE_ID_LINE.sub(
        r"\1 `(omitted from the document release)`",
        text,
    )
    return text


def strip_yaml(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    block = text[4:end]
    if ":" not in block:
        return text
    return text[end + 5 :]


def transform_outside_fences(text: str, fn) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    buf: list[str] = []
    fence: tuple[str, int] | None = None

    def flush() -> None:
        if buf:
            out.append(fn("".join(buf)))
            buf.clear()

    for line in lines:
        opener = re.match(r"^(\s{0,3})(`{3,}|~{3,})", line)
        if fence is None and opener:
            flush()
            mark = opener.group(2)
            fence = (mark[0], len(mark))
            out.append(line)
            continue
        if fence is not None:
            closer = re.match(
                r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*$",
                line,
            )
            out.append(line)
            if closer:
                fence = None
            continue
        buf.append(line)
    flush()
    return "".join(out)


def demote_headings(text: str, levels: int = 2) -> str:
    def one(chunk: str) -> str:
        kept: list[str] = []
        for line in chunk.splitlines(keepends=True):
            match = re.match(r"^(#{1,6})([ \t]+)(.*)$", line)
            if not match:
                kept.append(line)
                continue
            level = min(6, len(match.group(1)) + levels)
            nl = "\n" if line.endswith("\n") else ""
            kept.append("#" * level + match.group(2) + match.group(3).rstrip("\n") + nl)
        return "".join(kept)

    return transform_outside_fences(text, one)


def rewrite_images(text: str, source: Path) -> str:
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def repl(match: re.Match[str]) -> str:
        alt, dest = match.group(1), match.group(2).strip()
        parts = re.match(r"^(\S+)(?:\s+(\".*\"|'.*'))?$", dest)
        if not parts:
            return match.group(0)
        url = parts.group(1).strip("<>")
        if url.startswith(("http://", "https://", "data:")):
            return match.group(0)
        target = (source.parent / url).resolve()
        if not target.is_file():
            return match.group(0)
        title = f" {parts.group(2)}" if parts.group(2) else ""
        return f"![{alt}]({target.as_posix()}{title})"

    def one(chunk: str) -> str:
        return pattern.sub(repl, chunk)

    return transform_outside_fences(text, one)


def prepare_text(text: str, source: Path) -> str:
    text = redact(strip_yaml(text))
    text = demote_headings(text, 2)
    text = rewrite_images(text, source)
    return text.strip() + "\n"


def load_md(path: Path) -> Unit:
    rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    body = prepare_text(path.read_text(encoding="utf-8", errors="replace"), path)
    return Unit(rel, body)


def man_unit(rel: str) -> Unit:
    path = ROOT / rel
    proc = subprocess.run(
        ["pandoc", "-f", "man", "-t", "markdown-smart", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"pandoc could not read man page {rel}")
    body = prepare_text(proc.stdout, path)
    return Unit(rel, body)


def chapter_of(rel: str) -> str | None:
    if rel == "tools/release/how-to-read.md":
        return "01"
    if rel.startswith("tools/release/") or rel.startswith("release/"):
        return None
    if rel in {"README.md", "AGENTS.md", "docs/NEXT.md"}:
        return "01"
    if rel.startswith("formats/"):
        return "02"
    if rel.startswith("protocol/"):
        return "03"
    if rel.startswith("client-internals/") or rel.startswith("version-profiles/"):
        return "04"
    if rel.startswith("graal3d/") or rel.startswith("torque/"):
        return "05"
    if rel.startswith("tools/") or rel.startswith("live-runs/"):
        return "06"
    if rel.startswith("npc-library/") or rel == "server-notes/setcharprop-hash-n.md":
        return "07"
    if rel.startswith("recovered-hacks/") or rel.startswith("recovered-drive-tools/"):
        return "A-recovered"
    if rel.startswith("archive/"):
        return "A-assets"
    if (
        rel.startswith("server-notes/")
        or rel.startswith("ash/")
        or rel.startswith("archival/")
        or rel in {"CONSOLIDATED.md", "ARCHIVAL.md", "ARCHIVE.md"}
    ):
        return "A-other"
    raise SystemExit(f"unclassified markdown: {rel}")


def _section(title: str, blurb: str) -> tuple[str, str]:
    return ("section", f"## {title}\n\n{blurb.strip()}\n")


def _note(path: str) -> tuple[str, str]:
    return ("note", path)


def _batch(path: str) -> tuple[str, str]:
    return ("batch", path)


# Chapter 4 reading order. Do not replace this with a path sort.
# Path order is a directory dump: `decomp-findings-*` sorts between the
# topical notes (`damage-sources.md` then a dated batch, then `des-and-hidden-strings.md`).
# Every markdown file under client-internals/ and version-profiles/ is
# either a note below or a file inside one batch directory. A new note
# fails the build until it is placed here.
CHAPTER_04_READING: tuple[tuple[str, str], ...] = (
    _section(
        "Overview",
        "Architecture of the 2.05 client, the build catalogue, and how a "
        "version id and a version profile are read.",
    ),
    _note("client-internals/prior-attempts.md"),
    _note("client-internals/client-architecture-205.md"),
    _note("client-internals/client-assets.md"),
    _note("client-internals/build-catalogue.md"),
    _note("client-internals/drive-clients-inventory.md"),
    _note("client-internals/version-id-map.md"),
    _note("client-internals/version-tokens.md"),
    _note("client-internals/version/README.md"),
    _note("client-internals/version/VERSION.md"),
    _note("client-internals/version/docs/GraalEditor-README.md"),
    _note("client-internals/version/docs/GraalEditor-architecture.md"),
    _note("client-internals/version-profiles/README.md"),
    _note("client-internals/version-profiles/list-ports.md"),
    _note("version-profiles/matrix/README.md"),
    _note("version-profiles/matrix/seihai-gaps.md"),
    _note("version-profiles/version-coverage-2026-10-24.md"),
    _note("client-internals/reference-reimplementations/README.md"),
    _note("client-internals/reference-reimplementations/2dadventureclient.md"),
    _note("client-internals/reference-reimplementations/levelscripteditor.md"),
    _section(
        "Version timeline",
        "Precursors and early clients, then 1.x, 2.x, and later clients.",
    ),
    _note("client-internals/zelda-online-1998.md"),
    _note("client-internals/precursors-and-fan-builds.md"),
    _note("client-internals/precursor-runs-2026-10-30.md"),
    _note("client-internals/early-clients.md"),
    _note("version-profiles/matrix/rules-1st-graal.md"),
    _note("client-internals/gameboy-demo.md"),
    _note("client-internals/relay-room-bridge.md"),
    _note("client-internals/live-trace-early.md"),
    _note("client-internals/live-gserver13.md"),
    _note("client-internals/versions-133-139.md"),
    _note("version-profiles/matrix/rules-139.md"),
    _note("client-internals/cross-version-timeline.md"),
    _note("client-internals/newworld-betas.md"),
    _note("client-internals/v2.00-connect-path.md"),
    _note("client-internals/build-diff-204-205.md"),
    _note("client-internals/feature-timeline.md"),
    _note("client-internals/live-trace-205.md"),
    _note("version-profiles/2.22-2.31.md"),
    _note("client-internals/live-checks-editor-offline-sound.md"),
    _note("client-internals/player-mannerisms-live.md"),
    _note("version-profiles/matrix/builds-deltas.md"),
    _note("version-profiles/matrix/live-runs-2026-10-30.md"),
    _note("version-profiles/3.04-3.153.md"),
    _note("version-profiles/lab-304-linux-2026-10-30.md"),
    _note("client-internals/live-behaviour-404.md"),
    _note("version-profiles/lab-mac-tiger-2026-10-31.md"),
    _note("version-profiles/lab-v5-2026-10-30.md"),
    _section(
        "Topics",
        "Movement, then combat, then the HUD and presentation, then files "
        "and the session. A feature-spec note sits with the topic it "
        "describes. The feature-spec index is first.",
    ),
    _note("client-internals/feature-specs/README.md"),
    _note("client-internals/foot-test.md"),
    _note("client-internals/ledges-push-pull.md"),
    _note("client-internals/carry-hide-and-glove.md"),
    _note("client-internals/water-and-ganis.md"),
    _note("client-internals/feature-specs/11-emotes-ganis.md"),
    _note("client-internals/feature-specs/06-gmap-overworld.md"),
    _note("client-internals/feature-specs/02-weapons-combat.md"),
    _note("client-internals/combat-200-204.md"),
    _note("client-internals/damage-sources.md"),
    _note("client-internals/status-bit-0x20.md"),
    _note("client-internals/item-drops.md"),
    _note("client-internals/board-respawn.md"),
    _note("client-internals/feature-specs/04-death-respawn.md"),
    _note("client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md"),
    _note("client-internals/feature-specs/03-inventory.md"),
    _note("client-internals/id24-205.md"),
    _note("client-internals/rendering-observations.md"),
    _note("client-internals/status-display.md"),
    _note("client-internals/body-colours-and-attributes.md"),
    _note("client-internals/chat-text.md"),
    _note("client-internals/sign-panel.md"),
    _note("client-internals/feature-specs/09-options.md"),
    _note("client-internals/feature-specs/10-right-click-menu.md"),
    _note("client-internals/feature-specs/12-motd-rules.md"),
    _note("client-internals/feature-specs/13-ban-kick.md"),
    _note("client-internals/feature-specs/14-friends-ignore.md"),
    _note("client-internals/feature-specs/01-sound.md"),
    _note("client-internals/sound-and-music.md"),
    _note("client-internals/bare-level-names.md"),
    _note("client-internals/feature-specs/05-save-load.md"),
    _note("client-internals/config-and-input.md"),
    _note("client-internals/graalconfig-reference.md"),
    _note("client-internals/saved-passwords.md"),
    _note("client-internals/des-and-hidden-strings.md"),
    _note("client-internals/feature-specs/08-tampercheck.md"),
    _note("client-internals/feature-specs/07-udp-peer.md"),
    _note("client-internals/offline-play.md"),
    _note("client-internals/offline-training.md"),
    _note("client-internals/offline-tutorial-205.md"),
    _note("client-internals/level-editor-205.md"),
    _section(
        "Batch notes",
        "Dated decompile-finding batches. Each batch stays together, and "
        "the batches are in date order. The topic notes above are the "
        "place to start; these are the passes those notes came from.",
    ),
    _batch("client-internals/decomp-findings-2026-10-24"),
    _batch("client-internals/decomp-findings-2026-10-24-b"),
    _batch("client-internals/decomp-findings-2026-10-24-c"),
    _batch("client-internals/decomp-findings-2026-10-24-d"),
    _batch("client-internals/decomp-findings-2026-10-25-e"),
    _batch("client-internals/decomp-findings-2026-10-25-f"),
    _batch("client-internals/decomp-findings-2026-10-25-g"),
    _batch("client-internals/decomp-findings-2026-10-25-j"),
    _batch("client-internals/decomp-findings-2026-10-25-k"),
    _batch("client-internals/decomp-findings-2026-10-25-l"),
    _batch("client-internals/decomp-findings-2026-10-25-m"),
    _batch("client-internals/decomp-findings-2026-10-28"),
    _batch("client-internals/decomp-findings-2026-10-28-b"),
)


def batch_note_paths(folder: str) -> list[str]:
    """README first, then the numbered notes in name order."""
    directory = ROOT / folder
    if not directory.is_dir():
        raise SystemExit(f"chapter 4 batch is not a directory: {folder}")
    found = sorted(path.relative_to(ROOT).as_posix() for path in directory.glob("*.md"))
    if not found:
        raise SystemExit(f"chapter 4 batch has no notes: {folder}")
    nested = [path for path in directory.rglob("*.md") if path.parent != directory]
    if nested:
        names = ", ".join(path.relative_to(ROOT).as_posix() for path in nested)
        raise SystemExit(f"chapter 4 batch has nested notes: {names}")
    readmes = [rel for rel in found if rel.endswith("/README.md")]
    rest = [rel for rel in found if rel not in readmes]
    return readmes + rest


def load_chapter_04(paths: list[Path]) -> list[Unit]:
    by_rel = {path.relative_to(ROOT).as_posix(): path for path in paths}
    ordered: list[Unit] = []
    seen: list[str] = []
    for kind, payload in CHAPTER_04_READING:
        if kind == "section":
            ordered.append(Unit("", payload))
            continue
        if kind == "batch":
            rels = batch_note_paths(payload)
        elif kind == "note":
            rels = [payload]
        else:
            raise SystemExit(f"bad chapter 4 entry {kind}")
        for rel in rels:
            if rel in seen:
                raise SystemExit(f"chapter 4 lists {rel} twice")
            path = by_rel.get(rel)
            if path is None:
                raise SystemExit(f"chapter 4 lists missing note {rel}")
            seen.append(rel)
            ordered.append(load_md(path))
    extras = sorted(set(by_rel) - set(seen))
    if extras:
        raise SystemExit("chapter 4 order is missing notes:\n" + "\n".join(extras))
    intro = INTROS["04"].strip() + "\n"
    return [Unit("", intro), *ordered]


def collect_units() -> dict[str, list[Unit]]:
    grouped: dict[str, list[Path]] = {key: [] for key, *_ in CHAPTERS}
    seen: set[str] = set()
    for path in sorted(ROOT.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        chapter = chapter_of(rel)
        if chapter is None:
            continue
        if rel in seen:
            raise SystemExit(f"duplicate classification: {rel}")
        seen.add(rel)
        grouped[chapter].append(path)

    units: dict[str, list[Unit]] = {}
    for key, *_ in CHAPTERS:
        paths = grouped[key]

        def by_prefix(*prefixes: str) -> list[Path]:
            chosen = [
                path
                for path in paths
                if path.relative_to(ROOT).as_posix().startswith(prefixes)
            ]
            return sorted(chosen, key=lambda path: path.relative_to(ROOT).as_posix().lower())

        # Chapter 4 is CHAPTER_04_READING, not a path sort. A path sort dumps
        # dated decomp-findings folders between the topical notes.
        if key == "04":
            chapter_units = load_chapter_04(paths)
            units[key] = chapter_units
            notes = sum(1 for unit in chapter_units if unit.label)
            log(f"collect {key}: {notes} notes")
            continue
        if key == "05":
            paths = by_prefix("graal3d/") + by_prefix("torque/")
        elif key == "06":
            paths = by_prefix("tools/") + by_prefix("live-runs/")
        else:
            paths = sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix().lower())
        if key in {"05", "06"} and len(paths) != len(grouped[key]):
            raise SystemExit(f"chapter {key} dropped files while ordering")
        chapter_units = [load_md(path) for path in paths]
        if key == "02":
            chapter_units.extend(man_unit(rel) for rel in FORMAT_MAN)
        if key == "A-npc":
            chapter_units.extend(npc_name_units())
        intro = INTROS.get(key)
        if intro:
            chapter_units.insert(0, Unit("", intro.strip() + "\n"))
        if not chapter_units:
            raise SystemExit(f"chapter {key} has no notes")
        units[key] = chapter_units
        log(f"collect {key}: {len(chapter_units)} sections")
    return units


def npc_name_units() -> list[Unit]:
    groups: dict[tuple[str, str], list[str]] = {}
    for page in sorted((ROOT / "npc-library").rglob("page.json")):
        data = json.loads(page.read_text(encoding="utf-8"))
        genre = str(data.get("genre", ""))
        topic = str(data.get("topic", ""))
        rel = page.relative_to(ROOT).as_posix()
        rows = groups.setdefault((genre, topic), [])
        for index, script in enumerate(data["scripts"], start=1):
            image = str(script.get("image", "")).replace("`", "'").replace("\n", " ").strip()
            sources = script.get("files")
            count = len(sources) if isinstance(sources, list) else 0
            rows.append(f"- `{image}` — {count} source levels — `{rel}` #{index}")
    units: list[Unit] = []
    for genre, topic in sorted(groups):
        lines = sorted(groups[(genre, topic)], key=str.lower)
        body = redact("\n".join(lines) + "\n")
        units.append(Unit(f"npc-library/{genre}/{topic}", body))
    if not units:
        raise SystemExit("NPC name index is empty")
    return units


def assemble(title: str, units: list[Unit]) -> str:
    labels = [unit.label for unit in units if unit.label]
    parts = [f"# {title}", ""]
    if labels:
        parts.append(
            f"This part contains {len(labels)} notes, from `{labels[0]}` "
            f"through `{labels[-1]}`."
        )
        parts.append("")
    for unit in units:
        if unit.label:
            parts.append(f"## `{unit.label}`")
            parts.append("")
        if unit.body.strip():
            parts.append(unit.body.rstrip())
            parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def assert_clean(text: str, label: str) -> None:
    host = "(?:drive|docs)." + "google.com"
    checks = (
        (host, "Drive URL"),
        (r"FUN_[0-9a-fA-F]{6}", "FUN_ name"),
        (r"DAT_[0-9a-fA-F]{6}", "DAT_ name"),
        (r"\b0x00[4-6][0-9a-fA-F]{5}\b", "binary offset"),
        (r"graalonline\.com", "official host"),
        (r"graal\.in\b", "official host"),
        (r"graalreborn\.(?:com|net)", "official host"),
    )
    for pattern, name in checks:
        match = re.search(pattern, text, re.I)
        if match:
            raise SystemExit(f"{label} contains {name}: {match.group(0)}")
    for line in text.splitlines():
        for match in re.finditer(r"\b([0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
            if re.fullmatch(r"[0-9]\.[0-9]+\.[0-9]+\.[0-9]+", match.group(0)):
                continue
            raise SystemExit(f"{label} contains a dotted IP literal: {match.group(0)}")


def page_count(pdf: Path) -> int:
    proc = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"pdfinfo failed for {pdf}")
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    raise SystemExit(f"pdfinfo gave no page count for {pdf}")


_render_cache: dict[str, tuple[int, Path]] = {}


def render(title: str, units: list[Unit]) -> tuple[int, Path]:
    markdown = assemble(title, units)
    assert_clean(markdown, title)
    digest = hashlib.sha256(markdown.encode("utf-8")).hexdigest()[:16]
    cached = _render_cache.get(digest)
    if cached and cached[1].is_file():
        return cached
    md_path = WORK / "md" / f"{digest}.md"
    pdf_path = WORK / "pdf" / f"{digest}.pdf"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown, encoding="utf-8")
    log(f"pandoc {title} ({len(units)} sections, {len(markdown)} bytes)")
    proc = subprocess.run(
        [
            "pandoc",
            str(md_path),
            "-o",
            str(pdf_path),
            "--pdf-engine=weasyprint",
            "--css",
            str(CSS),
            "--metadata",
            f"title={title}",
            "--no-highlight",
            "--resource-path",
            str(ROOT),
            "-f",
            PANDOC_FROM,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or not pdf_path.is_file():
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"pandoc failed for {title}")
    pages = page_count(pdf_path)
    log(f"  {pages} pages")
    _render_cache[digest] = (pages, pdf_path)
    return pages, pdf_path


def split_half(units: list[Unit]) -> tuple[list[Unit], list[Unit]]:
    if len(units) < 2:
        raise SystemExit("cannot split a single section by files")
    total = sum(unit.nbytes for unit in units)
    acc = 0
    for index in range(len(units) - 1):
        acc += units[index].nbytes
        if acc >= total / 2:
            return units[: index + 1], units[index + 1 :]
    return units[:-1], units[-1:]


def split_unit(unit: Unit, pages: int) -> list[Unit]:
    lines = unit.body.splitlines()
    if len(lines) < 2:
        raise SystemExit(
            f"{unit.label or '(intro)'} is {pages} pages and has no split point"
        )
    pieces = max(2, (pages + 79) // 80)
    size = max(1, (len(lines) + pieces - 1) // pieces)
    out: list[Unit] = []
    label = unit.label or "continued"
    for start in range(0, len(lines), size):
        chunk = "\n".join(lines[start : start + size]).strip()
        if not chunk:
            continue
        suffix = "" if start == 0 else f" (continued {start // size + 1})"
        out.append(Unit(f"{label}{suffix}", chunk + "\n"))
    if len(out) < 2:
        raise SystemExit(f"could not split {unit.label}")
    return out


def partition(title: str, units: list[Unit], depth: int = 0) -> list[Piece]:
    if depth > 24:
        raise SystemExit(f"gave up splitting {title}")
    total_bytes = sum(unit.nbytes for unit in units)
    if total_bytes > BYTE_SPLIT and len(units) > 1:
        left, right = split_half(units)
        return partition(title, left, depth + 1) + partition(title, right, depth + 1)
    pages, pdf = render(title, units)
    if pages <= MAX_PAGES:
        return [Piece(units, pages, pdf)]
    if len(units) == 1:
        parts = split_unit(units[0], pages)
        found: list[Piece] = []
        for part in parts:
            found.extend(partition(title, [part], depth + 1))
        return found
    left, right = split_half(units)
    return partition(title, left, depth + 1) + partition(title, right, depth + 1)


def pack(pieces: list[Piece]) -> list[list[Unit]]:
    groups: list[list[Unit]] = []
    current: list[Unit] = []
    current_pages = 0
    for piece in pieces:
        if current and current_pages + piece.pages > MERGE_CAP:
            groups.append(current)
            current = []
            current_pages = 0
        current.extend(piece.units)
        current_pages += piece.pages
    if current:
        groups.append(current)
    return groups


def attach_section_heads(groups: list[list[Unit]]) -> list[list[Unit]]:
    """Keep an unlabeled heading with the notes that follow it.

    Chapter 4 inserts unlabeled section headings. A byte split can leave a
    heading as the last unit of a part. Move trailing headings onto the next
    part. Note order is unchanged.
    """
    moved: list[list[Unit]] = []
    carry: list[Unit] = []
    for group in groups:
        group = carry + list(group)
        carry = []
        # A heading-only group stays put. Pulling it onto the next group
        # undoes a split of one large note and the fitter loops.
        if any(unit.label for unit in group):
            while group and group[-1].label == "":
                carry.insert(0, group.pop())
        if group:
            moved.append(group)
    if carry:
        if moved:
            moved[-1].extend(carry)
        else:
            moved.append(carry)
    return moved


def fit(title_base: str, groups: list[list[Unit]]) -> list[tuple[str, int, Path, list[Unit]]]:
    pending = attach_section_heads(groups)
    for _ in range(40):
        count = len(pending)
        rendered: list[tuple[str, int, Path, list[Unit]]] = []
        overflow: int | None = None
        for index, group in enumerate(pending, start=1):
            title = title_base if count == 1 else f"{title_base}, part {index} of {count}"
            pages, pdf = render(title, group)
            rendered.append((title, pages, pdf, group))
            if pages > MAX_PAGES and overflow is None:
                overflow = index - 1
        if overflow is None:
            return rendered
        group = pending[overflow]
        log(f"resplit {title_base} group {overflow + 1} ({rendered[overflow][1]} pages)")
        if len(group) == 1:
            replacement = [[unit] for unit in split_unit(group[0], rendered[overflow][1])]
        else:
            left, right = split_half(group)
            replacement = [left, right]
        pending = attach_section_heads(
            pending[:overflow] + replacement + pending[overflow + 1 :]
        )
    raise SystemExit(f"could not fit {title_base} under {MAX_PAGES} pages")


def scan_pdf(pdf: Path) -> None:
    proc = subprocess.run(
        ["pdftotext", str(pdf), "-"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"pdftotext failed for {pdf}")
    assert_clean(proc.stdout, pdf.name)


def slug_for(parts: list[tuple[str, int, Path, list[Unit]]], slug: str) -> list[tuple[str, str, int, Path, list[Unit]]]:
    named = []
    count = len(parts)
    for index, (title, pages, pdf, units) in enumerate(parts, start=1):
        filename = f"{slug}.pdf" if count == 1 else f"{slug}-part-{index}.pdf"
        named.append((filename, title, pages, pdf, units))
    return named


RowMeta = tuple[str, str, str, int, str, int, list[str]]


def assemble_contents(rows: list[RowMeta], commit: str) -> str:
    lines = [
        f"# {CONTENTS_TITLE}",
        "",
        "Reading order for the chapter and appendix PDFs in this folder.",
        "",
        f"Built from commit `{commit}`.",
        "",
        "The notes viewer is in the source tree, not a separate download:",
        "`python3 tools/navigator/navigator.py` on loopback port 8765 (no venv).",
        "",
        "| Kind | # | PDF | Title | Pages |",
        "| --- | ---: | --- | --- | ---: |",
    ]
    total_pages = 0
    for kind, number, filename, title, pages, _part_title, _labels in rows:
        total_pages += pages
        lines.append(
            f"| {kind} | {number} | `{filename}` | {title} | {pages} |"
        )
    lines.append("")
    lines.append(
        f"{len(rows)} PDFs, {total_pages} pages. Each PDF is at most 100 pages."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_readme(rows: list[RowMeta], commit: str) -> None:
    lines = [
        "# Graal Analysis 0.0.1",
        "",
        "Document PDFs of the notes. Chiaki tags `v0.0.1`.",
        "Start with `ch-00-contents.pdf`.",
        "",
        "The notes viewer is part of the source tree at `tools/navigator/`.",
        "After `git pull` of the tagged source:",
        "`python3 tools/navigator/navigator.py` on loopback port 8765 (no venv).",
        "",
        f"Built from commit `{commit}`.",
        "Page counts below are `pdfinfo` measurements of the PDFs in this folder.",
        "`tools/release/build_book.py` writes this list.",
        "",
        "| Kind | # | PDF | Title | Pages | Sections |",
        "| --- | ---: | --- | --- | ---: | ---: |",
    ]
    total_pages = 0
    for kind, number, filename, title, pages, _part_title, labels in rows:
        total_pages += pages
        lines.append(
            f"| {kind} | {number} | `{filename}` | {title} | {pages} | {len(labels)} |"
        )
    lines.append("")
    lines.append(
        f"{len(rows)} PDFs, {total_pages} pages. Each PDF is at most 100 pages."
    )
    lines.append("")
    lines.append("## What each PDF contains")
    lines.append("")
    for kind, number, filename, title, pages, part_title, labels in rows:
        lines.append(f"### {kind} {number}: `{filename}`")
        lines.append("")
        lines.append(f"{part_title}. {pages} pages.")
        lines.append("")
        if not labels:
            lines.append("- (introductory text only)")
        for label in labels:
            lines.append(f"- `{label}`")
        lines.append("")
    (OUT_DIR / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def git_commit() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def table_stats(text: str) -> tuple[int, int]:
    count = 0
    pages = 0
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("| Kind") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        pages += int(cells[4])
        count += 1
    if count == 0:
        raise SystemExit("release table has no rows")
    return count, pages


def rewrite_total(text: str) -> str:
    count, pages = table_stats(text)
    new = f"{count} PDFs, {pages} pages. Each PDF is at most 100 pages."
    updated, found = re.subn(
        r"^\d+ PDFs, \d+ pages\. Each PDF is at most 100 pages\.$",
        new,
        text,
        count=1,
        flags=re.M,
    )
    if found != 1:
        raise SystemExit("page-total line missing")
    return updated


def replace_slug_table_rows(text: str, slug: str, new_rows: list[str]) -> str:
    lines = text.splitlines()
    indexes = [i for i, line in enumerate(lines) if line.startswith("|") and slug in line]
    if not indexes:
        raise SystemExit(f"no table rows for {slug}")
    if indexes != list(range(indexes[0], indexes[-1] + 1)):
        raise SystemExit(f"table rows for {slug} are not contiguous")
    out = lines[: indexes[0]] + new_rows + lines[indexes[-1] + 1 :]
    return "\n".join(out) + "\n"


def detail_block(rows: list[RowMeta]) -> str:
    lines: list[str] = []
    for kind, number, filename, _title, pages, part_title, labels in rows:
        lines.append(f"### {kind} {number}: `{filename}`")
        lines.append("")
        lines.append(f"{part_title}. {pages} pages.")
        lines.append("")
        if not labels:
            lines.append("- (introductory text only)")
        for label in labels:
            lines.append(f"- `{label}`")
        lines.append("")
    return "\n".join(lines)


def replace_detail(text: str, kind: str, number: int, next_heading: str, block: str) -> str:
    heading = f"### {kind} {number}:"
    start = text.find(heading)
    if start < 0:
        raise SystemExit(f"missing detail heading {heading}")
    end = text.find(next_heading, start + len(heading))
    if end < 0:
        raise SystemExit(f"missing heading after {heading}")
    return text[:start] + block.rstrip() + "\n\n" + text[end:]


def readme_table_row(row: RowMeta) -> str:
    kind, number, filename, title, pages, _part_title, labels = row
    return f"| {kind} | {number} | `{filename}` | {title} | {pages} | {len(labels)} |"


def contents_table_row(row: RowMeta) -> str:
    kind, number, filename, title, pages, _part_title, _labels = row
    return f"| {kind} | {number} | `{filename}` | {title} | {pages} |"


def set_contents_pages(text: str, pages: int) -> str:
    pattern = r"(\| Contents \| 0 \| `ch-00-contents\.pdf` \| Contents \| )\d+( \|)"
    updated, found = re.subn(pattern, rf"\g<1>{pages}\2", text, count=1)
    if found != 1:
        raise SystemExit("contents row missing from the release README")
    return updated


def publish_one(key: str) -> None:
    """Rebuild one chapter's PDFs and its rows in the release lists."""
    chosen = [item for item in CHAPTERS if item[0] == key]
    if len(chosen) != 1:
        raise SystemExit(f"unknown chapter key {key}")
    _key, slug, title, kind, number = chosen[0]
    following = [item for item in CHAPTERS if item[4] == number + 1 and item[3] == kind]
    if not following:
        raise SystemExit(f"no following {kind} after {number}; --only cannot patch the list")
    next_heading = f"### {following[0][3]} {following[0][4]}:"
    units = collect_units()[key]
    log(f"== {title}")
    pieces = partition(title, units)
    groups = pack(pieces)
    fitted = fit(title, groups)
    rows: list[RowMeta] = []
    written: set[str] = set()
    for filename, part_title, pages, pdf, group in slug_for(fitted, slug):
        if pages > MAX_PAGES:
            raise SystemExit(f"{filename} is {pages} pages")
        scan_pdf(pdf)
        target = OUT_DIR / filename
        shutil.copyfile(pdf, target)
        committed = page_count(target)
        if committed != pages:
            raise SystemExit(f"{filename} page count changed on copy: {pages} vs {committed}")
        if committed > MAX_PAGES:
            raise SystemExit(f"{filename} is {committed} pages")
        labels = [unit.label for unit in group if unit.label]
        rows.append((kind, number, filename, title, committed, part_title, labels))
        written.add(filename)
        log(f"wrote {filename} ({committed} pages)")
    for old in OUT_DIR.glob(slug + "*.pdf"):
        if old.name not in written:
            old.unlink()
            log(f"removed {old.name}")
    readme_path = OUT_DIR / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_slug_table_rows(readme, slug, [readme_table_row(row) for row in rows])
    readme = replace_detail(readme, kind, number, next_heading, detail_block(rows))
    readme = rewrite_total(readme)
    contents_path = OUT_DIR / "contents.md"
    contents = contents_path.read_text(encoding="utf-8")
    contents = replace_slug_table_rows(contents, slug, [contents_table_row(row) for row in rows])
    contents = rewrite_total(contents)
    assert_clean(contents, CONTENTS_TITLE)
    contents_path.write_text(contents, encoding="utf-8")
    c_pages, c_pdf = render(CONTENTS_TITLE, [Unit("release/0.0.1/contents.md", contents)])
    if c_pages > MAX_PAGES:
        raise SystemExit(f"{CONTENTS_SLUG}.pdf is {c_pages} pages")
    scan_pdf(c_pdf)
    contents_target = OUT_DIR / f"{CONTENTS_SLUG}.pdf"
    shutil.copyfile(c_pdf, contents_target)
    c_committed = page_count(contents_target)
    if c_committed != c_pages:
        raise SystemExit(
            f"{CONTENTS_SLUG}.pdf page count changed on copy: {c_pages} vs {c_committed}"
        )
    readme = set_contents_pages(readme, c_committed)
    readme = rewrite_total(readme)
    assert_clean(readme, "release README")
    readme_path.write_text(readme, encoding="utf-8")
    log(f"wrote {CONTENTS_SLUG}.pdf ({c_committed} pages)")
    log("done")


def main() -> None:
    only: str | None = None
    if len(sys.argv) == 3 and sys.argv[1] == "--only":
        only = sys.argv[2]
    elif len(sys.argv) != 1:
        raise SystemExit("usage: python3 tools/release/build_book.py [--only KEY]")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    missing = [cmd for cmd in ("pandoc", "weasyprint", "pdfinfo", "pdftotext") if shutil.which(cmd) is None]
    if missing:
        raise SystemExit("missing tools: " + ", ".join(missing))
    if only is not None:
        publish_one(only)
        return
    units = collect_units()
    commit = git_commit()
    staged: list[tuple[str, int, str, str, int, str, Path, list[str]]] = []
    for key, slug, title, kind, number in CHAPTERS:
        log(f"== {title}")
        pieces = partition(title, units[key])
        groups = pack(pieces)
        fitted = fit(title, groups)
        for filename, part_title, pages, pdf, group in slug_for(fitted, slug):
            if pages > MAX_PAGES:
                raise SystemExit(f"{filename} is {pages} pages")
            scan_pdf(pdf)
            labels = [unit.label for unit in group if unit.label]
            staged.append(
                (kind, number, filename, title, pages, part_title, pdf, labels)
            )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.pdf"):
        old.unlink()
    readme_rows: list[RowMeta] = []
    for kind, number, filename, book_title, pages, part_title, pdf, labels in staged:
        target = OUT_DIR / filename
        shutil.copyfile(pdf, target)
        # Measure the file that will be committed, not the build cache.
        committed_pages = page_count(target)
        if committed_pages != pages:
            raise SystemExit(
                f"{filename} page count changed on copy: {pages} vs {committed_pages}"
            )
        readme_rows.append(
            (
                kind,
                number,
                filename,
                book_title,
                committed_pages,
                part_title,
                labels,
            )
        )
        log(f"wrote {filename} ({committed_pages} pages)")
    contents_md = assemble_contents(readme_rows, commit)
    assert_clean(contents_md, CONTENTS_TITLE)
    contents_path = OUT_DIR / "contents.md"
    contents_path.write_text(contents_md, encoding="utf-8")
    contents_units = [Unit("release/0.0.1/contents.md", contents_md)]
    c_pages, c_pdf = render(CONTENTS_TITLE, contents_units)
    if c_pages > MAX_PAGES:
        raise SystemExit(f"{CONTENTS_SLUG}.pdf is {c_pages} pages")
    scan_pdf(c_pdf)
    contents_filename = f"{CONTENTS_SLUG}.pdf"
    contents_target = OUT_DIR / contents_filename
    shutil.copyfile(c_pdf, contents_target)
    c_committed = page_count(contents_target)
    if c_committed != c_pages:
        raise SystemExit(
            f"{contents_filename} page count changed on copy: {c_pages} vs {c_committed}"
        )
    readme_rows.insert(
        0,
        (
            "Contents",
            0,
            contents_filename,
            "Contents",
            c_committed,
            CONTENTS_TITLE,
            ["release/0.0.1/contents.md"],
        ),
    )
    log(f"wrote {contents_filename} ({c_committed} pages)")
    write_readme(readme_rows, commit)
    assert_clean((OUT_DIR / "README.md").read_text(encoding="utf-8"), "release README")
    log("done")


if __name__ == "__main__":
    main()
