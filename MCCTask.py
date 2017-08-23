import time
import json
import threading
import mccInterface
from HtpLogger import HtpLogger
from RTDataQueue import RTDataQueue


class MCCTask():
    def __init__(self):
        if not mccInterface.isMCCInitialized():
            HtpLogger.get().info("MCCTask Initializing MCC")
            mccInterface.initMCC()
        
        self.stop = False
        self.queueItUp = False
        self._value_lock = threading.Lock()

        return
    
    def terminate(self):
        self.stop = True
    
    
    def run(self):
        cc = 0
        rtq = RTDataQueue()
        while True:
            if self.stop:
                break
            rtData = mccInterface.readAllMCC()
            cc = cc + 1
            with self._value_lock:
                if self.queueItUp:  # Add to queue if requested
                    rtJson = "{0}".format(json.dumps(rtData, sort_keys=True))
                    rtq.put(rtJson)
                    self.queueItUp = False
    
        return        
    
    def queueIt(self):
        with self._value_lock:
            self.queueItUp = True
    
        