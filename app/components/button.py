import threading

from helpers.printer import print_status
from simulators.button import run_button_simulator


def button_callback(button_code):
    print_status(button_code, "PRESSED")


def run_button(settings, threads, button_code, stop_event):
    if settings['simulated']:
        button_thread = threading.Thread(target=run_button_simulator, args=(button_callback, button_code, stop_event))
        button_thread.start()
        threads.append(button_thread)
    else:
        from sensors.button import button_register
        button_thread = threading.Thread(target=button_register,
                                         args=(settings["pins"][0], lambda x: button_callback(button_code)))
        button_thread.start()
        threads.append(button_thread)
