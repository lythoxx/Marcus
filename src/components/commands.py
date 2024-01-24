from enum import Enum

from .speech import Speech
from .tts import TTS

from config.config import Config

import spacy
import sys
from dateutil import parser


class Commands(Enum):
    SETUP = ("setup","set up")
    HELP = ("help",)
    EXIT = ("exit",)
    TEST = ("test",)
    ALARM = ("alarm", "wake")
    STOP_ALARM = ("stop", "stop alarm")

    def get_command(keywords: list, entities: list, all_keywords: list):
        for keyword in all_keywords:
            print(keyword)
            match(keyword.lower()):
                case "setup":
                    print("Found setup")
                    return Commands.SETUP
                case "set up":
                    print("Found set up")
                    return Commands.SETUP
                case "help":
                    print("Found help")
                    return Commands.HELP
                case "exit":
                    print("Found exit")
                    return Commands.EXIT
                case "test":
                    print("Found test")
                    return Commands.TEST
                case "alarm":
                    print("Found alarm")
                    if "stop" in all_keywords:
                        return Commands.STOP_ALARM
                    return Commands.ALARM
                case "wake":
                    print("Found wake")
                    return Commands.ALARM
                case "stop":
                    print("Found stop")
                    return Commands.STOP_ALARM
                case "stop alarm":
                    print("Found stop alarm")
                    return Commands.STOP_ALARM
        else:
            return None

    def run_command(command, all_keywords=None, times=None) -> bool:
        match(command):
            case Commands.SETUP:
                return Commands.setup()
            case Commands.HELP:
                return Commands.help()
            case Commands.EXIT:
                return Commands.exit()
            case Commands.TEST:
                return Commands.test()
            case Commands.ALARM:
                return Commands.alarm(times)
            case _:
                return False


    def setup() -> bool:
        Config.create_config("setup")
        nlp = spacy.load("en_core_web_sm")
        tts = TTS()
        speech = Speech()
        tts.speak_openai("Starting setup.")
        tts.speak_openai("Please tell me my name.")
        user_input = speech.recognize()
        if user_input:
            doc = nlp(user_input)
            entities = [ent.text for ent in doc.ents]
            print(entities)
            if len(entities) > 1:
                tts.speak_openai("It seems you provided more than one name.")
                tts.speak_openai("I will use the first name provided.")
                tts.speak_openai("Set name to " + entities[0])
                tts.speak_openai("You can change the name anytime again.")
                Config.set_name(entities[0])
            elif len(entities) == 0:
                tts.speak_openai("No name provided. I will use the default name.")
                tts.speak_openai("Set name to Marcus")
                tts.speak_openai("You can change the name anytime again.")
                Config.set_name("Marcus")
            else:
                Config.set_name(entities[0])
                tts.speak_openai("Set name to " + entities[0])
                tts.speak_openai("You can change the name anytime again.")
        else:
            tts.speak_openai("No name provided. I will use the default name.")
            tts.speak_openai("Set name to Marcus")
            tts.speak_openai("You can change the name anytime again.")
            Config.set_name("Marcus")

        tts.speak_openai("Setup complete.")

        return True

    def help() -> bool:
        return True

    def exit():
        tts = TTS()
        tts.speak_openai("Goodbye. I hope I was helpful.")
        sys.exit(0)

    def test() -> bool:
        tts = TTS()
        tts.speak_openai("You activated the test command")
        tts.speak_openai("It worked!")
        tts.speak_openai("Test completed")
        return True

    def alarm(times) -> bool:
        print(times)
        tts = TTS()
        if len(times) == 0:
            tts.speak_openai("It seems you didn't provide a time for the alarm.")
            tts.speak_openai("Please provide a time when setting an alarm.")
            return False
        time = times[0]
        if len(times) > 1:
            tts.speak_openai("It seems you provided more than one time. I will use the first time provided.")
        try:
            alarm_time = parser.parse(time)
        except ValueError:
            tts.speak_openai("It seems you provided an invalid time. Please provide a valid time.")
            return False

        print(alarm_time.strftime("%H:%M:%S"))
        tts.speak_openai("Do you want to set a name for the alarm?")
        speech = Speech()
        answer = speech.recongnize_no_hotword()
        if answer:
            if "no" in answer.lower():
                Config.set_alarm(alarm_time.strftime("%H:%M:%S"))
                tts.speak_openai("Alarm set to " + alarm_time.strftime("%H:%M:%S") + ".")
            else:
                name = answer
                Config.set_alarm(alarm_time.strftime("%H:%M:%S"), name)
                tts.speak_openai("Alarm set to " + alarm_time.strftime("%H:%M:%S") + " with name " + name + ".")
        else:
            Config.set_alarm(alarm_time.strftime("%H:%M:%S"))
            tts.speak_openai("Alarm set to " + alarm_time.strftime("%H:%M:%S") + ".")
        return True
