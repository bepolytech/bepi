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
        if time.time_ns() - int(self.time_unix) > 300:
            return {"state": -1, "info": "Last update was too long ago, the door status was not updated. Local est alors sans doute fermé", "time": self.time}
        return {"state": self.state, "info": self.info, "time": self.time}
