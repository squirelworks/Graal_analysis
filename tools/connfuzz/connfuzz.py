#!/usr/bin/env python3
"""Loopback conf.gs connector fuzzer for Windows 6.1.1.3 (lab only).

Builds the signed connector-reply container documented in
../../protocol/connector-script.md (4-byte marker, 256-byte RSA-2048 signature
over the bare SHA-256 of the payload, a 4-byte inner length, then the encrypted
script payload), applies one mutation at a time, and serves it over plain HTTP
for GET /conf.gs?p=... so a real 6.113 client in a lab VM fetches it.

Design and triage: ../../protocol/conf-gs-fuzzing.md

LAB ONLY. This stands in for the connector host on the loopback address, behind
a VM/namespace with no route to the public network. It is never pointed at any
real connector host, and nothing here helps reach one. No key is embedded:
signing is done by an external command with a lab key at run time (see
sign_payload). No host, key or reply body is written to disk by this module.

Pure standard library, so it runs the same on Linux, macOS and Windows.
"""
from __future__ import annotations

import argparse
import struct
import subprocess
from dataclasses import dataclass, replace
from http.server import BaseHTTPRequestHandler, HTTPServer

# Container constants (../../protocol/connector-script.md section 2).
MARKER = b"\x00\x00\x01\x00"      # 4-byte reply marker
SIG_LEN = 256                      # RSA-2048 signature, bytes
LEN_PREFIX = b"\x00\x00"           # the two fixed bytes before the 16-bit length
INNER_LEN_FIELD = 4               # marker-independent inner-length field width
PLACEHOLDER_SIG = b"\x00" * SIG_LEN  # inert signature; real one comes from signing


# --------------------------------------------------------------------------- #
# Container
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Container:
    """One connector reply, field by field, before serialization.

    declared_len is the value written into the 16-bit inner-length field. When
    None it is set to len(payload) at serialize time; override it to desync the
    declared length from the body (a framing mutation).
    """
    marker: bytes = MARKER
    signature: bytes = PLACEHOLDER_SIG
    payload: bytes = b""
    declared_len: int | None = None

    def serialize(self) -> bytes:
        n = self.payload.__len__() if self.declared_len is None else self.declared_len
        # 16-bit length, masked so an oversize override still packs.
        inner = LEN_PREFIX + struct.pack(">H", n & 0xFFFF)
        return self.marker + self.signature + inner + self.payload


def build_container(payload: bytes, signature: bytes | None = None) -> Container:
    return Container(payload=payload, signature=signature or PLACEHOLDER_SIG)


# --------------------------------------------------------------------------- #
# Signing (external; no key is ever embedded or committed)
# --------------------------------------------------------------------------- #
def sign_payload(payload: bytes, signer_cmd: list[str]) -> bytes:
    """Sign the bare SHA-256 of the payload with a lab key via an external cmd.

    signer_cmd receives the payload on stdin and must return the 256-byte
    RSA-2048 PKCS#1 v1.5 type-1 signature over the *bare* 32-byte SHA-256 digest
    (no DigestInfo) on stdout -- the scheme in connector-script.md section 2.
    The key lives only in that external command; it is never passed here and
    never written by this module. Lab use only.
    """
    out = subprocess.run(signer_cmd, input=payload, capture_output=True, check=True).stdout
    if len(out) != SIG_LEN:
        raise ValueError(f"signer returned {len(out)} bytes, expected {SIG_LEN}")
    return out


# --------------------------------------------------------------------------- #
# Mutators -- each returns (label, Container). One field per mutation.
# Deterministic: a label fully identifies the mutation, so a finding reproduces.
# --------------------------------------------------------------------------- #
def _fixed_body(n: int = 16) -> bytes:
    # A deterministic, inert placeholder payload for container (phase-A) fuzzing.
    return bytes((i * 37 + 11) & 0xFF for i in range(n))


def _fixed_sig() -> bytes:
    # A deterministic, non-zero stand-in signature for the fuzz base, so that
    # zeroing the field is a real mutation. A live run replaces it with a real
    # lab signature from sign_payload().
    return bytes((i * 53 + 7) & 0xFF for i in range(SIG_LEN))


def fuzz_base(payload_bytes: int = 16) -> "Container":
    return Container(payload=_fixed_body(payload_bytes), signature=_fixed_sig())


