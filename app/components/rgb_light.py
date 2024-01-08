import threading
import time
import paho.mqtt.client as mqtt
from broker_config.broker_settings import HOSTNAME,PORT
import json

from helpers.printer import print_status
from simulators.rgb_light import run_rgb_simulator
from value_queue import value_queue

ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3",  "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0", "#"] 

def on_connect(client, userdata, flags, rc):
    client.subscribe("rgb_remote")

def on_message(client, userdata, msg):
    command = json.loads(msg.payload.decode('utf-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOSTNAME, PORT)
client.loop_start()

def rgb_callback(code, settings, status):
    print_status(code, status)
    val = {
        "measurementName": "RGBStatus",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": code,
        "deviceType": "RGB",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val)
    

def run(code, settings, threads, rgb_off_event, rgb_change_event, stop_event):
    if settings['simulated']:
        rgb_thread = threading.Thread(target=run_rgb_simulator,
                                      args=(lambda status: rgb_callback(code, settings, status), rgb_change_event,
                                            rgb_off_event, stop_event))
        rgb_thread.start()
        threads.append(rgb_thread)
    else:
        from actuators.rgb_light import rgb_register
        rgb_thread = threading.Thread(target=rgb_register, args=(
            settings["pins"], lambda status: rgb_callback(code, settings, status), rgb_change_event,
            rgb_off_event,stop_event))
        rgb_thread.start()
        threads.append(rgb_thread)
