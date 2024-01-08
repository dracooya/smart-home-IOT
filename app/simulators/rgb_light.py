def run_rgb_simulator(callback_fc, rgb_change_event, rgb_off_event, stop_event):
    @rgb_off_event.on
    def rgb_off():
        callback_fc("OFF")

    @rgb_change_event.on
    def change(mode):
        callback_fc(mode)

    while True:
        if stop_event.is_set():
            break
