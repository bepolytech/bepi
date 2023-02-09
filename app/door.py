# get unix time import ?
import time #time_ns() : int epoch Unix time, time() : float epoch Unix time

class Door:
    def __init__(self):
        # lest updated state
        self.state: int = 2
        # last updated info
        self.info: str = "No info"
        # last updated time (human readable and unix)
        self.time: str = "No time"
        self.time_unix: str = "1"

    def updateStatus(self, state: int = 2, info: str = "No info", time: str = "No time", time_unix: str = "1"):
        print("Updating door status")
        try:
            if int(time_unix) < int(self.time_unix):
                raise Exception("ERROR: Time incorrect")
            # TODO
            self.state = state
            self.info = info
            self.time = time
            print("Door status updated")
        except:
            print("ERROR: Door status update failed")
            return {"update": "failed"}
        return {"update": "success"}

    def getStatus(self):
        print("Getting door status")
        # TODO time.unix_time()
        pythonEpochTime = getEpochTime
        if pythonEpochTime - removeOffsetEpochTime(int(self.time_unix)) > 300000: # 5 minutes = 300000 ms
            print("python epoch time: " + str(pythonEpochTime))
            print("door epoch time: " + self.time_unix)
            print("difference too big: " + str(getEpochTime - int(self.time_unix)), " > 300000ms (5min)")
            print("door status = 2")
            return {"state": 2, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé", "time": self.time}
        print("door status = " + str(self.state) + ", info = " + self.info + ", time = " + self.time)
        return {"state": self.state, "info": self.info, "time": self.time}

def getEpochTime() -> int:
    epochTime = int(time.time())
    return epochTime

def removeOffsetEpochTime(epochTime: int) -> int:
    offset = 3600 # 1 hour, Brussels time (CET)
    return epochTime - offset
