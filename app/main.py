from fastapi import FastAPI, Body, Depends, HTTPException, status, Request
from app.auth.auth_bearer import JWTBearer
from fastapi.security.api_key import APIKey
import auth
from decouple import config

from door import Door

app = FastAPI()

# -- initialize door state -- #
door = Door()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"Hello": "BEP"}

@app.get("/bep/", tags=["bep"])
async def read_bep() -> dict:
    return {"BEP": "BEP!"}

# -- Door status -- #


@app.get("/door/", tags=["door"])
async def read_door() -> dict:
    return door.getState()


@app.post("/door/", dependencies=[Depends(auth.get_api_key)], tags=["door"])
async def post_door(api_key: APIKey = Depends(auth.get_api_key), state: int = -1, info: str = "No info", time: str = "No time", time_unix: int = 1) -> dict:
    #credentials_exception = HTTPException(
    #    status_code=status.HTTP_401_UNAUTHORIZED,
    #    detail="Could not validate credentials",
    #    headers={"WWW-Authenticate": "Bearer"},
    #)
    if api_key != config("API_KEY"):
        raise HTTPException(
            status_code=403, detail="Could not validate API KEY"
        )
        return {"update": "failed"}
    else:
        return door.update(state, info, time, time_unix)


# -- middleware -- #
#@app.middleware("http")
#async def add_process_time_header(request: Request, call_next):
#    start_time = time.time()
#    response = await call_next(request)
#    process_time = time.time() - start_time
#    response.headers["X-Process-Time"] = str(process_time)
#    return response
