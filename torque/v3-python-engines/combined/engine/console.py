"""Tiny console.

Eval lines that a client routine actually receives are in used.md:
Canvas.setContent, Canvas.pushDialog, Canvas.popDialog, start2D, resetCanvas.
echo, exec, and eval are named from a client routine, along with the
string helpers. Globals from a client routine: createCanvas, lockMouse, setNetPort,
the get* timers. Bare names from a client routine: nameToID, isObject, cancel,
isEventPending, deleteDataBlocks.
"""

from __future__ import annotations

import re
from pathlib import Path

from gui import GuiCanvas, GuiControl, GuiGraal3DCtrl, GuiGraalCtrl, GuiTSCtrl, build_controls
from netconnection import GameConnection, NetConnection
from shape import AdvancedCamera, Camera, ShapeBase

# a client routine. Stores were not walked, so the values start empty except noudp.
GRAAL_PREFS = (
    "$pref::Graal::fixedport",
    "$pref::Graal::fixedudpport",
    "$pref::Graal::noudp",
    "$pref::Graal::dontsavepasswords",
    "$pref::Graal::automapping",
    "$pref::Graal::nomassmessages",
    "$pref::Graal::notoalls",
    "$pref::Graal::dontloadlistheads",
    "$pref::Graal::dontconnectlevels",
    "$pref::Graal::limitnicknames",
    "$pref::Graal::nicknamelimit",
    "$pref::Graal::defaultfontsize",
)


