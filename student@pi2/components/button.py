import threading
import time
from helpers.printer import print_status
from simulators.button import run_button_simulator
from value_queue import value_queue
from broker_config.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish


def long_press_callback(code):
    publish.single("alarm", "ALARM_ON_DOOR_SENSOR_" + code, hostname=HOSTNAME, port=PORT)

def release_callback(code, settings, is_long, time):
    if is_long:
        publish.single("alarm", "ALARM_OFF", hostname=HOSTNAME, port=PORT)
    
    button_release_callback(code, settings, time)

def button_callback(code, settings, time):
    print_status(code, " DOOR OPENED (" + str(time) + ")")
    val = {
        "measurementName": "buttonStatus",
        "timestamp": round(time),
        "value": "DOOR OPENED",
        "deviceId": code,
        "deviceType": "BUTTON",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]

    }
    publish.single("DS", code, hostname=HOSTNAME, port=PORT)
    value_queue.put(val)


def button_release_callback(code, settings, time):
    print_status(code, " DOOR CLOSED (" + str(time) + ")")
    val = {
        "measurementName": "buttonStatus",
        "timestamp": round(time),
        "value": "DOOR CLOSED",
        "deviceId": code,
        "deviceType": "BUTTON",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]

    }
    value_queue.put(val)


def run_button(code, settings, threads, stop_event):
    if settings['simulated']:
        button_thread = threading.Thread(target=run_button_simulator, args=(lambda t: button_callback(code, settings, t),
                                                                            lambda: long_press_callback(code),
                                                                            lambda is_long, time: release_callback(code, settings, is_long, time),
                                                                            stop_event))
        button_thread.start()
        threads.append(button_thread)
    else:
        from sensors.button import button_register
        button_thread = threading.Thread(target=button_register,
                                         args=(settings["pins"][0], lambda t: button_callback(code, settings, t), 
                                               lambda: long_press_callback(code), lambda is_long, time: release_callback(code, settings, is_long, time)))
        button_thread.start()
        threads.append(button_thread)
