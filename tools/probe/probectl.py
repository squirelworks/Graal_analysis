#!/usr/bin/env python3
"""probectl: talk to a running gen5probe, one command or a whole plan.

  probectl.py CTLSOCK cmd 's2c 9 c:83 i5:1234'
  probectl.py CTLSOCK plan PLAN [VAR=VALUE ...]

Plan lines (a line starting with # is a comment; {VAR} is replaced from the arguments):
  waitsession [SECS]      wait until a logged-in session exists
  wait s2c|c2s ID [SECS]  wait until at least one more packet with that id passes
  sleep SECS
  shot NAME               run $PROBE_SHOT with {name} replaced (screenshot hook)
  sh COMMAND              run a shell command (observer hook, e.g. copy a log)
  anything else           sent to the proxy as a command (s2c, c2s, after, drop, mark, ...)
Every step is echoed with a monotonic timestamp, and also sent as `mark` so the proxy log
holds the same timeline. A plan stops on the first `err` reply.
"""
import os, socket, subprocess, sys, time


class Ctl:
    def __init__(self, path):
        for _ in range(120):  # the proxy may still be starting
            try:
                if path.startswith('tcp:'):
                    self.s = socket.create_connection(('%d.%d.%d.%d' % (127, 0, 0, 1), int(path[4:]))); break
                self.s = socket.socket(socket.AF_UNIX); self.s.connect(path); break
            except OSError:
                time.sleep(0.5)
        else:
            raise SystemExit('no control socket at %s' % path)
        self.f = self.s.makefile('rwb')

    def __call__(self, line):
        self.f.write((line + '\n').encode('latin1')); self.f.flush()
        return self.f.readline().decode('latin1').strip()


def seen(ctl, d, pid):
    r = ctl('seen %s %s' % (d, pid))
    return int(r.split()[1]) if r.startswith('ok') else -1


def run_plan(ctl, lines, var):
    t0 = time.monotonic()
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        for k, v in var.items():
            line = line.replace('{%s}' % k, v)
        print('%8.3f %s' % (time.monotonic() - t0, line), flush=True)
        op = line.split()[0]
        if op == 'waitsession':
            lim = float(line.split()[1]) if len(line.split()) > 1 else 60
            end = time.monotonic() + lim
            while not ctl('status').startswith('ok session'):
                if time.monotonic() > end:
                    print('TIMEOUT waitsession'); return 2
                time.sleep(0.5)
            continue
        ctl('mark plan: ' + line)
        if op == 'wait':
            _, d, pid, *rest = line.split(); lim = float(rest[0]) if rest else 30
            base = seen(ctl, d, pid); end = time.monotonic() + lim
            while seen(ctl, d, pid) <= base:
                if time.monotonic() > end:
                    print('TIMEOUT wait %s %s' % (d, pid)); break
                time.sleep(0.2)
        elif op == 'sleep':
            time.sleep(float(line.split()[1]))
        elif op == 'shot':
            cmd = os.environ.get('PROBE_SHOT')
            if cmd:
                subprocess.call(cmd.replace('{name}', line.split()[1]), shell=True)
        elif op == 'sh':
            subprocess.call(line[3:], shell=True)
        else:
            r = ctl(line); print('         -> ' + r, flush=True)
            if r.startswith('err'):
                return 1
    return 0


def main():
    path, mode = sys.argv[1], sys.argv[2]
    ctl = Ctl(path)
    if mode == 'cmd':
        print(ctl(sys.argv[3])); return 0
    var = dict(a.split('=', 1) for a in sys.argv[4:])
    return run_plan(ctl, open(sys.argv[3]).read().splitlines(), var)


if __name__ == '__main__':
    sys.exit(main())
