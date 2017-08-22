import threading
import time
import socket
import json
import mccInterface
from RTDataQueue import RTDataQueue 
from HtpLogger import HtpLogger


class RTStreamTask():
    def __init__(self):
        self.stopThread = False
        return
    
    def terminate(self):
        self.stopThread = True
        HtpLogger.get().debug("Request to terminate RTStreamTask.")
    
    # If there is something in the RTDataQueue, send it.
    def run(self, rtSocket):
        conn, address = rtSocket.accept()
        rtq = RTDataQueue()
        while True:
            if self.stopThread:
                HtpLogger.get().debug("self.stopThread is true.  Ready to terminate RTStreamTask.")
                break
            if rtq.isEmpty():  # Continue loop if nothing in the queue
                continue
            rtJson = rtq.get()            # read the queue
            HtpLogger.get().debug(">> {0}".format(rtJson))
            self._sendJson(rtJson, conn)  # send the data over the socket
        HtpLogger.get().debug("RTStreamTask terminating.")
        return        
        
        
    
        
    # Generates the payload JSON.
    def _getRTData(self):
        rtData = mccInterface.readAllMCC()
        rtJson = json.dumps(rtData)
        HtpLogger.get().info(rtJson)
        return rtJson
        
    def _sendJson(self, message, conn):
        # Prepend the message with the payload length
        l = len(message)
        message = "{:0>5d}".format(l) + message
        conn.sendall(str.encode(message))
#        HtpLogger.get().debug("Reply to client: {0}".format(message))
        return
        
        

        
        