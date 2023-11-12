from playsound import playsound
import threading
import time

stop_event_audio = threading.Event()

def sound_play(stop_event_audio) :
    while True:
        playsound("./sounds/buzzer.mp3")
        if stop_event_audio.is_set():
            break
    

def run_buzzer_simulator(callback_fc,buzzer_press_event, buzzer_release_event, stop_event):
    
    stop_event_audio = threading.Event()
    
    @buzzer_press_event.on
    def buzzer_press() :
        stop_event_audio.clear()
        audio_thread = threading.Thread(target=sound_play,args=(stop_event_audio,))
        audio_thread.start()
        callback_fc("PRESSED")

    @buzzer_release_event.on
    def buzzer_release() :
        stop_event_audio.set()
        callback_fc("RELEASED")

    while True:
        if stop_event.is_set():
                stop_event_audio.set()
                break