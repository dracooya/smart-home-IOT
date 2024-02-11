import RPi.GPIO as GPIO


def register(pin, motion_callback):
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=motion_callback)
