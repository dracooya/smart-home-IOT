import threading
import time

from helpers.printer import print_status
from simulators.buzzer import run_buzzer_simulator
from value_queue import value_queue


def buzzer_callback(code, settings, status):
    print_status(code, status)
    val = {
        "measurementName": "buzzerStatus",
        "timestamp": round(time.time() * 1000),
        "value": status,
        "deviceId": code,
        "deviceType": "BUZZER",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]

    }
    value_queue.put(val)


def run_buzzer(code, settings, threads, buzzer_press_event, buzzer_release_event, stop_event):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=run_buzzer_simulator,
                                         args=(lambda status: buzzer_callback(code, settings, status),
                                               buzzer_press_event, buzzer_release_event, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import buzzer_register
        buzzer_thread = threading.Thread(target=buzzer_register, args=(settings["pins"][0], 440,
                                                                       lambda status: buzzer_callback(code, settings,
                                                                                                      status),
                                                                       buzzer_press_event, buzzer_release_event, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
