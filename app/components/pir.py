import threading
import time

from helpers.printer import print_status
from value_queue import value_queue


def motion(code, settings):
    print_status(code, "MOTION DETECTED")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "MOTION",
        "deviceId": code,
        "deviceType": "PIR",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)


def no_motion(code, settings):
    print_status(code, "NO MOTION")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "NO-MOTION",
        "deviceId": code,
        "deviceType": "PIR",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)


def run(code, settings, threads, stop_event):
    if settings['simulated']:
        from simulators.pir import simulate
        thread = threading.Thread(target=simulate,
                                  args=(lambda: motion(code, settings), lambda: no_motion(code, settings), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.pir import register
        thread = threading.Thread(target=register,
                                  args=(settings["pins"][0], lambda: motion(code, settings),
                                        lambda: no_motion(code, settings)))
        thread.start()
        threads.append(thread)
