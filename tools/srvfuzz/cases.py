#!/usr/bin/env python3
"""Fuzz-case generators for srvfuzz (client->server, original Graal servers).

A Case is a named, categorised bundle of raw bytes already framed for the wire, plus a
flag for whether it should be sent after a clean login (`pre_login=True`) or on its own
to a fresh socket (`pre_login=False`, for pre-auth / frame / login cases).

Categories (pick one with srvfuzz `--only CAT`):

  frame        malformed u16/zlib framing: bad length, non-zlib, truncated, oversized,
               over-inflating, empty, and a frame packed with thousands of empty packets
  login        malformed gen-2 login: bad/empty/oversized token, wrong type byte,
               length-prefix overruns, truncated, duplicate logins   (gen2 only)
  idsweep      every client->server id 0..223 with an empty body, after a clean login
  body         well-known ids with malformed bodies: truncated numbers, oversized
               GSTRING length prefixes, out-of-range prop ids, path traversal in file
               requests, huge inline text, NUL / high bytes, embedded newlines
  listlogin    malformed pre-2.2 listserver login / request                (list only)

Each generator yields payload bytes; build() numbers them and tags the category. The
numbers are stable for a given code version, so `--resume N` is meaningful.

Everything is built on the loopback target only; see README.md. No payload here contains
a real host, IP or port.
"""
import os, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from srvfuzz import frame_zlib, login_gen2, list_login_frames  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'probe'))
from gen5probe import encode  # noqa: E402  (spec mini-language: 'id c:N s:N i3:N b:N t:TEXT str:TEXT hex:HEX')


class Case:
    __slots__ = ('n', 'cat', 'name', 'payload', 'pre_login')

    def __init__(self, cat, name, payload, pre_login):
        self.n = -1; self.cat = cat; self.name = name
        self.payload = payload; self.pre_login = pre_login


def u16(n):
    return (n & 0xffff).to_bytes(2, 'big')


# ------------------------------------------------------------------- frame-level cases

