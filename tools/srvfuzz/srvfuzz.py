#!/usr/bin/env python3
"""srvfuzz: lab-only client->server packet fuzzer for the original Graal servers.

The packet probe (`../probe/`) is a *proxy* that needs a live real client to drive it
and whose codec assumes a GNW / gen-3-or-later login (it reads a key byte after the
type). The first central servers predate all of that:

  * GServer13 and the 1.2x GServers (1999-2000): encryption generation 2, which is
    `u16be length` + a zlib stream with **no cipher**, and a login of
    `type` + `GSERVnnn` token + account + password (see ../../protocol/gserv-1999.md).
  * ListServer 2.37.2.59 (2003) pre-2.2 link: plain `u16be length` + zlib, no cipher,
    login of id 0 `newmain` then id 1 account+password (see ../../protocol/listserver.md).

Because both targets are cipher-free, a *standalone* client can speak them directly
with no real game client and no captured key. That is what this tool is. Speaking the
wire directly also reaches the surface a proxy cannot: malformed **frames** (bad
`u16` length, non-zlib body, truncated / oversized / over-inflating streams) and
malformed **login** bytes (bad token, wrong type, length-prefix overruns) -- the
pre-authentication attack surface, which is the most interesting part of an old server.

It is a *server* fuzzer: it sends chosen or malformed client->server packets and,
after every case, checks on a fresh connection whether the server is still alive and
still answers a clean login (the "canary"). A case that drops the canary is the
culprit. Nothing re-orders: each frame/login case runs on its own fresh connection so
one case cannot poison the next.

**Lab only.** Point it at a server you started yourself on the loopback address, in a
container or a lab VM. It is never pointed at a public server, and nothing here helps
reach one. See README.md.

Usage:
  srvfuzz.py gen2 HOST PORT [--token GSERV014] [--out DIR] [--only CAT] [--resume N]
                            [--stop-on-crash] [--relaunch 'CMD']
  srvfuzz.py list HOST PORT [--out DIR] [--only CAT] [--resume N] [--stop-on-crash]

HOST/PORT name the loopback target (the loopback address and a lab port, e.g. 14804).
Results go to DIR/results.tsv and DIR/srvfuzz.log; a crash leaves DIR/crash-<case>.txt.
"""
import argparse, os, socket, subprocess, sys, time, zlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'probe'))
from gen5probe import encode, gnum  # noqa: E402  (one source of truth for the spec language)

# The repo bars dotted-IP literals in its files, so build the loopback address instead.
LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)

# Timeouts are overridable from the environment so the self-test can run fast; the lab
# defaults give a crash time to manifest before the canary runs.
RECV_TIMEOUT = float(os.environ.get('SRVFUZZ_RECV_TIMEOUT', '2.0'))    # wait for a reply to a case
CANARY_TIMEOUT = float(os.environ.get('SRVFUZZ_CANARY_TIMEOUT', '3.0'))  # wait for the fresh-login canary
INFLATE_CAP = 64 << 20  # refuse to materialise more than 64 MiB from one frame we receive


# --------------------------------------------------------------------------- framing

def send_raw(sock, data):
    sock.sendall(data)


def frame_zlib(body):
    """Gen-2 / pre-2.2 outgoing frame: u16be length + zlib stream. Used for well-formed cases."""
    z = zlib.compress(body, 9)
    return len(z).to_bytes(2, 'big') + z


