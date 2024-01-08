current_status = "OFF"
last_mode = "WHITE"
def run_rgb_simulator(callback_fc, rgb_change_event, stop_event,client):
    @rgb_change_event.on
    def change(key):
        global current_status, last_mode
        if(key == "OK"):
            if current_status != "OFF":
                current_status = "OFF"
        elif(key == "0"):
            last_mode = "WHITE"
        elif(key == "1"):
            last_mode = "RED"
        elif(key == "2"):
            last_mode = "GREEN"
        elif(key == "3"):
            last_mode = "BLUE"
        elif(key == "4"):
            last_mode = "YELLOW"
        elif(key == "5"):
            last_mode = "PURPLE"
        elif(key == "6"):
            last_mode = "CYAN"
        elif(key == "*"):
            last_mode = "LUDILO"
        else:
            pass
        current_status = last_mode
        callback_fc(current_status)

    while True:
        if stop_event.is_set():
            client.disconnect()
            break
