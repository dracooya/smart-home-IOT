import threading

from helpers.printer import print_status


def motion(code):
    print_status(code, "MOTION DETECTED")


def no_motion(code):
    print_status(code, "NO MOTION")


def run(settings, threads, code, stop_event):
    if settings['simulated']:
        from simulators.pir import simulate
        thread = threading.Thread(target=simulate,
                                  args=(lambda: motion(code), lambda: no_motion(code), stop_event))
        thread.start()
        threads.append(thread)
    else:
        from sensors.pir import register
        thread = threading.Thread(target=register,
                                  args=(settings["pins"][0], lambda: motion(code), lambda: no_motion(code)))
        thread.start()
        threads.append(thread)
