"""SimObject and SimSet.

Evidence: a client routine at an address registers save, setName, getName,
getClassName, getId, getGroup, delete, schedule, dump, getType, and the
SimSet methods listObjects, add, remove, clear, getCount, getObject,
isMember, bringToFront, pushToBack. Strings SimObject and SimSet.
"""

from __future__ import annotations


class SimObject:
    _next_id = 1

    def __init__(self, name: str = "", class_name: str | None = None) -> None:
        self.name = name
        self.class_name = class_name or type(self).__name__
        self.fields: dict[str, str] = {}
        self.id = SimObject._next_id
        SimObject._next_id += 1
        self.group: SimSet | None = None
        self.deleted = False
        self.calls: list[tuple[str, tuple]] = []

    def setName(self, name: str) -> None:
        self.name = name

    def getName(self) -> str:
        return self.name

    def getClassName(self) -> str:
        return self.class_name

    def getId(self) -> int:
        return self.id

    def getGroup(self) -> SimSet | None:
        return self.group

    def getType(self) -> str:
        return self.class_name

    def dump(self) -> str:
        body = " ".join("%s=%s" % (k, v) for k, v in self.fields.items())
        return "%s %s(%d) %s" % (self.class_name, self.name, self.id, body)

    def delete(self) -> None:
        self.deleted = True
        if self.group is not None:
            self.group.remove(self)

    def save(self) -> str:
        return self.dump()

    def schedule(self, when: str = "", call: str = "") -> str:
        """a client routine. The body of the scheduler was not read."""
        self.calls.append(("schedule", (when, call)))
        return call

    def record(self, method: str, args: tuple) -> str:
        self.calls.append((method, args))
        return method


class SimSet(SimObject):
    """a client routine SimSet methods."""

    def __init__(self, name: str = "") -> None:
        super().__init__(name, "SimSet")
        self.objects: list[SimObject] = []

    def add(self, obj: SimObject) -> None:
        if obj not in self.objects:
            self.objects.append(obj)
            obj.group = self

    def remove(self, obj: SimObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)
            obj.group = None

    def clear(self) -> None:
        for obj in list(self.objects):
            self.remove(obj)

    def getCount(self) -> int:
        return len(self.objects)

    def getObject(self, index: int) -> SimObject:
        return self.objects[index]

    def isMember(self, obj: SimObject) -> bool:
        return obj in self.objects

    def listObjects(self) -> list[str]:
        return [obj.getName() or str(obj.getId()) for obj in self.objects]

    def bringToFront(self, obj: SimObject) -> None:
        self.remove(obj)
        self.objects.append(obj)
        obj.group = self

    def pushToBack(self, obj: SimObject) -> None:
        self.remove(obj)
        self.objects.insert(0, obj)
        obj.group = self
