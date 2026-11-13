"""Gui controls the Mac v3 image names.

GuiCanvas methods: a client routine.
GuiGraalCtrl methods: a client routine.
GuiTSCtrl: a client routine is 285 bytes and lists no methods.
GuiGraal3DCtrl: a client routine is about 500 bytes and lists no methods.
"Graal3D activated!" is referenced from a client routine, a client routine, a client routine.
The other Gui* classes are the control strings in v3-tge-rewrite/used.md.
"""

from __future__ import annotations

from draw2d import Drawer
from level import Level
from play import LocalPlay
from shape import Camera
from simobject import SimObject


CONTROL_NAMES = [
    "GuiArrayCtrl", "GuiAviBitmapCtrl", "GuiBackgroundCtrl", "GuiBitmapBorderCtrl",
    "GuiBitmapButtonCtrl", "GuiBorderButtonCtrl", "GuiBubbleTextCtrl",
    "GuiButtonBaseCtrl", "GuiButtonCtrl", "GuiCheckBoxCtrl", "GuiChunkedBitmapCtrl",
    "GuiClockHud", "GuiConsoleEditCtrl", "GuiConsoleTextCtrl", "GuiContextMenuCtrl",
    "GuiCrossHairHud", "GuiCursor", "GuiDrawingPanel", "GuiEditCtrl",
    "GuiFadeinBitmapCtrl", "GuiFilterCtrl", "GuiFrameSetCtrl", "GuiHealthBarHud",
    "GuiInputCtrl", "GuiInspector", "GuiMLTextCtrl", "GuiMLTextEditCtrl",
    "GuiMapOverviewCtrl", "GuiMenuBar", "GuiMessageVectorCtrl", "GuiMouseEventCtrl",
    "GuiNoMouseCtrl", "GuiPMCtrl", "GuiPMEditCtrl", "GuiPMHistoryCtrl",
    "GuiPlayerView", "GuiPopUpMenuCtrl", "GuiProgressCtrl", "GuiRadioCtrl",
    "GuiScrollCtrl", "GuiShapeNameHud", "GuiSliderCtrl",
    "GuiSpeedometerHud", "GuiTerrPreviewCtrl", "GuiTextCtrl", "GuiTextEditCtrl",
    "GuiTextEditSliderCtrl", "GuiTextListCtrl", "GuiTreeViewCtrl", "GuiWindowCtrl",
    "GuiConsole",
]


class GuiControl(SimObject):
    def __init__(self, name: str = "", class_name: str = "GuiControl") -> None:
        super().__init__(name, class_name or type(self).__name__)
        self.children: list[GuiControl] = []
        self.text = ""
        self.visible = True

    def add(self, child: GuiControl) -> None:
        self.children.append(child)

    def render(self) -> str:
        return ""


class GuiBitmapCtrl(GuiControl):
    """used.md names this as the blit surface. It holds the tile words."""

    def __init__(self, name: str = "GuiBitmapCtrl") -> None:
        super().__init__(name, "GuiBitmapCtrl")
        self.tiles: list[int] = []

    def set_level(self, level: Level | None) -> None:
        self.tiles = list(level.tiles) if level else []


class GuiShowImgCtrl(GuiControl):
    """used.md. The image name recovered next to a player field is wbow1.png."""

    def __init__(self, name: str = "GuiShowImgCtrl") -> None:
        super().__init__(name, "GuiShowImgCtrl")
        self.image = ""


class GuiTSCtrl(GuiControl):
    """a client routine registers the class and no console methods.

    Move and loadLevel are not methods here. GuiGraalCtrl pushes the cell
    and the level into this object when those a client routine methods run.
    """

    def __init__(self, name: str = "GuiTSCtrl") -> None:
        super().__init__(name, "GuiTSCtrl")
        self.level: Level | None = None
        self.x = 0
        self.y = 0
        self.facing = "down"
        self.camera: Camera | None = None

    def take_level(self, level: Level) -> None:
        self.level = level

    def take_cell(self, x: float, y: float, facing: str) -> None:
        self.x, self.y, self.facing = x, y, facing
        if self.camera is not None:
            self.camera.set_cell(x, y)


