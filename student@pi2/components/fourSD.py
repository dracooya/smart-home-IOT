from helpers.printer import print_status
from simulators.fourSD import run_fourSD_simulator
from value_queue import value_queue
import time
import threading
import paho.mqtt.client as mqtt
from broker_config.broker_settings import HOSTNAME,PORT

alarm_clock_buzz_event = None
alarm_clock_stop_event = None

def on_connect(client, userdata, flags, rc):
    client.subscribe("alarm_clock_buzz")

def on_message(client, userdata, msg):
    if msg == "STOP":
        alarm_clock_stop_event.trigger()

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

def run(code, settings, threads, alarm_clock_on_event, alarm_clock_off_event, stop_event):
    global alarm_clock_buzz_event, alarm_clock_stop_event
    alarm_clock_buzz_event = alarm_clock_on_event
    alarm_clock_stop_event = alarm_clock_off_event
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, PORT)
    client.loop_start()
    if settings['simulated']:
        fourSD_thread = threading.Thread(target=run_fourSD_simulator,
                                         args=(lambda status: fourSD_callback(code, settings, status), alarm_clock_on_event, alarm_clock_off_event, stop_event))
        fourSD_thread.start()
        threads.append(fourSD_thread)
    else:
        from actuators.fourSD import fourSD_register
        fourSD_thread = threading.Thread(target=fourSD_register, args=(settings["pins"], lambda status: fourSD_callback(code, settings, status), alarm_clock_on_event, alarm_clock_off_event, stop_event))
        fourSD_thread.start()
        threads.append(fourSD_thread)