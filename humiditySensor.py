import sched, time
from _thread import *

from mcc_libusb import mcc2408Module
import counterQueue

from random import randint 
import time


UPDATE_PERIOD = 1  # In seconds
PRIORITY = 1


def startHumThread():
    global curEvent
    global humSched
    
    humSched = sched.scheduler(time.time, time.sleep)
    curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, humDataHandler)
    start_new_thread(humThread, ())
    return 

    
def  humThread():
    #TODO: Add error handling
    global humSched
    global scheduleRunning

    scheduleRunning = True
    #Blocks while the schedule is running
    humSched.run()
    scheduleRunning = False
    print("humThread stopped")
    return
    
    
def testCounter0():
    for i in range(0,3):
        mcc2408Module.writeDOChannel(0, 0)
        mcc2408Module.writeDOChannel(0, 1)    
    
    
def humDataHandler(a = 'default'):
    #TODO: Add error handling
    global curEvent
    global humSched

    # Schedule new event, if still running
    if (scheduleRunning): # Check prevents race condition
        curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, humDataHandler)

    #Read the sensor (which was started last time this callback was called)    
    ctrQ = counterQueue.CounterDataQueue()
    count = mcc2408Module.readCntrChannel(0)    
    ctrQ.put((0,count))
    count = mcc2408Module.readCntrChannel(1)    
    ctrQ.put((1,count))

    # Start the counter for the next time
    mcc2408Module.startCntrChannel(0)
    mcc2408Module.startCntrChannel(1)

    return    
