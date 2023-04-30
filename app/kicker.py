#TODO: soon ;)
import time
from pydantic import BaseModel, Field
from decouple import config
from fastapi import HTTPException, status

class Kicker(BaseModel):

    id: int = Field(description="Kicker id, used if there are multiple kickers", example=1)

    def __init__(self, id: int) -> None:
        # NEEDS to call the super (BaseModel) __init__() from Pydantic to work
        super().__init__(id=id)

    def isKickerBusy(self):
        pass

    def isKickerAvailable(self):
        pass

    def lookingForPlayers(self):
        pass