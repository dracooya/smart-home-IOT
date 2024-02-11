import time

attempt = ""
send = False


def simulate(callback, stop_event):
    global attempt
    while True:
        if stop_event.is_set():
            break
        global send
        if send:
            for letter in attempt:
                callback(letter)
            send = False
        time.sleep(1)
