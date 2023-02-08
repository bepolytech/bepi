# get unix time import ?
import time

class Door:
    def __init__(self):
        # lest updated state
        self.state: int = -1
        # last updated info
        self.info: str = "No info"
        # last updated time (human readable and unix)
        self.time: str = "No time"
        self.time_unix: str = "1"

    def updateState(self, state: int = -1, info: str = "No info", time: str = "No time", time_unix: str = "1"):
        try:
            if int(time_unix) < int(self.time_unix):
                raise Exception("ERROR: Time incorrect")
            self.state = state
            self.info = info
            self.time = time
        except:
            print("ERROR: Door status update failed")
            return {"update": "failed"}
        return {"update": "success"}

    def getState(self):
        time.unix_time()
        if time.unix_time() - int(self.time_unix) > 300:
            return {"state": -1, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé", "time": self.time}
        return {"state": self.state, "info": self.info, "time": self.time}
