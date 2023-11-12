import RPi.GPIO as GPIO
import time


def get_distance(pins):
    trig_pin = pins[0]
    echo_pin = pins[1]

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, False)
    time.sleep(0.2)
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

    iter = 0
    while GPIO.input(echo_pin) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(echo_pin) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300)/2
    return distance

def run_uds_loop(pins, uds_code, callback, stop_event, delay):
    while True:
        distance = get_distance(pins)
        if distance is not None:
            callback(uds_code, f'DISTANCE: {distance} cm')
        else:
            callback(uds_code, 'MEASUREMENT TIMED OUT')
        if stop_event.is_set():
            break
        time.sleep(delay)