class Console:
    def __init__(self) -> None:
        self.vars: dict[str, str] = {
            "$pref::Video::resolution": "640 480",
            "$pref::Video::fullScreen": "0",
        }
        for name in GRAAL_PREFS:
            self.vars[name] = "1" if name.endswith("noudp") else ""
        self.canvas: GuiCanvas | None = None
        self.graal: GuiGraalCtrl | None = None
        self.ts: GuiTSCtrl | None = None
        self.view3d: GuiGraal3DCtrl | None = None
        self.net = NetConnection()
        self.game = GameConnection()
        self.camera = Camera()
        self.advanced = AdvancedCamera()
        self.objects: dict[str, object] = {
            "NetConnection": self.net,
            "GameConnection": self.game,
            "Camera": self.camera,
            "AdvancedCamera": self.advanced,
            "ShapeBase": ShapeBase(),
        }
        self.kinds = build_controls()
        self.log: list[str] = []
        self.mouse_locked = False
        self._seq = 0
        self.events: dict[int, str] = {}
        self._event_id = 1

    def echo(self, text: str) -> None:
        """a client routine names echo. The second echo xref a client routine did not decompile."""
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
        self.ts = GuiTSCtrl()
        self.view3d = GuiGraal3DCtrl()
        self.ts.camera = self.camera
        self.graal.attach(self.ts, self.view3d)
        self.objects[self.graal.getName()] = self.graal
        self.objects["GuiTSCtrl"] = self.ts
        self.objects["GuiGraal3DCtrl"] = self.view3d
        self.canvas.setContent(self.graal)
        for dialog in ("MainMenuGui2D", "ServerListGui", "LoadLevelGui", "PlayerProfileGui"):
            self.objects[dialog] = GuiControl(dialog, "GuiControl")
        return self.canvas

    def eval(self, line: str) -> str:
        """a client routine eval. Splits a short script on semicolons outside quotes and calls."""
        last = ""
        for part in _statements(line):
            last = self._one(part.strip())
        return last

    def exec(self, script: str) -> str:
        """a client routine exec. A path is read as text. Otherwise the string is the script."""
        path = Path(script.strip().strip("'\""))
        if path.is_file():
            script = path.read_text("latin1")
        return self.eval(script.replace("\n", ";"))

    def _one(self, text: str) -> str:
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

    def _lookup(self, name: str) -> object:
        if name not in self.objects:
            kind = self.kinds.get(name, GuiControl)
            self.objects[name] = kind(name)
        return self.objects[name]

    def _args(self, args: str) -> list:
        values = []
        for part in args.split(","):
            part = part.strip()
            if not part:
                continue
            if len(part) >= 2 and part[0] == part[-1] and part[0] in "'\"":
                values.append(part[1:-1])
            else:
                values.append(self.objects.get(part, part))
        return values

    def _call(self, obj_name: str, method: str, args: str) -> str:
        obj = self._lookup(obj_name)
        if method == "updateGraalOptions" and self.graal is not None:
            self.graal.options = {
                key: self.vars.get(key, "") for key in GRAAL_PREFS
            }
        fn = getattr(obj, method, None)
        if fn is None:
            self.echo("stub %s.%s" % (obj_name, method))
            return ""
        values = self._args(args)
        result = fn(*values) if values else fn()
        return "" if result is None else str(result)

    def _global(self, name: str, args: str) -> str:
        values = self._args(args)
        if name == "createCanvas":
            self.createCanvas(str(values[0]) if values else "Graal")
            return "Canvas"
        if name == "lockMouse":
            self.mouse_locked = True
            return "1"
        if name == "setNetPort":
            self.vars["$netPort"] = "" if not values else str(values[0])
            return self.vars["$netPort"]
        if name == "getVersionString":
            # a client routine registers the command. Its return text was not read.
            return "G3D28015"
        if name in ("getVersionNumber", "getBuildString", "getCompileTimeString"):
            return ""
        if name in ("getSimTime", "getRealTime"):
            self._seq += 1
            return str(self._seq)
        if name in ("saveJournal", "playJournal"):
            return ""
        if name == "echo":
            text = " ".join(str(v) for v in values)
            self.echo(text)
            return text
        if name == "eval":
            return self.eval(" ".join(str(v) for v in values))
        if name == "exec":
            return self.exec(" ".join(str(v) for v in values))
        if name == "isObject":
            return "1" if values and str(values[0]) in self.objects else "0"
        if name == "nameToID":
            obj = self.objects.get(str(values[0])) if values else None
            if obj is None or not hasattr(obj, "getId"):
                return "-1"
            return str(obj.getId())
        if name == "deleteDataBlocks":
            self.log.append("deleteDataBlocks")
            return ""
        if name == "schedule":
            ident = self._event_id
            self._event_id += 1
            self.events[ident] = " ".join(str(v) for v in values)
            return str(ident)
        if name == "cancel":
            if values:
                self.events.pop(int(str(values[0])), None)
            return ""
        if name == "isEventPending":
            if not values:
                return "0"
            return "1" if int(str(values[0])) in self.events else "0"
        if name in _STRINGS:
            return _STRINGS[name](*[str(v) for v in values])
        if self.graal and hasattr(self.graal, name):
            return self._call(self.graal.getName(), name, args)
        self.echo("stub %s" % name)
        return ""


def _statements(line: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    quote = ""
    for ch in line:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "'\"":
            quote = ch
            buf.append(ch)
            continue
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        if ch == ";" and depth == 0:
            parts.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return parts


def _strcmp(a: str = "", b: str = "") -> str:
    if a == b:
        return "0"
    return "-1" if a < b else "1"


def _strpos(a: str = "", b: str = "") -> str:
    return str(a.find(b))


_STRINGS = {
    "ExpandFilename": lambda a="": a,
    "strcmp": _strcmp,
    "stricmp": lambda a="", b="": _strcmp(a.lower(), b.lower()),
    "strlen": lambda a="": str(len(a)),
    "strstr": lambda a="", b="": a[a.find(b):] if b and b in a else "",
    "strpos": _strpos,
    "ltrim": lambda a="": a.lstrip(),
    "rtrim": lambda a="": a.rstrip(),
    "trim": lambda a="": a.strip(),
    "stripChars": lambda a="", b="": "".join(ch for ch in a if ch not in b),
    "strlwr": lambda a="": a.lower(),
    "strupr": lambda a="": a.upper(),
}
