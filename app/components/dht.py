import threading
import time

from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status
from value_queue import value_queue

import paho.mqtt.publish as publish


def callback(code, settings, humidity, temperature):
    print_status(code, f"Humidity: {humidity:.2f}, Temperature: {temperature:.2f}")
    val = {
        "measurementName": "hum&temp",
        "timestamp": round(time.time() * 1000),
        "value": str(round(humidity, 2)) + "%, " + str(round(temperature, 2)) + "°C",
        "deviceId": code,
        "deviceType": "DHT",
        "isSimulated": settings["simulated"],
        "pi": settings["pi"]
    }

    value_queue.put(val)

    if code[0] == 'G':  # GDHT
        publish.single("GDHT", f"Temp: {temperature:.2f}C Hum: {humidity:.2f}%", hostname=HOSTNAME, port=PORT)


def run(code, settings, threads, stop_event):
    delay = 2
    if settings['simulated']:
        from simulators.dht import simulate
        thread = threading.Thread(target=simulate, args=(lambda hum, temp: callback(code, settings, hum, temp),
                                                         stop_event, delay))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dht import run
        thread = threading.Thread(target=run, args=(settings["pins"][0],
                                                    lambda hum, temp: callback(code, settings, hum, temp),
                                                    stop_event, delay))
        thread.start()
        threads.append(thread)