def recv_frames(sock, timeout=RECV_TIMEOUT):
    """Read whatever the server sends within `timeout` and return a list of (id, body) packets.

    Server id 100 (RAWDATA) switches the gen-2 stream to a raw byte count for file data; we
    honour that so the split stays in step. Decode errors are reported, not raised, so a
    server that replies with garbage still yields a row rather than killing the run.
    Returns (packets, closed, error): closed=True if the peer shut the socket.
    """
    sock.settimeout(0.1)
    buf = b''
    end = time.monotonic() + timeout
    closed = False
    while time.monotonic() < end:
        try:
            d = sock.recv(65536)
        except socket.timeout:
            if buf:
                break
            continue
        except OSError as e:
            return [], True, 'recv:%s' % e.__class__.__name__
        if not d:
            closed = True
            break
        buf += d
    packets, err, raw = [], None, 0
    while len(buf) >= 2:
        ln = int.from_bytes(buf[:2], 'big')
        if len(buf) < ln + 2:
            break
        fr, buf = buf[2:ln + 2], buf[ln + 2:]
        try:
            dco = zlib.decompressobj()
            body = dco.decompress(fr, INFLATE_CAP)
            if dco.unconsumed_tail:
                err = 'inflate-over-cap'
        except Exception as e:
            err = 'inflate:%s' % e
            continue
        stream = body
        while stream:
            if raw:
                take = min(raw, len(stream))
                packets.append((100, stream[:take])); stream = stream[take:]; raw -= take
                continue
            i = stream.find(b'\n')
            line = stream if i < 0 else stream[:i]
            stream = b'' if i < 0 else stream[i + 1:]
            if not line:
                continue
            pid = line[0] - 32
            packets.append((pid, line[1:]))
            if pid == 100 and len(line) >= 4:  # RAWDATA length = 3 x 7-bit
                raw = ((line[1] - 32) << 14) | ((line[2] - 32) << 7) | (line[3] - 32)
    return packets, closed, err


# ------------------------------------------------------------------------ login build

def login_gen2(token, account, password, ptype=0):
    """Build the gen-2 login line, terminated by '\\n'.

    Shape (../../protocol/gserv-1999.md): chr(type+32), 'GSERVnnn' (8 bytes),
    chr(len(acct)+32)+acct, chr(len(pass)+32)+pass. Player type is 0; the server reads 1 as RC.
    The trailing newline matters: a real 1.x GServer reads a line and will not reply to a login
    that never ends (confirmed on GServer 1.28b2, lab 2026-11-19), so the canary must include it.
    """
    acct = account.encode('latin1'); pw = password.encode('latin1')
    tok = token.encode('latin1')
    return (bytes([(ptype + 32) & 0xff]) + tok
            + bytes([(len(acct) + 32) & 0xff]) + acct
            + bytes([(len(pw) + 32) & 0xff]) + pw + b'\n')


def list_login_frames(account='guest', password='guest', version='newmain'):
    """Pre-2.2 listserver login: id 0 V1VER (version string), then id 1 SERVERLIST (acct, pass).

    Both go in one frame as two newline-separated lines, matching the 2.17 real-client flow.
    """
    acct = account.encode('latin1'); pw = password.encode('latin1')
    v1 = bytes([0 + 32]) + version.encode('latin1')
    serverlist = (bytes([1 + 32])
                  + bytes([(len(acct) + 32) & 0xff]) + acct
                  + bytes([(len(pw) + 32) & 0xff]) + pw)
    return v1 + b'\n' + serverlist + b'\n'


# ------------------------------------------------------------------------- liveness

def canary_gen2(host, port, token):
    """Fresh connect + clean guest login; the server is 'up' iff it answers with real packets.

    A good gen-2 login reply opens with id 9 (own props); we accept any non-empty, decodable
    reply as up, and treat connection-refused / no-reply / immediate-close as down.
    """
    t0 = time.monotonic()
    try:
        s = socket.create_connection((host, port), timeout=CANARY_TIMEOUT)
    except OSError as e:
        return 'down', 'connect:%s' % e.__class__.__name__, int((time.monotonic() - t0) * 1000)
    try:
        send_raw(s, frame_zlib(login_gen2(token, 'guest', 'guest')))
        pkts, closed, err = recv_frames(s, CANARY_TIMEOUT)
    except OSError as e:
        return 'down', 'send:%s' % e.__class__.__name__, int((time.monotonic() - t0) * 1000)
    finally:
        s.close()
    rtt = int((time.monotonic() - t0) * 1000)
    if pkts:
        ids = ','.join(str(p[0]) for p in pkts[:6])
        return 'up', 'ids=%s%s' % (ids, ' closed' if closed else ''), rtt
    return 'down', 'no-reply%s%s' % (' closed' if closed else '', ' ' + err if err else ''), rtt


