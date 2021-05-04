from __future__ import annotations
from typing import Dict, Any
import requests


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


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
