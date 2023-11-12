import RPi.GPIO as GPIO
import threading
import time

buzz_stop_event = threading.Event()

def buzzer_register(pin, pitch, callback_fc,door_buzzer_press_event, door_buzzer_release_event):
    GPIO.setup(pin, GPIO.OUT)
    Buzz = GPIO.PWM(pin, 440)

    @door_buzzer_press_event.on
    def buzzer_on() :
        Buzz.ChangeFrequency(pitch)
        Buzz.start(100)
        callback_fc("PRESSED")
        while True:
            time.sleep(10000000000000)
            if buzz_stop_event.is_set():
                break

    @door_buzzer_release_event.on
    def buzzer_off() :
        callback_fc("RELEASED")
        Buzz.stop()
        buzz_stop_event.set()
        
    
