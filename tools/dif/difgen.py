#!/usr/bin/env python3
"""Write Torque interior (.dif) files from axis-aligned box brushes: our own
zoned, portaled version-44 interiors for the 5.12 lab (T3D-030, T3D-087).

The layout is the one the 5.12 loader accepts, the stock TGE 1.x / Marble
Blast form: InteriorResource version 44, Interior version 0, the TGE (not
TGEA) surface record (no trailing "unused" byte). The field order and widths
follow the MIT-licensed Torque 3D 1.1 interior source (interiorIO.cpp,
interiorRes.cpp) and agree with the BSD-licensed HiGuy Dif library's
version-0 writer; no code is copied from either. The 5.12 version gate itself
(44 / 0 / 0) is from our own read of Graal3DEngine.dll.

What a file holds, built here from nothing:

* a BSP over the brushes (axis-aligned split planes; every empty leaf names
  its zone, every solid leaf its surfaces),
* zones: zone 0 is the outside, every enclosed empty region is its own zone,
  and a portal rectangle in a doorway splits two zones,
* portals (a plane, a tri-fan, the zones in front and behind),
* surfaces: every brush face that touches empty space, merged into
  rectangles, with a texture generator and a lightmap place,
* one lightmap atlas (white) or none,
* one convex hull per brush with its emit strings and poly list (Torque's
  collision data), and the 16 x 16 coordinate bins over the hulls.

Python 3 standard library only. Command line:

    python3 tools/dif/difgen.py scene <name> OUT.dif     # a built-in scene
    python3 tools/dif/difgen.py list                     # the built-in scenes

`scenes()` names the lab scenes (an enclosed two-room house and its
deliberately inconsistent variants for the zone tests); `difdump.py` reads any
v44 file back (ours or a held one) and checks it.
"""

from __future__ import annotations

import math
import struct
import sys
import zlib
from collections import deque
from dataclasses import dataclass, field

RESOURCE_VERSION = 44
INTERIOR_VERSION = 0
MATERIAL_LIST_VERSION = 1
OUTSIDE_ZONE = 0
NUM_COORD_BINS = 16

SURFACE_OUTSIDE_VISIBLE = 0x10

AXES = "xyz"
# The two in-plane axes for a face whose normal is on axis a: (u, v).
UV_AXES = {0: (1, 2), 1: (0, 2), 2: (0, 1)}


# ------------------------------------------------------------------ input

@dataclass
class Box:
    """A solid axis-aligned brush. `omit` names faces to leave without a
    surface ("-x", "+y", ..., or "all"): the brush stays solid in the BSP and
    in collision, it just draws nothing on those sides."""
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    material: str
    omit: frozenset[str] = frozenset()


@dataclass
class Portal:
    """A rectangle on the plane `axis` = `at`, spanning `u` and `v` on the
    two other axes (in xyz order). `emit` False makes it a separator only:
    it still splits the zones on its two sides, but no portal is written, so
    nothing joins them (a deliberately broken file for the zone tests)."""
    axis: int
    at: float
    u: tuple[float, float]
    v: tuple[float, float]
    emit: bool = True


@dataclass
class Scene:
    boxes: list[Box]
    portals: list[Portal] = field(default_factory=list)
    # Points that fix the zone numbering: the zone holding seeds[0] is zone
    # 1, and so on (zones found later follow in scan order).
    seeds: list[tuple[float, float, float]] = field(default_factory=list)
    zones: str = "flood"          # "flood" or "single" (everything zone 0)
    lightmaps: str = "white"      # "white" (one or more white atlases) or "none"
    winding: str = "cw"           # "cw": Torque PlaneF(v0, v1, v2) gives the outward normal
    tex_scale: float = 4.0        # world units per texture repeat
    margin: float = 2.0


# ------------------------------------------------------------------ bytes

class Out:
    def __init__(self) -> None:
        self.b = bytearray()

    def u8(self, v): self.b += struct.pack("<B", v)
    def u16(self, v): self.b += struct.pack("<H", v)
    def u32(self, v): self.b += struct.pack("<I", v)
    def f32(self, v): self.b += struct.pack("<f", v)

    def vec(self, items, put):
        self.u32(len(items))
        for it in items:
            put(it)

    def string(self, s: str):
        raw = s.encode("ascii")
        if len(raw) > 255:
            raise ValueError("material name over 255 bytes")
        self.u8(len(raw))
        self.b += raw


