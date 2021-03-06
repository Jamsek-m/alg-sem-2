from __future__ import annotations
from typing import Dict, Any
import requests


class Point:
    @staticmethod
    def faultyPoint() -> Point:
        return Point(0.0, 0.0)

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self: Point) -> Point:
        return Point(self.x, self.y)


class Agent:
    def __init__(self, agentId: str, agentAddress: str):
        self.agentId = agentId
        self.address = agentAddress

    def queryCost(self: Agent, w: Point) -> Point:
        costUrl = self.address + "/cost"
        response = requests.post(costUrl, json={"w": {"x": w.x, "y": w.y}})
        if response.status_code == 200:
            payload: Any = response.json()
            gradient: Any = payload["grad"]
            return Point(float(gradient["x"]), float(gradient["y"]))
        else:
            raise Exception("Failed querying cost for agent {}".format(self.agentId))

    def toDict(self: Agent) -> Dict[Any, Any]:
        return {"id": self.agentId, "address": self.address}


class AgentConflict(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def toDict(self):
        return {"message": self.message}


class SystemFault(Exception):
    def __init__(self, n: int, f: int):
        Exception.__init__(self)
        self.message = "Too many faulty nodes! Out of {} nodes, at least {} are faulty. Algorithm needs 2f-redundancy to work properly.".format(n, f)

    def toDict(self):
        return {"message": self.message}
