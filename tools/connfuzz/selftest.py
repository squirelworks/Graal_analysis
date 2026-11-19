#!/usr/bin/env python3
"""Offline selftest for connfuzz. No client, no keys, no network.

Asserts the container layout, that each mutator changes exactly the field it
claims, and that the HTTP response composer honours its options. Run:

    python3 selftest.py

Pure standard library; the CI `checks` job can run it the way it runs
tools/probe/selftest.py.
"""
from __future__ import annotations

import struct
import sys

import connfuzz as cf


def _check(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_layout() -> None:
    body = bytes(range(20))
    c = cf.build_container(body)
    raw = c.serialize()
    _check(raw[0:4] == cf.MARKER, "marker at offset 0")
    _check(raw[4:4 + cf.SIG_LEN] == cf.PLACEHOLDER_SIG, "signature after marker")
    off = 4 + cf.SIG_LEN
    _check(raw[off:off + 2] == cf.LEN_PREFIX, "length prefix is 00 00")
    _check(struct.unpack(">H", raw[off + 2:off + 4])[0] == len(body), "declared len == body len")
    _check(raw[off + 4:] == body, "payload after inner length")
    _check(len(raw) == 4 + cf.SIG_LEN + cf.INNER_LEN_FIELD + len(body), "total length")


def test_mutators() -> None:
    base = cf.fuzz_base(16)
    base_raw = base.serialize()
    muts = dict(cf.mutators(base))

    _check(muts["baseline"].serialize() == base_raw, "baseline is unchanged")

    # Marker mutations touch only the first 4 bytes.
    for label in ("marker:flip0", "marker:wrong", "marker:zero", "marker:ff"):
        raw = muts[label].serialize()
        _check(raw[4:] == base_raw[4:], f"{label} changes only the marker")
        _check(raw[0:4] != base_raw[0:4], f"{label} actually changed the marker")

    # Signature field width mutations.
    _check(len(muts["sig:zero"].serialize()) == len(base_raw), "sig:zero keeps size")
    _check(muts["sig:zero"].serialize()[4:4 + cf.SIG_LEN] == b"\x00" * cf.SIG_LEN, "sig:zero is zeros")
    _check(muts["sig:ff"].serialize()[4:4 + cf.SIG_LEN] == b"\xff" * cf.SIG_LEN, "sig:ff is 0xff")
    _check(len(muts["sig:short"].signature) == cf.SIG_LEN - 1, "sig:short is 255 bytes")
    _check(len(muts["sig:long"].signature) == cf.SIG_LEN + 1, "sig:long is 257 bytes")
    _check(len(muts["sig:trunc_half"].signature) == cf.SIG_LEN // 2, "sig:trunc_half halves it")

    # Inner-length field mutations: read the declared 16-bit value back.
    def declared(raw: bytes) -> int:
        off = 4 + cf.SIG_LEN
        return struct.unpack(">H", raw[off + 2:off + 4])[0]

    body_len = len(base.payload)
    _check(declared(muts["len:oversize"].serialize()) == ((body_len + 0x4000) & 0xFFFF), "len:oversize declared")
    _check(declared(muts["len:zero_with_body"].serialize()) == 0, "len:zero_with_body declared 0")
    _check(declared(muts["len:max"].serialize()) == 0xFFFF, "len:max declared 0xFFFF")

    # High-bytes mutation flips the two fixed prefix bytes.
    hb = muts["len:highbytes"].serialize()
    off = 4 + cf.SIG_LEN
    _check(hb[off:off + 2] == b"\xff\xff", "len:highbytes sets non-zero high bytes")
    _check(hb[off:off + 2] != cf.LEN_PREFIX, "len:highbytes differs from stock prefix")

    # Payload-vs-declared mutations.
    sb = muts["payload:short_body"]
    _check(len(sb.payload) == body_len - 4 and sb.declared_len == body_len, "payload:short_body desyncs")
    lb = muts["payload:long_body"]
    _check(len(lb.payload) == body_len + 32 and lb.declared_len == body_len, "payload:long_body desyncs")
    _check(muts["payload:empty"].payload == b"" and muts["payload:empty"].declared_len == body_len,
           "payload:empty declares a body it does not send")
    _check(set(muts["payload:nul"].payload) <= {0}, "payload:nul is all NUL")

    # Every mutation must serialize without raising and differ from baseline
    # (except the baseline itself).
    for label, c in muts.items():
        raw = c.serialize()
        _check(isinstance(raw, bytes) and len(raw) >= 4, f"{label} serializes to bytes")
        if label != "baseline":
            _check(raw != base_raw, f"{label} differs from baseline")


def test_http() -> None:
    body = b"hello-body"
    r = cf.compose_http_response(body)
    _check(r.endswith(body), "response ends with the body")
    _check(b"Content-Length: 10\r\n" in r, "honest content-length")

    r2 = cf.compose_http_response(body, lie_content_length=9999)
    _check(b"Content-Length: 9999\r\n" in r2, "lied content-length header")
    _check(r2.endswith(body), "lie keeps the real body")

    r3 = cf.compose_http_response(body, truncate_to=4)
    _check(r3.endswith(body[:4]), "truncate_to cuts the body")
    _check(not r3.endswith(body), "truncate_to really truncated")


def main() -> int:
    for fn in (test_layout, test_mutators, test_http):
        fn()
        print(f"ok  {fn.__name__}")
    print("connfuzz selftest: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
