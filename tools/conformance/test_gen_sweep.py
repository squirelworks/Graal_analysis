"""Tests for gen_sweep.py: the surface is read whole, the generated probes and
cases are current, and the extractor classifies reports as documented."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_sweep as gs  # noqa: E402


def test_surface_is_read_whole():
    parents, members = gs.read_surface()
    assert len(parents) == 35
    assert sum(len(m) for m in members.values()) == 418


def test_generated_files_are_current():
    for p, text in gs.generated().items():
        assert p.exists() and p.read_text(encoding="utf-8") == text, f"stale: {p} (run gen_sweep.py gen)"


def test_every_member_is_in_the_manifest_once():
    _p, members = gs.read_surface()
    rows = gs.manifest_rows(members)
    keys = [(r[1], r[2]) for r in rows if r[3] in ("prop", "func")]
    assert len(keys) == len(set(keys)) == 418


def test_classify():
    c = gs.classify
    assert c("prop", "float rw", "d=0|w=0.5|j=0", False) == "works"
    assert c("prop", "float rw", "d=0|w=0|j=0", False) == "inert"
    assert c("prop", "float rw", "d=|w=0.5|j=zz", False) == "absent"
    assert c("prop", "string ro", "d=1 2 3", False) == "readonly"
    assert c("prop", "string ro", "d=", False) == "absent"
    assert c("func", "() -> void", "r=", False) == "ran"
    assert c("func", "(string) -> float", "r=12.5", False) == "works"
    assert c("func", "(int) -> object", "r=null", False) == "inert"
    assert c("func", "() -> string", "r=", False) == "absent"
    assert c("func", "() -> string", None, False) == "unrun"
    assert c("func", "() -> string", None, True) == "crash"
    assert c("prop", "int rw", "skip", False) == "skip"


def test_extract_on_a_fake_run(tmp_path):
    out = tmp_path / "5.12"
    d = out / "C049"
    d.mkdir(parents=True)
    d.joinpath("gserver.log").write_text(
        'trigger sent ("gui", "ConfProbe", "cf", "made", "1")\n'
        'trigger sent ("gui", "ConfProbe", "cf", "GameObject.alpha", "d=1|w=0.5|j=0")\n'
        'trigger sent ("gui", "ConfProbe", "cf", "done", "1")\n')
    results, summary = gs.extract([("5.12", out)])
    alpha = [r for r in results if r["class"] == "GameObject" and r["member"] == "alpha"][0]
    assert alpha["verdict"] == "works"
    assert summary["5.12"]["works"] >= 1


def test_extract_marks_a_crash_before_the_first_report(tmp_path):
    out = tmp_path / "5.12"
    d = out / "C054"
    d.mkdir(parents=True)
    d.joinpath("gserver.log").write_text('trigger sent ("gui", "ConfProbe", "cf", "made", "1")\n')
    results, _summary = gs.extract([("5.12", out)])
    c054 = [r for r in results if r["class"] == "TerrainEditor"]
    assert c054[0]["member"] == "@inst" and c054[0]["verdict"] == "crash"
    assert all(r["verdict"] == "unrun" for r in c054[1:])


def test_a_skipped_instance_touches_no_member():
    _p, members = gs.read_surface()
    for key in gs.SKIP:
        cls, member = key.split(".", 1)
        if member != "@inst":
            continue
        text = gs.gs2_class(cls, members[cls])
        assert "new " not in text and f'cf("{cls}.@inst", "skip");' in text
        assert text.count('"skip");') == len(members[cls]) + 1
