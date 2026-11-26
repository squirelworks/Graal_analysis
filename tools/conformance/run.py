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
import base64
import datetime as dt
import json
import re
import os
import shlex
import socket
import struct
import subprocess
import sys
import tarfile
import time
import tomllib
import zlib
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
    def __init__(self, name: str, conf: dict, work: Path, lab_sock: tuple[Path, Path],
                 lab_sock2: tuple[Path, Path] | None = None):
        self.name = name
        self.lab_sock2 = lab_sock2
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
        if self.lab_sock2 and c.get("lab_mac2"):
            # The server VM's second lab NIC: the second client of a
            # two-client case, on its own dgram pair, bridged in the VM.
            l2, r2 = self.lab_sock2
            a += ["-netdev", f"dgram,id=lab2,local.type=unix,local.path={l2},remote.type=unix,remote.path={r2}",
                  "-device", f"{c.get('nic', 'e1000')},netdev=lab2,mac={c['lab_mac2']}"]
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
        return ["-o", "StrictHostKeyChecking=no", "-o", f"UserKnownHostsFile={os.devnull}", "-o", "LogLevel=ERROR",
                "-o", "IdentitiesOnly=yes", "-i", self.conf["ssh_key"]]

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


# ------------------------------------------------------------------ VirtualBox

def png_to_ppm(data: bytes) -> bytes:
    """An 8-bit RGB/RGBA PNG (VirtualBox's screenshotpng) as a binary PPM."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    i, idat, hdr = 8, [], None
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        kind, body = data[i + 4:i + 8], data[i + 8:i + 8 + n]
        i += 12 + n
        if kind == b"IHDR":
            hdr = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
    w, h, depth, ctype, _, _, interlace = hdr
    if depth != 8 or ctype not in (2, 6) or interlace:
        raise ValueError(f"PNG depth {depth} type {ctype} interlace {interlace}: not supported")
    bpp = 3 if ctype == 2 else 4
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    prev = bytearray(stride)
    out = bytearray(b"P6\n%d %d\n255\n" % (w, h))
    pos = 0
    for _ in range(h):
        f = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + stride])
        pos += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            line = bytearray((a + b) & 255 for a, b in zip(line, prev))
        elif f == 3:
            for x in range(stride):
                left = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        if bpp == 3:
            out += line
        else:
            rgb = bytearray(line)
            del rgb[3::4]
            out += rgb
    return bytes(out)


def _mb(size: str) -> int:
    s = str(size).upper()
    return int(float(s[:-1]) * 1024) if s.endswith("G") else int(s.rstrip("M"))


class VBox:
    """VBoxManage, as the lab config's [virtualbox] table names it."""

    def __init__(self, conf: dict):
        self.conf = conf
        self.exe = conf.get("manage", "VBoxManage")

    def __call__(self, *args, check=True, timeout=600) -> subprocess.CompletedProcess:
        r = subprocess.run([self.exe] + [str(a) for a in args], capture_output=True, timeout=timeout)
        if check and r.returncode:
            raise RuntimeError(f"VBoxManage {' '.join(map(str, args[:3]))}: "
                               f"{r.stderr.decode(errors='replace').strip()[-400:]}")
        return r

    def out(self, *args, **kw) -> str:
        return self(*args, **kw).stdout.decode(errors="replace")

    def exists(self, name: str) -> bool:
        return f'"{name}"' in self.out("list", "vms")

    def running(self, name: str) -> bool:
        return f'"{name}"' in self.out("list", "runningvms")

    def ensure_dhcp(self, net: dict):
        """VirtualBox's own DHCP server on the internal network (it has no host
        address and routes nowhere): a fixed lease for each lab MAC."""
        v = self.conf
        args = [f"--network={v['intnet']}", f"--server-ip={v['dhcp_ip']}", f"--netmask={v['netmask']}",
                f"--lower-ip={v['dhcp_lower']}", f"--upper-ip={v['dhcp_upper']}", "--enable"]
        if v["intnet"] in self.out("list", "dhcpservers"):
            self("dhcpserver", "modify", *args)
        else:
            self("dhcpserver", "add", *args)
        for mac, ip in net.items():
            self("dhcpserver", "modify", f"--network={v['intnet']}", f"--mac-address={mac}",
                 f"--fixed-address={ip}")


