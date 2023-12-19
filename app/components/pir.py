import threading
from helpers.printer import print_status
import time
from value_queue import value_queue
import json

pir_id = ""
pir_settings = {}

def motion(code):
    print_status(code, "MOTION DETECTED")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "MOTION",
        "deviceId": pir_id,
        "deviceType": "PIR",
        "isSimulated": pir_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def no_motion(code):
    print_status(code, "NO MOTION")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "NO-MOTION",
        "deviceId": pir_id,
        "deviceType": "PIR",
        "isSimulated": pir_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def run(id, settings, threads, code, stop_event):
    global pir_id, pir_settings
    pir_id = id
    pir_settings = settings
    if settings['simulated']:
        from simulators.pir import simulate
        thread = threading.Thread(target=simulate,
                                  args=(lambda: motion(code), lambda: no_motion(code), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.pir import register
        thread = threading.Thread(target=register,
                                  args=(settings["pins"][0], lambda: motion(code), lambda: no_motion(code)))
        thread.start()
        threads.append(thread)
