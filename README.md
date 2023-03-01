# BEPI - BEP's API : https://api.bepolytech.be/docs
### API server for the local, like the door open status  

Built with FastAPI (Python)  
API token required for PUT requests (by ESP8266?)  
Uses slowapi for rate-limiting (120/min)  

#### Docker : from version 1.2.0, uses the alpine variant of python base image.
https://hub.docker.com/repository/docker/bepolytech/bepi/general

## Docs
docs available at https://api.bepolytech.be/docs (or https://api.bepolytech.be/redoc)

## Run
setup a `.env` file in /app (using the provided `.env_template` file).  
then either  
* install pip requirements, then  
  `cd` into /app and run `uvicorn main:app --reload` (--reload to hot-reload during dev),  
* or use docker (with provided docker-compose.yml file), run `docker-compose up -d`.

## License
MIT

### by PLucas 🚀