class VboxVm(Vm):
    """A lab VM as a throw-away VirtualBox linked clone of a base VM's
    snapshot (`vbox_base`, `vbox_snapshot`); the base is only ever read. The
    lab link is a VirtualBox internal network: VM-only, no host address. A
    server VM adds a NAT NIC with one SSH forward on the host loopback (its
    management channel). A Windows client is driven by guest control and the
    guest's desktop agent; screenshots are VirtualBox's own."""

    def __init__(self, name: str, conf: dict, work: Path, vb: VBox):
        super().__init__(name, conf, work, (work / "unused", work / "unused"))
        self.vb = vb
        self.clone = f"{vb.conf.get('prefix', 'conf')}-{name}"

    def running(self) -> bool:
        return self.vb.running(self.clone)

    def destroy(self):
        if self.vb.exists(self.clone):
            if self.running():
                self.vb("controlvm", self.clone, "poweroff", check=False)
                for _ in range(40):
                    if not self.running():
                        break
                    time.sleep(0.5)
                time.sleep(2)
            self.vb("unregistervm", self.clone, "--delete")

    def fresh_overlay(self):
        c, vb = self.conf, self.vb
        self.destroy()
        vb("clonevm", c["vbox_base"], "--snapshot", c["vbox_snapshot"], "--options", "link",
           "--name", self.clone, "--basefolder", vb.conf["basefolder"], "--register")
        info = vb.out("showvminfo", self.clone, "--machinereadable")
        for line in info.splitlines():       # the base's own port forwards are not ours
            if line.startswith("Forwarding("):
                for nic in ("natpf1", "natpf2"):
                    vb("modifyvm", self.clone, f"--{nic}", "delete", line.split('"')[1].split(",")[0], check=False)
        mac = c["lab_mac"].replace(":", "").upper()
        intnet = vb.conf["intnet"]
        a = ["modifyvm", self.clone, "--memory", _mb(c.get("mem", "2G")), "--cpus", c.get("smp", 2),
             "--description", "conformance runner throw-away clone; deleted at the end of the run"]
        if "ssh_port" in c:
            a += ["--nic1", "nat", "--natpf1", f"conf-ssh,tcp,{c['ssh_host']},{c['ssh_port']},,22",
                  "--nic2", "intnet", "--intnet2", intnet, "--macaddress2", mac, "--cableconnected2", "on"]
        else:
            a += ["--nic1", "intnet", "--intnet1", intnet, "--macaddress1", mac, "--cableconnected1", "on",
                  "--nic2", "none"]
        vb(*a)

    def argv(self) -> list[str]:
        return []

    def start(self, fresh=False):
        if self.running() and not fresh:
            return
        if fresh or not self.vb.exists(self.clone):
            self.fresh_overlay()
        log(f"boot {self.name}")
        self.vb("startvm", self.clone, "--type", "headless")
        if self.conf.get("os", "linux" if "ssh_port" in self.conf else "windows") == "windows":
            self.boot_windows()

    def stop(self):
        self.destroy()

    def screendump(self, out: Path):
        png = out.with_suffix(".png")
        self.vb("controlvm", self.clone, "screenshotpng", str(png.resolve()), check=False)
        if out.suffix == ".ppm" and png.exists():
            out.write_bytes(png_to_ppm(png.read_bytes()))

    # Windows guest control
    def auth(self) -> list[str]:
        v = self.vb.conf
        return [f"--username={v['guest_user']}", f"--passwordfile={v['guest_password_file']}"]

    def run_exe(self, exe: str, args: list[str], timeout=120) -> bytes:
        r = self.vb("guestcontrol", self.clone, "run", f"--exe={exe}", *self.auth(), f"--timeout={timeout * 1000}",
                    "--wait-stdout", "--wait-stderr", "--", *args, check=False, timeout=timeout + 60)
        return r.stdout

    def gx(self, ps: str, timeout=120) -> str:
        enc = base64.b64encode(("$ProgressPreference = 'SilentlyContinue'; " + ps).encode("utf-16-le")).decode()
        return self.run_exe(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                            ["-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                             "-EncodedCommand", enc], timeout).decode(errors="replace")


    def agent(self, *lines: str) -> str:
        """The guest's desktop agent (it runs in the console session, so what it
        launches is on the desktop): one command a line in cmd.txt."""
        d = self.conf.get("agent", r"C:\Users\Public\tg")
        body = "\n".join(lines).replace("'", "''")
        return self.gx(f"$n=@(Get-Content {d}\\agent.txt -EA 0).Count; Set-Content -Encoding utf8 {d}\\cmd.txt '{body}'; "
                       f"$t=0; while((Test-Path {d}\\cmd.txt) -and $t -lt 60){{ Start-Sleep -Milliseconds 250; $t++ }}; "
                       f"Start-Sleep -Milliseconds 1500; Get-Content {d}\\agent.txt -EA 0 | Select-Object -Skip $n", 90)

    SC = {"win_r": ["e0", "5b", "13", "93", "e0", "db"], "enter": ["1c", "9c"], "alt_y": ["38", "15", "95", "b8"],
          "ctrl_shift_enter": ["1d", "2a", "1c", "9c", "aa", "9d"], "ctrl": ["1d", "9d"], "esc": ["01", "81"]}

    def keys(self, name: str):
        self.vb("controlvm", self.clone, "keyboardputscancode", *self.SC[name], check=False)

    def type(self, text: str):
        self.vb("controlvm", self.clone, "keyboardputstring", text, check=False)

    def win_run(self, line: str, elevated=False):
        self.keys("esc")          # close a leftover dialog first
        time.sleep(0.5)
        self.keys("win_r")
        time.sleep(3)
        self.type(line)
        time.sleep(0.7)
        if elevated:
            self.keys("ctrl_shift_enter")
            time.sleep(6)
            self.keys("alt_y")    # accept the UAC prompt
        else:
            self.keys("enter")

    def boot_windows(self):
        """Wait for the desktop, start the desktop agent, then run the prep
        script elevated: the hosts file's loopback lines point at the server
        VM, and the lab's own guest set-up (e.g. the clock hold) runs."""
        c = self.conf
        t0 = time.time()
        while "explorer" not in self.gx("Get-Process explorer -EA 0 | % Name", 30):
            if time.time() - t0 > float(c.get("boot_seconds", 300)):
                raise RuntimeError(f"{self.name}: no desktop")
            time.sleep(10)
        if c.get("screen"):
            w, h = c["screen"]
            self.vb("controlvm", self.clone, "setvideomodehint", w, h, 32, check=False)
        time.sleep(15)
        d = c.get("agent", r"C:\Users\Public\tg")
        def agent_alive() -> bool:
            # a "wins" command is taken (cmd.txt removed) only by a running agent
            return "gone" in self.gx(f"Set-Content -Encoding utf8 {d}\\cmd.txt 'wins'; Start-Sleep 5; "
                                     f"if (Test-Path {d}\\cmd.txt) {{ Remove-Item {d}\\cmd.txt; 'left' }} else {{ 'gone' }}")
        for _ in range(6):
            if agent_alive():
                break
            self.win_run(c.get("agent_start", d + "\\a.cmd"))
            time.sleep(10)
        else:
            raise RuntimeError(f"{self.name}: the desktop agent did not start")
        server = self.server_ip
        # The lab's own elevated set-up first; it may write the hosts file
        # itself a little later (the T3D guests' clock hold does), so the
        # hosts edit is repeated for `prep_settle` seconds.
        settle = int(c.get("prep_settle", 60 if c.get("elevated") else 0))
        prep = ["Start-Transcript C:\\Users\\Public\\conf-prep.log"]
        prep += [f"Start-Process -WindowStyle Minimized cmd.exe -ArgumentList '/c {x}'" for x in c.get("elevated", [])]
        prep += [
            "$h = 'C:\\Windows\\System32\\drivers\\etc\\hosts'",
            f"for ($i = 0; $i -le {settle // 2}; $i++) {{",
            "  $l = Get-Content $h | % { if ($_ -match '^\\s*127\\.0\\.0\\.1\\s+(.*)$' -and $Matches[1] -notmatch '^localhost') "
            f"{{ '{server} ' + $Matches[1] }} else {{ $_ }} }}",
            "  try { [IO.File]::WriteAllLines($h, [string[]]$l) } catch { \"hosts: $_\" }",
            "  Start-Sleep 2",
            "}",
            "ipconfig /flushdns | Out-Null",
            # A guest that blocks outbound traffic by default may reach
            # the server VM, and only it.
            f"New-NetFirewallRule -DisplayName conf-lab-server -Direction Outbound -RemoteAddress {server} "
            "-Action Allow | Out-Null",
            "Get-Content $h | Select-String -NotMatch '^#'",
            "Stop-Transcript",
        ]
        prep.append("Set-Content C:\\Users\\Public\\conf-prep.ok ok")
        self.gx("Remove-Item C:\\Users\\Public\\conf-prep.ok -EA 0; Set-Content -Encoding utf8 C:\\Users\\Public\\conf-prep.ps1 @'\n"
                + "\n".join(prep) + "\n'@")
        for _ in range(4):
            self.win_run("powershell -ExecutionPolicy Bypass -WindowStyle Minimized -File C:\\Users\\Public\\conf-prep.ps1",
                         elevated=True)
            for _ in range(8 + settle // 5):
                time.sleep(5)
                if "ok" in self.gx("Get-Content C:\\Users\\Public\\conf-prep.ok -EA 0"):
                    break
                self.keys("alt_y")
            else:
                continue
            break
        else:
            raise RuntimeError(f"{self.name}: the elevated prep did not run")
        hosts = self.gx(r"Get-Content C:\Windows\System32\drivers\etc\hosts")
        if server not in hosts:
            raise RuntimeError(f"{self.name}: the hosts file does not name the server VM; prep log:\n"
                               + self.gx(r"Get-Content C:\Users\Public\conf-prep.log -EA 0"))
        want = c.get("wait_year")
        if want:
            for _ in range(12):
                if str(want) in self.gx("(Get-Date).Year"):
                    break
                time.sleep(5)
            else:
                raise RuntimeError(f"{self.name}: the guest clock is not at {want}")
        for line in c.get("guest_setup", []):   # PowerShell lines, run by guest control
            self.gx(line, 600)
        log(f"{self.name}: desktop, agent and prep ready")


# ------------------------------------------------------------------ the lab

class Lab:
    def __init__(self, conf: dict, work: Path):
        self.conf = conf
        self.work = work
        self.net = conf["net"]
        self.root = conf["server_vm"].get("root", "conformance")
        self.server_ready = False
        self.vbox = None
        if conf.get("hypervisor", "qemu") == "virtualbox":
            self.vbox = VBox(conf["virtualbox"])
            self.server = VboxVm("server", conf["server_vm"], work, self.vbox)
            self.clients = {n: VboxVm(f"client-{n}", v, work, self.vbox) for n, v in conf["client_vms"].items()}
            for v in self.clients.values():
                v.server_ip = self.net["server_ip"]
            return
        s, c = work / "srv.sock", work / "cli.sock"
        s2, c2 = work / "srv2.sock", work / "cli2.sock"
        for p in (s, c, s2, c2):
            if p.exists():
                p.unlink()
        self.server = Vm("server", conf["server_vm"], work, (s, c), (s2, c2))
        # A client VM with slot = 2 sits on the second link (two-client cases).
        self.clients = {n: Vm(f"client-{n}", v, work, (c2, s2) if v.get("slot", 1) == 2 else (c, s))
                        for n, v in conf["client_vms"].items()}
        self.root = conf["server_vm"].get("root", "conformance")
        self.server_ready = False

    # server VM
    def prepare_server(self, reuse=False):
        if self.vbox:
            # Fixed leases for the server and every client MAC (VirtualBox's
            # DHCP server on the internal network; labnet.py needs root).
            leases = {self.conf["server_vm"]["lab_mac"]: self.net["server_ip"]}
            for v in self.conf["client_vms"].values():
                leases[v["lab_mac"]] = self.net.get("static", {}).get(v["lab_mac"], self.net["client_ip"])
            self.vbox.ensure_dhcp(leases)
        self.server.start(fresh=self.conf["server_vm"].get("fresh", bool(self.vbox)) and not reuse)
        self.server.wait_ssh(int(self.conf["server_vm"].get("ssh_wait", 180)))
        R = self.root
        sv = self.conf["server_vm"]
        self.server.ssh(f"mkdir -p {R} && rm -rf {R}/guest {R}/base")
        self.server.scp_to([GUEST], f"{R}/")
        self.server.scp_to([Path(sv["base_world"])], f"{R}/base")
        # A Windows checkout may have given the scripts CRLF line ends.
        self.server.ssh(f"sed -i 's/\\r$//' {R}/guest/*")
        if sv.get("gserver_host"):
            self.server.scp_to([Path(sv["gserver_host"])], f"{R}/gserver")
            self.gsbin = f"{R}/gserver"
        else:
            self.gsbin = sv["gserver_vm"]
        n = self.net
        if self.vbox:
            # No root in the server VM: the guest's own network manager takes
            # the fixed lease on the lab NIC; wait for it.
            ip = n["server_ip"]
            for _ in range(36):
                if ip in self.server.ssh("ip -o -4 addr", check=False):
                    break
                time.sleep(5)
            else:
                raise RuntimeError(f"server VM: no {ip} on the lab link")
            self.server_ready = True
            return
        mac = self.conf["server_vm"]["lab_mac"]
        mac2 = self.conf["server_vm"].get("lab_mac2", "")
        addrs = " ".join(f"{a}/{n['prefix']}" for a in [n["server_ip"]] + n.get("aliases", []))
        find = "$(ip -o link | grep -i {} | awk -F': ' '{{print $2}}' | cut -d@ -f1)"
        if mac2:
            # Both lab NICs in one bridge, the addresses on the bridge.
            link = (f"IF1={find.format(shlex.quote(mac))}; IF2={find.format(shlex.quote(mac2))}; "
                    "sudo ip link add conf-br type bridge 2>/dev/null; "
                    "sudo ip link set $IF1 master conf-br; sudo ip link set $IF2 master conf-br; "
                    "sudo ip link set $IF1 up; sudo ip link set $IF2 up; IF=conf-br; ")
        else:
            link = f"IF={find.format(shlex.quote(mac))}; "
        static = ",".join(f"{m}={ip}" for m, ip in n.get("static", {}).items())
        self.server.ssh(
            link + "sudo ip link set $IF up; for a in " + addrs + "; do sudo ip addr replace $a dev $IF; done; "
            "sudo pkill -f guest/labnet.py; "
            f"sudo sh -c 'nohup python3 -I -u {R}/guest/labnet.py '$IF' {n['client_ip']} {n['server_ip']} "
            f"{n.get('dns_ip', n['server_ip'])} {n['prefix']} {static or '-'} > {R}/labnet.log 2>&1 &'; echo $IF")
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

    def mid_action(self, case: cf.Case, rundir: Path):
        """The case's action half way through a run."""
        if case.mid_action == "stop-server":
            self.stop_gserver()
        elif case.mid_action in ("inject-junk", "inject-flood"):
            port = self.conf.get("gserver_port", 14802)
            mode = " flood" if case.mid_action == "inject-flood" else ""
            out = self.server.ssh(f"python3 -I -u {self.root}/guest/junk.py {self.net['server_ip']} {port} "
                                  f"{self.root}/gserver.pid{mode}", check=False)
            (rundir / "inject.log").write_text(out)

    def between_sessions(self, case: cf.Case):
        """Swap served files between two sessions of a multi-session case."""
        for b in case.between:
            f = f"{self.root}/run/files"
            self.server.ssh(f"cp {f}/{shlex.quote(b['with'])} {f}/{shlex.quote(b['swap'])} && "
                            f"touch {f}/{shlex.quote(b['swap'])}")

    def stop_gserver(self):
        self.server.ssh(f"kill $(cat {self.root}/gserver.pid)", check=False)

    def pull(self, rundir: Path):
        R = self.root
        self.server.scp_from(f"{R}/out/gserver.log", rundir / "gserver.log")
        self.server.scp_from(f"{R}/run/g3d.tsv", rundir / "g3d.tsv")
        self.server.scp_from(f"{R}/out/lobby.log", rundir / "lobby.log")
        for tar, into in (("guest.tar", rundir), ("guest2.tar", rundir / "c2")):
            into.mkdir(exist_ok=True)
            if self.server.scp_from(f"{R}/out/{tar}", into / tar):
                with tarfile.open(into / tar) as t:
                    for m in t.getmembers():
                        name = Path(m.name).name
                        if m.isfile() and name in ("tasks.txt", "files.txt", "console.txt"):
                            (into / name).write_bytes(t.extractfile(m).read())


# ------------------------------------------------------------------ clients

WIN_LAUNCH = [["click", 960, 300], ["sleep", 0.8], ["key", "meta_l-r"], ["sleep", 1.5],
              ["type", "cmd /c cd /d {dir} & del {consoles} 2>nul{clean} & start {exe} {args}"], ["enter"]]
WIN_COLLECT_OPEN = [["click", 960, 300], ["sleep", 0.8], ["key", "meta_l-r"], ["sleep", 1.5],
                    ["type", "cmd"], ["enter"], ["sleep", 2.5]]


def win_cmd(q: Qmp, line: str, wait=1.5):
    q.type(line)
    q.key("ret")
    time.sleep(wait)


def run_windows(lab: Lab, vm: Vm, build: dict, case: cf.Case, rundir: Path,
                upload: str = "guest.tar", primary: bool = True, clean_cache: bool = True):
    q = vm.qmp
    rundir.mkdir(parents=True, exist_ok=True)
    n = lab.net
    consoles = " ".join(build.get("console", ["console.log"]))
    # The client's own download cache (5.12: levels3d and FILENAMECACHE.txt)
    # is removed before each launch, or a file fetched in one case is not
    # asked for again in the next and the `server` file checks miss it.
    clean = "".join(f" & rmdir /s /q {x} 2>nul & del /f /q {x} 2>nul"
                    for x in (build.get("clean", []) if clean_cache else []))
    subst = {"dir": build["dir"], "exe": build["exe"], "args": build.get("args", ""), "consoles": consoles,
             "server": n["server_ip"], "clean": clean}
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
        if primary and case.mid_action and not mid and time.time() - t0 > case.seconds / 2:
            lab.mid_action(case, rundir)
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
    win_cmd(q, f"curl -s -T %TEMP%\\o.tar http://{n['server_ip']}:{PUT_PORT}/{upload}", 3)
    win_cmd(q, "exit")


def vbox_steps(vm: VboxVm, seq: list, subst: dict):
    """UI steps on a VirtualBox Windows guest: ["sleep", s], ["click", x, y]
    (the guest agent's mclick, guest screen pixels), ["type", text],
    ["enter"], ["agent", line]."""
    for st in seq:
        op, *a = st
        a = [x.format(**subst) if isinstance(x, str) else x for x in a]
        if op == "sleep":
            time.sleep(float(a[0]))
        elif op == "click":
            vm.agent(f"mclick {int(a[0])} {int(a[1])}")
        elif op == "type":
            vm.type(a[0])
        elif op == "enter":
            vm.keys("enter")
        elif op == "agent":
            vm.agent(a[0])
        else:
            raise ValueError(f"unknown step {op}")


def run_windows_vbox(lab: Lab, vm: VboxVm, build: dict, case: cf.Case, rundir: Path, primary: bool = True,
                     clean_cache: bool = True):
    """A Windows client in a VirtualBox guest: guest control clears the
    client's cache and reads its logs back, the desktop agent launches and
    kills it, and VirtualBox takes the screenshots. Artefacts are written
    straight to RUNDIR (no upload over the lab link)."""
    rundir.mkdir(parents=True, exist_ok=True)
    d, exe = build["dir"], build["exe"]
    consoles = build.get("console", ["console.log"])
    gone = ",".join(f"'{d}\\{x}'" for x in consoles + (build.get("clean", []) if clean_cache else []))
    vm.gx(f"Remove-Item {gone} -Recurse -Force -EA 0")
    subst = {"dir": d, "exe": exe, "args": build.get("args", ""), "server": lab.net["server_ip"]}
    pid = vbox_launch(vm, d, exe)
    vbox_steps(vm, build.get("vbox_postlaunch", []), subst)
    t0 = time.time()
    mid = False
    every = float(lab.conf.get("shot_every", 10))
    while time.time() - t0 < case.seconds:
        time.sleep(every)
        vm.screendump(rundir / f"t{int(time.time() - t0):03d}.png")
        if primary and case.mid_action and not mid and time.time() - t0 > case.seconds / 2:
            lab.mid_action(case, rundir)
            mid = True
    vm.screendump(rundir / "shot.ppm")
    vbox_tasks(vm, pid, exe, rundir)
    vm.agent(f"killname {exe.rsplit('.', 1)[0]}")
    time.sleep(2)
    vbox_logs(vm, build, d, rundir)


def vbox_launch(vm: VboxVm, d: str, exe: str) -> int:
    """Launch through the desktop agent; its reply names the new process id.
    When the reply comes too late to be read, the one new process of that
    name is taken."""
    ids = f"Get-Process {exe.rsplit('.', 1)[0]} -EA 0 | % Id"
    before = set(vm.gx(ids).split())
    m = re.search(r"pid (\d+)", vm.agent(f"launch {d} {exe}"))
    if m:
        return int(m.group(1))
    for _ in range(10):
        new = set(vm.gx(ids).split()) - before
        if len(new) == 1:
            return int(new.pop())
        time.sleep(1)
    return 0


def vbox_tasks(vm: VboxVm, pid: int, exe: str, rundir: Path):
    """Whether the process the agent launched is still running (the guest
    control user cannot read the paths of the desktop user's processes, so
    the launch's own pid tells two clients in one guest apart)."""
    alive = pid and str(pid) in vm.gx(f"Get-Process -Id {pid} -EA 0 | % Id")
    (rundir / "tasks.txt").write_text(f"{exe} pid {pid} running\n" if alive else f"pid {pid} gone\n",
                                      encoding="utf-8")


def vbox_logs(vm: VboxVm, build: dict, d: str, rundir: Path):
    (rundir / "files.txt").write_text(
        vm.gx(f"Get-ChildItem -LiteralPath '{d}' -Recurse -File -EA 0 | % FullName"), encoding="utf-8")
    text = ""
    for c in build.get("console", ["console.log"]):
        text += vm.gx(f"$p = '{d}\\{c}'; if (Test-Path -LiteralPath $p) "
                      "{ [IO.File]::ReadAllText($p, [Text.Encoding]::GetEncoding(28591)) }")
    if text:
        (rundir / "console.txt").write_text(text, encoding="utf-8")


def vbox_pair_one_guest(lab: Lab, vm: VboxVm, build: dict, case: cf.Case, rundir: Path):
    """A two-client case with both clients in one guest (`pair_dir`: a second
    copy of the build there), for a host without the memory for a second
    client VM. One screenshot shows both windows, so both clients' screenshot
    checks read the same desktop."""
    d1, d2, exe = build["dir"], build["pair_dir"], build["exe"]
    c2 = rundir / "c2"
    c2.mkdir(parents=True, exist_ok=True)
    gone = ",".join(f"'{d}\\{x}'" for d in (d1, d2)
                    for x in build.get("console", ["console.log"]) + build.get("clean", []))
    vm.gx(f"Remove-Item {gone} -Recurse -Force -EA 0")
    pid1 = vbox_launch(vm, d1, exe)
    time.sleep(float(build.get("pair_delay", 25)))
    pid2 = vbox_launch(vm, d2, exe)
    t0 = time.time()
    every = float(lab.conf.get("shot_every", 10))
    while time.time() - t0 < case.seconds:
        time.sleep(every)
        vm.screendump(rundir / f"t{int(time.time() - t0):03d}.png")
    vm.screendump(rundir / "shot.ppm")
    (c2 / "shot.ppm").write_bytes((rundir / "shot.ppm").read_bytes())
    vbox_tasks(vm, pid1, exe, rundir)
    vbox_tasks(vm, pid2, exe, c2)
    vm.agent(f"killname {exe.rsplit('.', 1)[0]}")
    time.sleep(2)
    vbox_logs(vm, build, d1, rundir)
    vbox_logs(vm, build, d2, c2)


def run_client(lab: Lab, vm, build: dict, case: cf.Case, rundir: Path, upload="guest.tar", primary=True,
               clean_cache=True):
    if isinstance(vm, VboxVm):
        run_windows_vbox(lab, vm, build, case, rundir, primary, clean_cache=clean_cache)
    else:
        run_windows(lab, vm, build, case, rundir, upload=upload, primary=primary, clean_cache=clean_cache)


def run_ssh_client(lab: Lab, vm: Vm, build: dict, case: cf.Case, rundir: Path, primary: bool = True):
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
        if primary and case.mid_action and not mid and time.time() - t0 > case.seconds / 2:
            lab.mid_action(case, rundir)
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


def run_pair(lab: Lab, vm: Vm, vm2: Vm | None, build: dict, case: cf.Case, rundir: Path):
    """A two-client case: the same build in two client VMs (the second on
    the server VM's second lab NIC), the second launched `pair_delay`
    seconds after the first so it joins a world that already has a player.
    Windows clients only. Client 2's artefacts go to RUNDIR/c2."""
    import threading
    if vm2 is None:
        vbox_pair_one_guest(lab, vm, build, case, rundir)
        return
    vm2.start(fresh=not vm2.running())
    delay = float(build.get("pair_delay", 25))
    second = threading.Thread(target=lambda: (time.sleep(delay), run_client(
        lab, vm2, build, case, rundir / "c2", upload="guest2.tar", primary=False)))
    second.start()
    run_client(lab, vm, build, case, rundir)
    second.join()


# ------------------------------------------------------------------ main

def plan(conf: dict, cases: list[cf.Case], builds: list[str]) -> list[tuple[str, cf.Case]]:
    out = []
    for b in builds:
        if b not in conf["builds"]:
            continue
        have = set(conf["builds"][b].get("packs", [])) | set(conf.get("packs", {}))
        for c in sorted(cases, key=lambda c: (c.priority, c.id)):
            if c.clients == 2 and not (conf["builds"][b].get("pair_vm") or conf["builds"][b].get("pair_dir")):
                continue   # a two-client case needs a second client VM for this build
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
    ap.add_argument("--reuse", action="store_true", help="use VMs left running by --keep instead of fresh overlays")
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
        lab.prepare_server(a.reuse)
        for b, case in todo:
            bc = conf["builds"][b]
            vm = lab.clients[bc["vm"]]
            if current_vm is not vm:
                if current_vm:
                    current_vm.stop()
                vm.start(fresh=not (a.reuse and vm.running()))
                current_vm = vm
            rundir = work / "out" / b / case.id
            for d in (rundir, rundir / "c2"):
                if d.exists():
                    for p in d.iterdir():
                        if p.is_file():
                            p.unlink()
            rundir.mkdir(parents=True, exist_ok=True)
            packs = {k: Path(v) for k, v in conf.get("packs", {}).items()}
            overlay = cf.build_world(case, worlds, packs)
            log(f"{b} {case.id} {case.slug}")
            lab.case_up(case, overlay)
            try:
                if case.clients == 2:
                    run_pair(lab, vm, lab.clients[bc["pair_vm"]] if bc.get("pair_vm") else None, bc, case, rundir)
                else:
                    # A multi-session case relaunches the client on the same
                    # server run; the last session's artefacts are the ones
                    # judged, earlier ones stay in s1, s2, ...
                    for s in range(case.sessions):
                        last = s == case.sessions - 1
                        sdir = rundir if last else rundir / f"s{s + 1}"
                        sdir.mkdir(parents=True, exist_ok=True)
                        if s:
                            lab.between_sessions(case)
                        if bc.get("control", "qmp") == "ssh":
                            run_ssh_client(lab, vm, bc, case, sdir, primary=last)
                        else:
                            run_client(lab, vm, bc, case, sdir, primary=last,
                                       clean_cache=not (case.keep_cache and s))
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
            # A VirtualBox guest is re-cloned and re-prepared (minutes), so
            # only when the client left no console log: its own clean-up
            # step already resets the client folder between runs.
            bad = not (rundir / "console.txt").exists()
            if not lab.vbox:
                bad = bad or v["verdict"] != "PASS"
            if bad:
                vm.stop()
                vm.start(fresh=True)
        if a.record:
            (cf.SUITE / "RESULTS.md").write_text(cf.results_table(tsv, cf.load_cases()), encoding="utf-8")
    finally:
        if not a.keep:
            for v in lab.clients.values():
                v.stop()
            lab.server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
