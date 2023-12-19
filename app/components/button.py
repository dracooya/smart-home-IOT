import threading
import time
from helpers.printer import print_status
from simulators.button import run_button_simulator
from value_queue import value_queue;

button_id = ""
button_settings = {}

def button_callback(button_code):
    print_status(button_code, "PRESSED")
    val = {
        "measurementName": "buttonStatus",
        "timestamp": round(time.time()*1000),
        "value": "PRESSED",
        "deviceId": button_id,
        "deviceType": "BUTTON",
        "isSimulated": button_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def run_button(id,settings, threads, button_code, stop_event):
    global button_id, button_settings
    button_id = id
    button_settings = settings
    if settings['simulated']:
        button_thread = threading.Thread(target=run_button_simulator, args=(button_callback, button_code, stop_event))
        button_thread.start()
        threads.append(button_thread)
    else:
        from sensors.button import button_register
        button_thread = threading.Thread(target=button_register,
                                         args=(settings["pins"][0], lambda x: button_callback(button_code)))
        button_thread.start()
        threads.append(button_thread)
