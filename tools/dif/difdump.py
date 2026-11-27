#!/usr/bin/env python3
"""Read a Torque interior (.dif) back and check it: ours (difgen.py) or a
held one. Version 44 resource, interior version 0, TGE surface layout, the
same reading order as the 5.12-class loader (Torque 3D 1.1 interiorIO.cpp,
MIT, for the field order; the flex-width index lists that map2dif writes are
read too).

    python3 tools/dif/difdump.py FILE.dif [--zone X,Y,Z ...] [--json]

Prints the counts, the zones and portals, and the checks: every index in
range, the BSP walks to a leaf for every point asked (`--zone`), every
portal's two zones differ, and the winding sense of the surfaces against
their planes (how Torque's PlaneF(v0, v1, v2) of the strip's first triangle
compares with the stored plane: `cw` = the same direction).

Python 3 standard library only.
"""

from __future__ import annotations

import json
import struct
import sys


class DifError(Exception):
    pass


class R:
    def __init__(self, data: bytes) -> None:
        self.d = data
        self.p = 0

    def take(self, n):
        if self.p + n > len(self.d):
            raise DifError(f"short file at {self.p} (wanted {n} bytes)")
        v = self.d[self.p:self.p + n]
        self.p += n
        return v

    def u8(self): return self.take(1)[0]
    def u16(self): return struct.unpack("<H", self.take(2))[0]
    def u32(self): return struct.unpack("<I", self.take(4))[0]
    def f32(self): return struct.unpack("<f", self.take(4))[0]
    def vec3(self): return struct.unpack("<3f", self.take(12))

    def count(self, limit=1 << 24):
        n = self.u32()
        if n > limit:
            raise DifError(f"implausible count {n} at {self.p - 4}")
        return n

    def flex(self, wide, narrow):
        """A map2dif index list: the count's top bit set means one extra byte
        and narrow entries; else wide entries."""
        n = self.u32()
        if n & (1 << 31):
            n ^= (1 << 31)
            self.u8()
            get = narrow
        else:
            get = wide
        if n > 1 << 24:
            raise DifError("implausible flex count")
        return [get() for _ in range(n)]

    def png(self):
        if self.take(8) != b"\x89PNG\r\n\x1a\n":
            raise DifError(f"no PNG at {self.p - 8}")
        while True:
            ln = struct.unpack(">I", self.take(4))[0]
            kind = self.take(4)
            self.take(ln + 4)
            if kind == b"IEND":
                return


