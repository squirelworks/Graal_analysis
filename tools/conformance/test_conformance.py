"""Tests for the 3D conformance suite (no client, no VM): python3 -m pytest tools/conformance -q"""

from __future__ import annotations

import re
import struct
import sys
import tomllib
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import conformance as cf  # noqa: E402
import gen_content  # noqa: E402
import run  # noqa: E402

KNOWN_EXTRA_BUILDS = {"4.20r6L", "6.037F"}


@pytest.fixture(scope="module")
def cases():
    return cf.load_cases()


def test_cases_load_and_have_unique_ids(cases):
    assert len(cases) >= 15
    assert len({c.id for c in cases}) == len(cases)
    assert len({c.slug for c in cases}) == len(cases)


def test_every_row_is_on_the_board(cases):
    ids = cf.board_ids()
    for c in cases:
        for r in c.rows:
            assert r in ids, f"{c.id}: {r} is not on the board"


def test_builds_are_known(cases):
    for c in cases:
        for b in c.expect:
            assert b in cf.CORE_BUILDS or b in KNOWN_EXTRA_BUILDS, f"{c.id}: unknown build {b}"


def test_every_expectation_names_a_source(cases):
    for c in cases:
        for b, e in c.expect.items():
            assert e["source"].strip(), f"{c.id} {b}"


def test_scripts_exist_and_probe_cases_check_compilation(cases):
    for c in cases:
        for s in c.scripts:
            assert (cf.SCRIPTS / s).exists(), s
            assert "//#CLIENTSIDE" in (cf.SCRIPTS / s).read_text()
        if c.scripts:
            assert "compiled" in {k.id for k in c.checks}, c.id
            for b, e in c.expect.items():
                assert e.get("compiled") is False, f"{c.id} {b}: compiled must be false"


def test_probe_scripts_report_only_comma_free_values():
    for p in cf.SCRIPTS.glob("*.gs2"):
        for m in re.finditer(r'cf\("([^"]+)",\s*"([^"]*)"\)', p.read_text()):
            assert "," not in m.group(1) + m.group(2), p.name


def fake_pack(tmp_path):
    """A stand-in content pack: a .dts (version 24, exporter word 7) and a .dif (44)."""
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "shape.dts").write_bytes(struct.pack("<HH", 24, 7) + b"body")
    (pack / "room.dif").write_bytes(struct.pack("<I", 44) + b"body")
    return {"mbg": pack}


def test_build_world_writes_the_overlay(cases, tmp_path):
    packs = fake_pack(tmp_path)
    for c in cases:
        root = cf.build_world(c, tmp_path / "out", packs)
        world = (root / "config" / "graal3dworld.txt").read_text()
        for s in c.scripts:
            assert f"weapon3d {cf.PROBE_WEAPON} conf/{s}" in world
            assert (root / "conf" / s).exists()
        add = (root / "config" / "server.add").read_text()
        trace = "graal3dtrace = g3d.tsv" if c.server_kind == "v2" else "graal3d_trace = g3d.tsv"
        assert "graal3d = true" in add and trace in add
        assert f"name = {c.lobby_name}" in add
        # every shape and sky texture the world names is served
        served = {p.name for p in (root / "files").iterdir()}
        for line in world.splitlines():
            w = line.split()
            if w and w[0] in ("object", "playershape"):
                shape = w[2] if w[0] == "object" else w[1]
                if shape.startswith("conf_missing"):
                    continue   # left out on purpose (C022)
                assert shape in served, f"{c.id}: {shape}"
            if w and w[0] == "terrain":
                assert len(list((root / w[1]).glob("heights*-*.dat"))) == 256, c.id
                assert "heights.info" in served
                for tex in (root / "files" / "heights.info").read_text().split():
                    assert tex in served, f"{c.id}: {tex}"
            if w and w[0] == "water" and len(w) > 7:
                assert any(n.startswith(w[7]) for n in served), f"{c.id}: {w[7]}"
            if w and w[0] == "sky":
                for t in w[1].split(","):
                    assert f"{t}.png" in served and f"{t}.gif" in served, f"{c.id}: {t}"


