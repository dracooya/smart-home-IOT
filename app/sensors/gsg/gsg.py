#!/usr/bin/env python3
import MPU6050 
import time
import os


def register(callback):
    mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
    accel = [0] * 3  # store accelerometer data
    gyro = [0] * 3  # store gyroscope data
    mpu.dmp_initialize()    #initialize MPU6050
    while True:
        accel = mpu.get_acceleration()  # get accelerometer data
        gyro = mpu.get_rotation()  # get gyroscope data
        motion = False
        if motion:
            callback("MOTION")
        time.sleep(0.1)

