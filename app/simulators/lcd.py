import time
import random


to_display = "Temp: 0.00C Hum: 0.00%"


def simulate(callback, stop_event, change_display_event):
    while True:
        if stop_event.is_set():
            break
        humidity = random.uniform(40, 70)
        temperature = random.uniform(20, 30)
        to_display = "Temp: {0:.2f}C Hum: {1:.2f}%".format(temperature, humidity)
        callback(to_display)
        time.sleep(random.randint(2, 20))

    @change_display_event
    def change_display(new_display):
        global to_display
        to_display = new_display
        callback(to_display)
