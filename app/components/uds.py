import threading

from helpers.printer import print_status
from simulators.uds import run_uds_simulator
import time
from value_queue import value_queue
import json

uds_id = ""
uds_settings = {}


def uds_callback(uds_code, distance):
    print_status(uds_code, f'DISTANCE: {distance} cm')
    val = {
        "measurementName": "UDSDistance",
        "timestamp": round(time.time()*1000),
        "value": distance,
        "deviceId": uds_id,
        "deviceType": "UDS",
        "isSimulated": uds_settings["simulated"],
        "valueType": "float"
    }
    value_queue.put(val)


def run_uds(id, settings, threads, uds_code, stop_event):
    global uds_id, uds_settings
    uds_id = id
    uds_settings = settings
    if settings['simulated']:
        uds_thread = threading.Thread(target=run_uds_simulator, args=(uds_code, uds_callback, stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
    else:
        from sensors.uds import run_uds_loop
        uds_thread = threading.Thread(target=run_uds_loop,
                                      args=(settings["pins"], uds_code, uds_callback, stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
