from fastapi import FastAPI, Depends, HTTPException, Request, status
###from app.auth.auth_bearer import JWTBearer
#from fastapi.security.api_key import APIKey
import auth
#from decouple import config
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re

from door import Door
from local import Local

limiter = Limiter(key_func=get_remote_address, headers_enabled=True, default_limits=[
                  "300/minute"])  # 300 requests per minute = 5 requests per second
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -- initialize door state -- #
#door = Door()

# -- initialize Local -- #
local = Local()

@app.get("/", tags=["root"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_root(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("GET request at / (root) from " + str(origin_ip))
    return {"Hello": "BEP"}

@app.get("/bep/", tags=["bep"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_bep(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("GET request at /bep/ from " + str(origin_ip))
    return {"BEP": "BEP!"}


# -- Local status -- #

@app.get("/local/", tags=["local"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_door(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("GET request at /local/ from " + str(origin_ip))
    return local.getStatusJSON()
    ###return door.getStatus()


@app.post("/local/", dependencies=[Depends(auth.get_api_key)], tags=["local"])
@limiter.limit("300/minute") # 300 requests per minute = 5 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
#def post_door(request: Request, api_key: APIKey = Depends(auth.get_api_key), state: int = 2, info: str = "No info", time: str = "No time", time_unix: int = 1) -> dict:
def post_local(request: Request, door_state: int = 2, info: str = "No info", update_time: str = "No time", update_time_unix: int = 1, temperature: int = 10, humidity: int = 0) -> dict:
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

    origin_ip=""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("POST request at /local/ from " + str(origin_ip))
    if local.updateDoorStateTime(update_time, update_time_unix):
        local.updateDoorStatus(door_state)
        local.updateInfo(info)
        local.updateTempandHum(temperature, humidity)
        print("Local update POST request successfully processed")
        return {"update": "success"}
    print("Local update POST request process failed")
    return {"update": "failed"}


# -- Door status -- #

@app.get("/door/", tags=["door"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
async def get_door(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("GET request at /door/ from " + str(origin_ip))
    return {"door_state" : local.getDoorState}


# -- middleware -- #
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("Executing middleware")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
