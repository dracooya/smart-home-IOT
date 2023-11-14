import threading

from helpers.printer import print_status


def callback(code, message):
    print_status(code, message)


def run(settings, threads, code, stop_event):
    delay = 2

    if settings['simulated']:
        from simulators.dht import simulate
        thread = threading.Thread(target=simulate, args=(code, callback, stop_event, delay))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dht import run
        thread = threading.Thread(target=run, args=(settings["pins"][0], code, callback, stop_event, delay))
        thread.start()
        threads.append(thread)

