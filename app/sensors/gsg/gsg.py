import sensors.gsg.MPU6050 as MPU6050 
import time
import os


def register(callback, stop_event):
    mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
    accel = [0] * 3  # store accelerometer data
    gyro = [0] * 3  # store gyroscope data
        #initialize MPU6050
    first_time = True
    while True:
        if first_time:
            mpu.dmp_initialize()
            first_time = False
        accel = mpu.get_acceleration()  # get accelerometer data
        gyro = mpu.get_rotation()  # get gyroscope data
        motion = True
        if motion:
            callback("MOTION, " + str(accel) + " " + str(gyro))
        time.sleep(0.1)
        if stop_event.is_set():
            break


