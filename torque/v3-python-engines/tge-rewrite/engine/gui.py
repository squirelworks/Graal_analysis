"""Gui controls the Mac v3 image names.

GuiCanvas methods: a client routine.
GuiGraalCtrl methods: a client routine.
The other Gui* classes are the control strings in used.md. They hold
fields and a parent. Their draw methods are empty except GuiGraalCtrl,
which owns the player step, and GuiBitmapCtrl, which holds a tile grid.
"""

from __future__ import annotations

from draw2d import Drawer
from level import BOARD, Level
from simobject import SimObject

CONTROL_NAMES = [
    "GuiArrayCtrl", "GuiAviBitmapCtrl", "GuiBackgroundCtrl", "GuiBitmapBorderCtrl",
    "GuiBitmapButtonCtrl", "GuiBitmapCtrl", "GuiBorderButtonCtrl", "GuiBubbleTextCtrl",
    "GuiButtonBaseCtrl", "GuiButtonCtrl", "GuiCheckBoxCtrl", "GuiChunkedBitmapCtrl",
    "GuiClockHud", "GuiConsoleEditCtrl", "GuiConsoleTextCtrl", "GuiContextMenuCtrl",
    "GuiCrossHairHud", "GuiCursor", "GuiDrawingPanel", "GuiEditCtrl",
    "GuiFadeinBitmapCtrl", "GuiFilterCtrl", "GuiFrameSetCtrl", "GuiHealthBarHud",
    "GuiInputCtrl", "GuiInspector", "GuiMLTextCtrl", "GuiMLTextEditCtrl",
    "GuiMapOverviewCtrl", "GuiMenuBar", "GuiMessageVectorCtrl", "GuiMouseEventCtrl",
    "GuiNoMouseCtrl", "GuiPMCtrl", "GuiPMEditCtrl", "GuiPMHistoryCtrl",
    "GuiPlayerView", "GuiPopUpMenuCtrl", "GuiProgressCtrl", "GuiRadioCtrl",
    "GuiScrollCtrl", "GuiShapeNameHud", "GuiShowImgCtrl", "GuiSliderCtrl",
    "GuiSpeedometerHud", "GuiTerrPreviewCtrl", "GuiTextCtrl", "GuiTextEditCtrl",
    "GuiTextEditSliderCtrl", "GuiTextListCtrl", "GuiTreeViewCtrl", "GuiWindowCtrl",
    "GuiTSCtrl", "GuiGraal3DCtrl", "GuiConsole",
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
        self.cursor_pos = (x, y)

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
        if self.content is not None:
            parts.append(self.content.render())
        for dialog in self.dialogs:
            parts.append("dialog %s" % dialog.getName())
        return "\n".join(p for p in parts if p)


class GuiGraalCtrl(GuiControl):
    """a client routine. Move methods change the player by one cell.

    The binary does not contain a recovered step length. One cell is the
    BOARD grid unit from a client routine, and the 64-bound is the only test.
    """

    def __init__(self, name: str = "GraalCtrl") -> None:
        super().__init__(name, "GuiGraalCtrl")
        self.level: Level | None = None
        self.x = 0
        self.y = 0
        self.facing = "down"
        self.account = ""
        self.nick = ""
        self.password = ""
        self.language = ""
        self.chat = ""
        self.drawer = Drawer()
        self.notes: list[str] = []

    def _step(self, way: str, dx: int, dy: int) -> str:
        self.facing = way
        nx, ny = self.x + dx, self.y + dy
        if not (0 <= nx < BOARD and 0 <= ny < BOARD):
            note = "blocked %d,%d" % (nx, ny)
        else:
            self.x, self.y = nx, ny
            note = "move%s -> %d,%d" % (way.title(), self.x, self.y)
        self.notes.append(note)
        return note

    def moveUp(self) -> str:
        return self._step("up", 0, -1)

    def moveDown(self) -> str:
        return self._step("down", 0, 1)

    def moveLeft(self) -> str:
        return self._step("left", -1, 0)

    def moveRight(self) -> str:
        return self._step("right", 1, 0)

    def doA(self) -> str:
        return self._button("doA")

    def doS(self) -> str:
        return self._button("doS")

    def doD(self) -> str:
        return self._button("doD")

    def doQ(self) -> str:
        return self._button("doQ")

    def doP(self) -> str:
        return self._button("doP")

    def doM(self) -> str:
        return self._button("doM")

    def doMicro(self) -> str:
        return self._button("doMicro")

    def _button(self, name: str) -> str:
        self.notes.append(name)
        return name

    def setChat(self, text: str) -> None:
        self.chat = text

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
        return "openServerList"

    def selectServer(self, name: str) -> str:
        self.fields["server"] = name
        return name

    def selectServerCategory(self, name: str) -> str:
        self.fields["category"] = name
        return name

    def startOfflineMode(self) -> str:
        self.drawer.start2d()
        return "offline"

    def connectToSelectedServer(self) -> str:
        return self.fields.get("server", "")

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
        return self.level.magic

    def updatePlayerProfile(self, *_args: str) -> None:
        return None

    def updatePlayerMuted(self, flag: str) -> None:
        self.fields["muted"] = flag

    def updateMidiVolume(self, value: str) -> None:
        self.fields["midi"] = value

    def updateMp3Volume(self, value: str) -> None:
        self.fields["mp3"] = value

    def updateRadioVolume(self, value: str) -> None:
        self.fields["radio"] = value

    def updateMicroActivationLevel(self, value: str) -> None:
        self.fields["micro"] = value

    def updateGraalOptions(self) -> None:
        return None

    def render(self) -> str:
        return self.drawer.frame(self.level, self.x, self.y, self.facing)


def build_controls() -> dict[str, type]:
    kinds: dict[str, type] = {}
    for name in CONTROL_NAMES:
        kinds[name] = type(name, (GuiControl,), {"__doc__": "String in the Mac v3 image. Stub draw."})
    kinds["GuiCanvas"] = GuiCanvas
    kinds["GuiGraalCtrl"] = GuiGraalCtrl
    return kinds
