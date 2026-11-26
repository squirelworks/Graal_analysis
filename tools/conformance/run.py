#!/usr/bin/env python3
"""Run the 3D conformance cases on real clients in lab VMs (lab only).

Two VMs on one lab host, joined by a VM-only link (a QEMU `dgram` netdev over
two Unix sockets in the work folder: no host address, no outside network):

* the server VM (a Linux lab VM) runs seihai-gserver with the case's world,
  the conformance lobby, DHCP/DNS for the link (guest/labnet.py) and an
  artefact receiver. Its second NIC is QEMU user networking with
  `restrict=on` and one SSH forward on the host loopback: the runner's
  management channel only, with no way out.
* the client VM runs one real client build. A Windows VM is driven over QMP
  (keys, mouse, screendump) and has only the lab link; a Linux client VM may
  also have a restricted SSH NIC (`control = "ssh"`).

Both VMs run on throw-away qcow2 overlays in the work folder; the base images
are only ever read. Nothing here talks to a public server.

    run.py --lab LAB.toml [--case C001,C005] [--build 5.12,4.20r8] [--record] [--keep]
    run.py --lab LAB.toml --dry-run      the plan, with nothing started

LAB.toml is the lab's own config: VM images, client folders, addresses. It
stays on the lab host and is never committed; see lab.example.toml.

For each (build, case): build the case's world overlay, start it in the
server VM, launch the client, wait the case's seconds (taking the
case's mid action), screenshot, close the client and collect its console
log, file listing and process list, pull the server log and trace, then judge
(conformance.judge). Verdicts go to WORK/out/<build>/<case>/verdict.json, and
with --record one line per run to torque/conformance/results.tsv and the
table to torque/conformance/RESULTS.md. Captures (screenshots, logs) stay in
WORK/out, on the lab host.

Python 3.11+ standard library only; needs qemu-system-x86_64, qemu-img, ssh
and scp on the lab host.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shlex
import socket
import subprocess
import sys
import tarfile
import time
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import conformance as cf  # noqa: E402

GUEST = HERE / "guest"
PUT_PORT = 18080


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ QMP

class Qmp:
    """QMP over a Unix socket: keys, text, mouse and screendump."""

    CH = {" ": "spc", "\n": "ret", "\t": "tab", ".": "dot", ",": "comma", "/": "slash",
          "\\": "backslash", "-": "minus", "=": "equal", ";": "semicolon", "'": "apostrophe",
          "[": "bracket_left", "]": "bracket_right", "`": "grave_accent"}
    SH = {":": "semicolon", '"': "apostrophe", "_": "minus", "+": "equal", "?": "slash",
          "<": "comma", ">": "dot", "!": "1", "@": "2", "#": "3", "$": "4", "%": "5",
          "^": "6", "&": "7", "*": "8", "(": "9", ")": "0", "{": "bracket_left",
          "}": "bracket_right", "|": "backslash", "~": "grave_accent"}

    def __init__(self, path: Path, screen=(1024, 768)):
        self.path = path
        self.screen = screen

    def cmd(self, execute: str, **args):
        s = socket.socket(socket.AF_UNIX)
        s.connect(str(self.path))
        f = s.makefile("rw")
        f.readline()
        for c in ({"execute": "qmp_capabilities"}, {"execute": execute, **({"arguments": args} if args else {})}):
            f.write(json.dumps(c) + "\n")
            f.flush()
            while True:
                r = json.loads(f.readline())
                if "return" in r or "error" in r:
                    break
        s.close()
        return r

    def _keys(self, ch: str) -> list[str]:
        if ch.isalpha():
            return (["shift"] if ch.isupper() else []) + [ch.lower()]
        if ch.isdigit():
            return [ch]
        if ch in self.CH:
            return [self.CH[ch]]
        if ch in self.SH:
            return ["shift", self.SH[ch]]
        raise ValueError(f"no key for {ch!r}")

    def send(self, names: list[str], hold=60):
        self.cmd("send-key", keys=[{"type": "qcode", "data": n} for n in names], **{"hold-time": hold})

    def type(self, text: str):
        for ch in text:
            self.send(self._keys(ch), 30)
            time.sleep(0.09)

    def key(self, *combos: str):
        for c in combos:
            self.send(c.split("-") if c != "minus" else ["minus"], 100)
            time.sleep(0.2)

    def click(self, x: int, y: int, button="left"):
        w, h = self.screen
        self.cmd("input-send-event", events=[
            {"type": "abs", "data": {"axis": "x", "value": int(x * 32767 / max(w - 1, 1))}},
            {"type": "abs", "data": {"axis": "y", "value": int(y * 32767 / max(h - 1, 1))}}])
        time.sleep(0.15)
        for down in (True, False):
            self.cmd("input-send-event", events=[{"type": "btn", "data": {"down": down, "button": button}}])
            time.sleep(0.08)

    def screendump(self, out: Path):
        self.cmd("screendump", filename=str(out))

    def quit(self):
        try:
            self.cmd("quit")
        except OSError:
            pass


def steps(q: Qmp, seq: list, subst: dict):
    """Run a list of UI steps from the lab config: ["sleep", s], ["click", x, y],
    ["type", text], ["key", combo, ...], ["enter"]."""
    for st in seq:
        op, *a = st
        a = [x.format(**subst) if isinstance(x, str) else x for x in a]
        if op == "sleep":
            time.sleep(float(a[0]))
        elif op == "click":
            q.click(int(a[0]), int(a[1]))
        elif op == "type":
            q.type(a[0])
        elif op == "key":
            q.key(*a)
        elif op == "enter":
            q.key("ret")
        else:
            raise ValueError(f"unknown step {op}")


# ------------------------------------------------------------------ VMs

class Vm:
    def __init__(self, name: str, conf: dict, work: Path, lab_sock: tuple[Path, Path]):
        self.name = name
        self.conf = conf
        self.dir = work / "vm" / name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.disk = self.dir / "overlay.qcow2"
        self.qmp = Qmp(self.dir / "qmp.sock", tuple(conf.get("screen", (1024, 768))))
        self.lab_sock = lab_sock
        self.pidfile = self.dir / "vm.pid"

    def running(self) -> bool:
        try:
            pid = int(self.pidfile.read_text())
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            return False

    def fresh_overlay(self):
        if self.disk.exists():
            self.disk.unlink()
        subprocess.run(["qemu-img", "create", "-q", "-f", "qcow2", "-b", str(Path(self.conf["base"]).resolve()),
                        "-F", "qcow2", str(self.disk)], check=True)

    def argv(self) -> list[str]:
        c = self.conf
        local, remote = self.lab_sock
        a = [c.get("qemu", "qemu-system-x86_64"), "-name", f"conf-{self.name}", "-enable-kvm",
             "-machine", c.get("machine", "pc"), "-cpu", "host", "-smp", str(c.get("smp", 2)),
             "-m", c.get("mem", "2G"),
             "-drive", f"file={self.disk},if={c.get('disk_if', 'ide')},index=0,media=disk",
             "-netdev", f"dgram,id=lab,local.type=unix,local.path={local},remote.type=unix,remote.path={remote}",
             "-device", f"{c.get('nic', 'e1000')},netdev=lab,mac={c['lab_mac']}",
             "-vga", "std", "-usb", "-device", "usb-tablet", "-rtc", "base=localtime",
             "-display", "none", "-qmp", f"unix:{self.qmp.path},server,nowait",
             "-pidfile", str(self.pidfile), "-daemonize"]
        if "ssh_port" in c:
            # Management only: restrict=on gives the guest no way out; the one
            # forward is bound to the host address the lab config names
            # (its loopback address, never an outside interface).
            a += ["-netdev", f"user,id=mgmt,restrict=on,hostfwd=tcp:{c['ssh_host']}:{c['ssh_port']}-:22",
                  "-device", f"{c.get('mgmt_nic', 'e1000')},netdev=mgmt"]
        for cd in c.get("cdroms", []):
            a += ["-drive", f"file={cd},media=cdrom,readonly=on"]
        return a

    def start(self, fresh=False):
        if self.running() and not fresh:
            return
        if self.running():
            self.stop()
        if fresh or not self.disk.exists():
            self.fresh_overlay()
        log(f"boot {self.name}")
        subprocess.run(["nice", "-n", str(self.conf.get("nice", 5))] + self.argv(), check=True)
        time.sleep(float(self.conf.get("boot_seconds", 75)))

    def stop(self):
        if self.running():
            self.qmp.quit()
            for _ in range(20):
                if not self.running():
                    break
                time.sleep(0.5)

    # SSH (server VM, or a Linux client VM with a management NIC)
    def ssh_opts(self) -> list[str]:
        return ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "LogLevel=ERROR",
                "-i", self.conf["ssh_key"]]

    def ssh_base(self) -> list[str]:
        return self.ssh_opts() + ["-p", str(self.conf["ssh_port"])]

    def scp_base(self) -> list[str]:
        return self.ssh_opts() + ["-P", str(self.conf["ssh_port"])]

    def target(self) -> str:
        return f"{self.conf.get('user', 'lab')}@{self.conf['ssh_host']}"

    def ssh(self, command: str, check=True, timeout=120) -> str:
        r = subprocess.run(["ssh"] + self.ssh_base() + [self.target(), command],
                           capture_output=True, text=True, timeout=timeout)
        if check and r.returncode:
            raise RuntimeError(f"{self.name}: {command!r}: {r.stderr.strip()}")
        return r.stdout

    def scp_to(self, src: list[Path], dest: str):
        subprocess.run(["scp", "-q", "-r"] + self.scp_base() + [str(s) for s in src] + [f"{self.target()}:{dest}"],
                       check=True)

    def scp_from(self, src: str, dest: Path, check=False):
        r = subprocess.run(["scp", "-q"] + self.scp_base() + [f"{self.target()}:{src}", str(dest)],
                           capture_output=True)
        if check and r.returncode:
            raise RuntimeError(f"scp {src}: failed")
        return r.returncode == 0

    def wait_ssh(self, seconds=180):
        t = time.time()
        while time.time() - t < seconds:
            try:
                self.ssh("true", timeout=15)
                return
            except (RuntimeError, subprocess.TimeoutExpired):
                time.sleep(5)
        raise RuntimeError(f"{self.name}: no SSH after {seconds} s")


# ------------------------------------------------------------------ the lab

class Lab:
    def __init__(self, conf: dict, work: Path):
        self.conf = conf
        self.work = work
        self.net = conf["net"]
        s, c = work / "srv.sock", work / "cli.sock"
        for p in (s, c):
            if p.exists():
                p.unlink()
        self.server = Vm("server", conf["server_vm"], work, (s, c))
        self.clients = {n: Vm(f"client-{n}", v, work, (c, s)) for n, v in conf["client_vms"].items()}
        self.root = conf["server_vm"].get("root", "conformance")
        self.server_ready = False

    # server VM
    def prepare_server(self):
        self.server.start(fresh=self.conf["server_vm"].get("fresh", False))
        self.server.wait_ssh()
        R = self.root
        sv = self.conf["server_vm"]
        self.server.ssh(f"mkdir -p {R} && rm -rf {R}/guest {R}/base")
        self.server.scp_to([GUEST], f"{R}/")
        self.server.scp_to([Path(sv["base_world"])], f"{R}/base")
        if sv.get("gserver_host"):
            self.server.scp_to([Path(sv["gserver_host"])], f"{R}/gserver")
            self.gsbin = f"{R}/gserver"
        else:
            self.gsbin = sv["gserver_vm"]
        n = self.net
        mac = self.conf["server_vm"]["lab_mac"]
        addrs = " ".join(f"{a}/{n['prefix']}" for a in [n["server_ip"]] + n.get("aliases", []))
        self.server.ssh(
            "IF=$(ip -o link | grep -i " + shlex.quote(mac) + " | awk -F': ' '{print $2}'); "
            "sudo ip link set $IF up; for a in " + addrs + "; do sudo ip addr replace $a dev $IF; done; "
            "sudo pkill -f guest/labnet.py; "
            f"sudo sh -c 'nohup python3 -I -u {R}/guest/labnet.py '$IF' {n['client_ip']} {n['server_ip']} "
            f"{n.get('dns_ip', n['server_ip'])} {n['prefix']} > {R}/labnet.log 2>&1 &'; echo $IF")
        self.server_ready = True

    def case_up(self, case: cf.Case, overlay: Path):
        R = self.root
        self.server.ssh(f"rm -rf {R}/case && mkdir -p {R}/case")
        self.server.scp_to([p for p in overlay.iterdir()], f"{R}/case/")
        n = self.net
        port = self.conf.get("gserver_port", 14802)
        warp = f"{case.lobby_name},{n['server_ip']},{port}"
        out = self.server.ssh(f"sh {R}/guest/case.sh up {R} {R}/case {self.gsbin} {port} "
                              f"{self.conf.get('lobby_port', 14900)} {shlex.quote(warp)} {n['server_ip']}")
        if "up" not in out:
            raise RuntimeError("gserver did not start")

    def case_down(self):
        self.server.ssh(f"sh {self.root}/guest/case.sh down {self.root}", check=False)

    def stop_gserver(self):
        self.server.ssh(f"kill $(cat {self.root}/gserver.pid)", check=False)

    def pull(self, rundir: Path):
        R = self.root
        self.server.scp_from(f"{R}/out/gserver.log", rundir / "gserver.log")
        self.server.scp_from(f"{R}/run/g3d.tsv", rundir / "g3d.tsv")
        self.server.scp_from(f"{R}/out/lobby.log", rundir / "lobby.log")
        if self.server.scp_from(f"{R}/out/guest.tar", rundir / "guest.tar"):
            with tarfile.open(rundir / "guest.tar") as t:
                for m in t.getmembers():
                    name = Path(m.name).name
                    if m.isfile() and name in ("tasks.txt", "files.txt", "console.txt"):
                        data = t.extractfile(m).read()
                        (rundir / name).write_bytes(data)


# ------------------------------------------------------------------ clients

WIN_LAUNCH = [["click", 960, 300], ["sleep", 0.8], ["key", "meta_l-r"], ["sleep", 1.5],
              ["type", "cmd /c cd /d {dir} & del {consoles} 2>nul & start {exe} {args}"], ["enter"]]
WIN_COLLECT_OPEN = [["click", 960, 300], ["sleep", 0.8], ["key", "meta_l-r"], ["sleep", 1.5],
                    ["type", "cmd"], ["enter"], ["sleep", 2.5]]


def win_cmd(q: Qmp, line: str, wait=1.5):
    q.type(line)
    q.key("ret")
    time.sleep(wait)


def run_windows(lab: Lab, vm: Vm, build: dict, case: cf.Case, rundir: Path):
    q = vm.qmp
    n = lab.net
    consoles = " ".join(build.get("console", ["console.log"]))
    subst = {"dir": build["dir"], "exe": build["exe"], "args": build.get("args", ""), "consoles": consoles,
             "server": n["server_ip"]}
    steps(q, build.get("launch", WIN_LAUNCH), subst)
    steps(q, build.get("postlaunch", []), subst)
    t0 = time.time()
    mid = False
    every = float(lab.conf.get("shot_every", 10))
    i = 0
    while time.time() - t0 < case.seconds:
        time.sleep(every)
        i += 1
        q.screendump(rundir / f"t{int(time.time() - t0):03d}.ppm")
        if case.mid_action == "stop-server" and not mid and time.time() - t0 > case.seconds / 2:
            lab.stop_gserver()
            mid = True
    q.screendump(rundir / "shot.ppm")
    steps(q, WIN_COLLECT_OPEN, subst)
    win_cmd(q, "tasklist > %TEMP%\\tasks.txt")
    steps(q, build.get("close", [["type", "taskkill /im {exe}"], ["enter"], ["sleep", 4]]), subst)
    win_cmd(q, f"taskkill /f /im {build['exe']}", 2)
    win_cmd(q, f"cd /d {build['dir']}")
    win_cmd(q, "dir /s /b > %TEMP%\\files.txt", 3)
    win_cmd(q, f"type {consoles} > %TEMP%\\console.txt 2>nul")
    win_cmd(q, "tar -cf %TEMP%\\o.tar -C %TEMP% tasks.txt files.txt console.txt", 3)
    win_cmd(q, f"curl -s -T %TEMP%\\o.tar http://{n['server_ip']}:{PUT_PORT}/guest.tar", 3)
    win_cmd(q, "exit")


def run_ssh_client(lab: Lab, vm: Vm, build: dict, case: cf.Case, rundir: Path):
    """A Linux client VM with a management SSH NIC: the build's `launch` is a
    shell command run detached; the console log and listing are read back
    over SSH, the screenshot by the build's `screenshot` command (PPM on
    stdout) or by QMP screendump when the client draws on the VM's own display."""
    d = build["dir"]
    vm.ssh(f"cd {shlex.quote(d)} && rm -f {' '.join(build.get('console', []))}; "
           f"nohup sh -c {shlex.quote(build['launch'])} > /tmp/conf-client.log 2>&1 &", check=False)
    t0 = time.time()
    mid = False
    while time.time() - t0 < case.seconds:
        time.sleep(float(lab.conf.get("shot_every", 10)))
        if case.mid_action == "stop-server" and not mid and time.time() - t0 > case.seconds / 2:
            lab.stop_gserver()
            mid = True

    def shot(out: Path):
        if build.get("screenshot"):
            r = subprocess.run(["ssh"] + vm.ssh_base() + [vm.target(), build["screenshot"]],
                               capture_output=True, timeout=60)
            if r.returncode == 0 and r.stdout[:2] == b"P6":
                out.write_bytes(r.stdout)
        else:
            vm.qmp.screendump(out)
    shot(rundir / "shot.ppm")
    (rundir / "tasks.txt").write_text(vm.ssh("ps -eo comm,args", check=False))
    vm.ssh(build.get("close", f"pkill -f {shlex.quote(build['exe'])}"), check=False)
    time.sleep(3)
    vm.ssh(f"pkill -9 -f {shlex.quote(build['exe'])}", check=False)
    (rundir / "files.txt").write_text(vm.ssh(f"cd {shlex.quote(d)} && find . -type f", check=False))
    (rundir / "console.txt").write_text(
        vm.ssh(f"cd {shlex.quote(d)} && cat {' '.join(build.get('console', []))} 2>/dev/null", check=False))


