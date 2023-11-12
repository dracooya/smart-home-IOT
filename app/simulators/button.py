import time
import random

def run_button_simulator(callback, button_code, stop_event):
        while True:
            time.sleep(random.randint(2,100))
            callback(button_code)
            if stop_event.is_set():
                  break