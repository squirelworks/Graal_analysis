"""Exercise the real runner's plan/cleanup tail with inert commands only.

No clients, Wine, servers, namespace setup or screenshot hook are launched.
The existing screenshot-hook assignment marks the start of the tested tail.
"""
import os
from pathlib import Path
import shutil
import subprocess

import pytest


RUNNER = Path(__file__).parent / 'lab' / 'runwine.sh'
SHELL = shutil.which('sh')


@pytest.mark.skipif(SHELL is None, reason='POSIX shell required for the Wine runner')
@pytest.mark.parametrize('plan_status', [0, 1, 2, 137])
@pytest.mark.parametrize('cleanup_status', [0, 9])
def test_plan_result_survives_cleanup(tmp_path, plan_status, cleanup_status):
    source = RUNNER.read_text(encoding='utf-8')
    tail = source[source.index('export PROBE_SHOT='):]
    (tmp_path / 'out').mkdir()
    cleanup = tmp_path / 'k.sh'
    cleanup.write_text('#!/bin/sh\nprintf "cleanup\\n" >> cleanup.log\n'
                       'exit "$CLEANUP_STATUS"\n', encoding='utf-8', newline='\n')
    cleanup.chmod(0o755)
    # Deliberately fail both copy operations. The cleanup status also varies,
    # so neither log collection nor cleanup may replace the plan's result.
    setup = '''set -u
D=99; T=.; R=.; O=out; C=client; LOG=unused; PLAN=unused
python3() { printf 'stub plan output\\n'; return "$PLAN_STATUS"; }
cp() { return 11; }
'''
    env = dict(os.environ, PLAN_STATUS=str(plan_status), CLEANUP_STATUS=str(cleanup_status))
    result = subprocess.run([SHELL, '-c', setup + tail], cwd=tmp_path,
                            env=env, text=True, capture_output=True, timeout=10)
    assert result.returncode == plan_status, result.stderr
    assert (tmp_path / 'cleanup.log').read_text().splitlines() == ['cleanup']
    assert (tmp_path / 'out' / 'plan.log').read_text() == 'stub plan output\n'
    if plan_status == 0:
        assert result.stdout.splitlines() == ['done out']
        assert not result.stderr
    else:
        assert 'done' not in result.stdout
        assert f'plan failed ({plan_status}): out' in result.stderr
