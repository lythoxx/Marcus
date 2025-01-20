import datetime
import os
import socket
import time
import uuid

import audioread
import pyaudio
import requests
from playsound import playsound

from config.config import Config


def check_tasks(stop_alarm_event):
    # TODO IMPLEMENT ALL KINDS OF ALARMS
    # TODO IMPLEMENT PROPER ALARMS LOGIC (SCHEDULED)
    # TODO IMPLEMENT ALARMS FOR EARLIER TIME OF DAY
    while True:
        today = datetime.date.today()
        alarms = Config.get_alarms()
        recurring_alarms = Config.get_recurring_alarms()
        for alarm in alarms:
            time_object = datetime.datetime.strptime(alarm["time"], "%H:%M:%S").time()
            if datetime.datetime.now().time() >= time_object:
                print("An alarm is due!")  # Replace with actual task action
                while not stop_alarm_event.wait(timeout=1):
                    print("Playing alarm sound")
                    playsound("src/components/assets/sounds/beep-beep-6151.mp3")
                    time.sleep(0.5)

                print("Alarm stopped by user.")
                Config.remove_alarm(alarm.index())
                stop_alarm_event.clear()
                break

        for recurring_alarm in recurring_alarms:
            time_object = datetime.datetime.strptime(recurring_alarm["time"], "%H:%M:%S").time()
            if datetime.datetime.now().time() >= time_object:
                for day in recurring_alarm["days"].split(","):
                    if today.strftime("%A").lower() == day.lower():
                        print("An alarm is due!")  # Replace with actual task action
                        while not stop_alarm_event.wait(timeout=1):
                            print("Playing alarm sound")
                            playsound("src/components/assets/sounds/beep-beep-6151.mp3")
                            time.sleep(0.5)

                        print("Alarm stopped by user.")
                        recurring_alarm["pending"] = True
                        stop_alarm_event.clear()
                        break

        time.sleep(10)  # Wait for 10 seconds before checking again

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def play_mp3(file_path, stop_music_event):
    with audioread.audio_open(file_path) as audio_file:
        # Initialize PyAudio
        py_audio = pyaudio.PyAudio()

        # Open an audio stream with the appropriate settings
        stream = py_audio.open(
            format=py_audio.get_format_from_width(2),
            channels=audio_file.channels,
            rate=audio_file.samplerate,
            output=True
        )

        # Read and play the audio file in chunks
        for audio_chunk in audio_file:
            if stop_music_event.is_set():
                break
            stream.write(audio_chunk)

        # Close the stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        py_audio.terminate()
        os.remove(file_path)

def check_midnight():
    current_time = datetime.dateime.now().time()
    midnight = datetime.datetime.combine(datetime.datetime.now(), datetime.time(0, 0, 0))
    time_range = datetime.timedelta(seconds=30)
    is_near_midnight = (midnight - time_range) <= current_time <= (midnight + time_range)
    return is_near_midnight


def get_weather_descriptions(code: int, main: str) -> str | None:
    match main:
        case "Thunderstorm":
            match code:
                case 200:
                    return "Gewitter mit leichtem Regen"
                case 201:
                    return "Gewitter mit Regen"
                case 202:
                    return "Gewitter mit starkem Regen"
                case 210:
                    return "Leichtem Gewitter"
                case 211:
                    return "Gewitter"
                case 212:
                    return "Starkem Gewitter"
                case 221:
                    return "Schwerem Gewitter"
                case 230:
                    return "Gewitter mit leichtem Niesel"
                case 231:
                    return "Gewitter mit Niesel"
                case 232:
                    return "Gewitter mit starkem Niesel"
                case _:
                    return None
        case "Drizzle":
            match code:
                case 300:
                    return "Leichtem Niesel"
                case 301:
                    return "Niesel"
                case 302:
                    return "Starkem Niesel"
                case 310:
                    return "Leichtem Nieselregen"
                case 311:
                    return "Nieselregen"
                case 312:
                    return "Starkem Nieselregen"
                case 313 | 321:
                    return "Sprühregen"
                case 314:
                    return "Starkem Sprühregen"
                case _:
                    return None
        case "Rain":
            match code:
                case 500:
                    return "Leichtem Regen"
                case 501:
                    return "Regen"
                case 502:
                    return "Starkem Regen"
                case 503:
                    return "Sehr starkem Regen"
                case 504:
                    return "Schwerem Regen"
                case 511:
                    return "Gefrierendem Regen"
                case 520:
                    return "Leichtem Sprühregen"
                case 521:
                    return "Sprühregen"
                case 522 | 531:
                    return "Starkem Sprühregen"
                case _:
                    return None
        case "Snow":
            match code:
                case 600 | 620:
                    return "Leichtem Schneefall"
                case 601 | 621:
                    return "Schneefall"
                case 602 | 622:
                    return "Starkem Schneefall"
                case 611 | 616:
                    return "Schneeregen"
                case 612 | 615:
                    return "Leichtem Schneeregen"
                case 613:
                    return "Starkem Schneeregen"
                case _:
                    return None
        case "Clear":
            return "Klarem Himmel"
        case "Clouds":
            match code:
                case 801:
                    return "Wenigen Wolken"
                case 802:
                    return "Leicht Bewölktem Himmel"
                case 803:
                    return "Bewölktem Himmel"
                case 804:
                    return "Stark bewölktem Himmel"
                case _:
                    return None
        case _: # 7xx codes
            match code:
                case 701:
                    return "Nebel"
                case 711:
                    return "Rauch"
                case 721:
                    return "Dunst"
                case 731 | 761:
                    return "Verstaubter Luft"
                case 741:
                    return "Starkem Nebel"
                case 751:
                    return "Sandstürmen"
                case 762:
                    return "Vulkanasche in der Luft"
                case 771:
                    return "Sturm"
                case 781:
                    return "Tornados"
                case _:
                    return None