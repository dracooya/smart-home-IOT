import threading
import time
from helpers.printer import print_status
from simulators.button import run_button_simulator
from value_queue import value_queue
from broker_config.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish


def button_callback(code, settings):
    print_status(code, "PRESSED")
    val = {
        "measurementName": "buttonStatus",
        "timestamp": round(time.time()*1000),
        "value": "PRESSED",
        "deviceId": code,
        "deviceType": "BUTTON",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]

    }
    publish.single("DS", code, hostname=HOSTNAME, port=PORT)
    value_queue.put(val)


def run_button(code, settings, threads, stop_event):
    if settings['simulated']:
        button_thread = threading.Thread(target=run_button_simulator, args=(lambda: button_callback(code, settings),
                                                                            stop_event))
        button_thread.start()
        threads.append(button_thread)
    else:
        from sensors.button import button_register
        button_thread = threading.Thread(target=button_register,
                                         args=(settings["pins"][0], lambda: button_callback(code, settings)))
        button_thread.start()
        threads.append(button_thread)
