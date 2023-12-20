import atexit
import json

from flask import Flask
from flask_mqtt import Mqtt
from influxdb_client import WriteOptions, InfluxDBClient, WriteApi, Point, WritePrecision

from config import settings


def on_exit(db: InfluxDBClient, write_api: WriteApi, mqtt: Mqtt):
    write_api.close()
    db.close()
    mqtt.unsubscribe_all()


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = settings.HOSTNAME
app.config['MQTT_BROKER_PORT'] = settings.PORT

influxdb = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)
influxdb_write_api = influxdb.write_api(write_options=WriteOptions(batch_size=200))

mqtt = Mqtt(app)
atexit.register(on_exit, influxdb, influxdb_write_api, mqtt)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        mqtt.subscribe("measurements")
    else:
        print("Failed to connect to broker, return code", rc)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    point = Point(obj['measurementName']).field('_measurement', obj['value'])\
        .time(obj['timestamp'], write_precision=WritePrecision.MS)\
        .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated', obj['isSimulated'])
    # print(point)
    influxdb_write_api.write(bucket='smart_measurements', record=point)


@app.route('/')
def poy():
    return 'poy'


if __name__ == '__main__':
    app.run()
