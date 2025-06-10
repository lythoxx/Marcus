import datetime
import os
import socket
import time
import uuid

import audioread
import pyaudio
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
    language = Config.get_config("config")["language"]
    if code in range(700, 799):
        return Config.get_config("text")[language]["commands"]["weather"]["desc"]["7xx"][code]
    else:
        return Config.get_config("text")[language]["commands"]["weather"]["desc"][main][code]


def log_query(query: str, response: str, intent: str = None):
    log_entry = {
        "query": query,
        "response": response,
        "intent": intent,
        "timestamp": datetime.datetime.now().isoformat(),
        "uuid": str(uuid.uuid4())
    }
    log_path = os.path.join(Config.get_config("config")["asset_path"], "logs", "queries.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a") as log_file:
        log_file.write(f"{log_entry}\n")


def log_error(error: str, query: str = None):
    error_entry = {
        "error": error,
        "query": query,
        "timestamp": datetime.datetime.now().isoformat(),
        "uuid": str(uuid.uuid4())
    }
    log_path = os.path.join(Config.get_config("config")["asset_path"], "logs", "errors.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a") as log_file:
        log_file.write(f"{error_entry}\n")


def log_training(model_name: str, iterations: int, duration: float):
    training_entry = {
        "model_name": model_name,
        "iterations": iterations,
        "duration": duration,
        "timestamp": datetime.datetime.now().isoformat(),
        "uuid": str(uuid.uuid4())
    }
    log_path = os.path.join(Config.get_config("config")["asset_path"], "logs", "training.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a") as log_file:
        log_file.write(f"{training_entry}\n")
