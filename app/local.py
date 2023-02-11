import time
from pydantic import BaseModel, Field
from decouple import config

MAX_TIME: int = int(config("MAX_TIME", cast=int, default=300000)) # 5 minutes = 300000 ms

# uses Pydantic's BaseModel
class Local(BaseModel):
    """Local class, used to store local's data such as door state, info, temperature, humidity, etc."""

    # class attributes
    id: int = Field(description="Local id, used if there are multiple locals", example=1)
    temperature: int = Field(description="Temperature in Celcius", example=20)
    humidity: int = Field(description="Humidity in %", example=30)
    # doorState => 0 = closed, 1 = open, 2 = unknown :
    doorState: int = Field(description="Door state, 0=closed, 1=open, 2=unknown", example=0)
    doorUpdateTime: str = Field(description="Door update time, human readable", example="2021-05-01 12:00:00")
    doorUpdateTimeUnix: int = Field(description="Door update time, unix/epoch", example=1610000000)
    info: str = Field(description="Info about the local or door", example="Le BEP vous souhaite une bonne année!")

    # instace attributes
    def __init__(self, id:int) -> None:
        # NEEDS to call the super (BaseModel) __init__() from Pydantic to work
        super().__init__(id=id, temperature=0, humidity=0, doorState=2, doorUpdateTime="Unknown", doorUpdateTimeUnix=1, info="No info")

    def updateDoorStatus(self, doorState: int = 2):
        print("Updating door status")
        try:
            self.doorState = doorState
            print("Door status updated")
        except:
            print("ERROR: Door status update failed")

    def updateTempandHum(self, temperature: int = 0, humidity: int = 0):
        print("Updating temperature and humindity")
        try:
            self.temperature = temperature
            self.humidity = humidity
            print("Temperature and humidity updated")
        except:
            print("ERROR: Temperature and humidity update failed")

    def updateDoorStateTime(self, doorUpdateTime: str = "Unknown", doorUpdateTimeUnix: int = 1) -> bool:
        print("Updating door state time")
        try:
            if doorUpdateTimeUnix < 1:
                raise Exception("ERROR: Impossible unix time for update time")
            if doorUpdateTimeUnix < self.doorUpdateTimeUnix:
                raise Exception("ERROR: Update time received incorrect")
            self.doorUpdateTime = doorUpdateTime
            self.doorUpdateTimeUnix = doorUpdateTimeUnix
            print("Door updated state time updated")
            return True
        except:
            print("ERROR: Door updated state time update failed")
            return False
    
    def updateInfo(self, info: str = "No info"):
        print("Updating info")
        try:
            self.info = info
            print("Info updated")
        except:
            print("ERROR: Info update failed")

    def getStatusJSON(self):
        print("Getting local status")
        pythonEpochTime = getEpochTime()
        # 5 minutes = 300000 ms
        if pythonEpochTime - removeOffsetEpochTime(int(self.doorUpdateTimeUnix)) > MAX_TIME:
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + str(self.doorUpdateTimeUnix))
            print("difference too big: " + str(getEpochTime() - int(self.doorUpdateTimeUnix)), " > " + str(MAX_TIME) + " ms (" + str(MAX_TIME/60000) + " min)")
            print("door status = 2")
            return {"door_state": 2, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé.", "update_time": str(self.getUpdateTime()), "temperature": str(self.getTemperature()), "humidity": str(self.getHumidity())}
        print("door status = " + str(self.getDoorState()) + ", info = " + self.getInfo() + ", time = " + self.getUpdateTime())
        return {"temperature": self.getTemperature(), "humidity": self.getHumidity(), "door_state": self.getDoorState(), "info": self.getInfo(), "update_time": self.getUpdateTime()}

    def getDoorState(self) -> int:
        print("Getting door status")
        return self.doorState

    def getUpdateTime(self) -> str:
        print("Getting update time")
        return str(self.doorUpdateTime)

    def getInfo(self) -> str:
        print("Getting info")
        return str(self.info)

    def getTemperature(self) -> int:
        print("Getting temperature")
        return self.temperature

    def getHumidity(self) -> int:
        print("Getting humidity")
        if self.humidity < 0:
            print("Humidity < 0 ???")
            return 0
        elif self.humidity > 100:
            print("Humidity > 100 ???")
            return 100
        return self.humidity


def getEpochTime() -> int:
    epochTime = int(time.time())
    return epochTime


def removeOffsetEpochTime(epochTime: int) -> int:
    # default 1 hour, Brussels time (CET)
    offset: int =  int(config("UTC_OFFSET", cast=int, default="3600"))
    return epochTime - offset
