from helpers.printer import print_status
from simulators.fourSD import run_fourSD_simulator
from value_queue import value_queue
import time
import threading

def fourSD_callback(code, settings, status):
    print_status(code, status)
    val = {
        "measurementName": "fourSDStatus",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": code,
        "deviceType": "4SD",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]

    }
    value_queue.put(val)

def run(code, settings, threads, stop_event):
    if settings['simulated']:
        fourSD_thread = threading.Thread(target=run_fourSD_simulator,
                                         args=(lambda status: fourSD_callback(code, settings, status),stop_event))
        fourSD_thread.start()
        threads.append(fourSD_thread)
    else:
        from actuators.fourSD import fourSD_register
        fourSD_thread = threading.Thread(target=fourSD_register, args=(settings["pins"], stop_event))
        fourSD_thread.start()
        threads.append(fourSD_thread)