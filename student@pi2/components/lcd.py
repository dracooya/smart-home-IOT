import threading
import time

from helpers.printer import print_status
from value_queue import value_queue


def callback(code, settings, message):
    print_status(code, f"Message received: {message}")
    val = {
        "measurementName": "lcd",
        "timestamp": round(time.time() * 1000),
        "value": message,
        "deviceId": code,
        "deviceType": "LCD",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)


def run(code, settings, threads, stop_event):
    if settings['simulated']:
        from simulators.lcd import simulate
        thread = threading.Thread(target=simulate, args=(code, lambda val: callback(code, settings, val), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from actuators.lcd.lcd import register
        thread = threading.Thread(target=register, args=(code, settings["pins"], lambda val: callback(code, settings, val)))
        thread.start()
        threads.append(thread)
