from flask import Flask, jsonify
import requests
import os

SERVER_ADDR = os.getenv("ALG_SERVER_ADDR")
AGENT_ADDR = os.getenv("ALG_AGENT_ADDR", "http://localhost:5000")
AGENT_ID = os.getenv("ALG_AGENT_ID")
ENV_NAME = os.getenv("ALG_ENV", "dev")

agent = Flask(__name__)
if ENV_NAME != "prod":
    print("Running in DEV mode!")
    agent.config["DEBUG"] = True


def registerItself():
    url = SERVER_ADDR + "/register"
    print("Registering to server at: {}".format(url))
    response = requests.post(url, json={"id": AGENT_ID, "url": AGENT_ADDR})
    print("Received response with status: {}".format(response.status_code))
    if response.status_code == 200:
        print("Agent registered to server!")


registerItself()


@agent.route("/cost", methods=["POST"])
def getRegisteredAgents():
    return jsonify({"cost": 0.5})


@agent.errorhandler(404)
def notFoundErrorHandler(e):
    print(e)
    return jsonify({"status": 404, "error": "Requested resource not found!"})


if __name__ == "__main__":
    PORT = os.getenv("ALG_AGENT_PORT", "5000")
    agent.run(host="0.0.0.0", port=int(PORT), use_reloader=False)
