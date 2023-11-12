import threading
from simulators.led import run_led_simulator
from helpers.printer import printStatus

def led_callback(status):
    printStatus("DL", status)


def run_led(settings, threads, door_light_on_event, door_light_off_event, stop_event):

        if settings['simulated']:
            led_thread = threading.Thread(target = run_led_simulator, args=(led_callback, door_light_on_event, door_light_off_event, stop_event))
            led_thread.start()
            threads.append(led_thread)
        else:
            from actuators.led import led_register
            led_thread = threading.Thread(target=led_register, args=(settings["pins"][0], led_callback, door_light_on_event, door_light_off_event))
            led_thread.start()
            threads.append(led_thread)