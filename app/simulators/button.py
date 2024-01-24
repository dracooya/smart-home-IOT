import time
import random



def run_button_simulator(callback, long_press_callback, release_callback, stop_event):
    while True:
        time.sleep(random.randint(2, 20))
        callback_choice = random.randint(0,1)
        if callback_choice == 0:
            callback(time.time() * 1000)
        else:
            print("AYOOOO CLOSE THE FUCKING DOOR CHIEF PROMAJA")
            long_press_callback()
            time.sleep(random.randint(2,8))
            release_callback()
        if stop_event.is_set():
            break
