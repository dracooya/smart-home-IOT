import threading
import time

from helpers.printer import print_status
from value_queue import value_queue


def callback(code, settings, key):
    print_status(code, f"Key pressed: {key}")
    val = {
        "measurementName": "keypadInput",
        "timestamp": round(time.time()*1000),
        "value": key,
        "deviceId": code,
        "deviceType": "DMS",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val)


def run(code, settings, threads, stop_event):
    if settings['simulated']:
        from simulators.dms import simulate
        thread = threading.Thread(target=simulate, args=(lambda key: callback(code, settings, key), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dms import register
        thread = threading.Thread(target=register, args=(settings["pins"], lambda key: callback(code, settings, key)))
        thread.start()
        threads.append(thread)