def frame_cases():
    """Malformed framing, each on a fresh pre-auth connection. Hits the length reader and
    the zlib stage before any packet is parsed -- the first code an old server runs."""
    good = zlib.compress(encode('0'), 9)  # a trivially valid one-packet body

    yield Case('frame', 'len-zero', u16(0), False)
    yield Case('frame', 'len-zero-then-body', u16(0) + good, False)
    # length claims more than we send, then we stop: tests blocking/partial-read handling.
    yield Case('frame', 'len-overruns-short', u16(len(good) + 4096) + good, False)
    # length shorter than the real stream: the extra bytes should start the next frame (desync).
    yield Case('frame', 'len-underruns', u16(max(1, len(good) - 3)) + good, False)
    # a body that is not zlib at all.
    yield Case('frame', 'not-zlib', u16(16) + b'\x00\x01\x02\x03nonsensebytes!!', False)
    yield Case('frame', 'zlib-header-only', u16(2) + b'\x78\x9c', False)
    # a valid header then a truncated deflate stream.
    yield Case('frame', 'zlib-truncated', u16(len(good) // 2 or 1) + good[:max(1, len(good) // 2)], False)
    # maximum u16 frame of valid zlib (lots of small packets).
    big = zlib.compress(b''.join(encode(str(i % 50)) for i in range(2000)), 9)
    yield Case('frame', 'u16-max-valid', u16(len(big)) + big, False)
    # a decompression-ratio case: a few KB of zlib that inflates toward tens of MB. Bounded,
    # loopback only; tests whether the server inflates without a cap (a classic old-server DoS).
    bomb_src = b'A' * (8 << 20)  # 8 MiB of one byte -> a few KB compressed
    bomb = zlib.compress(bomb_src, 9)
    yield Case('frame', 'inflate-ratio-8mb', u16(len(bomb) & 0xffff) + bomb, False)
    # a frame whose inflated body is one enormous "packet" with no newline.
    noln = zlib.compress(bytes([0 + 32]) + b'Z' * (1 << 20), 9)
    yield Case('frame', 'giant-line-no-newline', u16(len(noln) & 0xffff) + noln, False)
    # a frame of only newlines (thousands of empty packets).
    empties = zlib.compress(b'\n' * 20000, 9)
    yield Case('frame', 'all-empty-packets', u16(len(empties) & 0xffff) + empties, False)
    # two length-prefixed frames back to back in one send.
    yield Case('frame', 'two-frames-one-send', frame_zlib(encode('0')) + frame_zlib(encode('0')), False)


# ------------------------------------------------------------------- gen-2 login cases

def gen2_login_cases(token):
    """Malformed gen-2 login lines. Each is its own fresh connection; all pre-auth."""
    def fr(body):
        return frame_zlib(body)

    # wrong / junk tokens
    for t in ('GSERV000', 'GSERV999', 'GSERV', 'ZZZZZZZZ', 'GNW30123', '\x00\x00\x00\x00\x00\x00\x00\x00'):
        yield Case('login', 'token-%s' % t.encode('latin1').hex()[:8], fr(login_gen2(t, 'guest', 'guest')), False)
    # token field too short: only 3 bytes where 8 are read -> reads into the length prefix.
    yield Case('login', 'token-short-3', fr(bytes([32]) + b'GSE' + bytes([32 + 5]) + b'guest' + bytes([32 + 5]) + b'guest'), False)
    # wrong type bytes (1 = RC path; others undefined)
    for ty in (1, 2, 5, 0x40, 0x7f):
        yield Case('login', 'type-%d' % ty, fr(login_gen2(token, 'guest', 'guest', ptype=ty)), False)
    # account / password length-prefix overruns: prefix says long, few bytes follow.
    yield Case('login', 'acct-len-overrun',
               fr(bytes([32]) + token.encode('latin1') + bytes([32 + 100]) + b'ab' + bytes([32 + 5]) + b'guest'), False)
    yield Case('login', 'pass-len-overrun',
               fr(bytes([32]) + token.encode('latin1') + bytes([32 + 5]) + b'guest' + bytes([32 + 100]) + b'ab'), False)
    # zero-length account and password.
    yield Case('login', 'empty-acct-pass', fr(login_gen2(token, '', '')), False)
    # very long account / password.
    yield Case('login', 'acct-250', fr(login_gen2(token, 'a' * 250, 'guest')), False)
    yield Case('login', 'pass-250', fr(login_gen2(token, 'guest', 'p' * 250)), False)
    # account with NUL and high bytes.
    yield Case('login', 'acct-nul-high',
               fr(bytes([32]) + token.encode('latin1') + bytes([32 + 6]) + b'a\x00b\xff c' + bytes([32 + 5]) + b'guest'), False)
    # login line with no fields at all after the type byte.
    yield Case('login', 'type-only', fr(bytes([32])), False)
    # truncated: type + partial token.
    yield Case('login', 'trunc-token', fr(bytes([32]) + b'GSERV'), False)
    # two login lines in one frame (each login_gen2 already ends in '\n').
    yield Case('login', 'double-login', fr(login_gen2(token, 'guest', 'guest') + login_gen2(token, 'guest', 'guest')), False)
    # a non-login id as the very first packet (login expected first).
    yield Case('login', 'first-packet-not-login', fr(encode('2 c:5 c:11')), False)


# --------------------------------------------------------------- post-login id sweep

def idsweep_cases():
    """Every client->server id 0..223 with an empty body, after a clean login.

    17 (BADDYADD) is included here against the *server* (unlike the client-side sweep, where an
    empty one crashes the 6.03r7 *client*); the server is the target and we want its reaction.
    """
    for i in range(0, 224):
        yield Case('idsweep', 'id-%d' % i, frame_zlib(encode(str(i))), True)


# --------------------------------------------------------------- post-login body cases

def body_cases():
    """Well-known client->server ids with malformed bodies, after a clean login.

    ids (../../protocol/OPCODE-SUMMARY.md): 0 LEVELWARP, 1 BOARDMODIFY, 2 PLAYERPROPS,
    3 NPCPROPS, 4 ADDBOMB, 20 OPENCHEST, 23 WANTFILE, 30 LEVELWARPMOD, 37 LANGUAGE,
    51..87 RC ops. We aim malformed shapes at the ones that parse a body.
    """
    def fr(spec):
        return frame_zlib(encode(spec))

    def frbytes(b):
        return frame_zlib(b)

    # LEVELWARP (0): coords then a level name. Truncate and overrun.
    yield Case('body', 'warp-truncated-coords', frbytes(bytes([0 + 32, 32])), True)
    yield Case('body', 'warp-name-250', fr('0 c:30 c:30 t:%s' % ('x' * 250)), True)
    yield Case('body', 'warp-name-traversal', fr('0 c:30 c:30 t:../../../../etc/passwd'), True)
    yield Case('body', 'warp-name-nul', frbytes(bytes([0 + 32, 62, 62]) + b'lvl\x00evil.nw'), True)

    # BOARDMODIFY (1): x, y, width, then tiles. Feed out-of-range geometry and short tile data.
    yield Case('body', 'board-huge-dims', fr('1 c:0 c:0 s:9999 s:9999'), True)
    yield Case('body', 'board-neg-ish', frbytes(bytes([1 + 32]) + bytes([0, 0, 0, 0])), True)
    yield Case('body', 'board-width-no-tiles', fr('1 c:10 c:10 c:64'), True)

    # PLAYERPROPS (2): a prop id then its value. Out-of-range prop ids and bad widths.
    for pid in (34, 90, 200, 223):
        yield Case('body', 'props-propid-%d' % pid, fr('2 c:%d c:5' % pid), True)
    yield Case('body', 'props-trunc-after-id', frbytes(bytes([2 + 32, 32 + 15])), True)  # prop 15 (X), no value
    yield Case('body', 'props-str-overrun', frbytes(bytes([2 + 32, 32 + 33, 32 + 100]) + b'ab'), True)  # nickname len overrun
    # nickname (prop 0) GSTRING: length byte caps at 223, so send prefix 223 + 250 bytes (overrun).
    yield Case('body', 'props-nick-223p', frbytes(bytes([2 + 32, 32 + 0, 32 + 223]) + b'n' * 250), True)
    yield Case('body', 'props-many', frbytes(bytes([2 + 32]) + bytes([(32 + (i % 40)) & 0xff for i in range(400)])), True)

    # NPCPROPS (3): an npc id (3 bytes) then props. Truncate the id, then overrun a prop.
    yield Case('body', 'npcprops-trunc-id', frbytes(bytes([3 + 32, 32, 32])), True)
    yield Case('body', 'npcprops-bad-prop', fr('3 i3:1 c:200 t:junk'), True)

    # WANTFILE (23): a file name string. Classic old-server file-request surface.
    yield Case('body', 'wantfile-traversal', fr('23 t:../../../../etc/passwd'), True)
    yield Case('body', 'wantfile-win-traversal', fr('23 t:..\\..\\..\\windows\\win.ini'), True)
    yield Case('body', 'wantfile-250', fr('23 t:%s.nw' % ('a' * 250)), True)
    yield Case('body', 'wantfile-nul', frbytes(bytes([23 + 32]) + b'levels/start.nw\x00.gmap'), True)
    yield Case('body', 'wantfile-empty', fr('23'), True)
    yield Case('body', 'wantfile-abs', fr('23 t:/etc/passwd'), True)

    # OPENCHEST (20) and LEVELWARPMOD (30): coord-bearing ids, truncated.
    yield Case('body', 'openchest-trunc', frbytes(bytes([20 + 32, 32])), True)
    yield Case('body', 'levelwarpmod-name-250', fr('30 c:30 c:30 t:%s' % ('w' * 250)), True)

    # LANGUAGE (37): a language string.
    yield Case('body', 'language-250', fr('37 t:%s' % ('L' * 250)), True)

    # RC op ids (51..87) with a body, after a *player* login (should be rejected / ignored).
    for i in (51, 60, 70, 80, 87):
        yield Case('body', 'rc-op-%d-asplayer' % i, fr('%d t:AAAA' % i), True)

    # a packet body with embedded newlines (splits into extra lines) and a lone-CR case.
    yield Case('body', 'embedded-newlines', frbytes(bytes([2 + 32]) + b'\n\n\n' + bytes([32 + 5, 32 + 11])), True)
    yield Case('body', 'embedded-cr', frbytes(bytes([2 + 32]) + b'a\rb' + b'\n'), True)
    # a single frame carrying many copies of a benign prop update (flood in one frame).
    yield Case('body', 'props-flood-500', frbytes((encode('2 c:5 c:11')) * 500), True)


# --------------------------------------------------------------- listserver cases

def list_login_cases():
    """Malformed pre-2.2 listserver logins / requests. Each on a fresh connection."""
    def fr(b):
        return frame_zlib(b)

    # well-formed baseline variants
    yield Case('listlogin', 'v1-only', fr(bytes([0 + 32]) + b'newmain' + b'\n'), False)
    yield Case('listlogin', 'serverlist-only', fr(bytes([1 + 32]) + bytes([32 + 5]) + b'guest' + bytes([32 + 5]) + b'guest' + b'\n'), False)
    # id 0 with a huge / odd version string
    yield Case('listlogin', 'v1-version-250', fr(bytes([0 + 32]) + b'n' * 250 + b'\n'), False)
    yield Case('listlogin', 'v1-empty', fr(bytes([0 + 32]) + b'\n'), False)
    # SERVERLIST account / password length overruns
    yield Case('listlogin', 'serverlist-acct-overrun', fr(bytes([1 + 32]) + bytes([32 + 100]) + b'ab' + bytes([32 + 5]) + b'guest' + b'\n'), False)
    # account GSTRING cannot express 250 in one GCHAR: prefix says 223, 250 bytes follow (overrun).
    yield Case('listlogin', 'serverlist-acct-223p', fr(bytes([1 + 32]) + bytes([32 + 223]) + b'a' * 250 + bytes([32 + 5]) + b'guest' + b'\n'), False)
    # unknown / out-of-range ids
    for i in (2, 3, 4, 6, 8, 50, 223):
        yield Case('listlogin', 'id-%d' % i, fr(bytes([(i + 32) & 0xff]) + b'junk' + b'\n'), False)
    # id 7 V2ENCRYPTKEYCL shape sent to a pre-2.2 server (no gen-5 follows)
    yield Case('listlogin', 'id7-v2key-to-pre22', fr(bytes([7 + 32, 32 + 42]) + b'GNW30123newmain' + b'\n'), False)
    # GRSECURELOGIN (223) Graal Reborn extension with a long blob
    yield Case('listlogin', 'grsecurelogin-blob', fr(bytes([223 + 32]) + b'G' * 120 + b'\n'), False)
    # id sweep against the listserver, empty bodies
    for i in range(0, 16):
        yield Case('listlogin', 'empty-id-%d' % i, fr(bytes([(i + 32) & 0xff]) + b'\n'), False)
    # frame-level cases apply to the listserver too (same framing)
    for c in frame_cases():
        yield Case('listlogin', 'frame-' + c.name, c.payload, False)


# --------------------------------------------------------------------------- build

def build(mode, token):
    out = []
    if mode == 'gen2':
        gens = [frame_cases(), gen2_login_cases(token), idsweep_cases(), body_cases()]
    elif mode == 'list':
        gens = [list_login_cases()]
    else:
        raise ValueError('unknown mode %r' % mode)
    n = 0
    for g in gens:
        for c in g:
            c.n = n; n += 1; out.append(c)
    return out


if __name__ == '__main__':  # `python3 cases.py gen2` prints the plan without sending anything
    m = sys.argv[1] if len(sys.argv) > 1 else 'gen2'
    for c in build(m, 'GSERV014'):
        print('%4d  %-10s  %-28s  %4d bytes  %s' % (c.n, c.cat, c.name, len(c.payload), 'post-login' if c.pre_login else 'fresh'))
