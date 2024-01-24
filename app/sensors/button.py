import RPi.GPIO as GPIO
import time



def button_register(pin,callback_fc, callback_long_fc, callback_release_fc):
    PORT_BUTTON = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    prev_button_state = GPIO.LOW
    button_state = None
    press_time_start = 0
    is_pressing = False
    is_long_detected = False
    LONG_PRESS_TIME = 5
    sent_alarm_alert = False

    while True:
        button_state = GPIO.input(PORT_BUTTON)

        if prev_button_state == GPIO.HIGH and button_state == GPIO.LOW:  # Button is pressed
            press_time_start = time.time()
            is_pressing = True
            is_long_detected = False

        elif prev_button_state == GPIO.LOW and button_state == GPIO.HIGH:  # Button is released
            is_pressing = False
            sent_alarm_alert = False
            callback_fc(press_time_start * 1000)
            if is_long_detected:
                callback_release_fc()

        if is_pressing and not is_long_detected:
            press_duration = time.time() - press_time_start

            if press_duration >= LONG_PRESS_TIME:
                print("A long press is detected")
                is_long_detected = True
                if not sent_alarm_alert:
                    callback_long_fc()
                    sent_alarm_alert = True

        prev_button_state = button_state
    #GPIO.add_event_detect(PORT_BUTTON, GPIO.RISING, callback = callback_fc , bouncetime = 100)