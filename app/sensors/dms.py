import RPi.GPIO as GPIO
import time


def register(pins, callback):
    # these GPIO pins are connected to the keypad
    # change these according to your connections!
    R1 = pins[0]
    R2 = pins[1]
    R3 = pins[2]
    R4 = pins[3]

    C1 = pins[4]
    C2 = pins[5]
    C3 = pins[6]
    C4 = pins[7]

    # Initialize the GPIO pins

    GPIO.setwarnings(False)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    # Make sure to configure the input pins to use the internal pull-down resistors

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # The read_line function implements the procedure discussed in the article
    # It sends out a single pulse to one of the rows of the keypad
    # and then checks each column for changes
    # If it detects a change, the user pressed the button that connects the given line
    # to the detected column

    def read_line(line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(C1) == 1:
            callback(characters[0])
        if GPIO.input(C2) == 1:
            callback(characters[1])
        if GPIO.input(C3) == 1:
            callback(characters[2])
        if GPIO.input(C4) == 1:
            callback(characters[3])
        GPIO.output(line, GPIO.LOW)

    while True:
        # call the read_line function for each row of the keypad
        read_line(R1, ["1", "2", "3", "A"])
        read_line(R2, ["4", "5", "6", "B"])
        read_line(R3, ["7", "8", "9", "C"])
        read_line(R4, ["*", "0", "#", "D"])
        time.sleep(0.2)
