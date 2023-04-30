from fastapi import FastAPI, Depends, Request, Response  # , HTTPException, status
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
from fastapi.middleware.cors import CORSMiddleware

from local import Local
from apiauth import ApiAuth

api_description = """
🚀 API for the BEP - Bureau Étudiant de Polytechnique ⚒️

### **🚨⚠️ Requests are rate-limited at 120/minute. ⚠️🚨**

## Local

You can **`GET /local/`**'s data:
* **Door state** (`"door_state" : int`)  
    0 = closed, 1 = open, 2 = unknown  
    _The door state is unknown when the last update was too long ago (more than 5 minutes), meaning a problem occured with the door status system._
* **Door update time** (`"update_time" : str`)  
    Human readable
* **Info** (`"info" : str`)  
    Info about the Local or door
* **Temperature** (`"temperature" : int`)  
    In °C
* **Humidity** (`"humidity" : int`)  
    In %
* **Door update time (UNIX)** (`"update_time_unix" : int`)  
    Epoch time, seconds since 1970-01-01 00:00:00 UTC

## Info (about BEP or Local)

You can **`GET /info/`**'s data:
* **Info** (`"info" : str`)  
    Info about the Local or door

## Door (in Local)

You can **`GET /door/`**'s data:
* **Door state** (`"door_state" : int`)  
    0 = closed, 1 = open, 2 = unknown  
    _The door state is unknown when the last update was too long ago (more than 5 minutes), meaning a problem occured with the door status system._
* **Door update time** (`"update_time" : str`)  
    Human readable
* **Door update time (UNIX)** (`"update_time_unix" : int`)  
    Epoch time, seconds since 1970-01-01 00:00:00 UTC

## Temperature and humidity (in Local)

You can **`GET /temp/`** data:
* **Temperature** (`"temperature" : int`)
    In °C
* **Humidity** (`"humidity" : int`)
    In %

## Other
BEP website: [bepolytech.be](http://bepolytech.be/)  

> *Notes:*
> - **`PUT /local/`** requires a private API key, reserved for BEP.  
> - **`PUT /info/`** requires a private API key, reserved for BEP.  
> - Any request to non-existent endpoints will return `{"detail": "Not Found"}`.
"""

tags_metadata = [
    {
        "name": "local",
        "description": "Info and operations with the BEP's Local data.",
    },
    {
        "name": "info",
        "description": "Info about BEP or its Local.",
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
    },
    {
        "name": "test",
        "description": "yea",
    }
]

