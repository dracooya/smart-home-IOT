import atexit
import json
import sched
import threading
import time

from flask import Flask, jsonify
from flask_mqtt import Mqtt
from flask_cors import CORS
from influxdb_client import WriteOptions, InfluxDBClient, WriteApi, Point, WritePrecision
from flask_socketio import SocketIO
from enum import Enum
from config import settings


def on_exit(db: InfluxDBClient, write_api: WriteApi, mqtt: Mqtt):
    write_api.close()
    db.close()
    mqtt.unsubscribe_all()


app = Flask(__name__)
socketio_app = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app)
app.config['MQTT_BROKER_URL'] = settings.HOSTNAME
app.config['MQTT_BROKER_PORT'] = settings.PORT

influxdb = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)
influxdb_write_api = influxdb.write_api(write_options=WriteOptions(batch_size=200))

mqtt = Mqtt(app)
atexit.register(on_exit, influxdb, influxdb_write_api, mqtt)
people_counter = 0
people_counter_lock = threading.Lock()

current_measurements = {}
devices = []
pi1_batch_size = 0
pi2_batch_size = 0
pi3_batch_size = 0


class AlarmState(Enum):
    OFF = 0
    ON = 1
    TRIGGERED = 2


alarm_state = AlarmState.OFF
alarm_state_lock = threading.Lock()
pin = '1234'


def set_alarm_state(state: AlarmState):
    global alarm_state
    with alarm_state_lock:
        alarm_state = state


def get_alarm_state():
    global alarm_state
    with alarm_state_lock:
        return alarm_state


def get_people_counter():
    global people_counter
    with people_counter_lock:
        return people_counter


def set_people_counter(value):
    global people_counter
    with people_counter_lock:
        people_counter = value


def send_status_summary():
    global current_measurements
    socketio_app.emit('status', json.dumps(current_measurements))


def load_devices():
    global devices
    with open("devices.json", 'r') as f:
        devices = json.load(f)
    for device in devices:
        current_measurements[device["id"]] = "---"


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        mqtt.subscribe("measurements")
        mqtt.subscribe("tracker")
        mqtt.subscribe("DMS")
    else:
        print("Failed to connect to broker, return code", rc)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    decoded_msg = message.payload.decode('utf-8')
    if decoded_msg[0] == 'E':
        global people_counter
        with people_counter_lock:
            if decoded_msg == 'ENTER':
                print("ENTERING")
                people_counter += 1
            elif decoded_msg == 'EXIT':
                print("EXITING")
                if people_counter > 0:
                    people_counter -= 1
                else:
                    print("INTRUDER LEAVING THROUGH THE WINDOW :O")
            print("People counter: " + str(people_counter))
        return

    def activate_alarm():
        set_alarm_state(AlarmState.ON)
        print("Alarm activated")

    if message.topic == "DMS":
        if decoded_msg == pin:
            print("PIN CORRECT")
            if get_alarm_state() == AlarmState.TRIGGERED or get_alarm_state() == AlarmState.ON:
                set_alarm_state(AlarmState.OFF)
                print("Alarm deactivated")
            elif get_alarm_state() == AlarmState.OFF:
                scheduler = sched.scheduler(time.time, time.sleep)
                scheduler.enter(10, 1, activate_alarm)
                scheduler.run()
        else:
            print("PIN INCORRECT")
        return

    global pi1_batch_size, pi2_batch_size, pi3_batch_size
    obj = json.loads(decoded_msg)
    if obj['deviceType'] == "DHT":
        tokens = obj['value'].split("%")
        humidity = tokens[0]
        temperature = tokens[1].split("°")[0].split(",")[1].strip()

        point_temp = Point('temperature').field('_measurement', float(temperature)) \
            .time(obj['timestamp'], write_precision=WritePrecision.MS) \
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated',
                                                                                       obj['isSimulated'])

        influxdb_write_api.write(bucket='smart_measurements', record=point_temp)

        point_hum = Point('humidity').field('_measurement', float(humidity)) \
            .time(obj['timestamp'], write_precision=WritePrecision.MS) \
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated',
                                                                                       obj['isSimulated'])

        influxdb_write_api.write(bucket='smart_measurements', record=point_hum)

    else:
        point = Point(obj['measurementName']).field('_measurement', obj['value']) \
            .time(obj['timestamp'], write_precision=WritePrecision.MS) \
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated',
                                                                                       obj['isSimulated'])
        influxdb_write_api.write(bucket='smart_measurements', record=point)

    if (obj['deviceType'] == "UDS"):
        obj['value'] = str(obj['value']) + " cm"

    current_measurements[obj["deviceId"]] = obj['value']

    if (obj['pi'] == 1):
        if pi1_batch_size == 49:
            pi1_batch_size = 0
            send_status_summary()
        else:
            pi1_batch_size += 1
    elif (obj['pi'] == 2):
        if pi2_batch_size == 49:
            pi2_batch_size = 0
            send_status_summary()
        else:
            pi2_batch_size += 1
    else:
        if pi3_batch_size == 49:
            pi3_batch_size = 0
            send_status_summary()
        else:
            pi3_batch_size += 1


@app.route('/')
def poy():
    return 'poy'


@app.route('/all', methods=['GET'])
def get_all_devices():
    devices_and_statuses = []
    for device in devices:
        key = device["id"]
        device_type = ""
        if key in ["DS1", "DS2"]:
            device_type = "DS"
        if key in ["DL"]:
            device_type = "LED"
        if key in ["DUS1", "DUS2"]:
            device_type = "UDS"
        if key in ["DB"]:
            device_type = "BUZZER"
        if key in ["BB"]:
            device_type = "ALARM"
        if key in ["DPIR1", "DPIR2", "RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
            device_type = "PIR"
        if key in ["RDHT1", "RDHT2", "RDHT3", "RDHT4", "GDHT"]:
            device_type = "DHT"
        if key in ["DMS"]:
            device_type = "DMS"
        if key in ["B4SD"]:
            device_type = "FOUR_SD"
        if key in ["BIR"]:
            device_type = "IR"
        if key in ["BGRB"]:
            device_type = "RGB"
        if key in ["GLCD"]:
            device_type = "LCD"
        if key in ["GSG"]:
            device_type = "GYRO"

        device_with_status = {
            "type": device_type,
            "id": device["id"],
            "name": device["name"],
            "status": current_measurements[device["id"]]
        }
        devices_and_statuses.append(device_with_status)
    return jsonify(devices_and_statuses)


if __name__ == '__main__':
    load_devices()
    socketio_app.run(app, debug=False)