def mutators(base: Container) -> list[tuple[str, Container]]:
    out: list[tuple[str, Container]] = [("baseline", base)]

    # Marker
    out.append(("marker:flip0", replace(base, marker=bytes([base.marker[0] ^ 0xFF]) + base.marker[1:])))
    out.append(("marker:wrong", replace(base, marker=b"\xde\xad\xbe\xef")))
    out.append(("marker:zero", replace(base, marker=b"\x00\x00\x00\x00")))
    out.append(("marker:ff", replace(base, marker=b"\xff\xff\xff\xff")))

    # Signature field
    out.append(("sig:zero", replace(base, signature=b"\x00" * SIG_LEN)))
    out.append(("sig:ff", replace(base, signature=b"\xff" * SIG_LEN)))
    out.append(("sig:short", replace(base, signature=base.signature[:-1])))        # 255
    out.append(("sig:long", replace(base, signature=base.signature + b"\x00")))    # 257
    out.append(("sig:trunc_half", replace(base, signature=base.signature[: SIG_LEN // 2])))

    # Inner length field (declared vs actual body)
    body = base.payload
    out.append(("len:oversize", replace(base, declared_len=len(body) + 0x4000)))
    out.append(("len:zero_with_body", replace(base, declared_len=0)))
    out.append(("len:max", replace(base, declared_len=0xFFFF)))
    # high two bytes of the 4-byte field non-zero: encode by widening the prefix.
    out.append(("len:highbytes", _HighBytes(base)))

    # Payload vs declared length
    out.append(("payload:short_body", replace(base, payload=body[: max(0, len(body) - 4)], declared_len=len(body))))
    out.append(("payload:long_body", replace(base, payload=body + b"\x41" * 32, declared_len=len(body))))
    out.append(("payload:empty", replace(base, payload=b"", declared_len=len(body))))
    out.append(("payload:nul", replace(base, payload=b"\x00" * len(body) if body else b"\x00")))

    return out


def _HighBytes(base: Container) -> Container:
    """A container whose 4-byte inner-length field has non-zero high bytes.

    The stock field is `00 00` + 16-bit length; this flips the two fixed bytes.
    Serialized via a thin subclass so the rest of the pipeline is unchanged.
    """
    return _HighBytesContainer(marker=base.marker, signature=base.signature,
                               payload=base.payload, declared_len=base.declared_len)


@dataclass(frozen=True)
class _HighBytesContainer(Container):
    def serialize(self) -> bytes:
        n = len(self.payload) if self.declared_len is None else self.declared_len
        inner = b"\xff\xff" + struct.pack(">H", n & 0xFFFF)   # high bytes non-zero
        return self.marker + self.signature + inner + self.payload


# --------------------------------------------------------------------------- #
# HTTP response composition (pure) + lab responder
# --------------------------------------------------------------------------- #
def compose_http_response(body: bytes, lie_content_length: int | None = None,
                          truncate_to: int | None = None) -> bytes:
    """The exact bytes an HTTP/1.0 200 reply would put on the wire.

    lie_content_length overrides the Content-Length header (transport mutation).
    truncate_to cuts the emitted body after the headers (early-EOF mutation).
    Kept pure so the offline selftest can assert it without a socket.
    """
    clen = len(body) if lie_content_length is None else lie_content_length
    head = (
        b"HTTP/1.0 200 OK\r\n"
        b"Content-Type: application/octet-stream\r\n"
        b"Content-Length: " + str(clen).encode() + b"\r\n"
        b"Connection: close\r\n\r\n"
    )
    out = head + body
    if truncate_to is not None:
        out = out[: len(head) + truncate_to]
    return out


def make_handler(reply_bytes: bytes, lie_content_length=None, truncate_to=None):
    composed = compose_http_response(reply_bytes, lie_content_length, truncate_to)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            # Serve the configured reply for the conf.gs fetch regardless of ?p=.
            self.wfile.write(composed)

        def log_message(self, *a):  # keep the lab console quiet
            pass

    return Handler


def serve(reply_bytes: bytes, port: int, host: str = "localhost",
          lie_content_length=None, truncate_to=None) -> None:
    """Serve one fixed (possibly mutated) reply on loopback. Lab use only."""
    httpd = HTTPServer((host, port), make_handler(reply_bytes, lie_content_length, truncate_to))
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Loopback conf.gs fuzzer (lab only).")
    ap.add_argument("--port", type=int, default=8080, help="loopback HTTP port")
    ap.add_argument("--mutation", default="baseline", help="mutation label to serve")
    ap.add_argument("--payload-bytes", type=int, default=16,
                    help="size of the inert placeholder payload (phase-A)")
    ap.add_argument("--list", action="store_true", help="list mutation labels and exit")
    args = ap.parse_args()

    base = fuzz_base(args.payload_bytes)
    muts = dict(mutators(base))
    if args.list:
        for label in muts:
            print(label)
        return
    if args.mutation not in muts:
        raise SystemExit(f"unknown mutation {args.mutation!r}; use --list")
    reply = muts[args.mutation].serialize()
    print(f"serving mutation {args.mutation} ({len(reply)} bytes) on localhost:{args.port}")
    serve(reply, args.port)


if __name__ == "__main__":
    main()
