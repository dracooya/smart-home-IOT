import threading
import time

from helpers.printer import print_status
from simulators.uds import run_uds_simulator
from value_queue import value_queue


last_distance = -1
second_last_distance = -1


def uds_callback(code, settings, distance):
    print_status(code, f'DISTANCE: {distance} cm')
    val = {
        "measurementName": "UDSDistance",
        "timestamp": round(time.time()*1000),
        "value": distance,
        "deviceId": code,
        "deviceType": "UDS",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val)
    global last_distance
    global second_last_distance
    second_last_distance = last_distance
    last_distance = distance


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
