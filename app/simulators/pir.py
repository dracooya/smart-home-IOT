import time
import random


def simulate(motion_callback, stop_event):
    while True:
        if stop_event.is_set():
            break
        time.sleep(random.randint(2, 30))
        motion_callback()
