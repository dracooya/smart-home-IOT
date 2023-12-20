import threading
import time

from helpers.printer import print_status
from simulators.led import run_led_simulator
from value_queue import value_queue


def led_callback(code, settings, status):
    print_status(code, status)
    val = {
        "measurementName": "LEDStatus",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": code,
        "deviceType": "LED",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val)


def run_led(code, settings, threads, door_light_on_event, door_light_off_event, stop_event):
    if settings['simulated']:
        led_thread = threading.Thread(target=run_led_simulator,
                                      args=(lambda status: led_callback(code, settings, status), door_light_on_event,
                                            door_light_off_event, stop_event))
        led_thread.start()
        threads.append(led_thread)
    else:
        from actuators.led import led_register
        led_thread = threading.Thread(target=led_register, args=(
            settings["pins"][0], lambda status: led_callback(code, settings, status), door_light_on_event,
            door_light_off_event))
        led_thread.start()
        threads.append(led_thread)