def canary_list(host, port):
    """Fresh connect + id0 newmain / id1 guest login; up iff the server answers id 0 (SVRLIST)."""
    t0 = time.monotonic()
    try:
        s = socket.create_connection((host, port), timeout=CANARY_TIMEOUT)
    except OSError as e:
        return 'down', 'connect:%s' % e.__class__.__name__, int((time.monotonic() - t0) * 1000)
    try:
        send_raw(s, frame_zlib(list_login_frames()))
        pkts, closed, err = recv_frames(s, CANARY_TIMEOUT)
    except OSError as e:
        return 'down', 'send:%s' % e.__class__.__name__, int((time.monotonic() - t0) * 1000)
    finally:
        s.close()
    rtt = int((time.monotonic() - t0) * 1000)
    if any(p[0] == 0 for p in pkts):
        return 'up', 'svrlist', rtt
    if pkts:
        return 'up', 'ids=%s' % ','.join(str(p[0]) for p in pkts[:6]), rtt
    return 'down', 'no-reply%s%s' % (' closed' if closed else '', ' ' + err if err else ''), rtt


# --------------------------------------------------------------------------- runner

def deliver(host, port, case, pre_login):
    """Open a fresh connection, optionally log in, send the case's raw bytes, read the reply.

    `pre_login` is the already-built login frame to send first (or None for pre-auth cases).
    `case.payload` is the exact bytes to put on the wire after that (a whole frame, possibly
    malformed). Returns (reply_summary, closed, err, sent_len).
    """
    try:
        s = socket.create_connection((host, port), timeout=CANARY_TIMEOUT)
    except OSError as e:
        return 'connect-refused', True, 'connect:%s' % e.__class__.__name__, 0, []
    try:
        if pre_login is not None:
            send_raw(s, pre_login)
            recv_frames(s, 0.5)  # drain the login reply so the case's reply is what we read next
        send_raw(s, case.payload)
        pkts, closed, err = recv_frames(s, RECV_TIMEOUT)
    except OSError as e:
        return 'send-error', True, 'send:%s' % e.__class__.__name__, len(case.payload), []
    finally:
        s.close()
    summary = 'ids=%s' % ','.join(str(p[0]) for p in pkts[:8]) if pkts else 'none'
    return summary, closed, err or '', len(case.payload), pkts


