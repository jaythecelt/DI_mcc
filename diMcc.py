from HtpLogger import HtpLogger

# Setup logger
logPrefix = "diMcc"
log = HtpLogger(logPrefix, HtpLogger.DEBUG, HtpLogger.INFO)

import dipServer


def main():

    try:
        log.info("Starting new server thread")
        dipServer.startServer()

        
        while True:
            pass


    except KeyboardInterrupt:
        dipServer.stopServer()
        log.info("Exiting")

    except Exception as e:
        log.error("Exception in main loop: {0}".format(e))
        
    finally:
        log.info("Shutting down the MCC Data Injector!.")

    

main()
        



        
