from __future__ import annotations
from lib import Agent
from typing import List


class AgentStore:
    def __init__(self):
        self.__agents: List[Agent] = []

    def addAgent(self: AgentStore, newAgent: Agent) -> bool:
        for agent in self.__agents:
            if agent.agentId == newAgent.agentId:
                return False
        self.__agents.append(newAgent)
        print("Agent {} registered!".format(newAgent.agentId))
        return True

    def getAgents(self: AgentStore) -> List[Agent]:
        return self.__agents.copy()
