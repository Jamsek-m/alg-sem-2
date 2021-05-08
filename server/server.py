import os
from flask import Flask, request, jsonify
from lib import AgentConflict, Agent, Point, SystemFault
from store import AgentStore
from typing import Any
from consensus import calculateConsensus

ENV_NAME = os.getenv("ALG_ENV", "dev")
ALG_SERVER_W_X = os.getenv("ALG_SERVER_W_X")
ALG_SERVER_W_Y = os.getenv("ALG_SERVER_W_Y")
ALG_STEP_SIZE = float(os.getenv("ALG_STEP_SIZE", "0.05"))
ALG_LIMIT = float(os.getenv("ALG_LIMIT", "0.05"))

server = Flask(__name__)
if ENV_NAME != "prod":
    print("Running in DEV mode!")
    server.config["DEBUG"] = True

W: Point = Point(float(ALG_SERVER_W_X), float(ALG_SERVER_W_Y))
AGENT_STORE = AgentStore()


@server.route("/agents", methods=["GET"])
def getRegisteredAgents():
    return jsonify(list(map(lambda a: a.toDict(), AGENT_STORE.getAgents())))


@server.route("/register", methods=["POST"])
def registerAgent():
    payload: Any = request.json
    agentId = str(payload["id"])
    agentUrl = str(payload["url"])
    agent = Agent(agentId, agentUrl)
    registered = AGENT_STORE.addAgent(agent)
    if registered:
        message = "Agent {} registered at {}!".format(agent.agentId, agent.address)
        return jsonify({"status": 200, "message": message})
    else:
        raise AgentConflict("Agent with given id already registered!")


@server.route("/consensus", methods=["POST"])
def getAgentCost():
    meetingPoint, steps = calculateConsensus(AGENT_STORE, W.copy(), step=ALG_STEP_SIZE, limit=ALG_LIMIT)
    return jsonify({"meetingPoint": {"x": meetingPoint.x, "y": meetingPoint.y}, "steps": steps})


@server.errorhandler(AgentConflict)
def agentConflictHandler(e: AgentConflict):
    response = jsonify(e.toDict())
    response.status_code = 409
    return response


@server.errorhandler(SystemFault)
def agentConflictHandler(e: SystemFault):
    response = jsonify(e.toDict())
    response.status_code = 400
    return response


@server.errorhandler(404)
def notFoundErrorHandler(e):
    print(e)
    return jsonify({"status": 404, "error": "Requested resource not found!"})


if __name__ == "__main__":
    PORT = os.getenv("ALG_SERVER_PORT", "5000")
    server.run(host="0.0.0.0", port=int(PORT), use_reloader=False)
