from fastapi import FastAPI, Depends, HTTPException, Request, status
#from app.auth.auth_bearer import JWTBearer
from fastapi.security.api_key import APIKey
import auth
from decouple import config
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from door import Door
from local import Local

limiter = Limiter(key_func=get_remote_address, headers_enabled=True, default_limits=[
                  "300/minute"])  # 300 requests per minute = 5 requests per second
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -- initialize door state -- #
door = Door()

# -- initialize Local -- #
local = Local()

@app.get("/", tags=["root"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_root(request: Request) -> dict:
    return {"Hello": "BEP"}

@app.get("/bep/", tags=["bep"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_bep(request: Request) -> dict:
    return {"BEP": "BEP!"}


# -- Local status -- #

@app.get("/local/", tags=["local"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_door(request: Request) -> dict:
    return local.getStatusJSON()
    ###return door.getStatus()


@app.post("/local/", dependencies=[Depends(auth.get_api_key)], tags=["local"])
@limiter.limit("300/minute") # 300 requests per minute = 5 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
#def post_door(request: Request, api_key: APIKey = Depends(auth.get_api_key), state: int = 2, info: str = "No info", time: str = "No time", time_unix: int = 1) -> dict:
def post_local(request: Request, doorState: str = "2", info: str = "No info", updateTime: str = "No time", updateTimeUnix: str = "1", temperature: str = "10", humidity: str = "0") -> dict:
    ###credentials_exception = HTTPException(
    ###    status_code=status.HTTP_401_UNAUTHORIZED,
    ###    detail="Could not validate credentials",
    ###    headers={"WWW-Authenticate": "Bearer"},
    ###)

    #if api_key != config("API_KEY"):
    #    print("Could not validate API KEY")
    #    raise HTTPException(
    #        #status_code=401, detail="Could not validate API KEY"
    #        status_code=status.HTTP_401_UNAUTHORIZED,
    #        detail = "Could not validate API KEY"
    #    )
    #    return {"update": "failed"}
    #else:
    #    print("API KEY is valid")
    #    return door.updateStatus(state, info, time, time_unix)

    print("POST request at /local/ from " + request.client.host) # TODO ?
    if local.updateDoorStateTime(updateTime, updateTimeUnix):
        local.updateDoorStatus(doorState)
        local.updateInfo(info)
        local.updateTempandHum(temperature, humidity)
        return {"update": "success"}
    return {"update": "failed"}


# -- Door status -- #

@app.get("/door/", tags=["door"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
async def get_door(request: Request) -> dict:
    return {"door_state" : local.getDoorState}


# -- middleware -- #
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
