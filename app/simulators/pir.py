import time
import random


def simulate(motion_callback, no_motion_callback, stop_event):
    while True:
        if stop_event.is_set():
            break
        time.sleep(random.randint(2, 25))
        while True:
            if stop_event.is_set():
                break
            motion_callback()
            time.sleep(2)
            if random.randint(1, 3) == 1:
                no_motion_callback()
                break
