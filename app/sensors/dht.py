import RPi.GPIO as GPIO
import time


class DHT(object):
    DHTLIB_OK = 0
    DHTLIB_ERROR_CHECKSUM = -1
    DHTLIB_ERROR_TIMEOUT = -2
    DHTLIB_INVALID_VALUE = -999

    DHTLIB_DHT11_WAKEUP = 0.020  # 0.018		#18ms
    DHTLIB_TIMEOUT = 0.0001  # 100us

    humidity = 0
    temperature = 0

    def __init__(self, pin):
        self.pin = pin
        self.bits = [0, 0, 0, 0, 0]
        GPIO.setmode(GPIO.BCM)

    # Read DHT sensor, store the original data in bits[]
    def read_sensor(self, pin, wakeupDelay):
        mask = 0x80
        idx = 0
        self.bits = [0, 0, 0, 0, 0]
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(wakeupDelay)
        GPIO.output(pin, GPIO.HIGH)
        # time.sleep(40*0.000001)
        GPIO.setup(pin, GPIO.IN)

        loop_count = self.DHTLIB_TIMEOUT
        t = time.time()
        while GPIO.input(pin) == GPIO.LOW:
            if (time.time() - t) > loop_count:
                # print ("Echo LOW")
                return self.DHTLIB_ERROR_TIMEOUT
        t = time.time()
        while GPIO.input(pin) == GPIO.HIGH:
            if (time.time() - t) > loop_count:
                # print ("Echo HIGH")
                return self.DHTLIB_ERROR_TIMEOUT
        for i in range(0, 40, 1):
            t = time.time()
            while GPIO.input(pin) == GPIO.LOW:
                if (time.time() - t) > loop_count:
                    # print ("Data Low %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT
            t = time.time()
            while GPIO.input(pin) == GPIO.HIGH:
                if (time.time() - t) > loop_count:
                    # print ("Data HIGH %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT
            if (time.time() - t) > 0.00005:
                self.bits[idx] |= mask
            # print("t : %f"%(time.time()-t))
            mask >>= 1
            if mask == 0:
                mask = 0x80
                idx += 1
        # print (self.bits)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        return self.DHTLIB_OK

    # Read DHT sensor, analyze the data of temperature and humidity
    def readDHT11(self):
        rv = self.read_sensor(self.pin, self.DHTLIB_DHT11_WAKEUP)
        if rv is not self.DHTLIB_OK:
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv
        self.humidity = self.bits[0]
        self.temperature = self.bits[2] + self.bits[3] * 0.1
        sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
        if self.bits[4] is not sumChk:
            return self.DHTLIB_ERROR_CHECKSUM
        return self.DHTLIB_OK


def run(pin, callback, stop_event, delay):
    dht = DHT(pin)  # create a DHT class object
    sum_count = 0  # number of reading times
    while True:
        sum_count += 1  # counting number of reading times
        chk = dht.readDHT11()  # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        #callback("The sum_count is : %d, \t chk    : %d" % (sum_count, chk))
        if chk is dht.DHTLIB_OK:  # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            #callback("DHT11,OK!")
            pass
        elif chk is dht.DHTLIB_ERROR_CHECKSUM:  # data check has errors
            callback(-1)
        elif chk is dht.DHTLIB_ERROR_TIMEOUT:  # reading DHT times out
            callback(-2)
        else:  # other errors
            callback(-3)

        if stop_event.is_set():
            break

        callback(dht.humidity, dht.temperature)
        time.sleep(delay)
