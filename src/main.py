import os
import threading
import time
from json import dumps, dump

from config.config import Config
from src.components.commands import Commands
from src.components.gpt import GPT
from src.components.processor import Processor
from src.components.speech import Speech
from src.components.tts import TTS
from src.components.training import train_intent_model, DATA_DE, DATA_EN

import src.utils as utils

stop_alarm_event = threading.Event()

async def main():
    if not Config.config_exists("config"):
        with open(os.path.join(os.getcwd(), "config", "config.json"), "w") as f:
            config = {
                "config_path": os.path.join(os.getcwd(), "config"),
                "asset_path": os.path.join(os.getcwd(), "src", "components", "assets"),
                "model_path": os.path.join(os.getcwd(), "src", "components", "models"),
                "log_path": os.path.join(os.getcwd(), "logs"),
                "gpt_model": "gpt-4.1-nano",
            }
            print("Hello! I see this is your first time running Marcus.")
            print("Let's get started by setting up some configurations.")
            print("First, let's set the language you want to use.")
            print("Currently, Marcus only supports English and German.")
            language = input("Please enter 'en' for English or 'de' for German: ").lower().strip()
            while language not in ["en", "de"]:
                language = input("Invalid input. Please enter 'en' for English or 'de' for German: ").lower().strip()
            config["language"] = language
            print(Config.get_config("text")[language]["setup"]["language_set"])
            print(Config.get_config("text")[language]["setup"]["api_keys"][0])
            print(Config.get_config("text")[language]["setup"]["api_keys"][1])
            openai_key = input(Config.get_config("text")[language]["setup"]["api_keys"][2])
            config["openai_key"] = openai_key.strip()
            azure_key = input(Config.get_config("text")[language]["setup"]["api_keys"][3])
            config["azure_key"] = azure_key.strip()
            weather_key = input(Config.get_config("text")[language]["setup"]["api_keys"][4])
            config["weather_key"] = weather_key.strip()
            print(Config.get_config("text")[language]["setup"]["api_keys"][5])
            print(Config.get_config("text")[language]["setup"]["training"])
            dump(config, f, indent=4)

        current_time = time.time()
        train_intent_model(DATA_DE, "de_core_news_md", model_path="src/components/models/intent_model_de", n_iter=20)
        utils.log_training(
            model_name="intent_model_de",
            iterations=20,
            duration=time.time() - current_time
        )
        current_time = time.time()
        train_intent_model(DATA_EN, "en_core_web_md", model_path="src/components/models/intent_model_en", n_iter=20)
        utils.log_training(
            model_name="intent_model_en",
            iterations=20,
            duration=time.time() - current_time
        )
        print(Config.get_config("text")[language]["setup"]["finished"])
    if not Config.config_exists("task"):
        with open(os.path.join(os.getcwd(), "config", "task.json"), "w") as f:
            dump({
                "alarms": [],
                "recurring_alarms": []
            }, f, indent=4)

    task_thread = threading.Thread(target=utils.check_tasks, daemon=True, args=(stop_alarm_event,))

    print("Starting...")
    speech = Speech()
    print("Speech initialized")
    tts = TTS()
    print("TTS initialized")
    gpt = GPT()
    print("GPT initialized")
    processor = Processor()
    print("Processor initialized")
    language = Config.get_config("config")["language"]
    await tts.speak_openai(Config.get_config("text")[language]["greeting"])

    # task_thread.start()

    while True:
        user_input = speech.recognize_hotword()
        if user_input:
            intent = processor.process_input(user_input)
            print(f"Intent: {intent[0]}, Score: {intent[1]}")
            if intent[0] in [None, "AI"]:
                response = gpt.prompt(user_input)
                await tts.speak_openai(response)
                utils.log_query(user_input, response, intent[0])
            else:
                keywords, entities, times, all_keywords = processor.process_keywords(user_input)
                args = [user_input, keywords, entities, times, all_keywords]
                try:
                    await Commands.execute(intent[0], args)
                except Exception as e:
                    print(f"Error executing command: {e.__class__.__name__}")
                    print(f"Error message: {e}")
                    await tts.speak_openai(Config.get_config("text")[language]["commands"]["error"])
                    utils.log_error(f"{e.__class__.__name__}: {e}", user_input)
                utils.log_query(user_input, "Executed Command", intent[0])