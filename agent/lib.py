from __future__ import annotations
import requests


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Agent:
    def __init__(self, agentId: str, address: str, x: float, y: float):
        self.location: Point = Point(x, y)
        self.id = agentId
        self.address = address

    def registerToServer(self: Agent, serverUrl: str):
        print("Registering to server at: {}".format(serverUrl))
        response = requests.post(serverUrl, json={"id": self.id, "url": self.address})
        print("Received response with status: {}".format(response.status_code))
        if response.status_code == 200:
            print("Agent registered to server!")

    def calculateGradient(self: Agent, w: Point) -> Point:
        return Point(w.x - self.location.x, w.y - self.location.y)
