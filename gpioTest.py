'''
    This is a test script used to work out the interface to the humidity sensor.
    This is not the module used in applications, but a simplified script intended
    to be used for development and testing.

'''

import RPi.GPIO as GPIO
import time
from HtpLogger import HtpLogger




'''
    Reads the sensor by manipulating the 'latchPin' GPIO to reset 
    and latch the counter.
    
    Also toggles the 'clkPin' GPIO to shift the sensor data from the 
    register one bit at a time ('dataPin'). Shifts 24 bits from the register
    MSB to LSB order.
    
'''
def readHSensor():
    global latchPin, clkPin, dataPin
    global H, L
    global log

    # == Reset counter ==
#    GPIO.output(latchPin, L)     # The latchPin is high when entering this method.
                                 #    this statement sets it low to reset the counter.
#    time.sleep(0.000010)         # Short delay (not sure if needed)

    # == Start counter ==
#    GPIO.output(latchPin, H)
    startTime = time.time()

    # Wait 1 sec
    time.sleep(1)

    # == Latch counter data ==
    endTime = time.time()
    GPIO.output(latchPin, L)     # Latch counter data to register
    time.sleep(0.000010)         # Short delay (not sure if needed)

    # Raise latchPin to read register
    #  This is needed since the register can't be read while the latchPin is low(???)
    GPIO.output(latchPin, H)     

    # == Shift data out from register ==
    #  Shifts left since the register is MSB first
    shift = 23
    val = 0
    for i in range(0,24):
        GPIO.output(clkPin, L)    # Drop the clk signal
        k = GPIO.input(dataPin)
        val = val | (k << shift)  # Shift 'k' to the left 'shift' times and OR with previous 'val'
        shift = shift - 1         # Decrement 'shift' 
        GPIO.output(clkPin, H)    # Raise the clk signal

    # == Normalize val to 1.000000 sec sample time ==
#    sampleTime = endTime - startTime  # Actual sample time in seconds
#    val = int(float(val)/sampleTime)  # Filter to compensate for variations in the sample period.
    
    log.info("val: " + str(val))
    

    
    
def readHSensor2():
    global latchPin, clkPin, dataPin
    global H, L
    global log

    # == Latch counter data ==
    GPIO.output(latchPin, L)     # Latch counter data to register
    GPIO.output(latchPin, H)     

    # == Shift garbage data out from register ==
    shift = 23
    val = 0
    for i in range(0,24):
        GPIO.output(clkPin, L)    # Drop the clk signal
        k = GPIO.input(dataPin)
        val = val | (k << shift)  # Shift 'k' to the left 'shift' times and OR with previous 'val'
        shift = shift - 1         # Decrement 'shift' 
        GPIO.output(clkPin, H)    # Raise the clk signal

    time.sleep(1)
    
    # == Latch counter data ==
    GPIO.output(latchPin, L)     # Latch counter data to register
    GPIO.output(latchPin, H)     

    # read previous value
    shift = 23
    val = 0
    for i in range(0,24):
        GPIO.output(clkPin, L)    # Drop the clk signal
        k = GPIO.input(dataPin)
        val = val | (k << shift)  # Shift 'k' to the left 'shift' times and OR with previous 'val'
        shift = shift - 1         # Decrement 'shift' 
        GPIO.output(clkPin, H)    # Raise the clk signal
        
    log.info("val: " + str(val))
    
    
    
    
    
    
    
'''
    Main method that initialized the GPIO and enters an infinte loop to
    call readHSensor().
    
    Cleans up the GPIO on exit.
'''    
def main():    
    global rstPin, latchPin, clkPin, dataPin
    global H, L
    global log

    # Pin definitions
    rstPin   = 6
    latchPin = 13
    clkPin   = 19
    dataPin  = 26
    H = GPIO.HIGH
    L = GPIO.LOW

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(26, GPIO.IN)

    # Setup logger
    
    log = HtpLogger("gpioTest", logging.DEBUG, logging.DEBUG)
    
    
    # Notes about this version
    log.info("\n\n== Note: has changes to debug the counter discrepencies noted in testing. ==\n\n")
    log.info("\nHighlights: \n\t- 'one shot' mode where it take one reading at a time.\n\n")

    try:
        while True:
            input("Press Enter to take a reading...")
            readHSensor2()

    except KeyboardInterrupt:
        log.info("Exiting")
        GPIO.cleanup()

    finally:
        GPIO.cleanup()
    
    
if __name__ == "__main__":
    main()



    
