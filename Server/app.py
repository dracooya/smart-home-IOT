from flask import Flask
from flask_mqtt import Mqtt

from broker_config import broker_settings

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = broker_settings.HOSTNAME
app.config['MQTT_BROKER_PORT'] = broker_settings.PORT

mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        mqtt.subscribe("measurements")
    else:
        print("Failed to connect to broker, return code", rc)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("Received message: " + message.payload.decode())


@app.route('/')
def poy():
    return 'poy'


if __name__ == '__main__':
    app.run()
