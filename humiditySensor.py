import sched, time
from _thread import *
import RPi.GPIO as GPIO
import counterQueue

UPDATE_PERIOD = 1  # In seconds
PRIORITY = 1


rstPin = 6
latchPin = 13
clkPin = 19
dataPin = 26
H = GPIO.HIGH
L = GPIO.LOW




def startHumThread():
    global curEvent
    global humSched
    
    initGPIO()
    humSched = sched.scheduler(time.time, time.sleep)
    curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, humDataHandler)
    start_new_thread(humThread, ())
    return 

def initGPIO():
    global startTime
    global endTime

    startTime = 0
    endTime = 1

    
    # Pin definitions
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rstPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(dataPin, GPIO.IN)



def cleanup():    
    GPIO.cleanup()
    
    
    
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
    

def resetAndStartCounter():
    global startTime
    
    #Reset counter
    GPIO.output(latchPin, H)  # Be sure counter is not latched
    GPIO.output(rstPin, H)
    time.sleep(0.000100)
    #Start counter
    GPIO.output(rstPin, L)
    startTime = time.time()
    return
    
def readCounter():
    global endTime
    
    #Latch counter data
    GPIO.output(latchPin, L)
    endTime = time.time()
    GPIO.output(latchPin, H)     
    GPIO.output(rstPin, H)
   
    #Shift data out from register
    shift = 23
    val = 0
    for i in range(0,24):
        #Drop the clk signal
        GPIO.output(clkPin, L)
        k = GPIO.input(dataPin)
        val = val | (k << shift)
        shift = shift - 1
        GPIO.output(clkPin, H) #Raise the clock
    return val
    
def humDataHandler(a = 'default'):
    #TODO: Add error handling
    global curEvent
    global humSched
    global startTime
    global endTime
    
    # Schedule new event, if still running
    if (scheduleRunning): # Check prevents race condition
        curEvent = humSched.enter(UPDATE_PERIOD,  PRIORITY, humDataHandler)

    #Read the sensor (which was started last time this callback was called)    
    ctrQ = counterQueue.CounterDataQueue()
    count = readCounter()
    sampleTime = endTime - startTime  # Actual sample time in seconds
    c = count
    count = int(float(count)/sampleTime)
    print("Count: ", c, " ", count, "  sample: ", sampleTime)    
    ctrQ.put((0,count))

    # Start the counter for the next time
    resetAndStartCounter()
    return    

    
    
    