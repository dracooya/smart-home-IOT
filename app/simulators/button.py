import time
import random


def run_button_simulator(callback, stop_event):
    while True:
        time.sleep(random.randint(15, 30))
        callback()
        if stop_event.is_set():
            break