def read_interior(r: R) -> dict:
    I: dict = {}
    I["version"] = r.u32()
    if I["version"] != 0:
        raise DifError(f"interior version {I['version']} (5.12 takes 0)")
    I["detail"] = r.u32()
    I["min_pixels"] = r.u32()
    I["bbox"] = struct.unpack("<6f", r.take(24))
    I["sphere"] = struct.unpack("<4f", r.take(16))
    I["alarm"] = r.u8()
    I["light_state_entries"] = r.u32()
    normals = [r.vec3() for _ in range(r.count())]
    planes = []
    for _ in range(r.count()):
        ni = r.u16()
        d = r.f32()
        if ni >= len(normals):
            raise DifError("plane normal index out of range")
        planes.append((normals[ni], d))
    I["normals"], I["planes"] = normals, planes
    I["points"] = [r.vec3() for _ in range(r.count())]
    I["point_vis"] = r.take(r.count())
    I["texgens"] = [struct.unpack("<8f", r.take(32)) for _ in range(r.count())]
    I["bsp"] = [(r.u16(), r.u16(), r.u16()) for _ in range(r.count())]
    I["solid_leaves"] = [(r.u32(), r.u16()) for _ in range(r.count())]
    mver = r.u8()
    if mver != 1:
        raise DifError(f"material list version {mver}")
    I["materials"] = [r.take(r.u8()).decode("latin-1") for _ in range(r.count())]
    I["windings"] = r.flex(r.u32, r.u16)
    I["winding_indices"] = [(r.u32(), r.u32()) for _ in range(r.count())]
    # portal start, portal count, surface start, surface count (16 bits), flags
    I["zones"] = [(r.u16(), r.u16(), r.u32(), r.u16(), r.u16()) for _ in range(r.count())]
    I["zone_surfaces"] = r.flex(r.u16, r.u16)
    I["zone_portals"] = r.flex(r.u16, r.u16)
    I["portals"] = [(r.u16(), r.u16(), r.u32(), r.u16(), r.u16()) for _ in range(r.count())]
    surfaces = []
    for _ in range(r.count()):
        s = {
            "wstart": r.u32(), "wcount": r.u8(), "plane": r.u16(), "texture": r.u16(),
            "texgen": r.u32(), "flags": r.u8(), "fan_mask": r.u32(), "final_word": r.u16(),
            "lm_dx": r.f32(), "lm_dy": r.f32(), "light_count": r.u16(), "light_start": r.u32(),
            "map": (r.u8(), r.u8(), r.u8(), r.u8()),
        }
        if s["wstart"] + s["wcount"] > len(I["windings"]):
            raise DifError("surface winding out of range (not the TGE v0 layout?)")
        if (s["plane"] & 0x7FFF) >= len(planes) or s["texture"] >= len(I["materials"]) \
                or s["texgen"] >= len(I["texgens"]):
            raise DifError("surface index out of range (not the TGE v0 layout?)")
        if (s["final_word"] >> 13) & 7 > 5:
            raise DifError("surface lightmap st encoding out of range")
        surfaces.append(s)
    I["surfaces"] = surfaces
    I["normal_lmap"] = r.flex(r.u8, r.u8)
    I["alarm_lmap"] = r.flex(r.u8, r.u8)
    I["null_surfaces"] = [(r.u32(), r.u16(), r.u8(), r.u8()) for _ in range(r.count())]
    nlm = r.count()
    for _ in range(nlm):
        r.png()
        r.u8()
    I["lightmaps"] = nlm
    I["solid_leaf_surfaces"] = r.flex(r.u32, r.u16)
    for _ in range(r.count()):          # animated lights
        r.take(4 + 4 + 2 + 2 + 4)
    for _ in range(r.count()):          # light states
        r.take(3 + 4 + 4 + 2)
    for _ in range(r.count()):          # state data
        r.take(4 + 4 + 2)
    n = r.count()
    r.u32()                             # flags
    r.take(n)
    r.take(r.count())                   # name buffer
    if r.count() != 0:
        raise DifError("sub-objects are not read here")
    hulls = []
    for _ in range(r.count()):
        h = {"hstart": r.u32(), "hcount": r.u16()}
        h["box"] = struct.unpack("<6f", r.take(24))
        h.update(sstart=r.u32(), scount=r.u16(), pstart=r.u32(),
                 plpstart=r.u32(), plptstart=r.u32(), plsstart=r.u32())
        hulls.append(h)
    I["hulls"] = hulls
    I["emit"] = r.take(r.count())
    I["hull_indices"] = r.flex(r.u32, r.u16)
    I["hull_planes"] = r.flex(r.u16, r.u16)
    I["hull_emit_indices"] = r.flex(r.u32, r.u16)
    I["hull_surfaces"] = r.flex(r.u32, r.u16)
    I["poly_planes"] = r.flex(r.u16, r.u16)
    I["poly_points"] = r.flex(r.u32, r.u16)
    I["poly_strings"] = r.take(r.count())
    I["coord_bins"] = [(r.u32(), r.u32()) for _ in range(256)]
    I["coord_bin_indices"] = r.flex(r.u16, r.u16)
    I["coord_bin_mode"] = r.u32()
    I["ambient"] = r.take(4), r.take(4)
    for _ in range(3):
        if r.u32() != 0:
            raise DifError("non-zero spare word")
    ext = r.u32()
    if ext == 1:
        r.u32()
        r.u32()
    return I


def read_dif(data: bytes) -> dict:
    r = R(data)
    v = r.u32()
    if v != 44:
        raise DifError(f"resource version {v} (5.12 takes 44)")
    if r.u8():
        r.png()
    detail = [read_interior(r) for _ in range(r.count(64))]
    tail = {}
    for k in ("sub_objects", "triggers", "path_followers", "force_fields", "ai_nodes"):
        tail[k] = r.u32()
    if any(tail.values()):
        # Not read here; leave the rest unchecked.
        return {"resource_version": v, "detail": detail, "tail": tail, "trailing": len(data) - r.p}
    tail["vehicle_collision"] = r.u32()
    if tail["vehicle_collision"] == 1:
        tail["vc_version"] = r.u32()
        tail["vc_lists"] = [r.u32() for _ in range(14)]
    if r.p < len(data):
        tail["game_entities"] = r.u32()
    return {"resource_version": v, "detail": detail, "tail": tail, "trailing": len(data) - r.p}


