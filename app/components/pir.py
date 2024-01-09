import threading
import time

from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status
from value_queue import value_queue

import paho.mqtt.publish as publish


def motion(code, settings):
    print_status(code, "MOTION DETECTED")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "MOTION",
        "deviceId": code,
        "deviceType": "PIR",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val)
    if code == "DPIR1":
        publish.single("DL", "ON", hostname=HOSTNAME, port=PORT)
    if code[0] == "D":
        publish.single("distanceCheck", "DUS" + code[-1], hostname=HOSTNAME, port=PORT)


def run(code, settings, threads, stop_event):
    if settings['simulated']:
        from simulators.pir import simulate
        thread = threading.Thread(target=simulate,
                                  args=(lambda: motion(code, settings), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.pir import register
        thread = threading.Thread(target=register,
                                  args=(settings["pins"][0], lambda: motion(code, settings)))
        thread.start()
        threads.append(thread)
