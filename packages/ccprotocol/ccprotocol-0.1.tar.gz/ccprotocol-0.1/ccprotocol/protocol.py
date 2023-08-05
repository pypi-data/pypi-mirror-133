from .backend import Backend


FUELS = [
    "minecraft:coal",
]


class Peripherals(Backend):
    """
    Peripherals controller.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)

    def __substitute(self, name: str):
        sides = ["top", "bottom", "left", "right"]
        if name in sides:
            return name

        names = {}
        for side in sides:
            names[side] = self.getType(side)
        value = [k for k, v in names.items() if v == name]
        if value:
            return value[0]
        return name

    def getNames(self):
        return self.call("peripheral", "getNames")

    def isPresent(self, name: str):
        return self.call("peripheral", "isPresent", self.__substitute(name))

    def getType(self, name: str):
        return self.call("peripheral", "getType", self.__substitute(name))

    def getMethods(self, name: str):
        return self.call("peripheral", "getMethods", self.__substitute(name))

    def peripheral_call(self, name: str, method: str, *args):
        return self.call("peripheral", "call", self.__substitute(name), method, *args)


class Turtle(Backend):
    """
    Initialize a computercraft turtle.

    `path` : str
        Path to the folder id of the computer.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.peripherals = Peripherals(path)

    @property
    def location(self):
        return self.call("gps", "locate")

    def inventory_items(self):
        items = []
        for i in range(1, 17):
            detail = self.getItemDetail(i)
            if detail:
                detail["position"] = i
                items.append(detail)
        return items

    def auto_refuel(self):
        """Sort through the inventory and find fuel, if it finds fuel, refuel. Returns the new fuel level"""
        items = self.inventory_items()

        for item in items:
            if item["name"] in FUELS:
                self.select(item["position"])
                self.refuel()

                return self.getFuelLevel()

        return self.getFuelLevel()

    def forward(self):
        return self.call("turtle", "forward")

    def back(self):
        return self.call("turtle", "back")

    def up(self):
        return self.call("turtle", "up")

    def down(self):
        return self.call("turtle", "down")

    def turnLeft(self):
        return self.call("turtle", "turnLeft")

    def turnRight(self):
        return self.call("turtle", "turnRight")

    def dig(self, side: str = ""):
        return self.call("turtle", "dig", side)

    def digUp(self, side: str = ""):
        return self.call("turtle", "digUp", side)

    def digDown(self, side: str = ""):
        return self.call("turtle", "digDown", side)

    def place(self, text: str = ""):
        return self.call("turtle", "place", text)

    def placeUp(self, text: str = ""):
        return self.call("turtle", "placeUp", text)

    def placeDown(self, text: str = ""):
        return self.call("turtle", "placeDown", text)

    def drop(self, count: int = ""):
        return self.call("turtle", "drop", count)

    def dropUp(self, count: int = ""):
        return self.call("turtle", "dropUp", count)

    def dropDown(self, count: int = ""):
        return self.call("turtle", "dropDown", count)

    def select(self, slot: int):
        return self.call("turtle", "select", slot)

    def getItemCount(self, slot: int):
        return self.call("turtle", "getItemCount", slot)

    def getItemSpace(self, slot: int):
        return self.call("turtle", "getItemSpace", slot)

    def detect(self):
        return self.call("turtle", "detect")

    def detectUp(self):
        return self.call("turtle", "detectUp")

    def detectDown(self):
        return self.call("turtle", "detectDown")

    def compare(self):
        return self.call("turtle", "compare")

    def compareUp(self):
        return self.call("turtle", "compareUp")

    def compareDown(self):
        return self.call("turtle", "compareDown")

    def attack(self, side: str = ""):
        return self.call("turtle", "attack", side)

    def attackUp(self, side: str = ""):
        return self.call("turtle", "attackUp", side)

    def attackDown(self, side: str = ""):
        return self.call("turtle", "attackDown", side)

    def suck(self, count: int = ""):
        return self.call("turtle", "suck", count)

    def suckUp(self, count: int = ""):
        return self.call("turtle", "suckUp", count)

    def suckDown(self, count: int = ""):
        return self.call("turtle", "suckDown", count)

    def getFuelLevel(self):
        return self.call("turtle", "getFuelLevel")

    def refuel(self, count: int = ""):
        return self.call("turtle", "refuel", count)

    def compareTo(self, slot: int):
        return self.call("turtle", "compareTo", slot)

    def transferTo(self, slot: int, count: int = ""):
        return self.call("turtle", "transferTo", slot, count)

    def getSelectedSlot(self):
        return self.call("turtle", "getSelectedSlot")

    def getFuelLimit(self):
        return self.call("turtle", "getFuelLimit")

    def equipLeft(self):
        return self.call("turtle", "equipLeft")

    def equipRight(self):
        return self.call("turtle", "equipRight")

    def inspect(self):
        return self.call("turtle", "inspect")

    def inspectUp(self):
        return self.call("turtle", "inspectUp")

    def inspectDown(self):
        return self.call("turtle", "inspectDown")

    def getItemDetail(self, slot: int, detailed: bool = False):
        return self.call("turtle", "getItemDetail", slot, detailed)

    def craft(self, limit: int = ""):
        return self.call("turtle", "craft", limit)
