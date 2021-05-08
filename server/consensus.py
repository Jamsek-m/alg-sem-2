from store import AgentStore
import math
from town import isInTown
from lib import Point, SystemFault
from typing import List, Tuple, cast, Set


def clipNorm(current: Point, largest: Point) -> Point:
    currentNorm = math.sqrt(math.pow(current.x, 2) + math.pow(current.y, 2))
    largestPossibleNorm = math.sqrt(math.pow(largest.x, 2) + math.pow(largest.y, 2))
    return Point(largestPossibleNorm / currentNorm * current.x, largestPossibleNorm / currentNorm * current.y)


def correctGradient(gradients: List[Point], n: int, f: int) -> Point:
    sortedGradients = sorted(gradients, key=lambda g: math.sqrt(math.pow(g.x, 2) + math.pow(g.y, 2)))
    for i in range(n - f, n):
        sortedGradients[i] = clipNorm(sortedGradients[i], sortedGradients[f])
    x, y = 0.0, 0.0
    for gi in sortedGradients:
        x += gi.x
        y += gi.y
    return Point(x, y)


def closeEnough(g: Point, limit=0.05) -> bool:
    return math.fabs(g.x) < limit and math.fabs(g.y) < limit


def isFaultyOrThrow(n: int, f: int) -> bool:
    if n - 2 * f > 0:
        return True
    raise SystemFault(n, f)


def calculateConsensus(agentStore: AgentStore, W: Point, step=0.05, limit=0.05) -> Tuple[Point, int]:
    agents = agentStore.getAgents()
    n = len(agents)
    faultyAgents: Set[str] = set()
    gradients: List[Point] = cast(List[Point], [None for _ in agents])
    stepCounter = 0
    while True:
        stepCounter += 1
        for index, agent in enumerate(agents):
            isFaultyOrThrow(n, len(faultyAgents))
            try:
                agentCost = agent.queryCost(W)
                if isInTown(W, agentCost):
                    gradients[index] = agentCost
                else:
                    faultyAgents.update([agent.agentId])
                    gradients[index] = Point.faultyPoint()
            except:
                faultyAgents.update([agent.agentId])
                gradients[index] = Point.faultyPoint()
        g = correctGradient(gradients, n, len(faultyAgents))
        if closeEnough(g, limit):
            return Point(W.x, W.y), stepCounter
        else:
            W.x = W.x - step * g.x
            W.y = W.y - step * g.y