class GuiGraal3DCtrl(GuiControl):
    """a client routine registers the class and no console methods.

    The activation text is the string at a client routine and its two neighbors.
    Nothing in the opened registrar sets it, so activated stays false until
    a caller stores it.
    """

    ACTIVATION = "Graal3D activated!"

    def __init__(self, name: str = "GuiGraal3DCtrl") -> None:
        super().__init__(name, "GuiGraal3DCtrl")
        self.level: Level | None = None
        self.x = 0
        self.y = 0
        self.facing = "down"
        self.activated = False

    def take_level(self, level: Level) -> None:
        self.level = level

    def take_cell(self, x: float, y: float, facing: str) -> None:
        self.x, self.y, self.facing = x, y, facing


class GuiCanvas(GuiControl):
    """a client routine. Dialogs are a stack. Content is one control."""

    def __init__(self) -> None:
        super().__init__("Canvas", "GuiCanvas")
        self.content: GuiControl | None = None
        self.dialogs: list[GuiControl] = []
        self.cursor = True
        self.cursor_pos = (0, 0)
        self.filter_state = "0"
        self.filter_color = "0 0 0 0"
        self.filter_mask = ""

    def setContent(self, ctrl: GuiControl) -> None:
        self.content = ctrl

    def getContent(self) -> GuiControl | None:
        return self.content

    def pushDialog(self, ctrl: GuiControl) -> None:
        self.dialogs.append(ctrl)

    def popDialog(self, ctrl: GuiControl | None = None) -> None:
        if not self.dialogs:
            return
        if ctrl is None or self.dialogs[-1] is ctrl:
            self.dialogs.pop()

    def popLayer(self) -> None:
        self.popDialog()

    def cursorOn(self) -> None:
        self.cursor = True

    def cursorOff(self) -> None:
        self.cursor = False

    def setCursor(self, name: str) -> None:
        self.fields["cursor"] = name

    def hideCursor(self) -> None:
        self.cursor = False

    def showCursor(self) -> None:
        self.cursor = True

    def isCursorOn(self) -> bool:
        return self.cursor

    def getCursorPos(self) -> tuple[int, int]:
        return self.cursor_pos

    def setCursorPos(self, x: int, y: int) -> None:
        self.cursor_pos = (int(x), int(y))

    def repaint(self) -> str:
        return self.renderFront()

    def reset(self) -> None:
        self.dialogs.clear()
        self.content = None

    def setFilterState(self, state: str) -> None:
        self.filter_state = state

    def setFilterColor(self, color: str) -> None:
        self.filter_color = color

    def setFilterMask(self, mask: str) -> None:
        self.filter_mask = mask

    def renderFront(self) -> str:
        parts = []
        if self.content is not None and hasattr(self.content, "render"):
            parts.append(self.content.render())
        for dialog in self.dialogs:
            parts.append("dialog %s" % dialog.getName())
        return "\n".join(p for p in parts if p)


