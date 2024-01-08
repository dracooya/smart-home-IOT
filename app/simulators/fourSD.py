import time

def run_fourSD_simulator(callback_fc, stop_event):
    while True:
        current_time = time.strftime("%H:%M", time.localtime())
        callback_fc("Current time: " + current_time)
        time.sleep(10)
        if stop_event.is_set():
            break