import time

class Local:
    def __init__(self):
        self.temperature: int = 0
        self.humidity: int = 0
        self.doorState: int = 2 # 0 = closed, 1 = open, 2 = unknown 
        self.doorUpdateTime: str = "Unknown"
        self.doorUpdateTimeUnix: int = 1
        self.info: str = "No info"

    def updateDoorStatus(self, doorState: str = "2"):
        print("Updating door status")
        try:
            self.doorState = int(doorState)
            print("Door status updated")
        except:
            print("ERROR: Door status update failed")

    def updateTempandHum(self, temperature: str = "0", humidity: str = "0"):
        print("Updating temperature and humindity")
        try:
            self.temperature = int(temperature)
            self.humidity = int(humidity)
            print("Temperature and humidity updated")
        except:
            print("ERROR: Temperature and humidity update failed")

    def updateDoorStateTime(self, doorUpdateTime: str = "Unknown", doorUpdateTimeUnix: str = "1") -> bool:
        print("Updating door state time")
        try:
            if int(doorUpdateTimeUnix) < 1:
                raise Exception("ERROR: Impossible unix time for update time")
            if int(doorUpdateTimeUnix) < self.doorUpdateTimeUnix:
                raise Exception("ERROR: Update time received incorrect")
            self.doorUpdateTime = doorUpdateTime
            self.doorUpdateTimeUnix = int(doorUpdateTimeUnix)
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
        pythonEpochTime = getEpochTime
        # 5 minutes = 300000 ms
        if pythonEpochTime - removeOffsetEpochTime(int(self.doorUpdateTimeUnix)) > 300000:
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + self.doorUpdateTimeUnix)
            print("difference too big: " + str(getEpochTime - int(self.doorUpdateTimeUnix)), " > 300000ms (5min)")
            print("door status = 2")
            return {"door_state": 2, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé", "update_time": self.getUpdateTime, "temperature": self.getTemperature, "humidity": self.getHumidity}
        print("door status = " + str(self.getDoorState) + ", info = " + self.getInfo + ", time = " + self.getUpdateTime)
        return {"temperature": self.getTemperature, "humidity": self.getHumidity, "door_state": self.getDoorState, "info": self.getInfo, "update_time": self.getUpdateTime}

    def getDoorState(self):
        print("Getting door status")
        return str(self.doorState)

    def getUpdateTime(self):
        print("Getting update time")
        return str(self.doorUpdateTime)

    def getInfo(self):
        print("Getting info")
        return str(self.info)

    def getTemperature(self):
        print("Getting temperature")
        if self.temperature < 10 | self.temperature > 35:
            return "Error°C"
        return str(self.temperature) + "°C"

    def getHumidity(self):
        print("Getting humidity")
        if self.humidity < 0 | self.humidity > 100:
            return "Error%"
        return str(self.humidity) + "%"


def getEpochTime() -> int:
    epochTime = int(time.time())
    return epochTime


def removeOffsetEpochTime(epochTime: int) -> int:
    offset = 3600  # 1 hour, Brussels time (CET)
    return epochTime - offset
