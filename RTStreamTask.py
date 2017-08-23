'''
    This task streams data from both the RTDataQueue and RTEventQueue out to a socket as defined by the 
    run(...) parameter.
    
    The run(...) method continually queries both queues for a message.  When a message is
    found, the message is sent over the open socket.

    This task is intended to be the single connection point for all real time data to be 
    streamed to the Data Injection Point.  As such, this task does not modify the message 
    content in any way before transmitting.
    
'''



import threading
import time
import socket
import json
import mccInterface
from RTDataQueue  import RTDataQueue 
from RTEventQueue import RTEventQueue
from HtpLogger import HtpLogger


class RTStreamTask():
    def __init__(self):
        self.stopThread = False
        self._value_lock = threading.Lock()
        return
    
    def terminate(self):
        self.stopThread = True
        self.currentSocket.close()  # Close the socket in case the run(...) method is blocking
        HtpLogger.get().debug("Request to terminate RTStreamTask.")
    
    # If there is something in the RTDataQueue, send it.
    def run(self, rtSocket):
        self.currentSocket = rtSocket
        connected = False
        rtq = RTDataQueue()
        rte = RTEventQueue()
        
        while not self.stopThread:
            HtpLogger.get().info ("Waiting for a client to connect the RT data stream")
            conn, address = rtSocket.accept() # Ready to accept a connection
            HtpLogger.get().info ("Client connected to the RT data stream: {0}".format(address))
            connected = True
            # Clear the queues, since we don't care what came before
            rtq.clear()
            rte.clear()
        
            while connected:
                if self.stopThread:
                    HtpLogger.get().debug("self.stopThread is true.  Ready to terminate RTStreamTask.")
                    break
                try:
                    if (not rtq.isEmpty()):
                        rtJson = rtq.get()            # read the queue
                        HtpLogger.get().debug(">> {0}".format(rtJson))
                        with self._value_lock:
                            self._sendJson(rtJson, conn)  # send the data over the socket
                    
                    if (not rte.isEmpty()):
                        rtJson = rte.get()            # read the queue
                        HtpLogger.get().debug(">> {0}".format(rtJson))
                        with self._value_lock:
                            self._sendJson(rtJson, conn)  # send the data over the socket
                except ConnectionError:
                    connected = False
                    HtpLogger.get().info ("RT data stream client disconnected")
            
        HtpLogger.get().debug("RTStreamTask terminating.")

        return        
        
    def _sendJson(self, message, conn):
        # Prepend the message with the payload length
        l = len(message)
        message = "{:0>5d}".format(l) + message
        conn.sendall(str.encode(message))
        return
        
        

        
        