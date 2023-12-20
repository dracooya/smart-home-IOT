import threading
import time

from helpers.printer import print_status
from value_queue import value_queue


def callback(code, settings, humidity, temperature):
    print_status(code, f"Humidity: {humidity:.2f}, Temperature: {temperature:.2f}")
    val_hum = {
        "measurementName": "humidity",
        "timestamp": round(time.time()*1000),
        "value": humidity,
        "deviceId": code,
        "deviceType": "DHT",
        "isSimulated": settings["simulated"]
    }

    val_temp = {
        "measurementName": "temperature",
        "timestamp": round(time.time()*1000),
        "value": temperature,
        "deviceId": code,
        "deviceType": "DHT",
        "isSimulated": settings["simulated"]
    }
    value_queue.put(val_hum)
    value_queue.put(val_temp)


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

