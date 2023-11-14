import RPi.GPIO as GPIO


def button_register(pin,callback_fc):
    PORT_BUTTON = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(PORT_BUTTON, GPIO.RISING, callback = callback_fc , bouncetime = 100)