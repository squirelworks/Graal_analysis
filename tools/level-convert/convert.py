#!/usr/bin/env python3
"""Convert one Graal level, or a directory of them, across the level generations.

    python3 tools/level-convert/convert.py <src> <dst>

The suffix chooses the file:

    .zelda   Z3-V1.04   board, links, baddies, signs. No NPC section, no chest section.
    .graal   GR-V1.03   those, plus NPCs and chests.
    .nw      GLEVNW01   those, plus a HEIGHTS overlay when the level has one.
    .gmap    GRMAP001   a grid of level-file names, built from a directory.
    .seihai  SEIHAI01   a future package around one .nw level or one .gmap. [inf]

A .gmap is not one level renamed. Give it a directory that holds grid.txt
or GraalLevelGen names (prefix_a-01.nw). Reading a .gmap back writes that
directory's grid.txt. It does not invent the level files.

Exit status 1 when the file is truncated. Other failures exit 2.
"""

import sys
from pathlib import Path

from errors import ConvertError, Truncated
import gmapio
import levelio
import package

_LEVEL = {'zelda', 'graal', 'nw'}
_EXT = {
    '.zelda': 'zelda',
    '.graal': 'graal',
    '.nw': 'nw',
    '.gmap': 'gmap',
    '.seihai': 'seihai',
}


def convert(src, dst):
    """Convert `src` to `dst`. Returns warning strings. Writes nothing on failure."""
    warnings = []
    src_path, dst_path = Path(src), Path(dst)
    src_kind = _src_kind(src_path)
    dst_kind = _dst_kind(dst_path)
    if src_path.resolve() == dst_path.resolve() and src_kind != 'dir':
        raise ConvertError('source and destination are the same file')
    if src_kind == 'dir' and dst_path.exists() and _inside(dst_path, src_path):
        raise ConvertError('destination is inside the source directory')

    if src_kind in _LEVEL and dst_kind in _LEVEL:
        level = levelio.load_path(src_path, warnings)
        _write_bytes(dst_path, levelio.dumps_level(level, dst_kind, warnings))
    elif src_kind in _LEVEL and dst_kind == 'seihai':
        _write_bytes(dst_path, _level_package(src_path, src_kind, warnings))
    elif src_kind == 'seihai' and dst_kind == 'nw':
        _write_bytes(dst_path, _nw_payload(levelio.read_file(src_path)))
    elif src_kind == 'seihai' and dst_kind in _LEVEL:
        level = _level_from_package(levelio.read_file(src_path), warnings)
        _write_bytes(dst_path, levelio.dumps_level(level, dst_kind, warnings))
    elif src_kind == 'dir' and dst_kind == 'gmap':
        gmap = gmapio.load_directory(src_path, warnings)
        _write_bytes(dst_path, gmapio.dumps(gmap))
    elif src_kind == 'dir' and dst_kind == 'seihai':
        gmap = gmapio.load_directory(src_path, warnings)
        payload = gmapio.dumps(gmap)
        gmapio.loads(payload)
        _write_bytes(dst_path, package.dumps('gmap', payload))
    elif src_kind == 'gmap' and dst_kind == 'gmap':
        data = levelio.read_file(src_path)
        gmap = gmapio.loads(data, warnings)
        _write_bytes(dst_path, gmapio.dumps(gmap))
    elif src_kind == 'gmap' and dst_kind == 'dir':
        gmap = gmapio.loads(levelio.read_file(src_path), warnings)
        _write_dir(dst_path, gmap)
    elif src_kind == 'gmap' and dst_kind == 'seihai':
        data = levelio.read_file(src_path)
        gmapio.loads(data, warnings)
        _write_bytes(dst_path, package.dumps('gmap', data))
    elif src_kind == 'seihai' and dst_kind == 'gmap':
        _write_bytes(dst_path, _gmap_payload(levelio.read_file(src_path), warnings))
    elif src_kind == 'seihai' and dst_kind == 'dir':
        gmap = gmapio.loads(_gmap_payload(levelio.read_file(src_path), warnings), warnings)
        _write_dir(dst_path, gmap)
    elif src_kind == 'seihai' and dst_kind == 'seihai':
        data = levelio.read_file(src_path)
        kind, payload = package.loads(data)
        if kind == 'nw':
            levelio.loads_nw(payload)
        else:
            gmapio.loads(payload)
        _write_bytes(dst_path, data)
    elif src_kind in _LEVEL and dst_kind == 'gmap':
        raise ConvertError(
            'a .gmap is a grid of level files, built from a directory, not one level renamed'
        )
    elif src_kind == 'gmap' and dst_kind in _LEVEL:
        raise ConvertError('a .gmap is a grid of level names, not one level')
    elif src_kind == 'dir' and dst_kind in _LEVEL:
        raise ConvertError(
            'a directory of levels becomes a .gmap, or a .seihai package of that gmap, not one level'
        )
    elif src_kind == 'dir' and dst_kind == 'dir':
        raise ConvertError('name a .gmap or a .seihai file as the destination of a directory')
    elif dst_kind == 'dir':
        raise ConvertError('only a .gmap, or a .seihai package of one, can be written as a directory')
    else:
        raise ConvertError(f'cannot convert {src_kind} to {dst_kind}')
    return warnings


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print(
            'usage: python3 tools/level-convert/convert.py <src> <dst>',
            file=sys.stderr,
        )
        return 2
    try:
        warnings = convert(args[0], args[1])
    except Truncated as exc:
        print(f'truncated: {exc}', file=sys.stderr)
        return 1
    except ConvertError as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
    for warning in warnings:
        print(f'warning: {warning}', file=sys.stderr)
    return 0


