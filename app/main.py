import threading

from colorama import Fore

from components import button, led, uds, buzzer, pir, dht, dms, fourSD, infrared, rgb_light
from events.BuzzerPressEvent import BuzzerPressEvent
from events.BuzzerReleaseEvent import BuzzerReleaseEvent
from events.DoorLightOffEvent import DoorLightOffEvent
from events.DoorLightOnEvent import DoorLightOnEvent
from events.RGBOffEvent import RGBOffEvent
from events.RGBChangeEvent import RGBChangeEvent
from settings import load_settings
from mqtt_publisher import publisher_task
import sys

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

door_light_on_event = DoorLightOnEvent()
door_light_off_event = DoorLightOffEvent()

buzzer_press_event = BuzzerPressEvent()
buzzer_release_event = BuzzerReleaseEvent()

rgb_off_event = RGBOffEvent()
rgb_change_event = RGBChangeEvent()


def user_input(stop_event):
    while True:
        some_input = input('\n')
        if some_input == "x" or some_input == "X":
            door_light_on_event.trigger()
        elif some_input == "z" or some_input == "Z":
            door_light_off_event.trigger()
        elif some_input == "o" or some_input == "O":
            buzzer_press_event.trigger()
        elif some_input == "p" or some_input == "P":
            buzzer_release_event.trigger()
        elif some_input == "q" or some_input == "Q":
            rgb_off_event.trigger()
        elif some_input == "w" or some_input == "W":
            rgb_change_event.trigger("1")
        else:
            pass

        if stop_event.is_set():
            break


def main():
    settings_file = sys.argv[1]
    settings = load_settings(settings_file)
    devices_threads = []
    stop_event = threading.Event()
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    print(Fore.MAGENTA + "----------------------------SMART HOME APP----------------------------")
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    print(Fore.LIGHTCYAN_EX + " x/X turns on the door light.")
    print(Fore.LIGHTCYAN_EX + " z/Z turns off the door light.")
    print(Fore.LIGHTCYAN_EX + " o/O turns on the door buzzer.")
    print(Fore.LIGHTCYAN_EX + " p/P turns off the door buzzer.")
    print(Fore.LIGHTCYAN_EX + " q/Q turns off the bedroom RGB light.")
    print(Fore.LIGHTCYAN_EX + " w/W turns on the bedroom RGB light.")
    print(Fore.MAGENTA + "----------------------------------------------------------------------")
    t2 = threading.Thread(target=user_input, args=(stop_event,), daemon=True)
    t2.start()
    publisher_thread = threading.Thread(target=publisher_task, args=(stop_event,), daemon=True)
    publisher_thread.start()
    try:
        for key in settings:
            if key in ["DS1", "DS2"]:
                button.run_button(key, settings[key], devices_threads, stop_event)
            if key in ["DL"]:
                led.run_led(key, settings[key], devices_threads, door_light_on_event, door_light_off_event, stop_event)
            if key in ["DUS1", "DUS2"]:
                uds.run_uds(key, settings[key], devices_threads, stop_event)
            if key in ["DB","BB"]:
                buzzer.run_buzzer(key, settings[key], devices_threads, buzzer_press_event, buzzer_release_event,
                                  stop_event)
            if key in ["DPIR1", "DPIR2", "RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
                pir.run(key, settings[key], devices_threads, stop_event)
            if key in ["RDHT1", "RDHT2", "RDHT3", "RDHT4", "GDHT"]:
                dht.run(key, settings[key], devices_threads, stop_event)
            if key in ["DMS"]:
                dms.run(key, settings[key], devices_threads, stop_event)
            if key in ["B4SD"]:
                fourSD.run(key, settings[key], devices_threads, stop_event)
            if key in ["BIR"]:
                infrared.run(key, settings[key], devices_threads, stop_event)
            if key in ["BGRB"]:
                rgb_light.run(key, settings[key], devices_threads, rgb_off_event, rgb_change_event, stop_event)
            
        while True:
            pass

    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()
