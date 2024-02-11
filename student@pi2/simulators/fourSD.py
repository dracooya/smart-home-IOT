import time

should_flicker = False

def run_fourSD_simulator(callback_fc, alarm_buzz_start_event, alarm_buzz_stop_event, stop_event):
    
    @alarm_buzz_start_event.on
    def alarm_flicker_on():
        global should_flicker
        should_flicker = True
        print("SCREEN FLICKERING")
        
    @alarm_buzz_stop_event.on
    def alarm_flicker_off() :
        global should_flicker
        should_flicker = False
        print("SCREEN NOT FLICKERING")

    while True:
        current_time = time.strftime("%H:%M", time.localtime())
        callback_fc("Current time: " + current_time)
        time.sleep(10)
        if stop_event.is_set():
            break