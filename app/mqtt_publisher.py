from value_queue import value_queue
from broker_config.broker_settings import HOSTNAME,PORT
import paho.mqtt.publish as publish
from value_queue import value_queue, BATCH_SIZE
import json


def publisher_task(stop_event):
    batch = []
    while True:        
        if value_queue.qsize() >= BATCH_SIZE:
            for _ in range(0,50):
                val = value_queue.get()
                batch.append(("measurements",json.dumps(val),0,True))
            publish.multiple(batch, hostname=HOSTNAME, port=PORT)
            print("BATCH SIZE AFTER: " + str(value_queue.qsize()))
            batch.clear()
        if stop_event.is_set():
            break

