import time
import random


def simulate(callback, stop_event):
    while True:
        if stop_event.is_set():
            break
        if random.randint(0, 300) == 0:
            callback("MOTION")
        time.sleep(0.1)
