import sched, time
from _thread import *
import RPi.GPIO as GPIO
import counterQueue
from HtpLogger import HtpLogger

UPDATE_PERIOD = 0.994  # In seconds
PRIORITY = 1

latchPin = 13
clkPin = 19
dataPin = 26
H = GPIO.HIGH
L = GPIO.LOW

log = HtpLogger.get()

saveStartTime = 0

# Public 
def startHumThread():
    global curEvent
    global humSched
    
    _initGPIO()
    log.debug("Start humiditySensor")
    humSched = sched.scheduler(time.time, time.sleep)
    curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, _humDataHandler)
    start_new_thread(_humThread, ())
    return 

# Public 
# Call to shutdown GPIO
def cleanup():    
    log.debug("Cleanup humiditySensor")
    GPIO.cleanup()
    
    
def _initGPIO():
    global startTime
    global endTime

    startTime = 0
    endTime = 1

    
    # Pin definitions
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(dataPin, GPIO.IN)



    
def  _humThread():
    #TODO: Add error handling
    global humSched
    global scheduleRunning

    scheduleRunning = True
    #Blocks while the schedule is running
    humSched.run()
    scheduleRunning = False
    log.warn("humThread stopped")
    return
    
   
'''
    Callback for the scheduler
'''
def _humDataHandler(a = 'default'):
    #TODO: Add error handling
    global curEvent
    global humSched
    global saveStartTime
    
    # Schedule new event, if still running
    if (scheduleRunning): # Check prevents race condition
        curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, _humDataHandler)

    # Latch counter data
    GPIO.output(latchPin, L)
    endTime = time.time()
    startTime = saveStartTime  # get the start time from the last time the handler was called

    # Restart the counter and get the start time
    #  i.e. start the new count
    GPIO.output(latchPin, H)     
    saveStartTime = time.time()    
   
    # Shift previous, latched data out from register
    shift = 23
    count = 0
    for i in range(0,24):
        #Drop the clk signal
        GPIO.output(clkPin, L)  # Clock pin to L
        k = GPIO.input(dataPin) # Read the bit
        count = count | (k << shift)
        shift = shift - 1
        GPIO.output(clkPin, H)  # Clock pin to H

    rawCount = count
    sampleTime = endTime - startTime  # Actual sample time in seconds
    count = int(float(count)/sampleTime)  # Filter to compensate for variations in the sample period.

    diff = rawCount - count
    log.debug("Count = %d  \t sample time = %f \t diff = %d", count, sampleTime, diff)
    
    ctrQ = counterQueue.CounterDataQueue() # get the counter data queue
    ctrQ.put((0,count))
   
    