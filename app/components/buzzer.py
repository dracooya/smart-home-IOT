import threading
from simulators.buzzer import run_buzzer_simulator
from helpers.printer import print_status
import time
from value_queue import value_queue
import json

buzzer_id = ""
buzzer_settings = {}

def buzzer_callback(status):
    print_status("DB", status)
    val = {
        "measurementName": "buzzerStatus",
        "timestamp": round(time.time()*1000),
        "value": status,
        "deviceId": buzzer_id,
        "deviceType": "BUZZER",
        "isSimulated": buzzer_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def run_buzzer(id, settings, threads, buzzer_press_event, buzzer_release_event, stop_event):
    global buzzer_id, buzzer_settings
    buzzer_id = id
    buzzer_settings = settings
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=run_buzzer_simulator,
                                         args=(buzzer_callback, buzzer_press_event, buzzer_release_event, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import buzzer_register
        buzzer_thread = threading.Thread(target=buzzer_register, args=(
        settings["pins"][0], 400, buzzer_callback, buzzer_press_event, buzzer_release_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
