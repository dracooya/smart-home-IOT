import atexit
import json
import threading
import random
import datetime
import time

from flask import Flask, jsonify, request
from flask_mqtt import Mqtt
from flask_cors import CORS
from influxdb_client import WriteOptions, InfluxDBClient, WriteApi, Point, WritePrecision
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

from config import settings
import sched
import time


def on_exit(db: InfluxDBClient, write_api: WriteApi, mqtt: Mqtt):
    write_api.close()
    db.close()
    mqtt.unsubscribe_all()
    scheduler.shutdown()


app = Flask(__name__)
socketio_app = SocketIO(app, cors_allowed_origins="http://localhost:5173", async_mode='threading')

CORS(app)
app.config['MQTT_BROKER_URL'] = settings.HOSTNAME
app.config['MQTT_BROKER_PORT'] = settings.PORT
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)


influxdb = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)
influxdb_write_api = influxdb.write_api(write_options=WriteOptions(batch_size=200))

mqtt = Mqtt(app)
atexit.register(on_exit, influxdb, influxdb_write_api, mqtt)
people_counter = 0
people_counter_lock = threading.Lock()

mqtt_scheduler_lock = threading.Lock()
super_secret_alarm_password = "4752"

current_measurements = {}
devices = []
pi1_batch_size = 0
pi2_batch_size = 0
pi3_batch_size = 0 

pir_last_motion_timestamp = {}
last_gsg_ping = 0

last_alarm_clock = ""
does_alarm_clock_work = False

last_alarm_reason = ""
does_alarm_work = None

alarm_type_with_info = {}


def initialize_alarm_map() :
    default_info = {
            "alarm_reason": "",
            "does_alarm_work": None,
            "alarm_type": ""
            }
    default_info["alarm_type"] = "RPIR_MOTION"
    alarm_type_with_info["RPIR_MOTION"] = default_info # no one's home and rpir detects motion
    default_info = default_info.copy()
    default_info["alarm_type"] = "DS_DURATION"
    alarm_type_with_info["DS_DURATION"] = default_info # doors are open for more than 5 seconds
    default_info = default_info.copy()
    default_info["alarm_type"] = "DS_SYS_ACT"
    alarm_type_with_info["DS_SYS_ACT"] = default_info # door sensor when system is activated
    default_info = default_info.copy()
    default_info["alarm_type"] = "GSG_MOTION"
    alarm_type_with_info["GSG_MOTION"] = default_info  # gun safe moved


def set_last_alarm_reason(reason, type):
    global alarm_type_with_info
    alarm_type_with_info[type]["alarm_reason"] = reason


def get_last_alarm_reason(type):
    global alarm_type_with_info
    return alarm_type_with_info[type]["alarm_reason"]


def set_alarm_clock_action():
    global last_alarm_clock, does_alarm_clock_work
    does_alarm_clock_work = True
    last_alarm_clock = time.strftime("%H:%M", time.localtime())
    mqtt.publish("alarm_clock_buzz", "START")
    info = {
        "alarm_clock_time": last_alarm_clock,
        "does_alarm_clock_work": does_alarm_clock_work
    }
    socketio_app.emit('alarm_clock_status', json.dumps(info))


def send_status_summary():
    global current_measurements
    now = time.time() * 1000
    if now - last_gsg_ping > 30000:
        current_measurements['GSG'] = 'NO MOTION'
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
        mqtt.subscribe("alarm")
        mqtt.subscribe("DMS")
        mqtt.subscribe("DS")
    else:
        print("Failed to connect to broker, return code", rc)


def send_people_counter():
    mqtt.publish("people_counter", str(people_counter))


def activate_alarm(type):
    global alarm_type_with_info
    alarm_type_with_info[type]["does_alarm_work"] = False
    print("Alarm of type " + type + " activated")


def deactivate_alarm(type, ping=True):
    global alarm_type_with_info
    alarm_type_with_info[type]["does_alarm_work"] = None
    print("Alarm of type " + type + " deactivated")

    stop_buzzing = True
    for alarm in alarm_type_with_info.values():
        if alarm["does_alarm_work"] is True:
            stop_buzzing = False

    if stop_buzzing:
        mqtt.publish("DB", "STOP")
        mqtt.publish("BB", "STOP")

    if ping:
        point_alarm = Point('alarm').field('_measurement', 'DEACTIVATED').time(datetime.datetime.utcnow(), WritePrecision.NS)\
            .tag('type', type)
        influxdb_write_api.write(bucket='smart_measurements', record=point_alarm)


