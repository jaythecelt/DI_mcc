'''
Counter Data Queue

The class is designed as a Singleton
'''
from HtpLogger import HtpLogger
import queue

QUEUE_MAX_SIZE = 10
QUEUE_PUT_TIMEOUT = 0.002
QUEUE_GET_TIMEOUT = 0.002

class CounterDataQueue:
    instance = None
    
    def __init__(self):
        if not CounterDataQueue.instance:
            CounterDataQueue.instance = CounterDataQueue.__CounterDataQueue()

    # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)


    # Inner class for the singlton implementation.
    # Method implementations go here.
    class __CounterDataQueue:
        cntrQ = None
        log = None
        
        def __init__(self):
            self.log = HtpLogger.get()
            self.cntrQ = queue.Queue(maxsize=QUEUE_MAX_SIZE)
   
        def __str__(self):
            return repr(self)
        
        def put(self, v):
            try:
                self.cntrQ.put(v, True, QUEUE_PUT_TIMEOUT)
            except (queue.Full):
                self.log.warning("Counter Data Queue is full, value dropped: " + str(v))
                return
                
        def get(self):
            try:
                rtn = self.cntrQ.get(True, QUEUE_GET_TIMEOUT)
            except (queue.Empty):
                rtn = None
            return rtn

        def isEmpty(self):
            return self.cntrQ.empty()

            