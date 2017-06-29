import json
import dipServer

try:
    print("Starting new server thread")
    dipServer.startServer()

    
    while True:
        pass
    
except Exception as e:
    print("Exception in main loop", str(e))


print("Shutting down the MCC Data Injector!.")
        
