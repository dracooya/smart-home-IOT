import time

attempt = ""


def simulate(callback, stop_event):
    global attempt
    prev_attempt = ""
    while True:
        if stop_event.is_set():
            break
        if attempt != prev_attempt:
            for letter in attempt:
                callback(letter)
            prev_attempt = attempt
        time.sleep(1)
