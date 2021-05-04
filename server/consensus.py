from store import AgentStore
import math
from lib import Point
from typing import List, Tuple, cast


def correctGradient(gradients: List[Point], n: int, f: int) -> Point:
    norms = []
    for gi in gradients:
        norms.append(math.sqrt(math.pow(gi.x, 2) + math.pow(gi.y, 2)))
    norms.sort()
    for i in range(n - f, n):
        norms[i] = norms[f]
        gradients[i] = gradients[f]
    x, y = 0.0, 0.0
    for gi in gradients:
        x += gi.x
        y += gi.y
    return Point(x, y)


def closeEnough(g: Point, limit=0.05) -> bool:
    return math.fabs(g.x) < limit and math.fabs(g.y) < limit


def calculateConsensus(agentStore: AgentStore, W: Point, step=0.05) -> Tuple[Point, int]:
    agents = agentStore.getAgents()
    n = len(agents)
    f = 2
    gradients: List[Point] = cast(List[Point], [None for _ in agents])
    stepCounter = 0
    while True:
        stepCounter += 1
        for index, agent in enumerate(agents):
            gradients[index] = agent.queryCost(W)
        g = correctGradient(gradients, n, f)
        if closeEnough(g):
            return Point(W.x, W.y), stepCounter
        else:
            W.x = W.x - step * g.x
            W.y = W.y - step * g.y
