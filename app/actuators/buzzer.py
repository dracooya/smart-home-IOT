import RPi.GPIO as GPIO
import threading
import time

buzz_stop_event = threading.Event()

def buzzer_register(pin, pitch, callback_fc, door_buzzer_press_event, door_buzzer_release_event, stop_event):
    GPIO.setup(pin, GPIO.OUT)
    Buzz = GPIO.PWM(pin, 440)

    @door_buzzer_press_event.on
    def buzzer_on() :
        callback_fc("PRESSED")
        Buzz.ChangeFrequency(pitch)
        Buzz.start(100)
        time.sleep(100000)
        
    @door_buzzer_release_event.on
    def buzzer_off() :
        callback_fc("RELEASED")
        Buzz.stop()
        #buzz_stop_event.set()
    
    while True:
        time.sleep(1000)
        if stop_event.is_set():
            break
        
    
