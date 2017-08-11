from HtpLogger import HtpLogger

# Setup logger
logPrefix = "diMcc"
log = HtpLogger(logPrefix, HtpLogger.DEBUG, HtpLogger.DEBUG)

import json
import dipServer
import humiditySensor



def main():

    try:
        log.info("Starting new server thread")
        dipServer.startServer()

        
        while True:
            pass


    except KeyboardInterrupt:
        log.info("Exiting")

    except Exception as e:
        log.error("Exception in main loop", str(e))
        
    finally:
        log.info("Shutting down the MCC Data Injector!.")
        humiditySensor.cleanup()
    

main()
        



        
