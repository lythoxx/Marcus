from src.utils import check_tasks
from src.components.commands import Commands
from src.components.gpt import GPT
from src.components.speech import Speech
from src.components.tts import TTS
from src.components.processor import Processor
from config.config import Config
from json import dump

import os
import threading

stop_alarm_event = threading.Event()

def main():
    if not Config.config_exists("config"):
        with open(os.path.join(os.getcwd(), "config", "config.json"), "w") as f:
            config = {
                "config_path": os.path.join(os.getcwd(), "config"),
                "asset_path": os.path.join(os.getcwd(), "src", "components", "assets"),
                "model_path": os.path.join(os.getcwd(), "src", "components", "models"),
                "gpt_model_local": "mistral-7b-openorca.Q4_0.gguf",
                "gpt_model": "gpt-3.5-turbo",
            }
            dump(config, f, indent=4)
    if not Config.config_exists("task"):
        with open(os.path.join(os.getcwd(), "config", "task.json"), "w") as f:
            dump({
                "alarms": {
                    "unnamed": []
                }
            }, f, indent=4)
    if not Config.config_exists("setup"):
        Commands.run_command(Commands.SETUP)

    speech = Speech()
    tts = TTS()
    # if not os.path.exists(os.path.join(os.getcwd(), "src", "components", "models", "mistral-7b-openorca.Q4_0.gguf")):
    #     tts.speak_openai("Downloading AI model...")
    gpt = GPT()
    processor = Processor()
    tts.speak_openai(f"My name is {Config.get_name()}. How can I help you today?")

    task_thread = threading.Thread(target=check_tasks, daemon=True, args=(stop_alarm_event,))
    task_thread.start()

    while True:
        user_input = speech.recognize()
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
                if command == Commands.STOP_ALARM:
                    stop_alarm_event.set()
                    Commands.run_command(command)
                else:
                    Commands.run_command(command, all_keywords, times)
            else:
                print("Nothing happened")
                pass
