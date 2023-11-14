import threading
from simulators.buzzer import run_buzzer_simulator
from helpers.printer import print_status


def buzzer_callback(status):
    print_status("DB", status)


def run_buzzer(settings, threads, buzzer_press_event, buzzer_release_event, stop_event):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=run_buzzer_simulator,
                                         args=(buzzer_callback, buzzer_press_event, buzzer_release_event, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import buzzer_register
        buzzer_thread = threading.Thread(target=buzzer_register, args=(
        settings["pins"][0], 400, buzzer_callback, buzzer_press_event, buzzer_release_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
