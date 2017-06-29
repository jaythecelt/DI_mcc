'''
Interface to the MCC 2408-2AO

'''
import json
import time

from mcc_libusb import mcc2408Module

from mccConfigData import *


def initMCC():
    #TODO Try/catch
    
    print(mcc2408Module.version())
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


    return



'''
Get the real time sensor data, based on the configuration data.
'''

'''
    "Reads all the data on the MCC and returns the json dictionary"
'''

def readAllMCC():

    # Dictionaries to hold data
    rtData = {} # all data elements
    tcData = {} # thermocouple data
    aiData = {} # analog input data
    diData = {} # digital input data

    # Thermocouples
    for k, v in tcConfig.items():
        j = mcc2408Module.readTCChannel(v[0])
        tcData[k] = j, v[3]

    # Analog Inputs
    for k, v in analogInConfig.items():
        j = mcc2408Module.readAIChannel(v[0])
        aiData[k] = j, VOLTS

    # Digital Inputs
    for k, v in digInConfig.items():
        j = mcc2408Module.readDIChannel(v[0])
        diData[k] = j

    rtData['TC'] = tcData
    rtData['AI'] = aiData
    rtData['DI'] = diData
   
    return rtData

    

