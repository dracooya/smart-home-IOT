import threading
from simulators.led import run_led_simulator
from helpers.printer import print_status
import time
from value_queue import value_queue
import json

led_id = ""
led_settings = {}

def led_callback(status):
    print_status("DL", status)
    val = {
        "measurementName": "LEDStatus",
        "timestamp": round(time.time()*1000),
        "value": status,
        "deviceId": led_id,
        "deviceType": "LED",
        "isSimulated": led_settings["simulated"],
        "valueType": "str"

    }
    value_queue.put(val)


def run_led(id, settings, threads, door_light_on_event, door_light_off_event, stop_event):
    global led_id, led_settings
    led_id = id
    led_settings = settings
    if settings['simulated']:
        led_thread = threading.Thread(target = run_led_simulator, args=(led_callback, door_light_on_event, door_light_off_event, stop_event))
        led_thread.start()
        threads.append(led_thread)
    else:
        from actuators.led import led_register
        led_thread = threading.Thread(target=led_register, args=(settings["pins"][0], led_callback, door_light_on_event, door_light_off_event))
        led_thread.start()
        threads.append(led_thread)