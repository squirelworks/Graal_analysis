#!/usr/bin/env python3
"""selftest: drive srvfuzz against the mock gen-2 server and mock listserver on loopback.

Checks, with no real binary and no network beyond loopback:
  * the gen-2 login + canary works (baseline up),
  * the whole real gen-2 case list runs to completion and every case leaves the mock up
    (so no case throws, and the inflate-ratio case does not take a capped server down),
  * the canary actually detects a dead server (a planted crash case flips it to down),
  * the same for the listserver mode.

Run standalone (`python3 selftest.py`) or under pytest (`python3 -m pytest tools/srvfuzz`).
Loopback only.
"""
import os, socket, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import srvfuzz as sf  # noqa: E402
import cases as caselib  # noqa: E402

LOOPBACK = sf.LOOPBACK


def start_mock(script):
    p = subprocess.Popen([sys.executable, os.path.join(HERE, script), LOOPBACK, '0'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line = p.stdout.readline().decode().strip()
    assert line.startswith('listening '), 'mock did not start: %r' % line
    return p, int(line.split()[1])


def _wait_down(canary_call, tries=20):
    for _ in range(tries):
        st = canary_call()[0]
        if st == 'down':
            return True
        time.sleep(0.2)
    return False


def test_gen2_integrity():
    """Full real gen-2 case list runs to completion; every case leaves the mock up."""
    p, port = start_mock('mockgen2.py')
    try:
        out = tempfile.mkdtemp(prefix='srvfuzz-g2-')
        rc = sf.run('gen2', LOOPBACK, port, 'GSERV014', out, None, 0, False, None)
        assert rc == 0, 'run() returned %r' % rc
        rows = open(os.path.join(out, 'results.tsv')).read().splitlines()[1:]
        assert len(rows) == len(caselib.build('gen2', 'GSERV014')), 'row count %d' % len(rows)
        downs = [r for r in rows if r.split('\t')[7] != 'up']
        assert not downs, 'cases unexpectedly took the mock down:\n' + '\n'.join(downs[:5])
    finally:
        p.terminate()


def test_gen2_crash_detected():
    """A planted crash case (WANTFILE CRASHME) must flip the canary to down."""
    p, port = start_mock('mockgen2.py')
    try:
        login = sf.frame_zlib(sf.login_gen2('GSERV014', 'guest', 'guest'))
        assert sf.canary_gen2(LOOPBACK, port, 'GSERV014')[0] == 'up', 'baseline not up'
        benign = caselib.Case('t', 'benign', sf.frame_zlib(b' '), True)  # id 0 empty, post-login
        sf.deliver(LOOPBACK, port, benign, login)
        assert sf.canary_gen2(LOOPBACK, port, 'GSERV014')[0] == 'up', 'benign case killed the mock'
        from gen5probe import encode
        crash = caselib.Case('t', 'crash', sf.frame_zlib(encode('23 t:levels/CRASHME.nw')), True)
        sf.deliver(LOOPBACK, port, crash, login)
        assert _wait_down(lambda: sf.canary_gen2(LOOPBACK, port, 'GSERV014')), 'canary did not detect the crash'
    finally:
        p.terminate()


def test_list_integrity_and_crash():
    """Listserver login + canary works, the list case set runs, and a crash is detected."""
    p, port = start_mock('mocklist.py')
    try:
        assert sf.canary_list(LOOPBACK, port)[0] == 'up', 'list baseline not up'
        out = tempfile.mkdtemp(prefix='srvfuzz-list-')
        rc = sf.run('list', LOOPBACK, port, 'GSERV014', out, None, 0, False, None)
        assert rc == 0, 'list run() returned %r' % rc
    finally:
        p.terminate()
    # separate fresh mock for the crash check (the list run above may have ended on various states)
    p, port = start_mock('mocklist.py')
    try:
        assert sf.canary_list(LOOPBACK, port)[0] == 'up'
        crash = caselib.Case('t', 'crash', sf.frame_zlib(bytes([223 + 32]) + b'CRASHME' + b'\n'), False)
        sf.deliver(LOOPBACK, port, crash, None)
        assert _wait_down(lambda: sf.canary_list(LOOPBACK, port)), 'list canary did not detect the crash'
    finally:
        p.terminate()


def main():
    fails = 0
    for t in (test_gen2_integrity, test_gen2_crash_detected, test_list_integrity_and_crash):
        try:
            t(); print('PASS', t.__name__)
        except AssertionError as e:
            fails += 1; print('FAIL', t.__name__, '--', e)
        except Exception as e:
            fails += 1; print('ERROR', t.__name__, '--', repr(e))
    print('%d passed, %d failed' % (3 - fails, fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
