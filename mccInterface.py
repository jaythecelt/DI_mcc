'''
Interface to the MCC 2408-2AO

'''
import time

from mcc_libusb import mcc2408Module
from HtpLogger import HtpLogger
from FormulaTimer import FormulaTimer

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
        HtpLogger.get().error("mccInterface module not initialized!")
    
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

        if k not in prevData:  # If prevDict has not been populated yet ... set the prev value to the current value.
            prevData[k] = j

        testForEvent = v[3]
        if testForEvent:
            RTEvent().submit(DIGITAL_INPUT_DATA_KEY, k, prevData[k], j, v[4], timeMark)
        
        data = { VAL_KEY : j, FORMULA_TIME_KEY :  timeMark}
        diData[k] = data
        prevData[k] = j

    # Counter Inputs
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

    
    