import datetime
import socket
import time

import fuzzy
from playsound import playsound

from config.config import Config


def check_tasks(stop_alarm_event):
    while True:
        alarms = Config.get_alarms()
        for unnamed in alarms["unnamed"]:
            time_object = datetime.datetime.strptime(unnamed, "%H:%M:%S").time()
            if datetime.datetime.now().time() >= time_object:
                print("An alarm is due!")  # Replace with actual task action
                while not stop_alarm_event.wait(timeout=1):
                    print("Playing alarm sound")
                    playsound("src/components/assets/sounds/beep-beep-6151.mp3")
                    time.sleep(0.5)

                print("Alarm stopped by user.")
                Config.remove_alarm("unnamed", alarms["unnamed"][alarms["unnamed"].index(unnamed)])
                stop_alarm_event.clear()
                break

        time.sleep(10)  # Wait for 10 seconds before checking again


def phonetic_compare(string_1: str, string_2: str):
    soundex = fuzzy.Soundex(4)
    return soundex(string_1) == soundex(string_2)

def get_phonetic(string):
    soundex = fuzzy.Soundex(4)
    return soundex(string)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]