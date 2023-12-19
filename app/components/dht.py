import threading
from helpers.printer import print_status
import time
from value_queue import value_queue
import json

dht_id = ""
dht_settings = {}


def callback(code, humidity, temperature):
    print_status(code, f"Humidity: {humidity:.2f}, Temperature: {temperature:.2f}")
    val_hum = {
        "measurementName": "humidity",
        "timestamp": round(time.time()*1000),
        "value": humidity,
        "deviceId": dht_id,
        "deviceType": "DHT",
        "isSimulated": dht_settings["simulated"],
        "valueType": "float"
    }

    val_temp = {
        "measurementName": "temperature",
        "timestamp": round(time.time()*1000),
        "value": temperature,
        "deviceId": dht_id,
        "deviceType": "DHT",
        "isSimulated": dht_settings["simulated"],
        "valueType": "float"
    }
    value_queue.put(val_hum)
    value_queue.put(val_temp)


def run(id, settings, threads, code, stop_event):
    delay = 2
    global dht_id, dht_settings
    dht_id = id
    dht_settings = settings
    if settings['simulated']:
        from simulators.dht import simulate
        thread = threading.Thread(target=simulate, args=(code, callback, stop_event, delay))
        thread.start()
        threads.append(thread)
    else:
        from sensors.dht import run
        thread = threading.Thread(target=run, args=(settings["pins"][0], lambda x,y: callback(code, x,y), stop_event, delay))
        thread.start()
        threads.append(thread)

