import RPi.GPIO as GPIO

def led_register(pin,callback_fc,door_light_on_event, door_light_off_event):

    GPIO.setup(pin,GPIO.OUT)
    
    @door_light_on_event.on
    def light_on() :
        GPIO.output(pin,GPIO.HIGH)
        callback_fc("ON")

    @door_light_off_event.on
    def light_off() :
        GPIO.output(pin,GPIO.LOW)
        callback_fc("OFF")