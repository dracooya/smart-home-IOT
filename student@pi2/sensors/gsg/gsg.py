import math

import sensors.gsg.MPU6050 as MPU6050
import time

movement_threshold = 2.0
movement_threshold_accel = 1.5

mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
accel = [0] * 3  # store accelerometer data
gyro = [0] * 3  # store gyroscope data


def setup():
    mpu.dmp_initialize()    #initialize MPU6050


def calculate_vector_magnitude(accel_data):
    return math.sqrt(sum(value ** 2 for value in accel_data))


def is_significant_movement_accel(accel_data):
    return calculate_vector_magnitude(accel_data) > movement_threshold_accel


def is_significant_movement(gyro_data):
    return any(abs(value) > movement_threshold for value in gyro_data)


def loop(callback, stop_event):
    while True:
        accel = mpu.get_acceleration()  # get accelerometer data
        gyro = mpu.get_rotation()  # get gyroscope data
        motion = is_significant_movement(gyro) or is_significant_movement_accel(accel)
        if motion:
            callback("MOTION")
        time.sleep(0.1)
        if stop_event.is_set():
            break


def register(callback, stop_event):
    print("GSG is starting...")
    setup()
    try:
        loop(callback, stop_event)
    except KeyboardInterrupt:
        pass
