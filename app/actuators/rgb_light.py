import RPi.GPIO as GPIO
import threading
import time
import random

ludilo_stop = threading.Event()
last_mode = None
current_status = "WHITE"

def rgb_register(pins, callback_fc, rgb_change_event, stop_event, client):
    global last_mode, current_status
    def white():
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)

    last_mode = white
    
    def red():
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)

    def green():
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        
    def blue():
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        
    def yellow():
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        
    def purple():
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        
    def cyan():
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)

    def turnOff():
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)

    def ludilo():
        while True:
            random_mode = random.randint(0,6)
            if random_mode == 0:
                white()
            elif random_mode == 1:
                red()
            elif random_mode == 2:
                green()
            elif random_mode == 3:
                blue()
            elif random_mode == 4:
                cyan()
            elif random_mode == 5:
                yellow()
            else:
                purple()
            time.sleep(0.5)
            if ludilo_stop.is_set():
                break


    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    RED_PIN = pins[0]
    GREEN_PIN = pins[1]
    BLUE_PIN = pins[2]

    #set pins as outputs
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)

    @rgb_change_event.on
    def change(key):
        global current_status, last_mode
        if(key == "OK"):
            if current_status != "OFF":
                current_status = "OFF"
                last_mode = turnOff
        elif(key == "0"):
            last_mode = white
            current_status = "WHITE"
        elif(key == "1"):
            current_status = "RED"
            last_mode = red
        elif(key == "2"):
            current_status = "GREEN"
            last_mode = green
        elif(key == "3"):
            current_status = "BLUE"
            last_mode = blue
        elif(key == "4"):
            current_status = "YELLOW"
            last_mode = yellow
        elif(key == "5"):
            current_status = "PURPLE"
            last_mode = purple
        elif(key == "6"):
            current_status = "CYAN"
            last_mode = cyan
        elif(key == "*"):
            current_status = "LUDILO"
            last_mode = ludilo
        else:
            pass
        last_mode()
        callback_fc(current_status)
    try:
        while True:
            if stop_event.is_set():
                ludilo_stop.set()
                break
    finally:
        GPIO.cleanup()
        client.disconnect()