def _level_package(path, kind, warnings):
    if kind == 'nw':
        payload = levelio.read_file(path)
        # Keep the file bytes. Parsing only rejects a truncated level.
        levelio.loads_nw(payload, [])
    else:
        level = levelio.load_path(path, warnings)
        payload = levelio.dumps_level(level, 'nw', warnings)
        levelio.loads_nw(payload)
    return package.dumps('nw', payload)


def _level_from_package(data, warnings):
    return levelio.loads_nw(_nw_payload(data), warnings)


def _nw_payload(data):
    kind, payload = package.loads(data)
    if kind != 'nw':
        raise ConvertError('this package holds a gmap, not one level')
    levelio.loads_nw(payload, [])
    return payload


def _gmap_payload(data, warnings):
    kind, payload = package.loads(data)
    if kind != 'gmap':
        raise ConvertError('this package holds one level, not a gmap')
    gmapio.loads(payload, warnings)
    return payload


def _src_kind(path):
    if not path.exists():
        raise ConvertError(f'file does not exist: {path}')
    if path.is_dir():
        return 'dir'
    kind = _EXT.get(path.suffix.lower())
    if kind is None:
        raise ConvertError(f'unknown source type {path.suffix!r}')
    return kind


def _dst_kind(path):
    if path.exists() and path.is_dir():
        return 'dir'
    kind = _EXT.get(path.suffix.lower())
    if kind is not None:
        return kind
    if path.suffix == '':
        return 'dir'
    raise ConvertError(f'unknown destination type {path.suffix!r}')


def _write_bytes(path, data):
    path = Path(path)
    if path.exists() and path.is_dir():
        raise ConvertError(f'{path} is a directory')
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data)
    tmp.replace(path)


def _write_dir(path, gmap):
    path = Path(path)
    if path.exists() and not path.is_dir():
        raise ConvertError(f'{path} is not a directory')
    if path.exists() and any(path.iterdir()):
        raise ConvertError(f'{path} is not empty')
    path.mkdir(parents=True, exist_ok=True)
    (path / gmapio.GRID_NAME).write_bytes(gmapio.dumps_grid(gmap).encode('latin-1'))


def _inside(child, parent):
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    sys.exit(main())
