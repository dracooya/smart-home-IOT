import threading

from helpers.printer import print_status


def callback(code, msg):
    print_status(code, f"Key pressed: {msg}")


def run(settings, threads, code, stop_event):
    if settings['simulated']:
        from simulators.dms import simulate
        thread = threading.Thread(target=simulate, args=(lambda x: callback(code, x), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dms import register
        thread = threading.Thread(target=register, args=(settings["pins"], lambda x: callback(code, x)))
        thread.start()
        threads.append(thread)
