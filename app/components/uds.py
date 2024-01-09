import threading
import time

from helpers.printer import print_status
from simulators.uds import run_uds_simulator
from value_queue import value_queue


def uds_callback(code, settings, distance):
    print_status(code, f'DISTANCE: {distance} cm')
    val = {
        "measurementName": "UDSDistance",
        "timestamp": round(time.time()*1000),
        "value": distance,
        "deviceId": code,
        "deviceType": "UDS",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)


def run_uds(code, settings, threads, stop_event):
    if settings['simulated']:
        uds_thread = threading.Thread(target=run_uds_simulator,
                                      args=(lambda distance: uds_callback(code, settings, distance), stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
    else:
        from sensors.uds import run_uds_loop
        uds_thread = threading.Thread(target=run_uds_loop,
                                      args=(settings["pins"], lambda distance: uds_callback(code, settings, distance),
                                            stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
