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


def run(code, settings, threads, stop_event, lcd_change_event):
    if settings['simulated']:
        from simulators.lcd import simulate
        thread = threading.Thread(target=simulate, args=(lambda val: callback(code, settings, val), stop_event,
                                                         lcd_change_event))
        thread.start()
        threads.append(thread)
    else:
        from actuators.lcd.lcd import register
        thread = threading.Thread(target=register, args=(settings["pins"], lambda val: callback(code, settings, val),
                                                         lcd_change_event))
        thread.start()
        threads.append(thread)
