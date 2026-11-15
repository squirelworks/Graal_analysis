"""Research-data regressions, not client protocol/runtime tests."""
import importlib.util
import re
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("token_map_generator", Path(__file__).with_name("generate.py"))
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)
ROWS = GEN.parse(GEN.SOURCE.read_text(encoding="utf-8"))


def matching(token, role=None):
    return [r for r in ROWS if r["token"] == token and (role is None or r["role"] == role)]


class TokenMapDataTests(unittest.TestCase):
    def test_shared_graal2002_versions_do_not_collapse_or_inherit_wire_grade(self):
        older = [r for r in matching("GNW03081") if "Graal 2002 ver" in r["build"]]
        assert len(older) == 3 and {r["grade"] for r in older} == {"B"}
        newer = matching("GNW31101", "game-login")
        assert len(newer) == 4
        assert [r["grade"] for r in newer if "ver10" in r["build"]] == ["W"]
        assert {r["grade"] for r in newer if "ver10" not in r["build"]} == {"B"}
        assert any("public release" in r["build"] for r in newer)
        assert any(r["grade"] == "W" and "2.05 rev2" in r["build"] for r in matching("GNW03081"))


    def test_same_version_field_and_same_token_are_not_unique_identity(self):
        same_version = [r for r in ROWS if "FileVersion 1.3.9.1" in r["build"]]
        assert {r["token"] for r in same_version} == {"GNW07080", "GNW23090"}
        assert {r["grade"] for r in matching("GSERV014", "game-login")} == {"W"}
        assert {r["grade"] for r in matching("GSERV014", "rc-login")} == {"B"}
        assert {r["platform"] for r in matching("GSERV025")} == {"Windows", "Linux"}


    def test_mobile_source_coverage_and_unresolved_apps(self):
        recovered = [r for r in ROWS if r["platform"] == "iOS" and r["role"] == "game-login" and r["grade"] == "B"]
        assert len(recovered) == 23
        assert len([r for r in recovered if r["token"] == "G3D04048"]) == 16
        assert len([r for r in recovered if r["token"] == "G3D18010"]) == 6
        assert len([r for r in recovered if r["token"] == "G3D0208A"]) == 1
        assert any("Belote (Expert Online) 1.50" in r["build"] for r in matching("G3D04048"))
        unknown = [r for r in ROWS if r["platform"] == "iOS" and r["state"] == "unresolved"]
        assert len(unknown) == 3
        assert all(r["grade"] == "L" for r in matching("G3D29090"))
        assert all("Belote 1.50" not in r["build"] for r in matching("G3D2504D"))


    def test_service_and_connector_evidence_is_not_fixed_game_login(self):
        assert {r["role"] for r in matching("newmain")} == {"list-service"}
        assert {r["role"] for r in matching("GNW30123")} == {"list-login"}
        assert {r["grade"] for r in matching("G3D2304D")} == {"C"}
        assert {r["grade"] for r in matching("Graal/6.77")} == {"B", "W"}
        assert {(r["grade"], r["role"], r["platform"]) for r in matching("Graal/6.111")} == {("W", "http-user-agent", "macOS")}
        assert not any(r["token"].startswith(("g3d", "gnp")) for r in ROWS)
        assert not matching("NW01") and not matching("GSERVL01")


    def test_generated_views_are_current_and_keep_all_associations(self):
        human, data = GEN.render(ROWS)
        assert GEN.MAP.read_text(encoding="utf-8") == human
        assert GEN.DATA.read_text(encoding="utf-8") == data
        assert len({(r["token"], r["state"], r["build"], r["platform"], r["role"]) for r in ROWS}) == len(ROWS)

    def test_same_build_name_can_keep_distinct_platform_associations(self):
        table = "### Family\n| " + " | ".join(GEN.HEADER) + " |\n"
        row = "| Shared build | `GNW03081` | B | public source | {} | game-login | | |\n"
        assert len(GEN.parse(table + row.format("Windows") + row.format("Linux"))) == 2
        with self.assertRaisesRegex(ValueError, "duplicate association"):
            GEN.parse(table + row.format("Windows") * 2)


    def test_all_public_markdown_source_links_resolve_including_fragments(self):
        texts = [(GEN.SOURCE, GEN.SOURCE.read_text(encoding="utf-8")),
                 (GEN.MAP, GEN.MAP.read_text(encoding="utf-8"))]
        for parent, text in texts:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target:
                    continue
                name, _, fragment = target.partition("#")
                path = (parent.parent / name).resolve() if name else parent
                assert path.is_file(), (parent.name, target)
                if fragment and path.suffix == ".md":
                    headings = {GEN.anchor(line.lstrip("# ")) for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("#")}
                    assert fragment in headings, (parent.name, target)


if __name__ == "__main__":
    unittest.main()
