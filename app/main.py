import threading
from settings import load_settings
from components.button import run_button
import time
from events.DoorLightOnEvent import DoorLightOnEvent
from events.DoorLightOffEvent import DoorLightOffEvent

from colorama import Fore
from playsound import playsound


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

door_light_on_event = DoorLightOnEvent()
door_light_off_rvent = DoorLightOffEvent()

devices_threads = []


@door_light_on_event.on
def doInput(num):
    print(Fore.RED + "OFFED DA BUZZER " + str(num))


def screen_output():
    while True:
        print(Fore.GREEN + "\nNEKO STANJE BZZZ")
        time.sleep(0.5)


def user_input():
    while True:
        some_input = input()
        if some_input == "x":
            door_light_on_event.trigger("1")

if __name__ == "__main__":
    
    settings = load_settings()
    print( Fore.MAGENTA + "----------------------------------------------------------------------")
    print( Fore.MAGENTA + "----------------------------SMART HOME APP----------------------------")
    print( Fore.MAGENTA + "----------------------------------------------------------------------")
    stop_event = threading.Event()
    #t1 = threading.Thread(target=screen_output, daemon = True)
    #t2 = threading.Thread(target=user_input, daemon = True)
    #t1.start()
    #t2.start()
    try:
        run_button(settings["DS1"],devices_threads,"DS1",stop_event)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for thread in devices_threads:
            stop_event.set()

   
