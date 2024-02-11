#!/usr/bin/env python3

from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO
from broker_config.broker_settings import HOSTNAME, PORT
from helpers.printer import print_status

to_display = "Hello World!"


def register(code, pins, callback):
    import paho.mqtt.client as mqtt

    def on_connect(client, userdata, flags, rc):
        print_status(code, "Connected to MQTT broker with result code " + str(rc))
        client.subscribe("GDHT")

    def on_message(client, userdata, msg):
        change_display(msg.payload.decode())

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOSTNAME, PORT)

    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    mcp = None
    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print('I2C Address Error !')
            exit(1)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=pins[0], pin_e=pins[1], pins_db=pins[2:], GPIO=mcp) # 0, 2, 4, 5, 6, 7
    try:
        mcp.output(3, 1)  # turn on LCD backlight
        lcd.begin(16, 2)  # set number of LCD lines and columns
        # lcd.clear()
        lcd.setCursor(0, 0)  # set cursor position
        global to_display
        lcd.message(to_display)  # display CPU temperature
        callback(to_display)
    except KeyboardInterrupt:
        lcd.clear()

    client.loop_start()

    def change_display(new_display):
        global to_display
        to_display = new_display
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.message(to_display)  # display CPU temperature
        callback(to_display)
