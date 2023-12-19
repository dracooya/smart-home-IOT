import time
import random


def run_uds_simulator(uds_code, callback, stop_event, delay):
    while True:
        time.sleep(delay)
        callback(uds_code, random.randint(0, 100))
        if stop_event.is_set():
            break
