from helpers.printer import print_status
from simulators.infrared import simulate
from value_queue import value_queue
import time
import threading

import paho.mqtt.publish as publish
from broker_config.broker_settings import HOSTNAME,PORT
import json

def infrared_callback(code, settings, status):
    print_status(code, status)
    val = {
        "measurementName": "infraredInput",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": code,
        "deviceType": "IR",
        "isSimulated": settings["simulated"]

    }
    value_queue.put(val)
    publish.single("rgb_remote",json.dumps(val), hostname=HOSTNAME, port=PORT)

def run(code, settings, threads, stop_event):
    if settings['simulated']:
        infrared_thread = threading.Thread(target=simulate,
                                         args=(lambda key: infrared_callback(code, settings, key),stop_event))
        infrared_thread.start()
        threads.append(infrared_thread)
    else:
        from sensors.infrared import infrared_register
        infrared_thread = threading.Thread(target=infrared_register, args=(settings["pins"][0], lambda key: infrared_callback(code, settings, key), stop_event))
        infrared_thread.start()
        threads.append(infrared_thread)