def trigger_alarm(type):
    global alarm_type_with_info
    alarm_type_with_info[type]["does_alarm_work"] = True
    print("Alarm of type " + type + " triggered")
    mqtt.publish("DB", "START")
    mqtt.publish("BB", "START")

    point_alarm = Point('alarm').field('_measurement', 'TRIGGERED').time(datetime.datetime.utcnow(), WritePrecision.NS)\
        .tag('type', type)
    influxdb_write_api.write(bucket='smart_measurements', record=point_alarm)


def alarm_on(type):
    global alarm_type_with_info
    return alarm_type_with_info[type]["does_alarm_work"] is True or alarm_type_with_info[type]["does_alarm_work"] is False


def alarm_off(type):
    global alarm_type_with_info
    return alarm_type_with_info[type]["does_alarm_work"] is None


def alarm_ready(type):
    global alarm_type_with_info
    return alarm_type_with_info[type]["does_alarm_work"] is False


def alarm_triggered(type):
    global alarm_type_with_info
    return alarm_type_with_info[type]["does_alarm_work"] is True


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    with mqtt_scheduler_lock:
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
                        print("INTRUDER LEAVING THROUGH THE WINDOW :O HOOOOMAGAAAAAAWD")
                send_people_counter()
                print("People counter: " + str(people_counter))
            return

        if message.topic == "DMS":
            if decoded_msg == super_secret_alarm_password:
                print("PIN CORRECT")
                alarm_type = "DS_SYS_ACT"
                if alarm_off(alarm_type):
                    scheduler = sched.scheduler(time.time, time.sleep)
                    scheduler.enter(10, 1, lambda: activate_alarm(alarm_type))
                    scheduler.run()
                elif alarm_ready(alarm_type):
                    deactivate_alarm(alarm_type, ping=False)
                elif alarm_triggered(alarm_type):
                    deactivate_alarm(alarm_type)
            else:
                print("PIN INCORRECT")
            return

        if message.topic == "DS":
            alarm_type = "DS_SYS_ACT"
            if alarm_triggered(alarm_type) or not alarm_ready(alarm_type):
                return
            set_last_alarm_reason("Door sensor motion detected while security system is activated (" + decoded_msg + ")",
                                  alarm_type)
            trigger_alarm(alarm_type)
            info = {
                "alarm_reason": get_last_alarm_reason(alarm_type),
                "does_alarm_work": True,
                "alarm_type": alarm_type
            }
            socketio_app.emit('alarm_status', json.dumps(info))
            return
        
        if message.topic == "alarm":
            alarm_type = ""
            if "ALARM_ON_" in decoded_msg:
                device_code = decoded_msg.split("_")[-1]
                print(decoded_msg + "\n")
                if "RPIR_MOTION" in decoded_msg:
                    alarm_type = "RPIR_MOTION"
                    set_last_alarm_reason("Room motion detected when no one's home (" + device_code + ")", alarm_type)
                elif "DOOR_SENSOR" in decoded_msg:
                    alarm_type = "DS_DURATION"
                    set_last_alarm_reason("Doors are open for more than 5 seconds (" + device_code + ") - Promaya", alarm_type)
                elif "GSG_MOTION" in decoded_msg:
                    alarm_type = "GSG_MOTION"
                    set_last_alarm_reason("Gun safe motion detected (" + device_code + ")", alarm_type)

                info = {
                    "alarm_reason": get_last_alarm_reason(alarm_type),
                    "does_alarm_work": True,
                    "alarm_type": alarm_type
                }
                socketio_app.emit('alarm_status', json.dumps(info))
                
            if decoded_msg == "ALARM_OFF":
                alarm_type = "DS_DURATION"
                deactivate_alarm(alarm_type)
                info = {
                    "alarm_reason": get_last_alarm_reason(alarm_type),
                    "does_alarm_work": False,
                    "alarm_type": alarm_type
                }
                socketio_app.emit('alarm_status', json.dumps(info))
                return

            trigger_alarm(alarm_type)
            return
    
        global pi1_batch_size, pi2_batch_size, pi3_batch_size
        obj = json.loads(decoded_msg)

        if obj["deviceType"] == "4SD":
            pass
            
        elif obj['deviceType'] == "DHT":
            tokens = obj['value'].split("%")
            humidity = tokens[0]
            temperature = tokens[1].split("°")[0].split(",")[1].strip()

            point_temp = Point('temperature').field('_measurement', float(temperature))\
            .time(obj['timestamp'], write_precision=WritePrecision.MS)\
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated', obj['isSimulated'])

            influxdb_write_api.write(bucket='smart_measurements', record=point_temp)

            point_hum = Point('humidity').field('_measurement', float(humidity))\
            .time(obj['timestamp'], write_precision=WritePrecision.MS)\
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated', obj['isSimulated'])

            influxdb_write_api.write(bucket='smart_measurements', record=point_hum)
        else:
            point = Point(obj['measurementName']).field('_measurement', obj['value'])\
            .time(obj['timestamp'], write_precision=WritePrecision.MS)\
            .tag('deviceId', obj['deviceId']).tag('deviceType', obj['deviceType']).tag('isSimulated', obj['isSimulated'])
            influxdb_write_api.write(bucket='smart_measurements', record=point)

        if(obj['deviceType'] == "UDS"):
            obj['value'] = str(obj['value']) + " cm"

        current_measurements[obj["deviceId"]] = obj['value']
        if(obj['deviceType'] == "PIR"):
            if pir_last_motion_timestamp.get(obj['deviceId']) is not None:
                if abs(pir_last_motion_timestamp[obj['deviceId']] - int(obj['timestamp'])) > 5000:
                    current_measurements[obj["deviceId"]] = "NO MOTION"
            else:
                now = time.time() * 1000
                if abs(now - int(obj['timestamp'])) > 5000:
                    current_measurements[obj["deviceId"]] = "NO MOTION"
            pir_last_motion_timestamp[obj['deviceId']] = int(obj['timestamp'])

        if (obj['deviceType'] == "GSG"):
            global last_gsg_ping
            last_gsg_ping = time.time() * 1000

        if(obj['pi'] == 1):
            if pi1_batch_size == 19:
                pi1_batch_size = 0
                send_status_summary()
            else:
                pi1_batch_size += 1
        elif(obj['pi'] == 2):
            if pi2_batch_size == 19:
                pi2_batch_size = 0
                send_status_summary()
            else:
                pi2_batch_size += 1
        else:
            if pi3_batch_size == 19:
                pi3_batch_size = 0
                send_status_summary()
            else:
                pi3_batch_size += 1

