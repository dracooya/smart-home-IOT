import threading
import time

from broker_config.broker_settings import HOSTNAME, PORT
from components import uds
from helpers.printer import print_status
from value_queue import value_queue
import paho.mqtt.client as mqtt
from broker_config.broker_settings import HOSTNAME,PORT

import paho.mqtt.publish as publish

people_count = 0
client = None

def on_connect(client, userdata, flags, rc):
    client.subscribe("people_counter")

def on_message(client, userdata, msg):
    global people_count
    people_count = int(msg.payload.decode('utf-8'))
    print("People count:" + str(people_count))


def motion(code, settings):
    print_status(code, "MOTION DETECTED")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "MOTION",
        "deviceId": code,
        "deviceType": "PIR",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)

    if code == "DPIR1":
        publish.single("DL", "ON", hostname=HOSTNAME, port=PORT)
    if code[0] == "D":
        print_status(code, "Last distance: " + str(uds.last_distance) + " cm, second last distance: " +
                     str(uds.second_last_distance) + " cm")
        if uds.last_distance < uds.second_last_distance:
            print_status(code, "Distance is decreasing, someone is entering")
            publish.single("tracker", "ENTER", hostname=HOSTNAME, port=PORT)
        else:
            print_status(code, "Distance is increasing, someone is leaving")
            publish.single("tracker", "EXIT", hostname=HOSTNAME, port=PORT)
    if code[0] == "R":
        print("People count (RPIR DETECTION):" + str(people_count))
        if people_count == 0:
            publish.single("alarm", "ALARM_ON_RPIR_MOTION_" + code, hostname=HOSTNAME, port=PORT)


def no_motion(code, settings):
    print_status(code, "NO MOTION")
    val = {
        "measurementName": "PIRStatus",
        "timestamp": round(time.time()*1000),
        "value": "NO-MOTION",
        "deviceId": code,
        "deviceType": "PIR",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)

def run(code, settings, threads, stop_event):
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, PORT)
    client.loop_start()
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
