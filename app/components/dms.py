import threading
from helpers.printer import print_status
import time
from value_queue import value_queue
import json

dms_id = ""
dms_settings = {}


def callback(code, key):
    print_status(code, f"Key pressed: {key}")
    val = {
        "measurementName": "keypadInput",
        "timestamp": round(time.time()*1000),
        "value": key,
        "deviceId": dms_id,
        "deviceType": "DMS",
        "isSimulated": dms_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def run(id, settings, threads, code, stop_event):
    global dms_id, dms_settings
    dms_id = id
    dms_settings = settings
    if settings['simulated']:
        from simulators.dms import simulate
        thread = threading.Thread(target=simulate, args=(lambda x: callback(code, x), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dms import register
        thread = threading.Thread(target=register, args=(settings["pins"], lambda x: callback(code, x)))
        thread.start()
        threads.append(thread)
