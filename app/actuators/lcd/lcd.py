#!/usr/bin/env python3

from time import sleep

from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO


to_display = "Hello World!"


def register(pins, callback, change_display_event):
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

    @change_display_event
    def change_display(new_display):
        global to_display
        to_display = new_display
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.message(to_display)  # display CPU temperature
        callback(to_display)
