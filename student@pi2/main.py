import threading

from colorama import Fore

from components import button, led, uds, buzzer, pir, dht, dms, fourSD, infrared, rgb_light, lcd, gsg
from events.AlarmOffEvent import AlarmOffEvent
from events.AlarmOnEvent import AlarmOnEvent
from events.BuzzerPressEvent import BuzzerPressEvent
from events.BuzzerReleaseEvent import BuzzerReleaseEvent
from events.DoorLightOffEvent import DoorLightOffEvent
from events.DoorLightOnEvent import DoorLightOnEvent
from events.RGBChangeEvent import RGBChangeEvent
from events.AlarmClockOnEvent import AlarmClockOnEvent
from events.AlarmClockOffEvent import AlarmClockOffEvent
import simulators.dms
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

rgb_change_event = RGBChangeEvent()

alarm_clock_on_event = AlarmClockOnEvent()
alarm_clock_off_event = AlarmClockOffEvent()

alarm_on_event = AlarmOnEvent()
alarm_off_event = AlarmOffEvent()


def invalid_input(some_input):
    if len(some_input) != 5:
        return True
    if some_input[-1] != "#":
        return True
    if not some_input[:-1].isdigit():
        return True
    return False


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
        elif '1' in sys.argv[1] and some_input[-1] == "#":  # check that it's pi 1 and that the input is valid
            if invalid_input(some_input):
                print(Fore.RED + "Invalid input! Enter a 4-digit pin code ending with #.")
                continue
            simulators.dms.attempt = some_input
            simulators.dms.send = True
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
            if key in ["DB", "BB"]:
                buzzer.run_buzzer(key, settings[key], devices_threads, buzzer_press_event, buzzer_release_event,
                                  alarm_clock_on_event, alarm_clock_off_event,
                                  stop_event, alarm_on_event, alarm_off_event)
            if key in ["DPIR1", "DPIR2", "RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
                pir.run(key, settings[key], devices_threads, stop_event)
            if key in ["RDHT1", "RDHT2", "RDHT3", "RDHT4", "GDHT"]:
                dht.run(key, settings[key], devices_threads, stop_event)
            if key in ["DMS"]:
                dms.run(key, settings[key], devices_threads, stop_event)
            if key in ["B4SD"]:
                fourSD.run(key, settings[key], devices_threads, alarm_clock_on_event, alarm_clock_off_event, stop_event)
            if key in ["BIR"]:
                infrared.run(key, settings[key], devices_threads, stop_event)
            if key in ["BGRB"]:
                rgb_light.run(key, settings[key], devices_threads, rgb_change_event, stop_event)
            if key in ["GLCD"]:
                lcd.run(key, settings[key], devices_threads, stop_event)
            if key in ["GSG"]:
                gsg.run(key, settings[key], devices_threads, stop_event)

        while True:
            pass

    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()
