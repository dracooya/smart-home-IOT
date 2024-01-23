import threading
import time

from broker_config.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish

from helpers.printer import print_status
from value_queue import value_queue


def callback(code, settings, key):
    print_status(code, key)
    val = {
        "measurementName": "gsgMotion",
        "timestamp": round(time.time() * 1000),
        "value": key,
        "deviceId": code,
        "deviceType": "GSG",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)
    publish.single("alarm", "ALARM_ON_GSG_MOTION_" + code, hostname=HOSTNAME, port=PORT)


def run(code, settings, threads, stop_event):
    if settings['simulated']:
        from simulators.gsg import simulate
        thread = threading.Thread(target=simulate, args=(lambda key: callback(code, settings, key), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.gsg.gsg import register
        thread = threading.Thread(target=register, args=(lambda key: callback(code, settings, key), stop_event))
        thread.start()
        threads.append(thread)
