import time
from pydantic import BaseModel, Field
from decouple import config
from fastapi import HTTPException, status

MAX_TIME: int = int(config("MAX_TIME", cast=int, default=300)) # 5 minutes = 300 s
UTC_OFFSET: int = int(config("UTC_OFFSET", cast=int, default=3600)) # UTC+2

# uses Pydantic's BaseModel
class Local(BaseModel):
    """Local class, used to store local's data such as door state, info, temperature, humidity, etc."""

    # class attributes
    id: int = Field(description="Local id, used if there are multiple locals", example=1)
    temperature: int = Field(description="Temperature in Celcius", example=21)
    humidity: int = Field(description="Humidity in %", example=15)
    # doorState => 0 = closed, 1 = open, 2 = unknown :
    doorState: int = Field(description="Door state, 0=closed, 1=open, 2=unknown", example=0)
    doorUpdateTime: str = Field(description="Door update time, human readable", example="01/05/2023 14:30:00")
    doorUpdateTimeUnix: int = Field(description="Door update time, unix/epoch", example=int(time.time()))
    info: str = Field(description="Info about the local or door", example="Le BEP vous souhaite une bonne année!")

    # instace attributes
    def __init__(self, id:int) -> None:
        # NEEDS to call the super (BaseModel) __init__() from Pydantic to work
        super().__init__(id=id, temperature=69, humidity=69, doorState=2, doorUpdateTime="Unknown", doorUpdateTimeUnix=int(time.time()), info="Pas d'info")

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

    def updateDoorStateTime(self, offsetDoorUpdateTimeUnix: int = 100) -> bool:
        print("Updating door state time")
        doorUpdateTimeUnix = removeOffsetEpochTime(offsetDoorUpdateTimeUnix)
        try:
            if doorUpdateTimeUnix < 1:
                print("ERROR: Impossible unix time for update time, cannot be negative")
                #raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="ERROR: Impossible unix time for update time, cannot be negative")
                raise ValueError("ERROR: Impossible unix time for update time, cannot be negative")
            if doorUpdateTimeUnix < self.doorUpdateTimeUnix:
                print("ERROR: Update time received incorrect, cannot be less than previous time")
                print("previous time: " + str(self.doorUpdateTimeUnix))
                print("new time: " + str(doorUpdateTimeUnix))
                #raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="ERROR: Update time received incorrect, cannot be less than previous time")
                raise ValueError("ERROR: Update time received incorrect, cannotbe less than previous time")
            if doorUpdateTimeUnix > (int(time.time()) + 120): # 2 minutes
                print("ERROR: Update time received incorrect, too far ahead from current time")
                print("current time: " + str(int(time.time())))
                print("new time: " + str(doorUpdateTimeUnix))
                print("more that 2 minutes ahead")
                print("difference: " + str(doorUpdateTimeUnix - int(time.time())) + " ms")
                #raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="ERROR: Update time received incorrect, too far ahead from current time")
                raise ValueError("ERROR: Update time received incorrect, too far ahead from current time")
            self.doorUpdateTime = str(HumanReadableTime(doorUpdateTimeUnix))
            self.doorUpdateTimeUnix = int(doorUpdateTimeUnix)
            print("Door updated state time updated")
            return True
        except:
            print("ERROR: Door updated state time update failed")
            return False
    
    def updateInfo(self, info: str = "Pas d'info"):
        print("Updating info")
        try:
            self.info = info
            print("Info updated")
        except:
            print("ERROR: Info update failed")

    def getStatusJSON(self):
        print("Getting local status")
        pythonEpochTime: int= getEpochTime()
        diff: int = pythonEpochTime - int(self.doorUpdateTimeUnix)
        # 5 minutes = 300 s
        if diff > int(MAX_TIME):
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + str(self.doorUpdateTimeUnix))
            print("difference too big: " + str(diff), "sec(" + str(diff/60) + "min) > " + str(MAX_TIME) + "sec(~" + str(MAX_TIME/60) + "min)")
            print("door status = 2")
            return {"door_state": 2, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé.", "update_time": self.getUpdateTime(), "temperature": self.getTemperature(), "humidity": self.getHumidity(), "update_time_unix": self.getUpdateTimeUnix()}
        print("door status = " + str(self.doorState) + ", info = " + self.info + ", time = " + self.doorUpdateTime, ", temperature = " + str(self.temperature), ", humidity = " + str(self.humidity), ", door_update_time_unix = " + str(self.doorUpdateTimeUnix))
        return {"temperature": self.getTemperature(), "humidity": self.getHumidity(), "door_state": self.getDoorState(), "info": self.getInfo(), "update_time": self.getUpdateTime(), "update_time_unix": self.getUpdateTimeUnix()}

    def getDoorState(self) -> int:
        pythonEpochTime: int = getEpochTime()
        diff: int = pythonEpochTime - int(self.doorUpdateTimeUnix)
        # 5 minutes = 300 s
        if diff > int(MAX_TIME):
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + str(self.doorUpdateTimeUnix))
            print("difference too big: " + str(diff), "sec(" + str(diff/60) +
                  "min) > " + str(MAX_TIME) + "sec(~" + str(MAX_TIME/60) + "min)")
            print("door status = 2")
            return 2
        print("Getting door status")
        return self.doorState

    def getUpdateTime(self) -> str:
        print("Getting update time")
        return str(self.doorUpdateTime)

    def getUpdateTimeUnix(self) -> int:
        print("Getting update time unix")
        return self.doorUpdateTimeUnix

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


def HumanReadableTime(epochTime = None) -> str:
    return time.strftime("%d/%m/%Y %H:%M", time.localtime(epochTime))


def getEpochTime() -> int:
    epochTime = int(time.time())
    print("getting Epoch time: " + str(epochTime))
    return epochTime


def removeOffsetEpochTime(epochTime: int) -> int:
    # default 1 hour, Brussels time (CET), winter time
    offset: int =  UTC_OFFSET
    res = epochTime - offset
    return res