def png_rgb(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    row = b"\0" + bytes(rgb) * width
    raw = row * height

    def chunk(kind: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + kind + body
                + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


# ------------------------------------------------------------------ build

LIGHTMAP_SIZE = 256
LUMEL_INV_SCALE = 256       # lightmap coord = p / 256 + d: one lumel per world unit


@dataclass
class Built:
    """Everything one Interior record holds, in file order."""
    bbox: tuple
    sphere: tuple
    normals: list
    planes: list            # (normal index, d)
    points: list
    texgens: list           # ((4 floats), (4 floats))
    bsp_nodes: list         # (plane, front, back)
    solid_leaves: list      # (surface start, count)
    materials: list
    windings: list
    winding_indices: list   # (start, count): the portals' tri-fans
    zones: list             # (portal start, portal count, surface start, surface count, flags)
    zone_surfaces: list
    zone_portal_list: list
    portals: list           # (plane, fan count, fan start, zone front, zone back)
    surfaces: list          # dicts
    normal_lmap: list
    alarm_lmap: list
    lightmaps: list         # PNG bytes
    solid_leaf_surfaces: list
    hulls: list             # dicts
    hull_emit_strings: bytes
    hull_indices: list
    hull_plane_indices: list
    hull_emit_string_indices: list
    hull_surface_indices: list
    poly_list_planes: list
    poly_list_points: list
    poly_list_strings: bytes
    coord_bins: list        # 256 x (start, count)
    coord_bin_indices: list
    # For tests and the dump: the zone of each empty cell, by name.
    report: dict


def _plane_eval(nrm, d, p):
    return nrm[0] * p[0] + nrm[1] * p[1] + nrm[2] * p[2] + d


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def torque_plane_normal(v0, v1, v2):
    """Torque's PlaneF(k, j, l): normal = (k - j) x (l - j)."""
    return _cross(_sub(v0, v1), _sub(v2, v1))


def build(scene: Scene) -> Built:
    boxes = scene.boxes
    if not boxes:
        raise ValueError("a scene needs at least one box")
    for b in boxes:
        if any(b.lo[a] >= b.hi[a] for a in range(3)):
            raise ValueError(f"empty box {b}")

    lo_all = tuple(min(b.lo[a] for b in boxes) for a in range(3))
    hi_all = tuple(max(b.hi[a] for b in boxes) for a in range(3))

    # Grid lines on each axis: every box face, every portal edge, and a
    # margin outside everything (so the outermost cells are outside air).
    lines = [set() for _ in range(3)]
    for b in boxes:
        for a in range(3):
            lines[a].add(b.lo[a])
            lines[a].add(b.hi[a])
    for p in scene.portals:
        ua, va = UV_AXES[p.axis]
        lines[p.axis].add(p.at)
        lines[ua].update(p.u)
        lines[va].update(p.v)
    for a in range(3):
        lines[a].add(lo_all[a] - scene.margin)
        lines[a].add(hi_all[a] + scene.margin)
    coords = [sorted(s) for s in lines]
    n = [len(c) - 1 for c in coords]

    def centre(a, i):
        return 0.5 * (coords[a][i] + coords[a][i + 1])

    def cell_of(p):
        idx = []
        for a in range(3):
            c = coords[a]
            if p[a] <= c[0] or p[a] >= c[-1]:
                return None
            lo, hi = 0, len(c) - 1
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if c[mid] <= p[a]:
                    lo = mid
                else:
                    hi = mid
            idx.append(lo)
        return tuple(idx)

    # Solid cells and which brush owns each (the first that holds it).
    owner = {}
    for i in range(n[0]):
        cx = centre(0, i)
        for j in range(n[1]):
            cy = centre(1, j)
            for k in range(n[2]):
                cz = centre(2, k)
                for bi, b in enumerate(boxes):
                    if (b.lo[0] < cx < b.hi[0] and b.lo[1] < cy < b.hi[1]
                            and b.lo[2] < cz < b.hi[2]):
                        owner[(i, j, k)] = bi
                        break

    def solid(c):
        return c in owner

    # Faces blocked by a portal (or separator) rectangle: between cell c and
    # its + neighbour on axis a.
    def blocked(c, a):
        at = coords[a][c[a] + 1]
        ua, va = UV_AXES[a]
        pu, pv = centre(ua, c[ua]), centre(va, c[va])
        for p in scene.portals:
            if p.axis == a and p.at == at and p.u[0] < pu < p.u[1] and p.v[0] < pv < p.v[1]:
                return True
        return False

    def neighbours(c):
        for a in range(3):
            for s in (-1, 1):
                m = list(c)
                m[a] += s
                if 0 <= m[a] < n[a]:
                    m = tuple(m)
                    lower = c if s == 1 else m
                    if not blocked(lower, a):
                        yield m

    zone_of = {}

    def flood(start, zone):
        q = deque([start])
        zone_of[start] = zone
        while q:
            c = q.popleft()
            for m in neighbours(c):
                if m not in zone_of and not solid(m):
                    zone_of[m] = zone
                    q.append(m)

    all_cells = [(i, j, k) for i in range(n[0]) for j in range(n[1]) for k in range(n[2])]
    for c in all_cells:
        on_edge = any(c[a] == 0 or c[a] == n[a] - 1 for a in range(3))
        if on_edge and not solid(c) and c not in zone_of:
            flood(c, OUTSIDE_ZONE)
    next_zone = 1
    for s in scene.seeds:
        c = cell_of(s)
        if c is None or solid(c):
            raise ValueError(f"zone seed {s} is not in an empty cell")
        if c not in zone_of:
            flood(c, next_zone)
            next_zone += 1
    for c in all_cells:
        if not solid(c) and c not in zone_of:
            flood(c, next_zone)
            next_zone += 1
    num_zones = next_zone
    if num_zones >= 0x0FFF:
        raise ValueError("too many zones")
    # The flood's regions stay known (`region_of`); a "single" file puts
    # every one of them in the outside zone and writes no portals.
    region_of = dict(zone_of)
    if scene.zones == "single":
        zone_of = {c: OUTSIDE_ZONE for c in zone_of}
        num_zones = 1

    # ---------------------------------------------------------- planes
    normals: list = []
    normal_idx: dict = {}
    planes: list = []
    plane_idx: dict = {}

    def plane(axis, sign, at):
        nrm = [0.0, 0.0, 0.0]
        nrm[axis] = float(sign)
        nrm = tuple(nrm)
        if nrm not in normal_idx:
            normal_idx[nrm] = len(normals)
            normals.append(nrm)
        d = -sign * at
        key = (normal_idx[nrm], d)
        if key not in plane_idx:
            if len(planes) >= 0x8000:
                raise ValueError("too many planes")
            plane_idx[key] = len(planes)
            planes.append(key)
        return plane_idx[key]

    def plane_value(pi, p):
        ni, d = planes[pi]
        return _plane_eval(normals[ni], d, p)

    # ---------------------------------------------------------- points
    points: list = []
    point_idx: dict = {}

    def point(p):
        p = tuple(float(x) for x in p)
        if p not in point_idx:
            point_idx[p] = len(points)
            points.append(p)
        return point_idx[p]

    # ---------------------------------------------------------- faces
    # A face: (axis, sign, layer index) + a cell rectangle on (u, v), keyed by
    # brush, material and zone so merged rectangles never mix them.
    groups: dict = {}
    for c, bi in owner.items():
        b = boxes[bi]
        for a in range(3):
            for s in (-1, 1):
                tag = ("+" if s > 0 else "-") + AXES[a]
                if "all" in b.omit or tag in b.omit:
                    continue
                m = list(c)
                m[a] += s
                m = tuple(m)
                if not (0 <= m[a] < n[a]) or solid(m):
                    continue
                layer = c[a] + 1 if s > 0 else c[a]
                ua, va = UV_AXES[a]
                key = (a, s, layer, bi, b.material, region_of[m])
                groups.setdefault(key, {})[(c[ua], c[va])] = c

    rects = []
    for key in sorted(groups):
        cells = groups[key]
        free = set(cells)
        for start in sorted(cells):
            if start not in free:
                continue
            u0, v0 = start
            u1 = u0
            while (u1 + 1, v0) in free:
                u1 += 1
            v1 = v0
            while all((u, v1 + 1) in free for u in range(u0, u1 + 1)):
                v1 += 1
            owned = []
            for u in range(u0, u1 + 1):
                for v in range(v0, v1 + 1):
                    free.discard((u, v))
                    owned.append(cells[(u, v)])
            rects.append((key, (u0, u1 + 1), (v0, v1 + 1), owned))

    # ---------------------------------------------------------- materials, texgens
    materials: list = []
    for b in boxes:
        if b.material not in materials:
            materials.append(b.material)

    texgens: list = []
    texgen_idx: dict = {}

    def texgen(a):
        ua, va = UV_AXES[a]
        px = [0.0, 0.0, 0.0, 0.0]
        py = [0.0, 0.0, 0.0, 0.0]
        px[ua] = 1.0 / scene.tex_scale
        py[va] = -1.0 / scene.tex_scale if va == 2 else 1.0 / scene.tex_scale
        key = (tuple(px), tuple(py))
        if key not in texgen_idx:
            texgen_idx[key] = len(texgens)
            texgens.append(key)
        return texgen_idx[key]

    # ---------------------------------------------------------- lightmaps
    lightmap_count = 0
    shelf = {"x": 0, "y": 0, "h": 0, "map": -1}

    def place_lumels(w, h):
        nonlocal lightmap_count
        if w > LIGHTMAP_SIZE or h > LIGHTMAP_SIZE or w > 255 or h > 255:
            raise ValueError("surface too large for one lightmap")
        if shelf["map"] < 0:
            shelf["map"] = 0
            lightmap_count = 1
        if shelf["x"] + w > LIGHTMAP_SIZE:
            shelf["x"] = 0
            shelf["y"] += shelf["h"]
            shelf["h"] = 0
        if shelf["y"] + h > LIGHTMAP_SIZE:
            shelf["map"] += 1
            lightmap_count += 1
            shelf["x"] = shelf["y"] = shelf["h"] = 0
        x, y = shelf["x"], shelf["y"]
        shelf["x"] += w
        shelf["h"] = max(shelf["h"], h)
        return shelf["map"], x, y

    # ---------------------------------------------------------- surfaces
    windings: list = []
    surfaces: list = []
    normal_lmap: list = []
    alarm_lmap: list = []
    surface_cells: list = []      # the solid cells each surface sits on
    surface_brush: list = []
    surface_zone: list = []
    surface_region: list = []     # the flood region, whatever the file says
    surface_poly: list = []       # corner point indices, polygon order

    for key, (u0, u1), (v0, v1), owned in rects:
        a, s, layer, bi, mat, region = key
        zone = OUTSIDE_ZONE if scene.zones == "single" else region
        ua, va = UV_AXES[a]
        at = coords[a][layer]
        U0, U1 = coords[ua][u0], coords[ua][u1]
        V0, V1 = coords[va][v0], coords[va][v1]

        def P(u, v):
            p = [0.0, 0.0, 0.0]
            p[a] = at
            p[ua] = u
            p[va] = v
            return tuple(p)

        corners = [P(U0, V0), P(U1, V0), P(U1, V1), P(U0, V1)]
        outward = [0.0, 0.0, 0.0]
        outward[a] = float(s)
        want = 1 if scene.winding == "cw" else -1
        if _dot(torque_plane_normal(*corners[:3]), outward) * want < 0:
            corners.reverse()
        ci = [point(p) for p in corners]
        # Torque surfaces are triangle strips: polygon a, b, c, d is a, b, d, c.
        strip = [ci[0], ci[1], ci[3], ci[2]]
        wstart = len(windings)
        windings.extend(strip)

        pl = plane(a, s, at)
        if scene.lightmaps == "white":
            lw = int(math.ceil(U1 - U0)) + 1
            lh = int(math.ceil(V1 - V0)) + 1
            lm, mx, my = place_lumels(lw, lh)
        else:
            lm, mx, my, lw, lh = 0, 0, 0, 0, 0
        sc, tc = ua, va
        st_enc = {(0, 1): 0, (0, 2): 1, (1, 0): 2, (1, 2): 3, (2, 0): 4, (2, 1): 5}[(sc, tc)]
        log_scale = int(math.log2(LUMEL_INV_SCALE))
        final_word = (st_enc << 13) | (log_scale << 6) | log_scale
        dx = (mx - U0) / LUMEL_INV_SCALE
        dy = (my - V0) / LUMEL_INV_SCALE
        surfaces.append({
            "winding_start": wstart, "winding_count": 4, "plane": pl,
            "texture": materials.index(mat), "texgen": texgen(a),
            "flags": SURFACE_OUTSIDE_VISIBLE if zone == OUTSIDE_ZONE else 0,
            "fan_mask": 0xF, "final_word": final_word, "lm_dx": dx, "lm_dy": dy,
            "light_count": 0, "light_state_start": 0,
            "map_x": mx, "map_y": my, "map_w": lw, "map_h": lh,
        })
        normal_lmap.append(lm)
        alarm_lmap.append(0xFF)
        surface_cells.append(owned)
        surface_brush.append(bi)
        surface_zone.append(zone)
        surface_region.append(region)
        surface_poly.append(ci)

    if len(surfaces) >= 0x10000:
        raise ValueError("too many surfaces")
    lightmaps = [png_rgb(LIGHTMAP_SIZE, LIGHTMAP_SIZE, (255, 255, 255))
                 for _ in range(lightmap_count)]

    # ---------------------------------------------------------- portals
    portals: list = []
    winding_indices: list = []
    for p in scene.portals:
        if not p.emit or scene.zones == "single":
            continue
        ua, va = UV_AXES[p.axis]

        def side(sign):
            q = [0.0, 0.0, 0.0]
            q[p.axis] = p.at + sign * 1e-4
            q[ua] = 0.5 * (p.u[0] + p.u[1])
            q[va] = 0.5 * (p.v[0] + p.v[1])
            c = cell_of(q)
            return zone_of.get(c) if c is not None else OUTSIDE_ZONE

        front, back = side(+1), side(-1)
        if front is None or back is None:
            raise ValueError(f"portal {p} has solid on one side")
        if front == back:
            raise ValueError(f"portal {p} joins zone {front} to itself (the zones leak)")

        def P(u, v):
            q = [0.0, 0.0, 0.0]
            q[p.axis] = p.at
            q[ua] = u
            q[va] = v
            return tuple(q)

        fan = [point(P(p.u[0], p.v[0])), point(P(p.u[1], p.v[0])),
               point(P(p.u[1], p.v[1])), point(P(p.u[0], p.v[1]))]
        fstart = len(windings)
        windings.extend(fan)
        winding_indices.append((fstart, len(fan)))
        portals.append((plane(p.axis, +1, p.at), 1, len(winding_indices) - 1, front, back))

    # ---------------------------------------------------------- zones
    zones: list = []
    zone_surfaces: list = []
    zone_portal_list: list = []
    for z in range(num_zones):
        sstart = len(zone_surfaces)
        zone_surfaces.extend(i for i, sz in enumerate(surface_zone) if sz == z)
        pstart = len(zone_portal_list)
        zone_portal_list.extend(i for i, pt in enumerate(portals) if z in (pt[3], pt[4]))
        # map2dif writes flags 1 on every inside zone, 0 on the outside one
        # (both held ROTC interiors); the count before it is 16 bits.
        zones.append((pstart, len(zone_portal_list) - pstart, sstart, len(zone_surfaces) - sstart,
                      0 if z == OUTSIDE_ZONE else 1))

    # ---------------------------------------------------------- BSP
    surfaces_of_cell: dict = {}
    for si, owned in enumerate(surface_cells):
        for c in owned:
            surfaces_of_cell.setdefault(c, []).append(si)

    bsp_nodes: list = []
    solid_leaves: list = []
    solid_leaf_surfaces: list = []

    def leaf_code(lo, hi):
        kinds = set()
        for i in range(lo[0], hi[0]):
            for j in range(lo[1], hi[1]):
                for k in range(lo[2], hi[2]):
                    c = (i, j, k)
                    kinds.add("S" if solid(c) else zone_of[c])
                    if len(kinds) > 1:
                        return None
        (kind,) = kinds
        if kind == "S":
            found = []
            for i in range(lo[0], hi[0]):
                for j in range(lo[1], hi[1]):
                    for k in range(lo[2], hi[2]):
                        for si in surfaces_of_cell.get((i, j, k), []):
                            if si not in found:
                                found.append(si)
            if len(solid_leaves) >= 0x4000:
                raise ValueError("too many solid leaves")
            solid_leaves.append((len(solid_leaf_surfaces), len(found)))
            solid_leaf_surfaces.extend(found)
            return 0xC000 | (len(solid_leaves) - 1)
        return 0x8000 | kind

    def split(lo, hi):
        code = leaf_code(lo, hi)
        if code is not None:
            return code
        a = max(range(3), key=lambda ax: hi[ax] - lo[ax])
        mid = (lo[a] + hi[a]) // 2
        at = coords[a][mid]
        me = len(bsp_nodes)
        if me >= 0x4000:
            raise ValueError("too many BSP nodes")
        bsp_nodes.append(None)
        flo, fhi = list(lo), list(hi)
        flo[a] = mid
        blo, bhi = list(lo), list(hi)
        bhi[a] = mid
        front = split(tuple(flo), tuple(fhi))
        back = split(tuple(blo), tuple(bhi))
        bsp_nodes[me] = (plane(a, +1, at), front, back)
        return me

    root = split((0, 0, 0), tuple(n))
    if not bsp_nodes:
        # One uniform region: a node whose both sides are that leaf.
        bsp_nodes.append((plane(0, +1, coords[0][0]), root, root))

    # ---------------------------------------------------------- hulls
    hulls: list = []
    hull_indices: list = []
    hull_plane_indices: list = []
    hull_surface_indices: list = []
    hull_emit_string_indices: list = []
    emit = bytearray()
    poly_planes: list = []
    poly_points: list = []
    poly_strings = bytearray()

    box_corners = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
                   (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    box_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]
    # Faces as corner quads, with the outward axis and sign.
    box_faces = [((0, 3, 7, 4), 0, -1), ((1, 2, 6, 5), 0, 1),
                 ((0, 1, 5, 4), 1, -1), ((3, 2, 6, 7), 1, 1),
                 ((0, 1, 2, 3), 2, -1), ((4, 5, 6, 7), 2, 1)]

    for bi, b in enumerate(boxes):
        mine = [si for si in range(len(surfaces)) if surface_brush[si] == bi]
        if not mine:
            continue
        if len(mine) > 255:
            raise ValueError("a brush with over 255 surfaces")
        corner_pts = [tuple(b.hi[a] if c[a] else b.lo[a] for a in range(3)) for c in box_corners]
        hstart = len(hull_indices)
        hull_indices.extend(point(p) for p in corner_pts)
        pstart = len(hull_plane_indices)
        face_planes = []
        for quad, a, s in box_faces:
            at = b.hi[a] if s > 0 else b.lo[a]
            face_planes.append(plane(a, s, at))
        hull_plane_indices.extend(face_planes)

        # Emit string (the whole box for every support point): points,
        # edges, then each face as a fan whose Torque plane faces outward.
        es = bytearray([8]) + bytes(range(8)) + bytes([len(box_edges)])
        for e0, e1 in box_edges:
            es += bytes([e0, e1])
        es.append(len(box_faces))
        for fi, (quad, a, s) in enumerate(box_faces):
            vs = [corner_pts[q] for q in quad]
            outward = [0.0, 0.0, 0.0]
            outward[a] = float(s)
            order = list(quad)
            if _dot(torque_plane_normal(*vs[:3]), outward) < 0:
                order.reverse()
            es += bytes([4, fi]) + bytes(order)
        eoff = len(emit)
        emit += es
        hull_emit_string_indices.extend([eoff] * 8)

        sstart = len(hull_surface_indices)
        hull_surface_indices.extend(mine)

        # Poly list (interior.cpp processHullPolyLists, MIT): unique planes
        # and points of the hull's surfaces, a plane-group mask per plane
        # (six planes, one group each), and the surfaces as fans.
        temps = []
        for si in mine:
            temps.append((surfaces[si]["plane"], surface_poly[si]))
        uplanes, upoints = [], []
        for pl, poly in temps:
            if pl not in uplanes:
                uplanes.append(pl)
            for q in poly:
                if q not in upoints:
                    upoints.append(q)
        if len(uplanes) > 8:
            raise ValueError("over 8 planes on a box hull")
        pmask = {pl: 1 << i for i, pl in enumerate(uplanes)}
        ptmask = [0] * len(upoints)
        for pl, poly in temps:
            for q in poly:
                ptmask[upoints.index(q)] |= pmask[pl]
        ps = bytearray([len(uplanes)]) + bytes(pmask[pl] for pl in uplanes)
        ps += bytes([(len(upoints) >> 8) & 0xFF, len(upoints) & 0xFF]) + bytes(ptmask)
        ps.append(len(temps))
        for pl, poly in temps:
            ps += bytes([len(poly), pmask[pl], uplanes.index(pl)])
            for q in poly:
                li = upoints.index(q)
                ps += bytes([(li >> 8) & 0xFF, li & 0xFF])
        hull = {
            "hull_start": hstart, "hull_count": 8,
            "min": b.lo, "max": b.hi,
            "surface_start": sstart, "surface_count": len(mine),
            "plane_start": pstart,
            "poly_plane_start": len(poly_planes), "poly_point_start": len(poly_points),
            "poly_string_start": len(poly_strings),
        }
        poly_planes.extend(uplanes)
        poly_points.extend(upoints)
        poly_strings += ps
        hulls.append(hull)

    # ---------------------------------------------------------- coord bins
    bx = (hi_all[0] - lo_all[0]) / NUM_COORD_BINS
    by = (hi_all[1] - lo_all[1]) / NUM_COORD_BINS
    coord_bins = []
    coord_bin_indices = []
    for i in range(NUM_COORD_BINS):
        x0, x1 = lo_all[0] + i * bx, lo_all[0] + (i + 1) * bx
        for j in range(NUM_COORD_BINS):
            y0, y1 = lo_all[1] + j * by, lo_all[1] + (j + 1) * by
            start = len(coord_bin_indices)
            for hi_, h in enumerate(hulls):
                if h["min"][0] <= x1 and h["max"][0] >= x0 and h["min"][1] <= y1 and h["max"][1] >= y0:
                    coord_bin_indices.append(hi_)
            coord_bins.append((start, len(coord_bin_indices) - start))

    centre_all = tuple(0.5 * (lo_all[a] + hi_all[a]) for a in range(3))
    radius = math.sqrt(sum((hi_all[a] - centre_all[a]) ** 2 for a in range(3)))

    report = {
        "zones": num_zones,
        "grid": n,
        "zone_of_point": lambda p: (lambda c: None if c is None else ("solid" if solid(c) else zone_of[c]))(cell_of(p)),
        "surface_zone": surface_zone,
        "surface_region": surface_region,
    }
    return Built(
        bbox=(lo_all, hi_all), sphere=(centre_all, radius),
        normals=normals, planes=planes, points=points, texgens=texgens,
        bsp_nodes=bsp_nodes, solid_leaves=solid_leaves, materials=materials,
        windings=windings, winding_indices=winding_indices,
        zones=zones, zone_surfaces=zone_surfaces, zone_portal_list=zone_portal_list,
        portals=portals, surfaces=surfaces, normal_lmap=normal_lmap, alarm_lmap=alarm_lmap,
        lightmaps=lightmaps, solid_leaf_surfaces=solid_leaf_surfaces, hulls=hulls,
        hull_emit_strings=bytes(emit), hull_indices=hull_indices,
        hull_plane_indices=hull_plane_indices,
        hull_emit_string_indices=hull_emit_string_indices,
        hull_surface_indices=hull_surface_indices,
        poly_list_planes=poly_planes, poly_list_points=poly_points,
        poly_list_strings=bytes(poly_strings),
        coord_bins=coord_bins, coord_bin_indices=coord_bin_indices, report=report,
    )


# ------------------------------------------------------------------ write

def write_interior(o: Out, B: Built) -> None:
    o.u32(INTERIOR_VERSION)
    o.u32(0)                    # detail level
    o.u32(250)                  # min pixels
    lo, hi = B.bbox
    for v in (*lo, *hi):
        o.f32(v)
    c, r = B.sphere
    for v in (*c, r):
        o.f32(v)
    o.u8(0)                     # has alarm state
    o.u32(0)                    # light state entries
    o.vec(B.normals, lambda nr: [o.f32(x) for x in nr])
    o.vec(B.planes, lambda p: (o.u16(p[0]), o.f32(p[1])))
    o.vec(B.points, lambda p: [o.f32(x) for x in p])
    o.u32(len(B.points))        # point visibility: all visible
    o.b += b"\xff" * len(B.points)
    o.vec(B.texgens, lambda t: [o.f32(x) for x in (*t[0], *t[1])])
    o.vec(B.bsp_nodes, lambda nd: (o.u16(nd[0]), o.u16(nd[1]), o.u16(nd[2])))
    o.vec(B.solid_leaves, lambda sl: (o.u32(sl[0]), o.u16(sl[1])))
    o.u8(MATERIAL_LIST_VERSION)
    o.vec(B.materials, o.string)
    o.vec(B.windings, o.u32)
    o.vec(B.winding_indices, lambda w: (o.u32(w[0]), o.u32(w[1])))
    o.vec(B.zones, lambda z: (o.u16(z[0]), o.u16(z[1]), o.u32(z[2]), o.u16(z[3]), o.u16(z[4])))
    o.vec(B.zone_surfaces, o.u16)
    o.vec(B.zone_portal_list, o.u16)
    o.vec(B.portals, lambda p: (o.u16(p[0]), o.u16(p[1]), o.u32(p[2]), o.u16(p[3]), o.u16(p[4])))

    def surface(s):
        o.u32(s["winding_start"])
        o.u8(s["winding_count"])
        o.u16(s["plane"])
        o.u16(s["texture"])
        o.u32(s["texgen"])
        o.u8(s["flags"])
        o.u32(s["fan_mask"])
        o.u16(s["final_word"])
        o.f32(s["lm_dx"])
        o.f32(s["lm_dy"])
        o.u16(s["light_count"])
        o.u32(s["light_state_start"])
        for k in ("map_x", "map_y", "map_w", "map_h"):
            o.u8(s[k])
    o.vec(B.surfaces, surface)
    o.vec(B.normal_lmap, o.u8)
    o.vec(B.alarm_lmap, o.u8)
    o.u32(0)                    # null surfaces
    o.u32(len(B.lightmaps))
    for png in B.lightmaps:
        o.b += png
        o.u8(1)                 # keep
    o.vec(B.solid_leaf_surfaces, o.u32)
    o.u32(0)                    # animated lights
    o.u32(0)                    # light states
    o.u32(0)                    # state data
    o.u32(0)                    # state data buffer size
    o.u32(0)                    # ... and its flags
    o.u32(0)                    # name buffer
    o.u32(0)                    # sub-objects

    def hull(h):
        o.u32(h["hull_start"])
        o.u16(h["hull_count"])
        o.f32(h["min"][0]); o.f32(h["max"][0])
        o.f32(h["min"][1]); o.f32(h["max"][1])
        o.f32(h["min"][2]); o.f32(h["max"][2])
        o.u32(h["surface_start"])
        o.u16(h["surface_count"])
        o.u32(h["plane_start"])
        o.u32(h["poly_plane_start"])
        o.u32(h["poly_point_start"])
        o.u32(h["poly_string_start"])
    o.vec(B.hulls, hull)
    o.u32(len(B.hull_emit_strings))
    o.b += B.hull_emit_strings
    o.vec(B.hull_indices, o.u32)
    o.vec(B.hull_plane_indices, o.u16)
    o.vec(B.hull_emit_string_indices, o.u32)
    o.vec(B.hull_surface_indices, o.u32)
    o.vec(B.poly_list_planes, o.u16)
    o.vec(B.poly_list_points, o.u32)
    o.u32(len(B.poly_list_strings))
    o.b += B.poly_list_strings
    for start, count in B.coord_bins:
        o.u32(start)
        o.u32(count)
    o.vec(B.coord_bin_indices, o.u16)
    o.u32(0)                    # coord bin mode: x/y
    o.b += bytes((0, 0, 0, 255))    # base ambient
    o.b += bytes((0, 0, 0, 255))    # alarm ambient
    o.u32(0)                    # (v < 10) spare
    o.u32(0)                    # (v < 11) spare
    o.u32(0)                    # (v < 11) spare
    o.u32(0)                    # no extended lightmap data


def write_dif(B: Built) -> bytes:
    o = Out()
    o.u32(RESOURCE_VERSION)
    o.u8(0)                     # no preview bitmap
    o.u32(1)                    # one detail level
    write_interior(o, B)
    for _ in range(5):          # sub-objects, triggers, path followers, force fields, AI nodes
        o.u32(0)
    # Vehicle collision present but empty (version 0, 14 empty lists), then
    # no game entities: the exact 88-byte tail map2dif writes (held ROTC files).
    o.u32(1)
    o.u32(0)
    for _ in range(14):
        o.u32(0)
    o.u32(0)
    return bytes(o.b)


# ------------------------------------------------------------------ scenes

# Colours of the test textures (nothing else in a conformance world has them).
COLOURS = {
    "conf_dif_out": (235, 235, 235),     # outside walls: near white
    "conf_dif_floor": (120, 80, 40),     # floors and ceilings: brown
    "conf_dif_a": (255, 0, 128),         # room A (zone 1): hot pink
    "conf_dif_b": (0, 128, 128),         # room B (zone 2): teal
}


def house(variant: str = "house") -> Scene:
    """An enclosed two-room house, 16 x 12 x 4.5, on its own floor slab.

    Interior coordinates (the GameObject's origin is the house's front-left
    corner at floor level; y runs from the front wall to the back):

        x -8 .. 8, y 0 .. 12, z -0.5 (floor slab) .. 4.5 (roof)
        room A: y 0.5 .. 6,  zone 1, hot pink walls
        room B: y 6.5 .. 11.5, zone 2, teal walls
        front door x -1 .. 1, z 0 .. 2.5 in the front wall (y 0 .. 0.5),
        portal outside <-> A on y = 0.5
        middle door x -1 .. 1, z 0 .. 2.5 in the middle wall (y 6 .. 6.5),
        portal A <-> B on y = 6.5

    Variants (each a deliberately chosen difference for one lab question):

    house       consistent: zones 0, 1, 2 and both portals
    single      the same geometry, everything in the outside zone, no portals
    noportal    the A <-> B doorway still splits the zones, but no portal is
                written: from inside A a zone renderer cannot reach B
    window      no front door; the front wall keeps its solid brush but has no
                surfaces, so a renderer that ignores zones shows room A from
                outside, and one that culls by zone shows nothing of it
    window1     the window file with everything in one zone (its baseline)
    """
    T = 0.5
    W, D, H = 8.0, 12.0, 4.0
    flr, a, b = "conf_dif_floor", "conf_dif_a", "conf_dif_b"   # outside faces: _outside_material
    boxes: list[Box] = []

    boxes.append(Box((-W, 0, -T), (W, D, 0), flr))              # floor slab
    boxes.append(Box((-W, 0, H), (W, D, H + T), flr))           # roof slab
    door = variant != "window" and variant != "window1"
    front_omit = frozenset({"all"}) if not door else frozenset()
    if door:
        boxes.append(Box((-W, 0, 0), (-1, T, H), a))            # front wall, left of the door
        boxes.append(Box((1, 0, 0), (W, T, H), a))              # right of the door
        boxes.append(Box((-1, 0, 2.5), (1, T, H), a))           # over the door
    else:
        boxes.append(Box((-W, 0, 0), (W, T, H), a, front_omit))
    boxes.append(Box((-W, 6, 0), (-1, 6 + T, H), a))            # middle wall
    boxes.append(Box((1, 6, 0), (W, 6 + T, H), a))
    boxes.append(Box((-1, 6, 2.5), (1, 6 + T, H), a))
    boxes.append(Box((-W, D - T, 0), (W, D, H), b))             # back wall
    # Side walls split at the middle wall so each room has its own colour.
    boxes.append(Box((-W, 0, 0), (-W + T, 6.25, H), a))
    boxes.append(Box((W - T, 0, 0), (W, 6.25, H), a))
    boxes.append(Box((-W, 6.25, 0), (-W + T, D, H), b))
    boxes.append(Box((W - T, 6.25, 0), (W, D, H), b))

    portals = []
    if door:
        portals.append(Portal(1, T, (-1, 1), (0, 2.5)))
    portals.append(Portal(1, 6 + T, (-1, 1), (0, 2.5), emit=(variant != "noportal")))
    seeds = [(0.0, 3.0, 2.0), (0.0, 9.0, 2.0)]
    zones = "single" if variant in ("single", "window1") else "flood"
    return Scene(boxes=boxes, portals=portals, seeds=seeds, zones=zones)


def _outside_material(B: Built, scene: Scene) -> None:
    """Outward-facing (zone 0) faces of the walls get the outside colour."""
    if "conf_dif_out" not in B.materials:
        B.materials.append("conf_dif_out")
    oi = B.materials.index("conf_dif_out")
    floor = B.materials.index("conf_dif_floor") if "conf_dif_floor" in B.materials else -1
    for s, z in zip(B.surfaces, B.report["surface_region"]):
        if z == OUTSIDE_ZONE and s["texture"] != floor:
            s["texture"] = oi


SCENES = {
    "house": lambda: house("house"),
    "single": lambda: house("single"),
    "noportal": lambda: house("noportal"),
    "window": lambda: house("window"),
    "window1": lambda: house("window1"),
}


def scene_bytes(name: str, **overrides) -> bytes:
    scene = SCENES[name]()
    for k, v in overrides.items():
        setattr(scene, k, v)
    B = build(scene)
    _outside_material(B, scene)
    return write_dif(B)


def main(argv: list[str]) -> int:
    if argv[:1] == ["list"]:
        for name in SCENES:
            print(name)
        return 0
    if len(argv) >= 3 and argv[0] == "scene":
        opts = {}
        for a in argv[3:]:
            k, _, v = a.partition("=")
            opts[k.lstrip("-")] = v
        data = scene_bytes(argv[1], **opts)
        with open(argv[2], "wb") as f:
            f.write(data)
        print(f"{argv[2]}: {len(data)} bytes")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
