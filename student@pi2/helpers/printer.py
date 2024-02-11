import threading
from colorama import Fore
from datetime import datetime


print_lock = threading.Lock()


def print_status(device_code, message):
    with print_lock:
        print(Fore.YELLOW + str(datetime.now()) +
              Fore.WHITE + " --- " + Fore.BLUE + device_code + Fore.WHITE + " : " + Fore.GREEN + message)
