import time
import random

ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3",  "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0", "#"] 

def simulate(stop_event, client):
    while True:
        if stop_event.is_set():
            client.disconnect()
            break
        #time.sleep(random.randint(10, 100))
        #for _ in range(random.randint(1, 5)):
        #    key = ButtonsNames[random.randint(0,16)]
        #    callback(key)
        #    time.sleep(1)