@socketio_app.on('rgb_remote')
def handle_message(message):
    command = {
        "value": message
    }
    mqtt.publish("rgb_remote_web", json.dumps(command))


@socketio_app.on('alarm_clock_time')
def handle_message(message):
    with mqtt_scheduler_lock:
        scheduler.add_job(
        id='alarm_buzz_' + str(random.randint(0,10000)),
        func=set_alarm_clock_action,
        trigger='date',
        run_date=datetime.datetime.fromtimestamp(int(message)/1000.0)
)

@socketio_app.on('alarm_clock')
def handle_message_alarm_clock(message):
    mqtt.publish("alarm_clock_buzz", message)


@socketio_app.on('alarm_clock_off')
def handle_alarm_clock_off(message):
    global does_alarm_clock_work
    does_alarm_clock_work = False
    mqtt.publish("alarm_clock_buzz", "STOP")
    

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
            continue
        if key in ["BGRB"]:
            device_type = "RGB"
        if key in ["GLCD"]:
            device_type = "LCD"
        if key in ["GSG"]:
            device_type = "GYRO"
        
        device_with_status =  {
            "type": device_type,
            "id": device["id"],
            "name": device["name"],
            "status": current_measurements[device["id"]]
        }
        devices_and_statuses.append(device_with_status)
    return jsonify(devices_and_statuses)


@app.route('/alarm_clock_status', methods=['GET'])
def get_alarm_clock_status():
    alarm_clock_time = {
        "alarm_clock_time": last_alarm_clock,
        "does_alarm_clock_work": does_alarm_clock_work,
    }
    return jsonify(alarm_clock_time)


@app.route('/alarm_status', methods=['GET'])
def get_alarm_status():
    global alarm_type_with_info
    statuses = []
    for key, val in alarm_type_with_info.items():
        alarm_status = {
            "alarm_reason": val["alarm_reason"],
            "does_alarm_work": val["does_alarm_work"],
            "alarm_type": key
        }
        statuses.append(alarm_status)
    return jsonify(statuses)


@app.route('/alarm_disable/<alarm_type>', methods=['PUT'])
def disable_alarm(alarm_type):
    try:
        data = request.get_json()
        password = data.get("password")
        if(password != super_secret_alarm_password):
            raise Exception
        deactivate_alarm(alarm_type)

        return jsonify({'message': 'Alarm of type ' + alarm_type + ' disabled'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    load_devices()
    initialize_alarm_map()
    scheduler_thread = threading.Thread(target=scheduler.start)
    scheduler_thread.start()
    socketio_app.run(app, debug=False)
    