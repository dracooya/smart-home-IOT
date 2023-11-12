import threading
from settings import load_settings
from components import button,led
import time
from colorama import Fore
from events.DoorLightOffEvent import DoorLightOffEvent
from events.DoorLightOnEvent import DoorLightOnEvent

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

door_light_on_event = DoorLightOnEvent()
door_light_off_event = DoorLightOffEvent()

def user_input(stop_event):
    while True:
        some_input = input()
        if some_input == "x" or some_input == "X":
            door_light_on_event.trigger()
        if some_input == "z" or some_input == "Z":
            door_light_off_event.trigger()
        
        if stop_event.is_set():
            break

if __name__ == "__main__":
    
    settings = load_settings()
    devices_threads = []
    stop_event = threading.Event()
    print( Fore.MAGENTA + "----------------------------------------------------------------------")
    print( Fore.MAGENTA + "----------------------------SMART HOME APP----------------------------")
    print( Fore.MAGENTA + "----------------------------------------------------------------------")
    
    t2 = threading.Thread(target=user_input, args=(stop_event,), daemon = True)
    t2.start()
    try:
        for key in settings:
            if(key in ["DS1"]):
                button.run_button(settings[key],devices_threads,key,stop_event)
            if(key in ["DL"]):
                led.run_led(settings[key],devices_threads,door_light_on_event, door_light_off_event, stop_event)
        while True:
            pass
            
    except KeyboardInterrupt:
        for thread in devices_threads:
            stop_event.set()

   