limiter = Limiter(key_func=get_remote_address, headers_enabled=False, default_limits=["300/minute"])  # 300 requests per minute = 5 requests per second
app = FastAPI(
    title="BEP API - BEPI",
    description=api_description,
    version="1.4.0",
    contact={
        "name": "BEP - Bureau Étudiant de Polytechnique",
        "url": "https://bepolytech.be/",
    },
    openapi_tags=tags_metadata
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# -- initialize Local(s) -- #
local = Local(0, "Local BEP - S.UB1.149") # id = 0
#if we want to add more locals, we would could another instance with another id to differentiate them, like this:
#local1 = Local(1, "BEP Cave - S.UA1.xxx") # id = 1
#we could then make a list of BEP's locals, if needed:
#locals = [local, local1]

# -- initialize API key auth -- #
auth = ApiAuth()


### ----- routes/requests handlers ----- ###

@app.get("/", tags=["root"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_root(request: Request) -> dict:
    #origin_ip = ""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
    #print("GET request at / (root) from " + str(origin_ip))
    print("GET request at / (root)")
    res = {"Hello": "BEP"}
    print("Sending response:")
    print(res)
    return res


@app.get("/quoi/", tags=["test"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def quoifeur(request: Request):
    # origin_ip = ""
    # print("Analyzing request headers for x-forwarded-for:")
    # for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
    # print("GET request at / (root) from " + str(origin_ip))
    print("GET request at /quoi/")
    res = "feur"
    print("Sending response:")
    print(res)
    return res

@app.get("/bep/", tags=["bep"])
@limiter.limit("120/minute") # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_bep(request: Request) -> dict:
    #origin_ip = ""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
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
    #origin_ip = ""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
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
        update_time_unix: int,
        temperature: int = 69,
        humidity: int = 69
    ) -> dict:

    #origin_ip=""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
    #print("PUT request at /local/ from " + str(origin_ip))
    print("PUT request at /local/")
    cond = local.checkDoorUpdateTimeCorrect(update_time_unix)
    if cond:
        local.updateDoorStateTime(update_time_unix)
        local.updateDoorStatus(door_state)
        local.updateTempandHum(temperature, humidity)
        print("Local update PUT request successfully processed")
        res = {"api_key": "correct", "auth": "yes", "update": "success"}
    else:
        print("Local update PUT request process failed")
        res = {"api_key": "correct", "auth": "yes", "update": "failed", "detail" : "update error, might be due to incorrect update_time_unix"}
    print("Sending response:")
    print(res)
    return res


@app.get("/info/", tags=["info"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_info(request: Request) -> dict:
    # origin_ip = ""
    # print("Analyzing request headers for x-forwarded-for:")
    # for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
    # print("GET request at /local/ from " + str(origin_ip))
    print("GET request at /info/")
    info = local.getInfo()
    res = {"info": info}
    print("Sending response:")
    print(res)
    return res


@app.put("/info/", dependencies=[Depends(auth.get_api_key)], tags=["info"])
@limiter.limit("300/minute")  # 300 requests per minute = 5 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
def update_info(*, request: Request,
                 info: str = "Pas d'info"
                 ) -> dict:
    print("PUT request at /info/")
    try:
        local.updateInfo(info)
        print("Info update PUT request successfully processed")
        res = {"api_key": "correct", "auth": "yes", "update": "success"}
    except:
        print("Info update PUT request process failed")
        res = {"api_key": "correct", "auth": "yes", "update": "failed", "detail": "info update failed"}
    finally:
        return res


# -- Door status -- #

@app.get("/door/", tags=["door"])
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
async def read_door(request: Request) -> dict:
    #origin_ip = ""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #    else:
    #        print("No x-forwarded-for header found")
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
    #origin_ip = ""
    #print("Analyzing request headers for x-forwarded-for:")
    #for header in request.headers.raw:
    #    if header[0] == 'x-forwarded-for'.encode('utf-8'):
    #        origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
    #        print(f"origin_ip:\t{origin_ip}")
    #        print(f"forward_ip:\t{forward_ip}")
    #print("GET request at /temps/ from " + str(origin_ip))
    print("GET request at /temps/")
    res = {"temperature": local.getTemperature(), "humidity": local.getHumidity()}
    print("Sending response:")
    print(res)
    return res

# -- images -- #


@app.get("/images/{filename}", tags=["images"],
    # Set what the media type will be in the autogenerated OpenAPI specification.
    # fastapi.tiangolo.com/advanced/additional-responses/#additional-media-types-for-the-main-response
    responses={
        200: {
            "content": {"image/svg": {}}
        }
    },
    # Prevent FastAPI from adding "application/json" as an additional
    # response media type in the autogenerated OpenAPI specification.
    # https://github.com/tiangolo/fastapi/issues/3258
    response_class=Response
)
@limiter.limit("120/minute")  # 120 requests per minute = 2 requests per second
# request argument must be explicitly passed to your endpoint, or slowapi won't be able to hook into it :
def get_image_bep_simple(request: Request, filename: str):
    images = {
        "bep-simple.svg": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1078.2812 541.7083"><defs><style>.cls-1{fill:#114994;}.cls-2{fill:#4472c4;}.cls-3{fill:#8faadc;}.cls-4{fill:#1c1c1a;}.cls-5{fill:#114a95;}.cls-6{fill:#1c1c19;}</style></defs><title>bep simple</title><g id="Dark_Blue_Strip" data-name="Dark Blue Strip"><rect class="cls-1" y="122.125" width="732.1666" height="56.75"/></g><g id="Blule_Strip" data-name="Blule Strip"><rect class="cls-2" x="246.6667" y="61.0625" width="485.5" height="56.75"/></g><g id="Light_Blue_Strip" data-name="Light Blue Strip"><rect class="cls-3" x="489.875" width="242.2916" height="56.75"/></g><g id="EPB"><polygon class="cls-4" points="1078.281 337.042 898.952 337.042 1043.859 34.422 736.948 178.875 736.948 0 1078.281 0 1078.281 337.042"/><path class="cls-5" d="M739.87,192.6735l220.4375-73.0469L884.7135,332.3141C884.6042,256.22,822.2292,199.3454,739.87,192.6735Z"/></g><g id="BEP"><path class="cls-6" d="M0,219.6875H133.1042c116.625,0,120.4583,135.1875,51.5833,149.2708,40.0417,8.5833,60.7083,41.5833,60.7083,77.3333,0,35.4167-16.3333,95.4167-117.9928,95.4167H55.2292V496.625h75.75c48.8333,0,63.8125-22.4167,63.8125-49.25,0-35.7917-21.6875-50.8281-71.25-50.8281H55.01V351.0313h69.8438c20.75,0,56.4583-1.1562,56.7083-41.1562.1242-19.8746-3-46-64.9583-45.5625H0Z"/><rect class="cls-6" x="1.2917" y="270.5625" width="47.9375" height="269.875"/><rect class="cls-6" x="360.0625" y="353.375" width="160.6667" height="44"/><polygon class="cls-6" points="540.729 219.687 305.271 219.687 305.271 541.708 547.646 541.708 547.646 496.437 355.073 496.437 355.073 264.493 540.729 264.493 540.729 219.687"/><path class="cls-6" d="M661.7292,219.6875h82.6667c106.5,0,109.845,75.4375,109.845,95.8127,0,17.7081-5.6784,98.8748-114.3711,98.8748H661.7292V369.2083h83c20.6667,0,59.5417-9.5833,59.5417-53.75,0-23.2083-11.1667-51.5833-58.2694-51.5833H661.7292Z"/><rect class="cls-6" x="607.2604" y="219.6875" width="49.057" height="322.0208"/></g></svg>
    """,
        "bep-nah.svg": """nah"""
   }
    #data = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1078.2812 541.7083"><defs><style>.cls-1{fill:#114994;}.cls-2{fill:#4472c4;}.cls-3{fill:#8faadc;}.cls-4{fill:#1c1c1a;}.cls-5{fill:#114a95;}.cls-6{fill:#1c1c19;}</style></defs><title>bep simple</title><g id="Dark_Blue_Strip" data-name="Dark Blue Strip"><rect class="cls-1" y="122.125" width="732.1666" height="56.75"/></g><g id="Blule_Strip" data-name="Blule Strip"><rect class="cls-2" x="246.6667" y="61.0625" width="485.5" height="56.75"/></g><g id="Light_Blue_Strip" data-name="Light Blue Strip"><rect class="cls-3" x="489.875" width="242.2916" height="56.75"/></g><g id="EPB"><polygon class="cls-4" points="1078.281 337.042 898.952 337.042 1043.859 34.422 736.948 178.875 736.948 0 1078.281 0 1078.281 337.042"/><path class="cls-5" d="M739.87,192.6735l220.4375-73.0469L884.7135,332.3141C884.6042,256.22,822.2292,199.3454,739.87,192.6735Z"/></g><g id="BEP"><path class="cls-6" d="M0,219.6875H133.1042c116.625,0,120.4583,135.1875,51.5833,149.2708,40.0417,8.5833,60.7083,41.5833,60.7083,77.3333,0,35.4167-16.3333,95.4167-117.9928,95.4167H55.2292V496.625h75.75c48.8333,0,63.8125-22.4167,63.8125-49.25,0-35.7917-21.6875-50.8281-71.25-50.8281H55.01V351.0313h69.8438c20.75,0,56.4583-1.1562,56.7083-41.1562.1242-19.8746-3-46-64.9583-45.5625H0Z"/><rect class="cls-6" x="1.2917" y="270.5625" width="47.9375" height="269.875"/><rect class="cls-6" x="360.0625" y="353.375" width="160.6667" height="44"/><polygon class="cls-6" points="540.729 219.687 305.271 219.687 305.271 541.708 547.646 541.708 547.646 496.437 355.073 496.437 355.073 264.493 540.729 264.493 540.729 219.687"/><path class="cls-6" d="M661.7292,219.6875h82.6667c106.5,0,109.845,75.4375,109.845,95.8127,0,17.7081-5.6784,98.8748-114.3711,98.8748H661.7292V369.2083h83c20.6667,0,59.5417-9.5833,59.5417-53.75,0-23.2083-11.1667-51.5833-58.2694-51.5833H661.7292Z"/><rect class="cls-6" x="607.2604" y="219.6875" width="49.057" height="322.0208"/></g></svg>"""
    return Response(content=images[filename], media_type="image/svg")


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

origins = [
    "https://bepolytech.be",
    "http://localhost",
    "http://localhost:8000",
    "*" # ALLOW ALL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
