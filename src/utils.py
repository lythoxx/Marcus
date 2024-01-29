import datetime
import os
import socket
import time

import audioread
import fuzzy
from playsound import playsound
import pyaudio
import requests
import uuid
import json


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
            if alarm["pending"]:
                if check_midnight():
                    alarm["pending"] = False
                else:
                    continue
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
            if recurring_alarm["pending"]:
                if check_midnight():
                    recurring_alarm["pending"] = False
                else:
                    continue
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

def stream_audio(file_path, audio_stream, stop_music_event):
    # Stream audio using PyAudio
    with audioread.audio_open(f"output/{file_path}") as audio_file:
        py_audio = pyaudio.PyAudio()
        stream = py_audio.open(
            format=py_audio.get_format_from_width(2),
            channels=audio_file.channels,
            rate=audio_file.samplerate,
            output=True
        )
        for audio_chunk in audio_file:
            if stop_music_event.is_set():
                break
            stream.write(audio_chunk)
        stream.stop_stream()
        stream.close()
        py_audio.terminate()
        os.remove("output/" + audio_stream.default_filename)

def check_midnight():
    current_time = datetime.dateime.now().time()
    midnight = datetime.datetime.combine(datetime.datetime.now(), datetime.time(0, 0, 0))
    time_range = datetime.timedelta(seconds=30)
    is_near_midnight = (midnight - time_range) <= current_time <= (midnight + time_range)
    return is_near_midnight

def translate_en(text):
    # Add your key and endpoint
    key = Config.get_config("config")["translator_key"]
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "germanywestcentral"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'de',
        'to': ['en',]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    return json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))['translations'][0]['text']