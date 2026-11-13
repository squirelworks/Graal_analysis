"""Tiny console.

Eval lines that a client routine actually receives are in used.md:
Canvas.setContent, Canvas.pushDialog, Canvas.popDialog, start2D, resetCanvas.
set, echo, exec, and eval are the builtins around a client routine.
Globals from a client routine: createCanvas, lockMouse, setNetPort, the get* timers.
"""

from __future__ import annotations

import re

from gui import GuiCanvas, GuiControl, GuiGraalCtrl, build_controls
from netconnection import NetConnection


class Console:
    def __init__(self) -> None:
        self.vars: dict[str, str] = {
            "$pref::Video::resolution": "640 480",
            "$pref::Video::fullScreen": "0",
            "$pref::Graal::noudp": "1",
        }
        self.canvas: GuiCanvas | None = None
        self.graal: GuiGraalCtrl | None = None
        self.net = NetConnection()
        self.objects: dict[str, GuiControl] = {}
        self.kinds = build_controls()
        self.log: list[str] = []
        self.mouse_locked = False
        self._seq = 0

    def echo(self, text: str) -> None:
        self.log.append(text)
        print("echo", text)

    def createCanvas(self, title: str = "Graal") -> GuiCanvas:
        if self.canvas is not None:
            self.echo("cCreateCanvas: canvas has already been instantiated")
            return self.canvas
        self.canvas = GuiCanvas()
        self.canvas.fields["title"] = title
        self.objects["Canvas"] = self.canvas
        self.graal = GuiGraalCtrl()
        self.objects[self.graal.getName()] = self.graal
        self.canvas.setContent(self.graal)
        for dialog in ("MainMenuGui2D", "ServerListGui", "LoadLevelGui", "PlayerProfileGui"):
            ctrl = GuiControl(dialog, "GuiControl")
            self.objects[dialog] = ctrl
        return self.canvas

    def eval(self, line: str) -> str:
        text = line.strip().rstrip(";")
        if not text:
            return ""
        if text.startswith("echo ") or text == "echo":
            self.echo(text[5:])
            return text[5:]
        if text.startswith("set "):
            name, _, value = text[4:].partition(" ")
            self.vars[name] = value
            return value
        if text.startswith("$") and "=" in text:
            name, _, value = text.partition("=")
            self.vars[name.strip()] = value.strip()
            return value.strip()
        if text in ("start2D()", "start2D"):
            if self.graal:
                self.graal.drawer.start2d()
            return "start2D"
        if text in ("resetCanvas()", "resetCanvas"):
            if self.canvas:
                self.canvas.reset()
            return "reset"
        if text in ("createCanvas()", "createCanvas"):
            self.createCanvas()
            return "Canvas"
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\((.*)\)", text)
        if match:
            return self._call(match.group(1), match.group(2), match.group(3))
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\((.*)\)", text)
        if match:
            return self._global(match.group(1), match.group(2))
        self.echo("unparsed " + text)
        return ""

    def exec(self, script: str) -> str:
        last = ""
        for line in script.splitlines():
            last = self.eval(line)
        return last

    def _lookup(self, name: str) -> GuiControl:
        if name not in self.objects:
            kind = self.kinds.get(name, GuiControl)
            self.objects[name] = kind(name)
        return self.objects[name]

    def _call(self, obj_name: str, method: str, args: str) -> str:
        obj = self._lookup(obj_name)
        fn = getattr(obj, method, None)
        if fn is None:
            self.echo("stub %s.%s" % (obj_name, method))
            return ""
        values = []
        for part in args.split(","):
            part = part.strip()
            if not part:
                continue
            values.append(self.objects.get(part, part))
        result = fn(*values) if values else fn()
        return "" if result is None else str(result)

    def _global(self, name: str, args: str) -> str:
        if name == "createCanvas":
            self.createCanvas(args or "Graal")
            return "Canvas"
        if name == "lockMouse":
            self.mouse_locked = True
            return "1"
        if name == "setNetPort":
            self.vars["$netPort"] = args
            return args
        if name == "getVersionString":
            return "G3D28015"
        if name in ("getVersionNumber", "getBuildString", "getCompileTimeString"):
            return ""
        if name in ("getSimTime", "getRealTime"):
            self._seq += 1
            return str(self._seq)
        if name in ("saveJournal", "playJournal"):
            return ""
        if self.graal and hasattr(self.graal, name):
            return self._call(self.graal.getName(), name, args)
        self.echo("stub %s" % name)
        return ""
