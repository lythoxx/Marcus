import os
import threading
from json import dump

from config.config import Config
from src.components.commands import Commands
from src.components.gpt import GPT
from src.components.processor import Processor
from src.components.speech import Speech
from src.components.tts import TTS
from src.utils import check_tasks

stop_alarm_event = threading.Event()

def main():
    if not Config.config_exists("config"):
        with open(os.path.join(os.getcwd(), "config", "config.json"), "w") as f:
            config = {
                "config_path": os.path.join(os.getcwd(), "config"),
                "asset_path": os.path.join(os.getcwd(), "src", "components", "assets"),
                "model_path": os.path.join(os.getcwd(), "src", "components", "models"),
                "gpt_model": "gpt-4o-mini",
            }
            dump(config, f, indent=4)
            print("Hello! I see this is your first time running Marcus.")
            print("Let's get started by setting up some configurations.")
            print("First, let's set the language you want to use.")
            print("Currently, Marcus only supports English and German.")
            language = input("Please enter 'en' for English or 'de' for German: ")
            while language not in ["en", "de"]:
                language = input("Invalid input. Please enter 'en' for English or 'de' for German: ")
            Config.set_config("config", "language", language)
            print("Language set successfully!")
            print("Next, let's set the API keys for the services Marcus uses.")
            print("By default, Marcus uses OpenAI and Microsoft Azure for core functionality. OpenWeatherMap is also used for weather data.")
            openai_key = input("Please enter your OpenAI API key: ")
            Config.set_config("config", "openai_key", openai_key)
            azure_key = input("Please enter your Azure API key: ")
            Config.set_config("config", "azure_key", azure_key)
            weather_key = input("Please enter your OpenWeatherMap API key: ")
            Config.set_config("config", "weather_key", weather_key)
            print("API keys set successfully!")
            print("That's it for the initial setup. You can always change these settings manually in the config file.")
    if not Config.config_exists("task"):
        with open(os.path.join(os.getcwd(), "config", "task.json"), "w") as f:
            dump({
                "alarms": [],
                "recurring_alarms": []
            }, f, indent=4)

    task_thread = threading.Thread(target=check_tasks, daemon=True, args=(stop_alarm_event,))

    print("Starting...")
    speech = Speech()
    print("Speech initialized")
    tts = TTS()
    print("TTS initialized")
    gpt = GPT()
    print("GPT initialized")
    processor = Processor()
    print("Processor initialized")
    tts.speak_openai(f"Mein Name ist Marcus. Wie kann ich behilflich sein?")

    task_thread.start()

    while True:
        user_input = speech.recognize_hotword()
        if user_input:
            print(user_input)
            keywords, entities, times, all_keywords = processor.process_keywords(user_input)
            command = processor.process_command(keywords, entities, all_keywords)
            if command == None:
                print("Asking AI")
                tts.speak_openai(gpt.prompt(user_input))
            elif command:
                print("Running command")
                Commands.run_command(command=command, user_input=user_input)
            else:
                print("Nothing happened")
                pass
