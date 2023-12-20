import time
import random


def run_uds_simulator(callback, stop_event, delay):
    while True:
        time.sleep(delay)
        callback(random.randint(0, 100))
        if stop_event.is_set():
            break
