import time
import random


def simulate(callback, stop_event):
    while True:
        if stop_event.is_set():
            break
        time.sleep(random.randint(2, 20))
        for i in range(4):
            if stop_event.is_set():
                break
            callback(str(random.randint(0, 9)))
            time.sleep(1)
        callback("#")
