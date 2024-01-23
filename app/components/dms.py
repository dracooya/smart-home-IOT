import threading
import time

from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status
from value_queue import value_queue

import paho.mqtt.publish as publish


full_attempt = ""


def callback(code, settings, key):
    global full_attempt

    if key != "#":
        full_attempt += key
        return

    print_status(code, f"Code entered: {full_attempt}")
    val = {
        "measurementName": "keypadInput",
        "timestamp": round(time.time()*1000),
        "value": full_attempt,
        "deviceId": code,
        "deviceType": "DMS",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)
    # SEND TO SERVER PIN ATTEMPT
    publish.single("DMS", full_attempt, hostname=HOSTNAME, port=PORT)
    full_attempt = ""


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
