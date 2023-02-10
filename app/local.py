import time

class Local:
    def __init__(self):
        self.temperature: int = 0
        self.humidity: int = 0
        self.doorState: int = 2 # 0 = closed, 1 = open, 2 = unknown 

    def updateDoorStatus(self, doorState: int = 2):
        print("Updating door status")
        try:
            self.doorState = doorState
            print("Door status updated")
        except:
            print("ERROR: Local status update failed")
            return {"update": "failed"}
        return {"update": "success"}

    def updateTempandHum(self, temperature: int = 0, humidity: int = 0):
        print("Updating temperature")
        try:
            self.temperature = temperature
            self.humidity = humidity
            print("Temperature and Humidity and humindity updated")
        except:
            print("ERROR: Temperature update failed")
            return {"update": "failed"}
        return {"update": "success"}

    def getStatus(self):
        print("Getting local status")
        pythonEpochTime = getEpochTime
        # 5 minutes = 300000 ms
        if pythonEpochTime - removeOffsetEpochTime(int(self.time_unix)) > 300000:
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + self.time_unix)
            print("difference too big: " + str(getEpochTime - int(self.time_unix)), " > 300000ms (5min)")
            print("door status = 2")
            return {"state": 2, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé", "time": self.time}
        print("door status = " + str(self.state) + ", info = " + self.info + ", time = " + self.time)
        return {"temperature": self.temperature, "humidity": self.humidity, "door": self.doorState}

    def getDoorStatus(self):
        print("Getting door status")
        return self.doorState


def getEpochTime() -> int:
    epochTime = int(time.time())
    return epochTime


def removeOffsetEpochTime(epochTime: int) -> int:
    offset = 3600  # 1 hour, Brussels time (CET)
    return epochTime - offset
