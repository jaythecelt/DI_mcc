'''
    Interface to the MCC USB2408 or USB2408-2AO and other sensors.  Also digital outputs and analog outputs.
    
    This module reads data from all of the sensors, including the ones wired to the MCC USB2408.
    
    TODO:  This module could use a rewrite to separate the MCC functions from the other sensors.  Technically this
    module is for all sensors, not just the MCC.
    
    
    readAllMCC() is the primary function for reading the sensors.  It reads all of the sensors as defined in the 
    mccConfigData module and detects any real time events (also as configured).
    
    Reading sensors:
        - Reads sensor data from the MCC box
        - Since the humidity sensor is sampled over a period of time, and the reading is not available with each readAllMCC()
          invocation, the sensor reading is pulled from the counterQueue (also a candidate for refactoring).  If no new reading
          is available in the counterQueue, the latest value is sent.
        - All sensor data is 'time stampped' using the elapsed time from the FormulaTimer class.  If
          this timer is not running, the time stamp is 0.
        - The 'time stamp' or 'formula time' is marked immediately after the sensor data is read to provide the time 
          as close as practical to the reading of the value. 
          
          
    Communicating results:
        - Sensor data is compiled into a Python dictionary and returned by readAllMCC().  This dictionary can be converted
          directly to json by the caller if desired.
        - As real time events are detected by readAllMCC(), the event json is placed into a separate real time event queue so that it
          is available for immediate processing, independent of the sensor data returned by readAllMCC().


    digitialOut(label, value) sets the digital output on the MCC that corresponds to the label parameter.  value is a boolean where
    True is a logical 1 and False is a logical 0.
    
    TODO:  Throw a custom excpetion when the label is no defined in the config data.




'''
import time

from mcc_libusb import mcc2408Module
from HtpLogger import HtpLogger
from FormulaTimer import FormulaTimer
from RTEvent import RTEvent
from RTEventQueue import RTEventQueue

from mccConfigData import *
import counterQueue



VAL_KEY = "value"
UNITS_KEY = "units"
FORMULA_TIME_KEY = "formulaTime"

prevData = {}  #Dictionary that holds raw data from the last loop.

initialized = False

def initMCC():
    global initialized
    #TODO Try/catch
    HtpLogger.get().info(mcc2408Module.version())
    mcc2408Module.init()

    ### Init the MCC's channels per config data ###
    # Thermocouples
    for k, v in tcConfig.items():
        mcc2408Module.setTCConfig(v[0], v[1], v[2], ord(v[3]))

    ### Digital Inputs
    for k, v in digInConfig.items():
        mcc2408Module.setDIConfig(v[0], v[1], v[2])
        
    ### Digital Outputs
    for k, v in digOutConfig.items():
        mcc2408Module.setDOConfig(v[0], v[1], v[2])

    ### Analog Inputs
    for k, v in analogInConfig.items():
        mcc2408Module.setAIConfig(v[0], v[1], v[2], v[3], v[4])

    ### Analog Outputs
    for k, v in analogOutConfig.items():
        mcc2408Module.setAOConfig(v[0], v[1])

    ### Counters
    for k, v in counterConfig.items():
        mcc2408Module.setCntrConfig(v[0], v[1])
    
    
    ctrQ = counterQueue.CounterDataQueue()
    ctrQ.setSupressQueueFullWarning(True)

    initialized = True
    HtpLogger.get().info("MCC Completed Initialization")

    return


def isMCCInitialized():
    global initialized
    
    return initialized


'''
Get the real time sensor data, based on the configuration data.
'''

'''
    "Reads all the data on the MCC and returns the json dictionary"
'''
def readAllMCC():
    if not isMCCInitialized():
        HtpLogger.get().critical("mccInterface module not initialized!")
        return
    
    # Note: does *not* read the counter values #

    # Dictionaries to hold data
    rtData = {} # all data elements
    tcData = {} # thermocouple data
    aiData = {} # analog input data
    diData = {} # digital input data
    ctrData = {}# counter data
    ft = FormulaTimer()

    # Thermocouples
    for k, v in tcConfig.items():
        j = mcc2408Module.readTCChannel(v[0])
        j = round(j, 2)
        data = { VAL_KEY : j, UNITS_KEY : v[3], FORMULA_TIME_KEY : ft.getElapsedTime() }
        tcData[k] = data
        prevData[k] = j

    # Analog Inputs
    for k, v in analogInConfig.items():
        j = mcc2408Module.readAIChannel(v[0])
        j = round(j, 6)
        data = { VAL_KEY : j, UNITS_KEY : VOLTS, FORMULA_TIME_KEY : ft.getElapsedTime() }
        aiData[k] = data
        prevData[k] = j

    # Digital Inputs
    for k, v in digInConfig.items():
        j = mcc2408Module.readDIChannel(v[0])
        timeMark = ft.getElapsedTime()

        if k not in prevData:  # If prevData has not been populated yet ... set the prev value to the current value.
            prevData[k] = j

        testForEvent = v[3]
        if testForEvent:
            rteJson = RTEvent().submit(DIGITAL_INPUT_DATA_KEY, k, prevData[k], j, v[4], timeMark)
            if (rteJson is not None):
                rteq = RTEventQueue()
                rteq.put(rteJson)
        data = { VAL_KEY : j, FORMULA_TIME_KEY :  timeMark}
        diData[k] = data
        prevData[k] = j   # Rewrite previous data with the current value

    # Counter Inputs
    # From the counterQueue ... i.e. the humidity sensor
    # TODO This should be cleaned up.
    ctrQ = counterQueue.CounterDataQueue()
    ctrArray = [None, None]
    while not ctrQ.isEmpty():
        ctrTuple = ctrQ.get()  #  Returns a tuple with index, value
        if ctrTuple[1] is not None:
            ix = ctrTuple[0]
            val = ctrTuple[1]
            ctrArray[ix] = val

    for k,v in counterConfig.items():
        ctrData[k] = { VAL_KEY : ctrArray[v[0]], FORMULA_TIME_KEY : ft.getElapsedTime() }
        prevData[k] = ctrArray[v[0]]
    
    if len(tcData)>0:
        rtData['TC'] = tcData
    if len(aiData)>0:
        rtData['AI'] = aiData
    if len(diData)>0:
        rtData['DI'] = diData

#Humidity Sensor Data is in the counter Queue ... TODO: fix this on the rewrite.
    if len(ctrData)>0:
        rtData['HM'] = ctrData

    return rtData



'''
    Sets a single digital output that corresponds to <label> to <value>.
    <value> is a boolean where True == logical 1 and False == logical 0.
    Critical error when:
        - <label> is not found in the config data.
        - MCC was not initialized
'''
def digitalOut(label, bval):
    if (not isMCCInitialized()):
        HtpLogger.get().critical("mccInterface module not initialized!")
        return
    if (label not in digOutConfig):
        HtpLogger.get().critical("digitalOut(...) label parameter <{0}> not defined in the config data".format(label))
        return
    
    channel = (digOutConfig[label])[0]
    mcc2408Module.writeDOChannel(channel, bval);
    

def p2():
    tt = 0
    while True:
        tt = tt + 0.001
        digitalOut('DO0', True)
        time.sleep(tt)
        digitalOut('DO0', False)
        time.sleep(tt)
    
        digitalOut('DO1', True)
        time.sleep(tt)
        digitalOut('DO1', False)
        time.sleep(tt)
    
        digitalOut('DO2', True)
        time.sleep(tt)
        digitalOut('DO2', False)
        time.sleep(tt)
    
    