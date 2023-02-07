from typing import Union

from fastapi import FastAPI

from door import Door

app = FastAPI()

# -- initialize door state -- #
door = Door()

@app.get("/")
def read_root():
    return {"Hello": "BEP"}

@app.get("/bep/")
def read_bep():
    return {"BEP": "BEP!"}

# -- Door status -- #
@app.get("/door/")
def read_door():
    return door.getState()

@app.post("/door/")
def post_door(state: int = -1, info: str = "No info", time: str = "No time", time_unix: int = 1):
    return door.update(state, info, time, time_unix)