# ------------------------------------------------------------------ main

def plan(conf: dict, cases: list[cf.Case], builds: list[str]) -> list[tuple[str, cf.Case]]:
    out = []
    for b in builds:
        if b not in conf["builds"]:
            continue
        have = set(conf["builds"][b].get("packs", [])) | set(conf.get("packs", {}))
        for c in sorted(cases, key=lambda c: (c.priority, c.id)):
            if b in c.expect and set(c.needs) <= have:
                out.append((b, c))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lab", type=Path, required=True)
    ap.add_argument("--case", default="")
    ap.add_argument("--build", default="")
    ap.add_argument("--record", action="store_true", help="append to results.tsv and rewrite RESULTS.md")
    ap.add_argument("--keep", action="store_true", help="leave the VMs running at the end")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    conf = tomllib.loads(a.lab.read_text(encoding="utf-8"))
    work = Path(conf["work"]).expanduser()
    only = set(a.case.split(",")) - {""} or None
    cases = cf.load_cases(only)
    builds = [b for b in a.build.split(",") if b] or list(conf["builds"])
    todo = plan(conf, cases, builds)
    if a.dry_run:
        for b, c in todo:
            bc = conf["builds"][b]
            print(f"{b:<8} {c.id} {c.slug:<22} vm={bc['vm']:<8} {c.seconds:>3} s  {c.title}")
        print(f"{len(todo)} runs")
        return 0

    work.mkdir(parents=True, exist_ok=True)
    worlds = work / "worlds"
    lab = Lab(conf, work)
    server_label = conf.get("server_label", "seihai-gserver")
    tsv = cf.SUITE / "results.tsv"
    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    current_vm = None
    try:
        lab.prepare_server()
        for b, case in todo:
            bc = conf["builds"][b]
            vm = lab.clients[bc["vm"]]
            if current_vm is not vm:
                if current_vm:
                    current_vm.stop()
                vm.start(fresh=True)
                current_vm = vm
            rundir = work / "out" / b / case.id
            if rundir.exists():
                for p in rundir.iterdir():
                    if p.is_file():
                        p.unlink()
            rundir.mkdir(parents=True, exist_ok=True)
            overlay = cf.build_world(case, worlds)
            log(f"{b} {case.id} {case.slug}")
            lab.case_up(case, overlay)
            try:
                if bc.get("control", "qmp") == "ssh":
                    run_ssh_client(lab, vm, bc, case, rundir)
                else:
                    run_windows(lab, vm, bc, case, rundir)
            finally:
                time.sleep(2)
                lab.case_down()
                lab.pull(rundir)
            v = cf.judge(case, b, rundir, bc.get("exe", ""))
            (rundir / "verdict.json").write_text(json.dumps(v, indent=1) + "\n")
            log(f"{b} {case.id}: {v['verdict']} {' '.join(v.get('mismatches', []))}")
            if a.record:
                cf.append_result(tsv, v, stamp, server_label, bc.get("label", b))
            # A run that never reached a console log, or failed, may have left
            # the guest in a bad state: start the next run on a fresh overlay.
            if v["verdict"] != "PASS" or not (rundir / "console.txt").exists():
                vm.stop()
                vm.start(fresh=True)
        if a.record:
            (cf.SUITE / "RESULTS.md").write_text(cf.results_table(tsv, cf.load_cases()), encoding="utf-8")
    finally:
        if not a.keep:
            if current_vm:
                current_vm.stop()
            lab.server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
