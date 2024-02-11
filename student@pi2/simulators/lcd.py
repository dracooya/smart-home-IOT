import time

from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status


def simulate(code, callback, stop_event):
    import paho.mqtt.client as mqtt

    def on_connect(client, userdata, flags, rc):
        print_status(code, "Connected to MQTT broker with result code " + str(rc))
        client.subscribe("GDHT")

    def on_message(client, userdata, msg):
        callback(msg.payload.decode())

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOSTNAME, PORT)

    client.loop_start()
    while True:
        if stop_event.is_set():
            break
        time.sleep(0.5)
