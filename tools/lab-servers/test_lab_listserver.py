"""Pytest wrapper: start the lab listserver, then run test_listserver.py."""
import os
import signal
import subprocess
import sys
import time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


@pytest.fixture(scope='module')
def lab_listserver():
    import tempfile
    log_path = os.path.join(tempfile.gettempdir(), 'graal-listserver-pytest.log')
    log = open(log_path, 'w')
    proc = subprocess.Popen(
        [PY, os.path.join(HERE, 'listserver.py'), log_path],
        cwd=HERE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    # Wait until the gserver port accepts connections.
    deadline = time.time() + 5
    import socket
    sys.path.insert(0, HERE)
    from listserver import LOOPBACK  # noqa: E402
    while time.time() < deadline:
        if proc.poll() is not None:
            log.flush()
            raise RuntimeError('listserver exited early:\n' + open(log_path).read())
        try:
            s = socket.create_connection((LOOPBACK, 14900), timeout=0.2)
            s.close()
            break
        except OSError:
            time.sleep(0.05)
    else:
        proc.terminate()
        raise RuntimeError('listserver did not accept connections:\n' + open(log_path).read())
    try:
        yield proc
    finally:
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
        log.close()


def test_listserver_login_shapes(lab_listserver):
    result = subprocess.run(
        [PY, os.path.join(HERE, 'test_listserver.py')],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + '\n' + result.stderr
