import os
import threading
from json import dump

from config.config import Config
from src.components.commands import Commands
from src.components.gpt import GPT
from src.components.interface.interface import run
from src.components.processor import Processor
from src.components.speech import Speech
from src.components.tts import TTS
from src.utils import check_tasks

stop_alarm_event = threading.Event()
stop_music_event = threading.Event()

music_thread = None

def play_music_thread(query, stop_music_event, type="songs"):
    Commands.play_music(query, stop_music_event, type)

def manage_music_thread(command, user_input):
    global music_thread

    if command == Commands.PLAY_MUSIC:
        query_parts = user_input.lower().split("play", 1)
        music_query = {"query": query_parts[1]}

        if music_thread is not None and music_thread.is_alive():
            stop_music_event.set()
            music_thread.join()

        stop_music_event.clear()
        music_thread = threading.Thread(target=play_music_thread, daemon=True, args=(music_query, stop_music_event))
        music_thread.start()

    elif command == Commands.STOP:
        if music_thread is not None and music_thread.is_alive():
            stop_music_event.set()
            music_thread.join()

def main():
    if not Config.config_exists("config"):
        with open(os.path.join(os.getcwd(), "config", "config.json"), "w") as f:
            config = {
                "config_path": os.path.join(os.getcwd(), "config"),
                "asset_path": os.path.join(os.getcwd(), "src", "components", "assets"),
                "model_path": os.path.join(os.getcwd(), "src", "components", "models"),
                "gpt_model_local": "mistral-7b-openorca.Q4_0.gguf",
                "gpt_model": "gpt-4-1106-preview",
            }
            dump(config, f, indent=4)
    if not Config.config_exists("task"):
        with open(os.path.join(os.getcwd(), "config", "task.json"), "w") as f:
            dump({
                "alarms": {
                    "unnamed": []
                }
            }, f, indent=4)

    task_thread = threading.Thread(target=check_tasks, daemon=True, args=(stop_music_event,))
    interface_thread = threading.Thread(target=run, daemon=True)

    speech = Speech()
    tts = TTS()
    # if not os.path.exists(os.path.join(os.getcwd(), "src", "components", "models", "mistral-7b-openorca.Q4_0.gguf")):
    #     tts.speak_openai("Downloading AI model...")
    gpt = GPT()
    processor = Processor()
    tts.speak_openai(f"Mein Name ist {Config.get_name()}. Wie kann ich behilflich sein?")

    task_thread.start()
    interface_thread.start()

    while True:
        user_input = speech.recognize_hotword()
        if user_input:
            print(user_input)
            # tts.speak_local(user_input)
            keywords, entities, times, all_keywords = processor.process_keywords(user_input)
            command = processor.process_command(keywords, entities, all_keywords)
            if command == None:
                print("Asking AI")
                tts.speak_openai(gpt.prompt(user_input))
            elif command:
                print("Running command")
                if command == Commands.STOP:
                    # TODO ALARM CHECKING
                    manage_music_thread(command, user_input)
                elif command == Commands.PLAY_MUSIC:
                    manage_music_thread(command, user_input)
                else:
                    Commands.run_command(command, all_keywords, times)
            else:
                print("Nothing happened")
                pass