# ------------------------------------------------------------------ checks

def plane_of(I, pi):
    nrm, d = I["planes"][pi & 0x7FFF]
    if pi & 0x8000:
        return (-nrm[0], -nrm[1], -nrm[2]), -d
    return nrm, d


def zone_for_point(I, p):
    """Interior::getZoneForPoint: -1 for solid or no zone."""
    node = 0
    for _ in range(100000):
        pl, front, back = I["bsp"][node]
        nrm, d = plane_of(I, pl)
        dist = nrm[0] * p[0] + nrm[1] * p[1] + nrm[2] * p[2] + d
        nxt = front if dist >= 0 else back
        if nxt & 0x8000:
            if nxt & 0x4000:
                return -1
            z = nxt & ~0xC000
            return -1 if z == 0x0FFF else z
        node = nxt
    raise DifError("BSP loop")


def winding_sense(I):
    cw = ccw = 0
    for s in I["surfaces"]:
        if s["wcount"] < 3:
            continue
        w = I["windings"][s["wstart"]:s["wstart"] + 3]
        v0, v1, v2 = (I["points"][i] for i in w)
        a = tuple(v0[k] - v1[k] for k in range(3))
        b = tuple(v2[k] - v1[k] for k in range(3))
        c = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
        nrm, _ = plane_of(I, s["plane"])
        dot = sum(c[k] * nrm[k] for k in range(3))
        if dot > 1e-9:
            cw += 1
        elif dot < -1e-9:
            ccw += 1
    return {"cw": cw, "ccw": ccw}


def check(I) -> list[str]:
    bad = []
    np_, ns, nw = len(I["points"]), len(I["surfaces"]), len(I["windings"])
    if any(w >= np_ for w in I["windings"]):
        bad.append("winding point out of range")
    for i, (pl, f, b) in enumerate(I["bsp"]):
        if (pl & 0x7FFF) >= len(I["planes"]):
            bad.append(f"bsp node {i} plane out of range")
        for c in (f, b):
            if c & 0x8000:
                if c & 0x4000 and (c & ~0xC000) >= len(I["solid_leaves"]):
                    bad.append(f"bsp node {i} solid leaf out of range")
                if not c & 0x4000 and (c & ~0xC000) not in (0x0FFF,) and (c & ~0xC000) >= len(I["zones"]):
                    bad.append(f"bsp node {i} empty-leaf zone out of range")
            elif c >= len(I["bsp"]):
                bad.append(f"bsp node {i} child out of range")
    for s, c in I["solid_leaves"]:
        if s + c > len(I["solid_leaf_surfaces"]):
            bad.append("solid leaf surfaces out of range")
    if any((x & 0x7FFFFFFF) >= ns for x in I["solid_leaf_surfaces"] if not x & (1 << 31)):
        bad.append("solid leaf surface index out of range")
    for zi, (ps, pc, ss, sc, _fl) in enumerate(I["zones"]):
        if ps + pc > len(I["zone_portals"]) or ss + sc > len(I["zone_surfaces"]):
            bad.append(f"zone {zi} lists out of range")
        for pi in I["zone_portals"][ps:ps + pc]:
            if pi >= len(I["portals"]):
                bad.append(f"zone {zi} portal out of range")
            elif zi not in (I["portals"][pi][3], I["portals"][pi][4]):
                bad.append(f"zone {zi} lists portal {pi}, which does not touch it")
    if any(s >= ns for s in I["zone_surfaces"]):
        bad.append("zone surface out of range")
    for pi, (pl, fc, fs, zf, zb) in enumerate(I["portals"]):
        if fs + fc > len(I["winding_indices"]):
            bad.append(f"portal {pi} fan out of range")
    for ws, wc in I["winding_indices"]:
        if ws + wc > nw:
            bad.append("tri-fan out of range")
    for hi, h in enumerate(I["hulls"]):
        if h["hstart"] + h["hcount"] > len(I["hull_indices"]):
            bad.append(f"hull {hi} points out of range")
        if h["sstart"] + h["scount"] > len(I["hull_surfaces"]):
            bad.append(f"hull {hi} surfaces out of range")
        if h["hstart"] + h["hcount"] > len(I["hull_emit_indices"]):
            bad.append(f"hull {hi} emit indices out of range")
        if h["plsstart"] > len(I["poly_strings"]):
            bad.append(f"hull {hi} poly string out of range")
    if any(e >= len(I["emit"]) for e in I["hull_emit_indices"]):
        bad.append("emit string index out of range")
    if any(i >= np_ for i in I["hull_indices"]):
        bad.append("hull point out of range")
    if any(i >= len(I["hulls"]) for i in I["coord_bin_indices"]):
        bad.append("coord bin hull out of range")
    for s, c in I["coord_bins"]:
        if s + c > len(I["coord_bin_indices"]):
            bad.append("coord bin out of range")
            break
    if len(I["normal_lmap"]) != ns:
        bad.append("normal lightmap indices do not match the surfaces")
    if I["lightmaps"] and any(x >= I["lightmaps"] for x in I["normal_lmap"]):
        bad.append("surface names a lightmap that is not in the file")
    return bad


