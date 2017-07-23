'''
Data Injection Point Server


'''


import socket
import json
import time
from _thread import *

import humiditySensor

import mccInterface



HOST = ''
PORT = 5560
HDR_LEN = 5   # Message header length

RT_CMD = "RT"



def startServer():
    global skt
    
    #Initialize the MCC
    mccInterface.initMCC()
    
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.bind((HOST, PORT))
    except socket.error as msg:
        print(msg)

    skt.listen(1) #Allow one connection at a time.
    start_new_thread(threaded_server, ())
    
    humiditySensor.startHumThread()
    
    return
    
def sendMessage(message, conn):
    # Prepend the message with the payload length
    l = len(message)
    message = "{:0>5d}".format(l) + message
    conn.sendall(str.encode(message))
    return

def receiveMessage(conn):
    # Read the header bytes, which will tell us the length of the payload.
    payloadLen = int(conn.recv(HDR_LEN))
    payload = ""
    # Receive the payload
    while (payloadLen>0):
        payloadBytes = conn.recv(1024)
        payloadLen -= len(payloadBytes)
        payload = payload + payloadBytes.decode('utf-8')

    return payload
    
# Generates the payload JSON.
def getRTData():
    rtData = mccInterface.readAllMCC()
    rtJson = json.dumps(rtData)
    print(rtJson)
    return rtJson


def threaded_server():    
    global skt
    while True:
        # Block to accept commands from the dipClient
        conn, address = skt.accept()
        clientMsg = receiveMessage(conn)
        if not clientMsg:
            print("Breaking out of thread .... due missing client message")
            break
        message = str(clientMsg)
        messageHandler(message, conn)

    skt.close()
    conn.close()
    return
   
   
# Handles messages from the dip Client
def messageHandler(message, conn):
    if (message=="RT"):
        rtJson = getRTData()
        sendMessage(rtJson, conn)
    elif (message=="AI"):
        pass
    else:
        sendMessage("{ \"Error\":\"Unknown request\"}", conn)

    return
    
    
    
    