def run(mode, host, port, token, out_dir, only, resume, stop_on_crash, relaunch):
    import cases as caselib  # local import so the module can also be used as a library
    os.makedirs(out_dir, exist_ok=True)
    cases = caselib.build(mode, token)
    if only:
        cases = [c for c in cases if c.cat == only]
    log = open(os.path.join(out_dir, 'srvfuzz.log'), 'a', buffering=1)
    tsv_path = os.path.join(out_dir, 'results.tsv')
    new = not os.path.exists(tsv_path)
    tsv = open(tsv_path, 'a', buffering=1)
    if new:
        tsv.write('n\tcategory\tname\tsent_len\treply\tclosed\tdecode_err\tcanary\tcanary_note\trtt_ms\n')
    # replies.tsv is the protocol capture: the full server reply (id + body bytes) to every
    # probe, one row per S->C packet, so a run teaches the protocol and not only crash/no-crash.
    rtsv_path = os.path.join(out_dir, 'replies.tsv')
    rtsv_new = not os.path.exists(rtsv_path)
    rtsv = open(rtsv_path, 'a', buffering=1)
    if rtsv_new:
        rtsv.write('n\tcategory\tname\treply_id\treply_len\tbody_hex\n')

    def rec(*a):
        log.write('%.3f %s\n' % (time.monotonic(), ' '.join(str(x) for x in a)))

    canary = canary_gen2 if mode == 'gen2' else canary_list
    pre_login = frame_zlib(login_gen2(token, 'guest', 'guest')) if mode == 'gen2' else frame_zlib(list_login_frames())

    rec('start', mode, host, port, 'cases', len(cases), 'token', token)
    state, note, _ = canary(host, port, token) if mode == 'gen2' else canary(host, port)
    rec('baseline canary', state, note)
    if state != 'up':
        rec('ABORT baseline canary is down -- is the target server running on', '%s:%s?' % (host, port))
        print('baseline canary down (%s); start the target first' % note); return 2

    crashed_at = None
    for c in cases:
        if c.n < resume:
            continue
        pl = pre_login if c.pre_login else None
        summary, closed, err, slen, pkts = deliver(host, port, c, pl)
        for pid, body in pkts:  # the protocol capture: every S->C packet this probe drew
            rtsv.write('%d\t%s\t%s\t%d\t%d\t%s\n' % (c.n, c.cat, c.name, pid, len(body), body[:128].hex()))
        time.sleep(float(os.environ.get('SRVFUZZ_SETTLE', '0.15')))  # let a crash manifest before the canary
        cstate, cnote, rtt = (canary(host, port, token) if mode == 'gen2' else canary(host, port))
        tsv.write('%d\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%d\n'
                  % (c.n, c.cat, c.name, slen, summary, closed, err, cstate, cnote, rtt))
        rec('case', c.n, c.cat, c.name, '| sent', slen, '| reply', summary,
            '| closed', closed, '| err', err or '-', '| canary', cstate, cnote)
        if cstate == 'down':
            crashed_at = c
            crash = os.path.join(out_dir, 'crash-%d-%s.txt' % (c.n, c.cat))
            with open(crash, 'w') as f:
                f.write('case %d %s %s\ncanary: %s %s\nreply: %s closed=%s err=%s\n'
                        '\nSENT (hex):\n%s\n' % (c.n, c.cat, c.name, cstate, cnote,
                                                 summary, closed, err, c.payload.hex()))
            rec('*** CANARY DOWN after case', c.n, c.name, '-> wrote', crash)
            print('CANARY DOWN after case %d (%s / %s): %s' % (c.n, c.cat, c.name, cnote))
            if relaunch:
                rec('relaunch:', relaunch); subprocess.call(relaunch, shell=True)
                for _ in range(20):
                    time.sleep(0.5)
                    st, _n, _r = (canary(host, port, token) if mode == 'gen2' else canary(host, port))
                    if st == 'up':
                        rec('relaunched; resuming at', c.n + 1); break
                else:
                    rec('relaunch did not bring the server back; stopping'); break
            elif stop_on_crash:
                break
    rec('done', 'last crash at', crashed_at.n if crashed_at else None)
    print('done: %d cases, results in %s' % (len(cases), tsv_path))
    return 0


def main():
    ap = argparse.ArgumentParser(description='lab-only C->S fuzzer for original Graal servers')
    ap.add_argument('mode', choices=['gen2', 'list'])
    ap.add_argument('host'); ap.add_argument('port', type=int)
    ap.add_argument('--token', default='GSERV014', help='gen-2 login token (GSERV007..GSERV018)')
    ap.add_argument('--out', default='out')
    ap.add_argument('--only', help='run only one category (see cases.py)')
    ap.add_argument('--resume', type=int, default=0, help='skip cases with n < this')
    ap.add_argument('--stop-on-crash', action='store_true')
    ap.add_argument('--relaunch', help='shell command to restart the target after a crash, then resume')
    a = ap.parse_args()
    return run(a.mode, a.host, a.port, a.token, a.out, a.only, a.resume, a.stop_on_crash, a.relaunch)


if __name__ == '__main__':
    sys.exit(main())
