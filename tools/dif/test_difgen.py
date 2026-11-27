"""Tests for difgen.py / difdump.py: our v44 interiors read back whole, with
the zones, portals, BSP and collision data the scene asks for.

    python3 -m pytest tools/dif -q

Set DIF_SAMPLES to a folder of held .dif files (e.g. a checkout of
fr1tz/rotc-ethernet-game) to also read those back.
"""

import os
import struct
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import difdump  # noqa: E402
import difgen  # noqa: E402


def interior(name, **kw):
    D = difdump.read_dif(difgen.scene_bytes(name, **kw))
    assert D["trailing"] == 0
    assert len(D["detail"]) == 1
    return D, D["detail"][0]


@pytest.mark.parametrize("name", list(difgen.SCENES))
@pytest.mark.parametrize("lightmaps", ["white", "none"])
def test_every_scene_reads_back_clean(name, lightmaps):
    D, I = interior(name, lightmaps=lightmaps)
    assert D["resource_version"] == 44 and I["version"] == 0
    assert difdump.check(I) == []
    assert difdump.winding_sense(I)["ccw"] == 0
    assert I["lightmaps"] == (1 if lightmaps == "white" else 0)
    # The map2dif tail: empty vehicle collision, no game entities.
    assert D["tail"]["vehicle_collision"] == 1 and D["tail"]["vc_lists"] == [0] * 14


def test_house_zones_and_portals():
    _, I = interior("house")
    assert len(I["zones"]) == 3
    assert [z[4] for z in I["zones"]] == [0, 1, 1]      # flags: inside zones 1
    pts = {(0, -3, 1): 0, (0, 3, 1): 1, (0, 9, 1): 2, (0, 20, 1): 0, (0, 0.25, 1): 0,
           (3, 0.25, 1): -1, (0, 6.25, 1): 1, (0, 3, -0.25): -1, (0, 3, 10): 0}
    for p, z in pts.items():
        assert difdump.zone_for_point(I, p) == z, p
    portals = {(zf, zb) for _, _, _, zf, zb in I["portals"]}
    assert portals == {(1, 0), (2, 1)}
    # Every surface is in exactly one zone's list.
    assert sorted(I["zone_surfaces"]) == list(range(len(I["surfaces"])))


def test_variants_differ_only_where_meant():
    _, house = interior("house")
    _, single = interior("single")
    _, nop = interior("noportal")
    _, win = interior("window")
    assert len(single["zones"]) == 1 and not single["portals"]
    assert len(single["surfaces"]) == len(house["surfaces"])
    assert len(nop["zones"]) == 3 and len(nop["portals"]) == 1
    assert difdump.zone_for_point(nop, (0, 9, 1)) == 2
    # The window house: front wall solid but with no surface; room A sealed.
    assert difdump.zone_for_point(win, (0, 0.25, 1)) == -1
    assert difdump.zone_for_point(win, (0, 3, 1)) == 1
    assert all(zf != 0 and zb != 0 for _, _, _, zf, zb in win["portals"])


def test_surfaces_face_into_empty_space():
    _, I = interior("house")
    for s in I["surfaces"]:
        nrm, d = difdump.plane_of(I, s["plane"])
        pts = [I["points"][i] for i in I["windings"][s["wstart"]:s["wstart"] + s["wcount"]]]
        c = [sum(p[k] for p in pts) / len(pts) for k in range(3)]
        assert abs(sum(nrm[k] * c[k] for k in range(3)) + d) < 1e-5
        front = [c[k] + 0.01 * nrm[k] for k in range(3)]
        back = [c[k] - 0.01 * nrm[k] for k in range(3)]
        assert difdump.zone_for_point(I, front) >= 0 or _outside(I, front)
        assert difdump.zone_for_point(I, back) == -1


def _outside(I, p):
    lo, hi = I["bbox"][:3], I["bbox"][3:]
    return any(p[k] < lo[k] or p[k] > hi[k] for k in range(3))


def test_hull_emit_strings_face_outward():
    _, I = interior("house")
    for h in I["hulls"]:
        es = I["emit"][I["hull_emit_indices"][h["hstart"]]:]
        npts = es[0]
        idx = list(es[1:1 + npts])
        pos = 1 + npts
        nedges = es[pos]
        pos += 1 + 2 * nedges
        npolys = es[pos]
        pos += 1
        corners = [I["points"][I["hull_indices"][h["hstart"] + i]] for i in range(h["hcount"])]
        assert idx == list(range(8)) and npolys == 6
        for _ in range(npolys):
            vc, pl = es[pos], es[pos + 1]
            vs = list(es[pos + 2:pos + 2 + vc])
            pos += 2 + vc
            nrm = difgen.torque_plane_normal(*(corners[v] for v in vs[:3]))
            hnrm, _ = difdump.plane_of(I, I["hull_planes"][h["pstart"] + pl])
            assert sum(nrm[k] * hnrm[k] for k in range(3)) > 0


def test_coord_bins_cover_every_hull():
    _, I = interior("house")
    seen = set(I["coord_bin_indices"])
    assert seen == set(range(len(I["hulls"])))


def test_leaky_portal_is_refused():
    sc = difgen.house("house")
    sc.portals.append(difgen.Portal(0, 0.0, (2, 3), (1, 2)))     # in room A's open air
    with pytest.raises(ValueError, match="itself"):
        difgen.build(sc)


def test_versions_are_the_512_gate():
    data = difgen.scene_bytes("house")
    assert struct.unpack_from("<I", data, 0)[0] == 44
    assert data[4] == 0                                       # no preview
    assert struct.unpack_from("<II", data, 5) == (1, 0)       # one detail level, interior v0


SAMPLES = os.environ.get("DIF_SAMPLES")


@pytest.mark.skipif(not SAMPLES, reason="DIF_SAMPLES not set")
def test_held_samples_read_back():
    files = sorted(Path(SAMPLES).rglob("*.dif"))
    assert files
    for f in files:
        D = difdump.read_dif(f.read_bytes())
        assert D["trailing"] == 0, f
        assert difdump.check(D["detail"][0]) == [], f
