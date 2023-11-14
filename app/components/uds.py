import threading

from helpers.printer import print_status
from simulators.uds import run_uds_simulator


def uds_callback(uds_code, message):
    print_status(uds_code, message)


def run_uds(settings, threads, uds_code, stop_event):
    if settings['simulated']:
        uds_thread = threading.Thread(target=run_uds_simulator, args=(uds_code, uds_callback, stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
    else:
        from sensors.uds import run_uds_loop
        uds_thread = threading.Thread(target=run_uds_loop,
                                      args=(settings["pins"], uds_code, uds_callback, stop_event, 2))
        uds_thread.start()
        threads.append(uds_thread)
