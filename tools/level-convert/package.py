"""Future Seihai package. [inf] Not a historical Graal format.

See SEIHAI-FORMAT.md. A 2.22 client does not read this. The payload is an
unchanged GLEVNW01 level or an unchanged GRMAP001 map.
"""

from errors import ConvertError, Truncated

MAGIC = b'SEIHAI01\n'
KINDS = ('nw', 'gmap')


def dumps(kind, payload):
    """Wrap `payload` bytes. `kind` is `nw` or `gmap`."""
    if kind not in KINDS:
        raise ConvertError('seihai kind must be nw or gmap')
    if not isinstance(payload, (bytes, bytearray)):
        raise ConvertError('seihai payload must be bytes')
    header = MAGIC + f'kind {kind}\nbytes {len(payload)}\n'.encode('ascii')
    return header + bytes(payload)


def loads(data):
    """Return `(kind, payload)`. Raises Truncated when the declared length is past EOF."""
    if not isinstance(data, (bytes, bytearray)):
        raise ConvertError('seihai package must be bytes')
    data = bytes(data)
    if len(data) < len(MAGIC):
        raise Truncated('seihai package is shorter than the SEIHAI01 header')
    if not data.startswith(MAGIC):
        raise ConvertError('not a SEIHAI01 package')
    rest = data[len(MAGIC):]
    kind, rest = _header_line(rest, 'kind')
    if not kind.startswith('kind '):
        raise ConvertError('seihai header has no kind line')
    kind = kind[5:]
    if kind not in KINDS:
        raise ConvertError('seihai kind must be nw or gmap')
    bline, payload = _header_line(rest, 'bytes')
    if not bline.startswith('bytes '):
        raise ConvertError('seihai header has no bytes line')
    try:
        declared = int(bline[6:], 10)
    except ValueError as exc:
        raise ConvertError('seihai bytes line is not a length') from exc
    if declared < 0:
        raise ConvertError('seihai payload length is negative')
    if len(payload) < declared:
        raise Truncated(
            f'seihai payload declared {declared} bytes but {len(payload)} remain'
        )
    if len(payload) != declared:
        raise ConvertError('seihai package has bytes after the payload')
    _check_payload(kind, payload)
    return kind, payload


def _header_line(buf, what):
    nl = buf.find(b'\n')
    if nl < 0:
        raise Truncated(f'seihai {what} line is cut off')
    try:
        text = buf[:nl].decode('ascii')
    except UnicodeDecodeError as exc:
        raise ConvertError(f'seihai {what} line is not ASCII') from exc
    return text, buf[nl + 1:]


def _check_payload(kind, payload):
    if kind == 'nw':
        if not payload.startswith(b'GLEVNW01'):
            raise ConvertError('kind nw payload is not GLEVNW01')
    elif not payload.startswith(b'GRMAP001'):
        raise ConvertError('kind gmap payload is not GRMAP001')
