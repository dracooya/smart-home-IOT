from colorama import Fore
from datetime import datetime

def printStatus(deviceCode, message):
    print(Fore.YELLOW + str(datetime.now()) +  Fore.WHITE + " --- " + Fore.BLUE + deviceCode + Fore. WHITE + " : " + Fore.GREEN + message)