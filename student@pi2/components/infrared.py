from helpers.printer import print_status
from simulators.infrared import simulate
from value_queue import value_queue
import time
import threading

import paho.mqtt.client as mqtt
from broker_config.broker_settings import HOSTNAME,PORT
import json

Code = ""
Settings = {}

def on_connect(client, userdata, flags, rc):
    client.subscribe("rgb_remote_web")

def on_message(client, userdata, msg):
    command = json.loads(msg.payload.decode('utf-8'))["value"]
    infrared_callback(command)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOSTNAME, PORT)
client.loop_start()

def infrared_callback(status):
    print_status(Code, status)
    val = {
        "measurementName": "infraredInput",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": Code,
        "deviceType": "IR",
        "isSimulated": Settings["simulated"],
        "pi": 3

    }
    value_queue.put(val)
    client.publish("rgb_remote",json.dumps(val))

def run(code, settings, threads, stop_event):
    global Code, Settings
    Code = code
    Settings = settings
    if settings['simulated']:
        infrared_thread = threading.Thread(target=simulate, args=(stop_event, client))
        infrared_thread.start()
        threads.append(infrared_thread)
    else:
        from sensors.infrared import infrared_register
        infrared_thread = threading.Thread(target=infrared_register, args=(settings["pins"][0], lambda key: infrared_callback(key), stop_event, client))
        infrared_thread.start()
        threads.append(infrared_thread)