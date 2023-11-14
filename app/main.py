import threading

from colorama import Fore

from components import button, led, uds, buzzer, pir
from events.BuzzerPressEvent import BuzzerPressEvent
from events.BuzzerReleaseEvent import BuzzerReleaseEvent
from events.DoorLightOffEvent import DoorLightOffEvent
from events.DoorLightOnEvent import DoorLightOnEvent
from settings import load_settings

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

door_light_on_event = DoorLightOnEvent()
door_light_off_event = DoorLightOffEvent()

buzzer_press_event = BuzzerPressEvent()
buzzer_release_event = BuzzerReleaseEvent()


def user_input(stop_event):
    while True:
        some_input = input()
        if some_input == "x" or some_input == "X":
            door_light_on_event.trigger()
        elif some_input == "z" or some_input == "Z":
            door_light_off_event.trigger()
        elif some_input == "o" or some_input == "O":
            buzzer_press_event.trigger()
        elif some_input == "p" or some_input == "P":
            buzzer_release_event.trigger()
        else:
            pass

        if stop_event.is_set():
            break


def main():
    global settings
    settings = load_settings()
    devices_threads = []
    stop_event = threading.Event()
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    print(Fore.MAGENTA + "----------------------------SMART HOME APP----------------------------")
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    print(Fore.LIGHTCYAN_EX + " x/X turns on the door light.")
    print(Fore.LIGHTCYAN_EX + " z/Z turns off the door light.")
    print(Fore.LIGHTCYAN_EX + " o/O turns on the door buzzer.")
    print(Fore.LIGHTCYAN_EX + " p/P turns off the door buzzer.")
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    t2 = threading.Thread(target=user_input, args=(stop_event,), daemon=True)
    t2.start()
    try:
        for key in settings:
            if key in ["DS1"]:
                button.run_button(settings[key], devices_threads, key, stop_event)
            if key in ["DL"]:
                led.run_led(settings[key], devices_threads, door_light_on_event, door_light_off_event, stop_event)
            if key in ["DUS1"]:
                uds.run_uds(settings[key], devices_threads, key, stop_event)
            if key in ["DB"]:
                buzzer.run_buzzer(settings[key], devices_threads, buzzer_press_event, buzzer_release_event, stop_event)
            if key in ["DPIR1", "RPIR1", "RPIR2"]:
                pir.run(settings[key], devices_threads, key, stop_event)
        while True:
            pass

    except KeyboardInterrupt:
        for thread in devices_threads:
            stop_event.set()


if __name__ == "__main__":
    main()
