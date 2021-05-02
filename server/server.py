import requests
import os
from flask import Flask, request, jsonify
from lib import AgentConflict

ENV_NAME = os.environ["ALG_ENV"] or "dev"

server = Flask(__name__)
if ENV_NAME != "prod":
    print("Running in DEV mode!")
    server.config["DEBUG"] = True

AGENTS = []


def addAgent(newAgent) -> bool:
    for agent in AGENTS:
        if agent["id"] == newAgent["id"]:
            return False
    AGENTS.append(newAgent)
    print("Agent {} registered!".format(newAgent["id"]))
    return True


@server.route("/agents", methods=["GET"])
def getRegisteredAgents():
    return jsonify(AGENTS)


@server.route("/register", methods=["POST"])
def registerAgent():
    payload = request.json
    agentId = payload["id"]
    agentUrl = payload["url"]
    registered = addAgent({"id": agentId, "url": agentUrl})
    if registered:
        message = "Agent {} registered at {}!".format(agentId, agentUrl)
        return jsonify({"status": 200, "message": message})
    else:
        raise AgentConflict("Agent with given id already registered!")


def queryAgentCost(agent) -> float:
    costUrl = agent["url"] + "/cost"
    response = requests.post(costUrl)
    if response.status_code == 200:
        payload = response.json()
        return float(payload["cost"])


@server.route("/cost", methods=["POST"])
def getAgentCost():
    print("Started querying costs...")
    summa = 0
    for agent in AGENTS:
        summa += queryAgentCost(agent)
    print("Aggregated costs: " + str(summa))
    return jsonify({"cost": summa})


@server.errorhandler(AgentConflict)
def agentConflictHandler(e: AgentConflict):
    response = jsonify(e.toDict())
    response.status_code = 409
    return response


@server.errorhandler(404)
def notFoundErrorHandler(e):
    print(e)
    return jsonify({"status": 404, "error": "Requested resource not found!"})


if __name__ == "__main__":
    PORT = os.environ["ALG_SERVER_PORT"] or "5000"
    server.run(host="0.0.0.0", port=int(PORT), use_reloader=False)
