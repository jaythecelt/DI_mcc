'''
    Unit test for the mmcInterface

'''
import sys
sys.path.append('/home/pi/DI_mcc')  # Add the application folder to the path
import threading
from _thread import *
import time
from HtpLogger import HtpLogger
from MCCTask import MCCTask
from RTDataQueue import RTDataQueue
from RTEventQueue import RTEventQueue
from RTEventMonitor import RTEventMonitor
from FormulaTimer import FormulaTimer



def main():
    # Start the MCC task running in a thread ... this gets data from the MCC
    mccTask = MCCTask()
    t = threading.Thread(target=mccTask.run, args=())
    t.start()
    
    rtem = RTEventMonitor()
    tt = threading.Thread(target=rtem.run, args=())
    tt.start()
    
    
    start_new_thread(_eventMonitor, ())
    
    rtQueue = RTDataQueue()
    ft = FormulaTimer()
    ft.start()
    try:
        while True:
            mccTask.queueIt()
            time.sleep(5.0) #  time delay before reading queue ... expect one entry in the queue
            cc=1
            while not rtQueue.isEmpty():
                json = rtQueue.get()
                print ("<<{1}>>{0}".format(json, cc))
                cc = cc + 1
        

        HtpLogger.get().warning("while True loop in main exited.")

    except KeyboardInterrupt:
        HtpLogger.get().info ("Exiting")

    finally:
        mccTask.terminate()
        rtem.terminate()

if __name__ == "__main__":
    logPrefix = "mccInterface_test"
    log = HtpLogger(logPrefix, HtpLogger.DEBUG, HtpLogger.DEBUG)
    main()