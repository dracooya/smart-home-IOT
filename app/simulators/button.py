import time
import random


def run_button_simulator(callback, stop_event):
    while True:
        time.sleep(random.randint(2, 10))
        callback()
        if stop_event.is_set():
            break
