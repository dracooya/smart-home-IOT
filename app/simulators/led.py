import sched
import time

from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status


def run_led_simulator(code, callback_fc, door_light_on_event, door_light_off_event, stop_event):
    import paho.mqtt.client as mqtt

    def on_connect(client, userdata, flags, rc):
        print_status(code, "Connected to MQTT broker with result code " + str(rc))
        client.subscribe(code)

    def on_message(client, userdata, msg):
        def turn_off():
            callback_fc("OFF")

        if msg.payload.decode() == 'ON':
            callback_fc("ON")
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(10, 1, turn_off)
            scheduler.run()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOSTNAME, PORT)

    @door_light_on_event.on
    def light_on():
        callback_fc("ON")

    @door_light_off_event.on
    def light_off():
        callback_fc("OFF")

    client.loop_start()
    while True:
        if stop_event.is_set():
            break
