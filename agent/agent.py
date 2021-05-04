from flask import Flask, jsonify, request
from typing import Any
import os
from lib import Agent, Point

# Load agent configuration
SERVER_ADDR = os.getenv("ALG_SERVER_ADDR")
AGENT_ADDR = os.getenv("ALG_AGENT_ADDR", "http://localhost:5000")
AGENT_ID = os.getenv("ALG_AGENT_ID")
ENV_NAME = os.getenv("ALG_ENV", "dev")
AGENT_POS_X = os.getenv("ALG_AGENT_X")
AGENT_POS_Y = os.getenv("ALG_AGENT_Y")

# Create agent
AGENT = Agent(AGENT_ID, AGENT_ADDR, float(AGENT_POS_X), float(AGENT_POS_Y))

# Create REST agent
agentService = Flask(__name__)
if ENV_NAME != "prod":
    print("Running in DEV mode!")
    agentService.config["DEBUG"] = True

AGENT.registerToServer(SERVER_ADDR + "/register")


@agentService.route("/cost", methods=["POST"])
def calculateAgentCost():
    payload: Any = request.json
    initialVector: Any = payload["w"]
    w = Point(float(initialVector["x"]), float(initialVector["y"]))
    newGradient = AGENT.calculateGradient(w)
    return jsonify({"grad": {"x": newGradient.x, "y": newGradient.y}})


@agentService.errorhandler(404)
def notFoundErrorHandler(e):
    print(e)
    return jsonify({"status": 404, "error": "Requested resource not found!"})


if __name__ == "__main__":
    PORT = os.getenv("ALG_AGENT_PORT", "5000")
    agentService.run(host="0.0.0.0", port=int(PORT), use_reloader=False)