def test_expected_table_is_current(cases):
    text = cf.expected_table(cases)
    on_disk = (cf.SUITE / "EXPECTED.md").read_text(encoding="utf-8")
    assert text == on_disk, "run: python3 tools/conformance/conformance.py expected --write"


def test_results_table_is_current(cases):
    text = cf.results_table(cf.SUITE / "results.tsv", cases)
    on_disk = (cf.SUITE / "RESULTS.md").read_text(encoding="utf-8")
    assert text == on_disk, "run: python3 tools/conformance/conformance.py table torque/conformance/results.tsv --write"


def test_derived_versions(cases, tmp_path):
    packs = fake_pack(tmp_path)
    root = cf.build_world(case(cases, "C016"), tmp_path / "out", packs)
    v = {n: struct.unpack("<HH", (root / "files" / n).read_bytes()[:4]) for n in
         ("conf_v16.dts", "conf_v24.dts", "conf_v25.dts")}
    assert v == {"conf_v16.dts": (16, 7), "conf_v24.dts": (24, 7), "conf_v25.dts": (25, 7)}
    root = cf.build_world(case(cases, "C017"), tmp_path / "out", packs)
    assert struct.unpack("<I", (root / "files" / "conf_v45.dif").read_bytes()[:4]) == (45,)
    with pytest.raises(cf.CaseError):
        cf.build_world(case(cases, "C016"), tmp_path / "out2", {})


# ------------------------------------------------------------------ content

def test_3ds_chunk_trees_are_well_formed():
    files = gen_content.files()
    red = gen_content.chunk_ids(files["conf_red.3ds"])
    assert red[0] == 0x4D4D and 0xAFFF in red and 0x4130 in red and 0x4140 not in red
    nomat = gen_content.chunk_ids(files["conf_nomat.3ds"])
    assert 0xAFFF not in nomat and 0x4130 not in nomat and 0x4120 in nomat
    tex = gen_content.chunk_ids(files["conf_tex.3ds"])
    assert 0xA300 in tex and 0x4140 in tex
    assert b"conf_tex.png\0" in files["conf_tex.3ds"]


def test_flat_terrain_chunk_decodes():
    import zlib
    raw = zlib.decompress(gen_content.flat_chunk())
    bits = "".join(f"{b:08b}"[::-1] for b in raw)   # LSB first
    def field(at, n):
        return int(bits[at:at + n][::-1], 2)
    assert field(0, 8) == 0 and field(8, 16) == 0          # mode, h0
    assert set(bits[24:24 + 2048]) == {"0"}                # 256 zero deltas
    assert field(24 + 2048, 6) == 1 and field(30 + 2048, 5) == 0  # one material, id 0
    assert len(gen_content.flat_terrain()) == 256


