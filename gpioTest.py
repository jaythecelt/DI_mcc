import threading
import RPi.GPIO as GPIO
import time



def toggleClk():
    GPIO.output(clkPin, L)
    time.sleep(0.000010)
    GPIO.output(clkPin, H)
    time.sleep(0.000010)



def readHSensor():
    print("Read Humidity Sensor")
    #Reset counter
    GPIO.output(latchPin, L)
    GPIO.output(rstPin, L)
    time.sleep(0.000010)
    GPIO.output(latchPin, H)  # Be sure counter is not latched
    GPIO.output(rstPin, H)
    #Start counter
    startTime = time.time()

    #Wait 1 sec
    time.sleep(1)
    #Latch counter data
    endTime = time.time()
    GPIO.output(latchPin, L)
    GPIO.output(rstPin, L)
    time.sleep(0.000010)
    GPIO.output(latchPin, H)     
    GPIO.output(rstPin, H)

    
    #Shift data out from register
    shift = 23
    val = 0
    for i in range(0,24):
        #Drop the clk signal
        GPIO.output(clkPin, L)
        #threading.Thread(target=toggleClk ).start()
        k = GPIO.input(dataPin)
        val = val | (k << shift)
        shift = shift - 1
        GPIO.output(clkPin, H) #Raise the clock
#        time.sleep(0.000001) #small delay


    sampleTime = endTime - startTime  # Actual sample time in seconds
    val = int(float(val)/sampleTime)  # Filter to compensate for variations in the sample period.
    

    
    print("Value read is: ", val, " Elapsed sec: ", endTime - startTime)

            
        






# Pin definitions
rstPin = 6
latchPin = 13
clkPin = 19
dataPin = 26
H = GPIO.HIGH
L = GPIO.LOW

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

print("Version with filter/removed rst/latch timing changes")

try:

    while True:
        readHSensor()

except KeyboardInterrupt:
    print("Exiting")

finally:
    GPIO.cleanup()
    