def summary(D: dict, zone_points=()) -> dict:
    I = D["detail"][0]
    out = {
        "resource_version": D["resource_version"],
        "interior_version": I["version"],
        "detail_levels": len(D["detail"]),
        "trailing_bytes": D["trailing"],
        "counts": {k: len(I[k]) for k in (
            "normals", "planes", "points", "texgens", "bsp", "solid_leaves", "materials",
            "windings", "zones", "portals", "surfaces", "hulls")},
        "lightmaps": I["lightmaps"],
        "materials": I["materials"],
        "zones": [{"portals": I["zone_portals"][ps:ps + pc], "surfaces": sc, "flags": fl}
                  for ps, pc, ss, sc, fl in I["zones"]],
        "portals": [{"front": zf, "back": zb, "plane": plane_of(I, pl)}
                    for pl, _, _, zf, zb in I["portals"]],
        "winding": winding_sense(I),
        # map2dif leaves some free-floating portals (front == back, or both
        # 0xFFFF); Torque's traversal skips them, so they are noted, not errors.
        "free_portals": sum(1 for p in I["portals"] if p[3] == p[4]),
        "problems": check(I),
    }
    if zone_points:
        out["zone_for_point"] = {",".join(f"{c:g}" for c in p): zone_for_point(I, p) for p in zone_points}
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    path, pts, as_json = argv[0], [], False
    i = 1
    while i < len(argv):
        if argv[i] == "--zone":
            pts.append(tuple(float(x) for x in argv[i + 1].split(",")))
            i += 2
        elif argv[i] == "--json":
            as_json = True
            i += 1
        else:
            print(f"unknown argument {argv[i]}", file=sys.stderr)
            return 2
    with open(path, "rb") as f:
        data = f.read()
    try:
        D = read_dif(data)
    except DifError as e:
        print(f"{path}: not readable: {e}")
        return 1
    S = summary(D, pts)
    if as_json:
        print(json.dumps(S, indent=1))
    else:
        print(f"{path}: resource {S['resource_version']}, interior {S['interior_version']}, "
              f"{S['detail_levels']} detail level(s), {S['trailing_bytes']} trailing bytes")
        print("  counts: " + ", ".join(f"{k} {v}" for k, v in S["counts"].items()))
        print(f"  lightmaps {S['lightmaps']}; materials {S['materials']}")
        for zi, z in enumerate(S["zones"]):
            print(f"  zone {zi}: {z['surfaces']} surfaces, flags {z['flags']}, portals {z['portals']}")
        for pi, p in enumerate(S["portals"]):
            print(f"  portal {pi}: front zone {p['front']}, back zone {p['back']}, plane {p['plane']}")
        print(f"  winding sense: {S['winding']}; free-floating portals: {S['free_portals']}")
        for k, v in S.get("zone_for_point", {}).items():
            print(f"  zone at {k}: {v}")
        print("  problems: " + ("; ".join(S["problems"]) if S["problems"] else "none"))
    return 1 if S["problems"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
