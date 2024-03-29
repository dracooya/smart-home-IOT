import RPi.GPIO as GPIO
import threading
import time

should_buzz = False

def buzzer_register(pin, pitch, callback_fc, door_buzzer_press_event, door_buzzer_release_event, alarm_buzz_start_event, alarm_buzz_stop_event, stop_event,
                    alarm_on_event, alarm_off_event):
    global should_buzz
    GPIO.setup(pin, GPIO.OUT)
    #Buzz = GPIO.PWM(pin, 440)
    buzz_stop_event = threading.Event()
    
    def buzz(pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(pin, True)
            time.sleep(delay)
            GPIO.output(pin, False)
            time.sleep(delay)


    @door_buzzer_press_event.on
    def buzzer_on() :
        global should_buzz
        callback_fc("PRESSED")
        #Buzz.ChangeFrequency(pitch)
        #Buzz.start(100)
        should_buzz = True
        
    @door_buzzer_release_event.on
    def buzzer_off() :
        global should_buzz
        callback_fc("RELEASED")
        #Buzz.stop()
        should_buzz = False
        buzz_stop_event.set()

    @alarm_buzz_start_event.on
    @alarm_on_event.on
    def alarm_buzzer_start() :
        global should_buzz
        callback_fc("ALARM ON")
        #Buzz.ChangeFrequency(pitch)
        #Buzz.start(100)
        should_buzz = True
        
    @alarm_buzz_stop_event.on
    @alarm_off_event.on
    def alarm_buzzer_stop() :
        global should_buzz
        callback_fc("ALARM OFF")
        #Buzz.stop()
        should_buzz = False
        buzz_stop_event.set()
    
    while True:
        if should_buzz:
            buzz(pitch,0.1)
            time.sleep(1)
        if stop_event.is_set():
            break
        
    
