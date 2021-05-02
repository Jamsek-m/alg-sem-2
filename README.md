# ALG seminarska 2

## Run 

Use docker-compose to build and run server and agents:

```bash
docker-compose up --build
```

### Run locally

Run `pip install -r requirements.txt` in virtualenv to install required dependencies.

Server is configured using following environment variables:
* **ALG_SERVER_PORT** (port where server should run, like `5000`)
* **ALG_ENV** (either set to `prod` or `dev` (default), to enable debugger's logs)

Agent is configured using following environment variables:
* **ALG_AGENT_ID** (unique agent id, like `agent-1`)
* **ALG_SERVER_ADDR** (root url of server, ie. `http://localhost:5000`)
* **ALG_AGENT_ADDR** (root url of agent, ie. `http://localhost:5001`)
* **ALG_AGENT_PORT** (port where agent should run, like `5001+`)
* **ALG_ENV** (either set to `prod` or `dev` (default), to enable debugger's logs)


### Build Docker image
To build docker image for either service, run from project root:
```bash
docker build -f Dockerfile.server -t alg-server:latest .
docker build -f Dockerfile.agent -t alg-agent:latest .
```
