import threading
import time
import paho.mqtt.client as mqtt
from broker_config.broker_settings import HOSTNAME,PORT
import json

from helpers.printer import print_status
from simulators.rgb_light import run_rgb_simulator
from value_queue import value_queue

RGB_change_event = None

def on_connect(client, userdata, flags, rc):
    client.subscribe("rgb_remote")

def on_message(client, userdata, msg):
    command = json.loads(msg.payload.decode('utf-8'))["value"]
    RGB_change_event.trigger([command])


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
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }
    value_queue.put(val)
    

def run(code, settings, threads, rgb_change_event, stop_event):
    global RGB_change_event
    RGB_change_event = rgb_change_event
    if settings['simulated']:
        rgb_thread = threading.Thread(target=run_rgb_simulator,
                                      args=(lambda status: rgb_callback(code, settings, status), RGB_change_event, stop_event, client))
        rgb_thread.start()
        threads.append(rgb_thread)
    else:
        from actuators.rgb_light import rgb_register
        rgb_thread = threading.Thread(target=rgb_register, args=(
            settings["pins"], lambda status: rgb_callback(code, settings, status), RGB_change_event,stop_event, client))
        rgb_thread.start()
        threads.append(rgb_thread)