def test_images():
    files = gen_content.files()
    p = files["conf_tex.png"]
    assert p[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", p[16:24]) == (256, 256)
    g = files["conf_sky0.gif"]
    assert g[:6] == b"GIF87a" and g[-1:] == b";"
    assert g[13:16] == bytes(gen_content.SKY_COLOURS[0])
    assert len({files[f"conf_sky{i}.png"] for i in range(6)}) == 6


# ------------------------------------------------------------------ judging

def ppm(path: Path, w: int, h: int, fill, box=None, box_colour=(0, 0, 0)):
    pix = bytearray(bytes(fill) * (w * h))
    if box:
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                pix[(y * w + x) * 3:(y * w + x) * 3 + 3] = bytes(box_colour)
    path.write_bytes(f"P6\n# test\n{w} {h}\n255\n".encode() + bytes(pix))


def test_colour_fraction(tmp_path):
    p = tmp_path / "s.ppm"
    ppm(p, 100, 100, (10, 10, 10), (0, 0, 50, 100), (220, 0, 0))
    assert abs(cf.colour_fraction(p, (220, 0, 0), 30) - 0.5) < 0.02
    assert cf.colour_fraction(p, (0, 255, 0), 30) == 0.0


def _run(tmp_path, *, log="", trace="", console="", tasks="", shot=None):
    (tmp_path / "gserver.log").write_text(log)
    if trace is not None:
        (tmp_path / "g3d.tsv").write_text(trace)
    (tmp_path / "console.txt").write_text(console)
    (tmp_path / "tasks.txt").write_text(tasks)
    if shot:
        ppm(tmp_path / "shot.ppm", 64, 48, *shot)
    return tmp_path


def case(cases, cid):
    return next(c for c in cases if c.id == cid)


def test_colour_blobs(tmp_path):
    p = tmp_path / "s.ppm"
    w, h = 80, 60
    pix = bytearray(bytes((0, 0, 0)) * (w * h))
    for (x0, y0) in ((10, 10), (50, 30)):
        for y in range(y0, y0 + 14):
            for x in range(x0, x0 + 14):
                pix[(y * w + x) * 3:(y * w + x) * 3 + 3] = bytes((220, 0, 0))
    p.write_bytes(f"P6 {w} {h} 255\n".encode() + bytes(pix))
    sizes = cf.colour_blobs(p, (220, 0, 0), 30, 10)
    assert len(sizes) == 2 and sizes[0] == 49


def test_two_client_checks_read_client_two(cases, tmp_path):
    c = case(cases, "C020")
    d = _run(tmp_path, trace="1\tpc:2\t24\tlinked from lab (5.x); 1 other 3D players; spawn 2,0,1\n",
             tasks="Graal.exe\n")
    (d / "c2").mkdir()
    (d / "c2" / "tasks.txt").write_text("")
    v = cf.judge(c, "5.12", d, "Graal.exe")
    assert v["checks"]["second_links"]["observed"] is True
    assert v["checks"]["c1_alive"]["observed"] is True and v["checks"]["c2_alive"]["observed"] is False


def test_judge_link_pass_and_fail(cases, tmp_path):
    c = case(cases, "C001")
    good = _run(tmp_path, log="[ 1.0] peer guest logged in as player 1\nGraal3D: pc:1: control object delivered (seq 3)\n",
                trace="17636\tpc:1\t24\tlinked from lab (4.20r8, 5.x); 0 other 3D players\n",
                console="Graal has been activated!\n", tasks="Graal.exe   1234 Console\n")
    v = cf.judge(c, "5.12", good, "Graal.exe")
    assert v["verdict"] == "PASS", v
    assert v["checks"]["activated"]["expected"] == "?" and v["checks"]["activated"]["observed"] is True
    v = cf.judge(c, "4.04r2", good, "Graal.exe")
    assert v["verdict"] == "FAIL" and set(v["mismatches"]) == {"protocol19", "protocol24"}


def test_judge_missing_artefact_is_error(cases, tmp_path):
    c = case(cases, "C005")
    d = _run(tmp_path, log="file conf_red.3ds: sent\n", tasks="Graal.exe\n")
    v = cf.judge(c, "5.12", d, "Graal.exe")
    assert v["verdict"] == "ERROR" and v["missing"] == ["red_drawn"]
    ppm(d / "shot.ppm", 64, 48, (255, 255, 0), (20, 20, 30, 30), (220, 0, 0))
    assert cf.judge(c, "5.12", d, "Graal.exe")["verdict"] == "PASS"


def test_judge_probe(cases, tmp_path):
    c = case(cases, "C008")
    d = _run(tmp_path, log=("Graal3D: player 1: trigger ignored (gui,ConfProbe,cf,ready,1)\n"
                            "Graal3D: player 1: trigger ignored (gui,ConfProbe,cf,tick,5)\n"))
    assert cf.judge(c, "5.12", d)["verdict"] == "PASS"
    (d / "gserver.log").write_text("Graal3D: weapon3d ConfProbe: not compiled (x); sending the source\n")
    v = cf.judge(c, "5.12", d)
    assert v["verdict"] == "FAIL" and set(v["mismatches"]) == {"compiled", "ready", "tick"}


def test_probe_values_take_quoted_fields():
    log = 'trigger ignored ("gui","ConfProbe","cf","tv3_delta","6")\ntrigger ignored (gui,ConfProbe,cf,tv3_delta,7)'
    assert cf.probe_values(log, "tv3_delta") == ["6", "7"]


def test_no_trace_file_means_no_link(cases, tmp_path):
    c = case(cases, "C002")
    d = _run(tmp_path, log="[1.0] peer guest logged in as player 1\n", trace=None, tasks="Graal.exe\n")
    assert cf.judge(c, "5.12", d, "Graal.exe")["verdict"] == "PASS"


def test_results_round_trip(cases, tmp_path):
    tsv = tmp_path / "results.tsv"
    c = case(cases, "C002")
    d = _run(tmp_path, log="logged in as player 1\n", trace=None, tasks="Graal.exe\n")
    cf.append_result(tsv, cf.judge(c, "5.12", d, "Graal.exe"), "2026-11-26", "gs", "5.12 Windows")
    cf.append_result(tsv, cf.judge(c, "3.153", d, "Graal.exe"), "2026-11-26", "gs", "3.153")
    table = cf.results_table(tsv, cases)
    row = next(line for line in table.splitlines() if line.startswith("| [C002]"))
    assert "PASS (2026-11-26)" in row
    assert "udp_link=no" in tsv.read_text()   # the 3.153 "?" observation is recorded


# ------------------------------------------------------------------ runner

def test_lab_example_parses_and_plans(cases):
    conf = tomllib.loads((HERE / "lab.example.toml").read_text())
    todo = run.plan(conf, cases, list(conf["builds"]))
    assert {b for b, _ in todo} == {"3.153", "4.04r2", "4.20r8", "5.12", "6.037"}
    # two-client cases only where the build names a pair VM
    assert {b for b, c in todo if c.clients == 2} == {"5.12"}
    # pack cases only with the pack configured
    no_packs = dict(conf, packs={})
    assert not [c for _, c in run.plan(no_packs, cases, list(conf["builds"])) if c.needs]
    for b, c in todo:
        assert b in c.expect
        assert conf["builds"][b]["vm"] in conf["client_vms"]
    # priority 1 cases first within each build
    for b in conf["builds"]:
        pr = [c.priority for bb, c in todo if bb == b]
        assert pr == sorted(pr)


def test_vm_command_lines_stay_on_the_lab_link(tmp_path):
    conf = tomllib.loads((HERE / "lab.example.toml").read_text())
    lab_conf = conf["client_vms"]["win10"]
    vm = run.Vm("w", lab_conf, tmp_path, (tmp_path / "a.sock", tmp_path / "b.sock"))
    argv = " ".join(vm.argv())
    assert "dgram,id=lab,local.type=unix" in argv
    assert "user," not in argv          # the Windows client has no other NIC
    srv = run.Vm("s", conf["server_vm"], tmp_path, (tmp_path / "b.sock", tmp_path / "a.sock"))
    argv = " ".join(srv.argv())
    assert re.search(r"user,id=mgmt,restrict=on(,net=[^,]*)?,hostfwd=tcp:", argv)
    assert "id=lab2" not in argv             # no second socket pair given
    srv2 = run.Vm("s", conf["server_vm"], tmp_path, (tmp_path / "b.sock", tmp_path / "a.sock"),
                  (tmp_path / "d.sock", tmp_path / "c.sock"))
    assert "netdev=lab2,mac=" in " ".join(srv2.argv())


def test_png_to_ppm_unfilters(tmp_path):
    import zlib as z
    w, h = 3, 2
    rows = [bytes([1, 10, 20, 30, 255, 5, 5, 5, 0, 1, 1, 1, 0]),       # Sub, RGBA
            bytes([2, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 0])]            # Up
    def chunk(k, b):
        return struct.pack(">I", len(b)) + k + b + struct.pack(">I", z.crc32(k + b))
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", z.compress(b"".join(rows))) + chunk(b"IEND", b""))
    ppm = run.png_to_ppm(png)
    p = tmp_path / "s.ppm"
    p.write_bytes(ppm)
    w2, h2, pix = cf.read_ppm(p)
    assert (w2, h2) == (3, 2)
    assert pix[:9] == bytes([10, 20, 30, 15, 25, 35, 16, 26, 36])
    assert pix[9:] == bytes([11, 21, 31, 17, 27, 37, 19, 29, 39])


def test_virtualbox_lab_plans_and_clones_stay_on_the_internal_network(tmp_path, cases):
    conf = tomllib.loads((HERE / "lab.example.toml").read_text())
    conf["hypervisor"] = "virtualbox"
    conf["work"] = str(tmp_path)
    for v in [conf["server_vm"]] + list(conf["client_vms"].values()):
        v.update(vbox_base="base", vbox_snapshot="snap")
    lab = run.Lab(conf, tmp_path)
    assert isinstance(lab.server, run.VboxVm)
    assert all(isinstance(v, run.VboxVm) for v in lab.clients.values())
    calls = []

    class FakeVb(run.VBox):
        def __call__(self, *args, check=True, timeout=600):
            calls.append([str(a) for a in args])
            out = b'Forwarding(0)="base-ssh,tcp,,2224,,22"\n' if args[0] == "showvminfo" else b""
            return run.subprocess.CompletedProcess(args, 0, out, b"")
    vb = FakeVb(conf["virtualbox"])
    for vm in [lab.server, lab.clients["win10"]]:
        vm.vb = vb
        calls.clear()
        vm.fresh_overlay()
        clone = next(c for c in calls if c[0] == "clonevm")
        assert clone[1:4] == ["base", "--snapshot", "snap"] and "link" in clone
        assert ["modifyvm", vm.clone, "--natpf1", "delete", "base-ssh"] in calls
        mod = " ".join(next(c for c in calls if c[0] == "modifyvm" and "--memory" in c))
        if vm is lab.server:
            assert "--nic1 nat --natpf1 conf-ssh,tcp," in mod and "--nic2 intnet --intnet2 conf-lab" in mod
        else:
            assert "--nic1 intnet --intnet1 conf-lab" in mod and "--nic2 none" in mod
            assert "nat" not in mod.replace("--nic2 none", "")


def test_no_addresses_or_home_paths_in_the_suite():
    dotted = re.compile(r"\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
    for p in list(HERE.rglob("*")) + list(cf.SUITE.rglob("*")):
        if p.is_file() and p.suffix in (".py", ".toml", ".md", ".sh", ".gs2", ".tsv"):
            text = p.read_text(encoding="utf-8")
            assert not dotted.search(text), p
            assert not re.search(r"/home/(?!user\b|runner\b|<)[a-z]", text), p


def test_grid_lines_centre_the_field():
    lines = cf.grid_lines([{"name": "D", "shape": "conf_red.3ds", "nx": 2, "ny": 2, "step": 4, "z": 1}]).split("\n")
    assert lines[:4] == ["object D0 conf_red.3ds -2 -2 1", "object D1 conf_red.3ds 2 -2 1",
                         "object D2 conf_red.3ds -2 2 1", "object D3 conf_red.3ds 2 2 1"]


def test_inject_checks_read_the_inject_log(tmp_path):
    (tmp_path / "inject.log").write_text("udp sent 706\ntcp sent 5\ngserver alive\n")
    chk = cf.Check(id="a", kind="inject", pattern="^gserver alive")
    assert cf.observe(chk, tmp_path)[0] is True
    (tmp_path / "inject.log").write_text("udp sent 706\ngserver gone\n")
    assert cf.observe(chk, tmp_path)[0] is False


def test_count_checks_need_that_many_matches(tmp_path):
    (tmp_path / "gserver.log").write_text("logged in as player\nlogged in as player\n")
    two = cf.Check(id="a", kind="server", pattern="logged in as player", count=2)
    three = cf.Check(id="b", kind="server", pattern="logged in as player", count=3)
    assert cf.observe(two, tmp_path)[0] is True
    assert cf.observe(three, tmp_path)[0] is False


def test_multi_session_cases_swap_served_files(cases):
    served = set(gen_content.files())
    for c in cases:
        for b in c.between:
            assert b["swap"] in served and b["with"] in served, c.id
            assert any(f == b["with"] for f in c.files), f"{c.id}: {b['with']} is not served"


def test_probe_values_with_spaces_come_back_whole():
    log = ("Graal3D: player 3: trigger ignored (gui,ConfProbe,cf,getposition,2,3,4)\n"
           "Graal3D: player 3: trigger sent (gui,ConfProbe,cf,x,2)\n"
           "Graal3D: player 3: trigger sent (gui,ConfProbe,cf,x_gone,1)\n"
           "Graal3D: player 3: trigger sent (gui,ConfProbe,cf,d_shape)\n")
    assert cf.probe_values(log, "getposition") == ["2 3 4"]
    assert cf.probe_values(log, "x") == ["2"]
    assert cf.probe_values(log, "d_shape") == [""]


def test_results_keep_a_probe_value_observed(tmp_path):
    v = {"case": "C026", "build": "5.12", "verdict": "PASS", "mismatches": [],
         "checks": {"p": {"expected": "?", "observed": True, "detail": "", "value": "2 3 4"}}}
    cf.append_result(tmp_path / "r.tsv", v, "2026-11-26", "srv", "cli")
    assert "p=yes(2 3 4)" in (tmp_path / "r.tsv").read_text()


def test_probe_reports_are_read_from_ignored_or_routed_trigger_lines():
    log = ("Graal3D: player 3: trigger ignored (gui,ConfProbe,cf,made,1)\n"
           "Graal3D: player 3: trigger sent (gui,ConfProbe,cf,done,1)\n")
    assert cf.probe_values(log, "made") == ["1"]
    assert cf.probe_values(log, "done") == ["1"]


def test_v2_cases_get_v2_option_names(cases, tmp_path):
    v2 = [c for c in cases if c.server_kind == "v2"]
    assert {c.id for c in v2} >= {"C038", "C039", "C040", "C045"}
    for c in v2:
        add = (cf.build_world(c, tmp_path / "out") / "config" / "server.add").read_text()
        assert "graal3dtrace = g3d.tsv" in add and "graal3d_trace" not in add
    add = (cf.build_world(case(cases, "C001"), tmp_path / "out") / "config" / "server.add").read_text()
    assert "graal3d_trace = g3d.tsv" in add


def test_server_kind_is_checked(tmp_path):
    src = case_path("C038").read_text(encoding="utf-8")
    bad = tmp_path / "bad.toml"
    bad.write_text(src.replace('kind = "v2"', 'kind = "v3"'), encoding="utf-8")
    with pytest.raises(cf.CaseError, match="server.kind"):
        cf.load_case(bad)
    bad.write_text(src.replace('files = [', 'terrain = ["conf_ter"]\nfiles = ['), encoding="utf-8")
    with pytest.raises(cf.CaseError, match="no terrain"):
        cf.load_case(bad)


def test_served_name_takes_another_generated_file(cases, tmp_path):
    root = cf.build_world(case(cases, "C035"), tmp_path / "out")
    assert (root / "files" / "heights.info").read_bytes() == b"conf_ground.png\nconf_grass.png\n"
    assert not (root / "files" / "heights_grass.info").exists()
    # the terrain folder carries the same heights.info (seihai-gserver #222 checks)
    assert (root / "conf_ter" / "heights.info").read_bytes() == b"conf_ground.png\nconf_grass.png\n"


def test_raw_grass_cases_carry_the_generated_line(cases):
    for cid, r in (("C036", 4), ("C037", 8)):
        line = gen_content.grass_rawobject("ConfGrassRaw", 20, 20, 0, r, 40, 60, "conf_grass.png")
        assert line in case(cases, cid).world
        assert f" u8:{r} u8:40 u8:60 " in line
    # Every field is one rawobject accepts, and the update is 6 + 6 sign/int15
    # pairs after the counts (the box), as seihai-gserver's Replicator::write.
    for tok in line.split()[2:]:
        assert re.fullmatch(r"f[01]|i\d+:-?\d+|u(8|16|32):\d+|f32:-?[\d.]+|str:\S+", tok), tok
    assert line.count("i15:") == 6


def test_huge_png_claims_its_size_with_a_valid_crc():
    import zlib
    d = gen_content.huge_png()
    assert struct.unpack(">II", d[16:24]) == (100000, 100000)
    assert struct.unpack(">I", d[29:33])[0] == zlib.crc32(d[12:29])
    assert "conf_huge.png" in gen_content.files()["conf_huge.3ds"].decode("latin-1")


def case_path(cid):
    return next(p for p in cf.CASES.glob("*.toml") if tomllib.loads(p.read_text(encoding="utf-8"))["id"] == cid)
