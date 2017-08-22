'''
Data Injection Point Server


'''
import socket
from socket import timeout as TimeoutException
import json
from FormulaTimer import FormulaTimer
import time
from _thread import *
import threading

import mccInterface

from HtpLogger import HtpLogger
from RTStreamTask import RTStreamTask
from MCCTask import MCCTask
from HumiditySensorTask import HumiditySensorTask

HOST = ''
COMS_PORT = 5560
RT_STREAM_PORT = 5561
HDR_LEN = 5   # Message header length
RT_CMD = "RT"

log = HtpLogger.get()


'''
    Public method to start the DIP server
'''
def startServer():
    global comsSocket, rtStreamSocket
    global mccTask, humTask, rtTask
    
    # Initialize the MCC
    mccInterface.initMCC()

    # Initialize sockets for commands and real time streaming    
    comsSocket = _initComs(COMS_PORT, 1)
    rtStreamSocket = _initComs(RT_STREAM_PORT, 1)

    # Start the main server thread to listen for, and handle, requests
    start_new_thread(_serverThread, ())

    # Start the humidity sensor thread
    humTask = HumiditySensorTask()
    t = threading.Thread(target=humTask.run, args=())
    t.start()

    # Start the MCC task running in a thread ... this gets data from the MCC
    mccTask = MCCTask()
    t = threading.Thread(target=mccTask.run, args=())
    t.start()

    # Start the real time data stream thread.  But doesn't send data until instructed to do so.
    rtTask = RTStreamTask()
    t = threading.Thread(target=rtTask.run, args=(rtStreamSocket,))
    t.start()

    return

def stopServer():
    global mccTask, humTask, rtTask
    HtpLogger.get().debug("Stopping dipServer")
    mccTask.terminate()
    humTask.terminate()
    rtTask.terminate()



'''
    Public method to send messages to the DIP
'''
def sendMessage(message, conn):
    # Prepend the message with the payload length
    l = len(message)
    message = "{:0>5d}".format(l) + message
    conn.sendall(str.encode(message))
    log.debug("Reply to client: {0}".format(message))
    return

############################################################################


def _initComs(port, numConnections):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        skt.bind((HOST, port))
    except socket.error as msg:
        log.error(msg)
    skt.listen(numConnections)
    return skt
    

'''
    Thread that waits for client requests and passes them to the _messageHandler()
'''
def _serverThread():    
    global comsSocket
    while True:
        # Block to accept commands from the dipClient
        conn, address = comsSocket.accept()
        clientMsg = _receiveMessage(conn)
        if not clientMsg:
            log.warning("Empty client message")
            continue
        message = str(clientMsg)
        _messageHandler(message, conn)

    log.warning("_serverThreadStopped")
    conn.close()
    comsSocket.close()
    return


'''
    Handles DI point client requests.
'''
def _messageHandler(message, conn):
    global rtTask, rtStreamSocket
    global mccTask, rtdRun
    
    if (message=="RT"):               # Request for real time data
        rtdRun = True
        t = threading.Thread(target=_queueRTD, args=())
        t.start()
        sendMessage("{\"rtStream\":\"Started\"}", conn)

    elif (message=="RTStop"):
        rtdRun = False
        sendMessage("{\"rtStream\":\"Stopped\"}", conn)

    elif (message=="TStart"):          # Start Timer
        FormulaTimer().start()
        sendMessage("{\"Timer\":\"Started\"}", conn)
        
    elif (message=="T"):
        t = FormulaTimer().getElapsedTimeSec()
        msg = "{{\"Timer\":\"{0}\"}}".format(t)
        sendMessage(msg, conn)
        
    elif (message=="TStop"):
        FormulaTimer().stop()
        sendMessage("{\"Timer\":\"Stopped\"}", conn)
        
    elif (message=="TStat"):
        if FormulaTimer().isRunning():
            s = "Running"
        else:
            s = "Stopped"
        msg = "{{\"Timer\":\"{0}\"}}".format(s)
        sendMessage(msg, conn)
            
    else:
        sendMessage("{ \"Error\":\"Unknown request\"}", conn)
        log.error("Error: Unknown request: {0}".format(message))

    return




def _queueRTD():
    global rtdRun, mccTask
    
    while rtdRun:
        mccTask.queueIt()
        time.sleep(1)

    
def _receiveMessage(conn):
    # Read the header bytes, which will tell us the length of the payload.
    try:
        payloadLen = int(conn.recv(HDR_LEN))
    except ValueError:
        log.warning("Invalid payload length from client")
        return None
    except ConnectionError :
        log.warning("Client connection error")
        return None
    
    payload = ""
    # Receive the payload
    while (payloadLen>0):
        payloadBytes = conn.recv(1024)
        payloadLen -= len(payloadBytes)
        payload = payload + payloadBytes.decode('utf-8')

    return payload










    
# Generates the payload JSON.
def _getRTData():
    rtData = mccInterface.readAllMCC()
    rtJson = json.dumps(rtData)
    log.info(rtJson)
    return rtJson


  
    
    
    
    


