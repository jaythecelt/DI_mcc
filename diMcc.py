import json
import dipServer
import humiditySensor

try:
    print("Starting new server thread")
    dipServer.startServer()

    
    while True:
        pass


except KeyboardInterrupt:
    print("Exiting")

except Exception as e:
    print("Exception in main loop", str(e))
    
finally:
    print("Shutting down the MCC Data Injector!.")
    humiditySensor.cleanup()
    


        



        