class GuiGraalCtrl(GuiControl):
    """a client routine stores a key flag. a client routine applies the step.

    moveUp/Left/Down/Right are a client routine and the three neighbors. Each
    calls a client routine on the argument and a client routine stores that 0 or 1
    at a client global plus the direction index (up 0, left 1, down 2, right 3).
    a client routine then adds the unit vector at the pointer in a client global
    (0.0,-1), (-1,0), (0,1), (1,0), multiplied by 0.5. That 0.5 is
    DOUBLE_006481e8, the plain scale in a client routine when field +0x4d is 0,
    the state at +0x13d is not 0xe, the tile type is not 0x14, and field
    +0xae is not above 2.
    """

    # Direction index from the move* tail calls into a client routine.
    _SLOTS = {"up": 0, "left": 1, "down": 2, "right": 3}
    # Doubles at the address stored in a client global, times the plain scale.
    _VECTORS = {"up": (0.0, -0.5), "left": (-0.5, 0.0), "down": (0.0, 0.5), "right": (0.5, 0.0)}

    def __init__(self, name: str = "GraalCtrl") -> None:
        super().__init__(name, "GuiGraalCtrl")
        self.level: Level | None = None
        self.x = 0.0
        self.y = 0.0
        self.facing = "down"
        self.keys = [0] * 11
        self.account = ""
        self.nick = ""
        self.password = ""
        self.language = ""
        self.chat = ""
        self.drawer = Drawer()
        self.notes: list[str] = []
        self.bitmap = GuiBitmapCtrl()
        self.showimg = GuiShowImgCtrl()
        self.ts: GuiTSCtrl | None = None
        self.view3d: GuiGraal3DCtrl | None = None
        self.options: dict[str, str] = {}
        self.play = LocalPlay()
        self.remotes: dict[int, dict] = {}
        self.file_asks: list[str] = []

    def attach(self, ts: GuiTSCtrl, view3d: GuiGraal3DCtrl) -> None:
        self.ts = ts
        self.view3d = view3d

    def _publish(self) -> None:
        if self.ts is not None:
            self.ts.take_cell(self.x, self.y, self.facing)
        if self.view3d is not None:
            self.view3d.take_cell(self.x, self.y, self.facing)

    def _pressed(self, arg: str | None) -> int:
        """a client routine. "true", "1", or a non-zero atoi is 1. Anything else is 0."""
        if arg is None:
            return 1
        text = str(arg)
        if text in ("true", "1"):
            return 1
        try:
            return 0 if int(text, 10) == 0 else 1
        except ValueError:
            return 0

    def _step(self, way: str, arg: str | None = None) -> str:
        flag = self._pressed(arg)
        self.keys[self._SLOTS[way]] = flag
        if flag == 0:
            note = "key %s 0" % way
        else:
            dx, dy = self._VECTORS[way]
            scale = self.play.hidden_scale()
            self.facing = way
            self.x += dx * scale
            self.y += dy * scale
            note = "move%s -> %.1f,%.1f" % (way.title(), self.x, self.y)
        self._publish()
        self.notes.append(note)
        return note

    def moveUp(self, arg: str | None = None) -> str:
        return self._step("up", arg)

    def moveDown(self, arg: str | None = None) -> str:
        return self._step("down", arg)

    def moveLeft(self, arg: str | None = None) -> str:
        return self._step("left", arg)

    def moveRight(self, arg: str | None = None) -> str:
        return self._step("right", arg)

    def doA(self) -> str:
        note = self.play.do_a(self.level, self.x, self.y, self.facing)
        self.notes.append(note)
        return note

    def doS(self) -> str:
        note = self.play.do_s()
        self.notes.append(note)
        return note

    def doD(self) -> str:
        note = self.play.do_d()
        self.notes.append(note)
        return note

    def doQ(self) -> str:
        return self._button("doQ")

    def doP(self) -> str:
        return self._button("doP")

    def doM(self) -> str:
        note = self.play.do_m()
        self.notes.append(note)
        return note

    def doMicro(self) -> str:
        return self._button("doMicro")

    def _button(self, name: str) -> str:
        self.notes.append(name)
        return name

    def setChat(self, text: str) -> None:
        """a client routine copies the line and a client routine sends id 0x16.

        The text is truncated to 0xdc. The UDP wrapper a client routine is not built.
        """
        self.chat = text
        self.play.chat = text

    def setNickName(self, text: str) -> None:
        self.nick = text

    def setAccountName(self, text: str) -> None:
        self.account = text

    def setPassWord(self, text: str) -> None:
        self.password = text

    def setLanguage(self, text: str) -> None:
        self.language = text

    def retrieveAccountFields(self) -> str:
        return "%s %s" % (self.account, self.nick)

    def openServerList(self) -> str:
        """a client routine calls the lister. A later id 0 on that connection fills the rows."""
        self.play.server_list_open = True
        return "openServerList"

    def showPlayerList(self) -> str:
        """2.05 F7 list. This image has GuiPlayerView and no method of that name."""
        self.play.player_list_open = True
        if self.nick and self.nick not in self.play.players:
            self.play.players.append(self.nick)
        return "players %d" % len(self.play.players)

    def selectServer(self, name: str) -> str:
        self.fields["server"] = name
        self.play.selected_server = name
        self.play.selected_row = None
        for row in self.play.rows:
            if name in (row.get("line"), row.get("name")):
                self.play.selected_row = row
                break
        return name

    def selectServerCategory(self, name: str) -> str:
        self.fields["category"] = name
        return name

    def startOfflineMode(self) -> str:
        self.drawer.start2d()
        return "offline"

    def connectToSelectedServer(self) -> str:
        """a client routine. Field 6 is the host and field 7 is the port.

        The login frames are built by GraalLink.login. This stores the address
        the next dial uses. A port a client routine rejected stays unset.
        """
        row = self.play.selected_row
        if row is None:
            return self.play.selected_server or self.fields.get("server", "")
        self.play.host = row.get("host") or ""
        port = row.get("port")
        if port is None or port == 0xFFFFFFFF:
            self.play.port = None
            return self.play.host
        self.play.port = int(port)
        return "%s:%d" % (self.play.host, self.play.port)

    def serverDirectConnect(self, address: str) -> str:
        self.fields["server"] = address
        return address

    def updateLoadLevelFields(self) -> str:
        return self.level.magic if self.level else ""

    def loadLevel(self, text: str) -> str:
        self.level = Level()
        self.level.load(text)
        self.x = 0
        self.y = 0
        self.bitmap.set_level(self.level)
        if self.ts is not None:
            self.ts.take_level(self.level)
        if self.view3d is not None:
            self.view3d.take_level(self.level)
        self._publish()
        return self.level.magic

    def updatePlayerProfile(self, *_args: str) -> None:
        self.record("updatePlayerProfile", _args)

    def updatePlayerMuted(self, flag: str) -> None:
        self.fields["muted"] = flag

    def updateMidiVolume(self, value: str) -> None:
        """a client routine. Stores the argument. The pref key text was not walked."""
        self.fields["midi"] = str(value)

    def updateMp3Volume(self, value: str) -> None:
        self.fields["mp3"] = str(value)

    def updateRadioVolume(self, value: str) -> None:
        self.fields["radio"] = str(value)

    def updateMicroActivationLevel(self, value: str) -> None:
        self.fields["micro"] = str(value)

    def updateGraalOptions(self) -> str:
        """a client routine. Copies the prefs a client routine binds, when the console set them."""
        self.fields.update(self.options)
        return " ".join("%s=%s" % (k, v) for k, v in self.options.items())

    def editorOpen(self) -> str:
        """2.05 F4. Refused there while online. This client is offline when it opens."""
        self.play.editing = True
        return "editor"

    def editorPlaceTile(self, x: str, y: str, tile: str) -> str:
        if self.level is None:
            return "no level"
        self.level.put(int(x), int(y), int(tile))
        return "tile %s %s %s" % (x, y, tile)

    def editorPlaceNpc(self, image: str, x: str, y: str) -> str:
        if self.level is None:
            return "no level"
        from level import Npc
        self.level.npcs.append(Npc(image, float(x), float(y), "// stub"))
        return "npc %s" % image

    def editorSave(self, path: str) -> str:
        if self.level is None:
            return "no level"
        from pathlib import Path
        dest = Path(path)
        dest.write_text(self.level.save(), "latin1")
        return "saved %s" % dest

    def requestFile(self, name: str) -> str:
        from protocol import file_extension
        if file_extension(name) == ".gft":
            return "skip %s" % name
        note = self.play.files.request(name)
        if note.startswith("ask") and name not in self.file_asks and len(self.file_asks) < 4:
            self.file_asks.append(name)
        return note

    def render(self) -> str:
        body = self.drawer.frame(self.level, self.x, self.y, self.facing, self.remotes)
        extra = self.play.status()
        if not extra:
            return body
        return body + "\n" + "\n".join(extra)


def build_controls() -> dict[str, type]:
    kinds: dict[str, type] = {}
    for name in CONTROL_NAMES:
        kinds[name] = type(name, (GuiControl,), {"__doc__": "String in the Mac v3 image. Stub draw."})
    kinds["GuiCanvas"] = GuiCanvas
    kinds["GuiGraalCtrl"] = GuiGraalCtrl
    kinds["GuiTSCtrl"] = GuiTSCtrl
    kinds["GuiGraal3DCtrl"] = GuiGraal3DCtrl
    kinds["GuiBitmapCtrl"] = GuiBitmapCtrl
    kinds["GuiShowImgCtrl"] = GuiShowImgCtrl
    return kinds
