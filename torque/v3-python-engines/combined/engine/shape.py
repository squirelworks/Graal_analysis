"""Camera, AdvancedCamera, and ShapeBase.

a client routine lists Camera getPosition, setOrbitMode, setFlyMode.
a client routine lists the AdvancedCamera methods below.
ShapeBase has 8 code refs. Those two functions do not list ShapeBase::
methods, so ShapeBase only records calls that were not in either list.
"""

from __future__ import annotations

from simobject import SimObject


class ShapeBase(SimObject):
    """No ShapeBase:: method list was in the two opened registrars."""

    def __init__(self, name: str = "ShapeBase") -> None:
        super().__init__(name, "ShapeBase")
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set_cell(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Camera(ShapeBase):
    """a client routine."""

    def __init__(self, name: str = "Camera") -> None:
        super().__init__(name)
        self.class_name = "Camera"

    def getPosition(self) -> str:
        self.record("getPosition", ())
        return "%.1f %.1f %.1f" % (self.x, self.y, self.z)

    def setOrbitMode(self, *args: str) -> str:
        return self.record("setOrbitMode", args)

    def setFlyMode(self, *args: str) -> str:
        return self.record("setFlyMode", args)


class AdvancedCamera(ShapeBase):
    """a client routine. Each method records its arguments. No body was read."""

    METHODS = (
        "getCameraPosition", "setCameraPosition", "setPlayerObject", "setTargetObject",
        "clearPlayerObject", "clearTargetObject", "setFlyMode", "setTrackMode",
        "setThirdPersonMode", "setThirdPersonPanMode", "setThirdPersonTargetMode",
        "setGodViewMode", "setOrbitMode", "setFollowTerrainMode", "setLookAtOffset",
        "setThirdPersonOffset", "setGodViewOffset", "getLookAtOffset",
        "getThirdPersonOffset", "getGodViewOffset", "cameraPlayerInput",
        "setOrbitMinMaxZoom", "setOrbitMinMaxDeclination", "setOrbitChangeAngle",
        "setOrbitChangeZoom",
    )

    def __init__(self, name: str = "AdvancedCamera") -> None:
        super().__init__(name)
        self.class_name = "AdvancedCamera"
        for method in self.METHODS:
            setattr(self, method, self._make(method))

    def _make(self, method: str):
        def call(*args: str, _method: str = method) -> str:
            if _method == "getCameraPosition":
                self.record(_method, args)
                return "%.1f %.1f %.1f" % (self.x, self.y, self.z)
            return self.record(_method, args)
        return call
