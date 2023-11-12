
def run_led_simulator(callback_fc,door_light_on_event, door_light_off_event, stop_event):

    @door_light_on_event.on
    def light_on() :
        callback_fc("ON")

    @door_light_off_event.on
    def light_off() :
        callback_fc("OFF")

    while True:
        if stop_event.is_set():
                break
