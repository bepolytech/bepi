from fastapi import FastAPI, Depends, Request #, HTTPException, status
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re

from local import Local
from apiauth import ApiAuth

api_description = """
🚀 API for the BEP - Bureau Étudiant de Polytechnique ⚒️

### **🚨⚠️ Requests are rate-limited at 120/minute. ⚠️🚨**

## Local

You can **`GET /local`**'s data:
* **Door state** (`"door_state" : int`)  
    0 = closed, 1 = open, 2 = unknown  
    _The door state is unknown when the last update was too long ago (more than 5 minutes), meaning a problem occured with the door status system._
* **Door update time** (`"update_time" : str`)  
    Human readable
* **Info** (`"info" : str`)  
    Info about the local or door
* **Temperature** (`"temperature" : int`)  
    In °C
* **Humidity** (`"humidity" : int`)  
    In %
* **Door update time (UNIX)** (`"update_time_unix" : int`)  
    Epoch time, seconds since 1970-01-01 00:00:00 UTC(+1)  
    ⚠️ this has an offset of UTC+1 applied (so +3600 compared to true UNIX time(UTC))

## Door (in Local)

You can **`GET /door`**'s data:
* **Door state** (`"door_state" : int`)  
    0 = closed, 1 = open, 2 = unknown  
    _The door state is unknown when the last update was too long ago (more than 5 minutes), meaning a problem occured with the door status system._
* **Door update time** (`"update_time" : str`)  
    Human readable
* **Door update time (UNIX)** (`"update_time_unix" : int`)  
    Epoch time, seconds since 1970-01-01 00:00:00 UTC(+1)  
    ⚠️ this has an offset of UTC+1 applied (so +3600 compared to true UNIX time(UTC))

## Temperature and humidity (in Local)

You can **`GET /temp`** data:
* **Temperature** (`"temperature" : int`)
    In °C
* **Humidity** (`"humidity" : int`)
    In %

## Other
BEP website: [bepolytech.be](http://bepolytech.be/)  

> *Notes:*
> - **`PUT /local`** requires a private API key, reserved for BEP.  
> - Any request to non-existent endpoints will return `{"detail": "Not Found"}`.
"""

tags_metadata = [
    {
        "name": "local",
        "description": "Operations with the BEP's Local data.",
    },
    {
        "name": "door",
        "description": "Data about the BEP's door.",
    },
    {
        "name": "temp",
        "description": "Data about the BEP Local's temperature and humidity, updated at the same time with the door status.",
    },
    {
        "name": "bep",
        "description": "BEP!",
    }
]

limiter = Limiter(key_func=get_remote_address, headers_enabled=False, default_limits=[
                  "300/minute"])  # 300 requests per minute = 5 requests per second
app = FastAPI(
    title="BEP API - BEPI",
    description=api_description,
    version="1.2.2",
    contact={
        "name": "BEP - Bureau Étudiant de Polytechnique",
        "url": "http://bepolytech.be/",
    },
    openapi_tags=tags_metadata
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# -- initialize Local(s) -- #
local = Local(1) # id = 1
#if we want to add more locals, we would could another instance with another id to differentiate them, like this:
#local2 = Local(2) # id = 2
#we could then make a list of BEP's locals, if needed:
#locals = [local1, local2]

# -- initialize API key auth -- #
auth = ApiAuth()


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
        else:
            print("No x-forwarded-for header found")
    #print("GET request at / (root) from " + str(origin_ip))
    print("GET request at / (root)")
    res = {"Hello": "BEP"}
    print("Sending response:")
    print(res)
    return res

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
        else:
            print("No x-forwarded-for header found")
    #print("GET request at /bep/ from " + str(origin_ip))
    print("GET request at /bep/")
    res = {"BEP": "BEP!"}
    print("Sending response:")
    print(res)
    return res


# -- Local status -- #

@app.get("/local/", tags=["local"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_local(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
        else:
            print("No x-forwarded-for header found")
    #print("GET request at /local/ from " + str(origin_ip))
    print("GET request at /local/")
    res = local.getStatusJSON()
    print("Sending response:")
    print(res)
    return res


@app.put("/local/", dependencies=[Depends(auth.get_api_key)], tags=["local"])
@limiter.limit("300/minute") # 300 requests per minute = 5 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
def update_local(*, request: Request,
        door_state: int = 2,
        info: str = "No info",
        update_time: str = "No time",
        update_time_unix: int,
        temperature: int = 69,
        humidity: int = 420
    ) -> dict:

    origin_ip=""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
        else:
            print("No x-forwarded-for header found")
    #print("PUT request at /local/ from " + str(origin_ip))
    print("PUT request at /local/")
    if local.updateDoorStateTime(update_time, update_time_unix):
        local.updateDoorStatus(door_state)
        local.updateInfo(info)
        local.updateTempandHum(temperature, humidity)
        print("Local update PUT request successfully processed")
        res = {"api_key": "correct", "auth": "yes", "update": "success"}
        print("Sending response:")
        print(res)
        return res
    print("Local update PUT request process failed")
    res = {"api_key": "correct", "auth": "yes", "update": "failed", "detail" : "unix time error"}
    print("Sending response:")
    print(res)
    return res


# -- Door status -- #

@app.get("/door/", tags=["door"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_door(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
        else:
            print("No x-forwarded-for header found")
    #print("GET request at /door/ from " + str(origin_ip))
    print("GET request at /door/")
    res = {"door_state": local.getDoorState(), "update_time": local.getUpdateTime(), "update_time_unix": local.getUpdateTimeUnix()}
    print("Sending response:")
    print(res)
    return res

# -- Temp and Hum -- #


@app.get("/temp/", tags=["temp"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_temp(request: Request) -> dict:
    origin_ip = ""
    print("Analyzing request headers for x-forwarded-for:")
    for header in request.headers.raw:
        if header[0] == 'x-forwarded-for'.encode('utf-8'):
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    print("GET request at /temps/ from " + str(origin_ip))
    res = {"temperature": local.getTemperature(), "humidity": local.getHumidity()}
    print("Sending response:")
    print(res)
    return res


# -- testing -- #

@app.post("/test/", tags=["test"])
@limiter.limit("60/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def update_test(request: Request) -> dict:
    res = {"test": "success"}
    print("Sending response:")
    print(res)
    return res

#@app.get("/test/", tags=["test"])
#@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
## request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
#async def read_test(request: Request) -> dict:
#    return local.getStatusJSON()
#
#@app.put("/test/", tags=["test"])
#@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
## request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
#async def update_test2(request: Request, updated_local: Local = local) -> dict:
#    return updated_local.getStatusJSON()


# -- middleware -- #
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("Executing middleware")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Process time: {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    print("Middleware finished, added process time to response headers")
    return response
