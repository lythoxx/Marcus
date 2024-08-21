import datetime
import os
from json import dump, load


class Config:

    config_path = os.path.join(os.getcwd(), "config")

    @staticmethod
    def config_exists(config):
        return os.path.exists(os.path.join(Config.config_path, f"{config}.json"))

    @staticmethod
    def create_config(config):
        with open(os.path.join(Config.config_path, f"{config}.json"), "w") as f:
            dump({}, f, indent=4)

    @staticmethod
    def set_name(name):
        with open(os.path.join(os.getcwd(), "config", "setup.json"), "r") as f:
            config = load(f)
            config["name"] = name
            with open(os.path.join(os.getcwd(), "config", "setup.json"), "w") as f:
                dump(config, f, indent=4)

    @staticmethod
    def get_config(config):
        with open(os.path.join(Config.config_path, f"{config}.json"), "r") as f:
            config = load(f)
            return config

    @staticmethod
    def set_alarm(time, days:str=None):
        with open(os.path.join(Config.config_path, "task.json"), "r") as f:
            tasks = load(f)
        with open(os.path.join(Config.config_path, "task.json"), "w") as f:
            if days:
                if datetime.datetime.strptime(time, "%H:%M") < datetime.datetime.now():
                    pending = True
                tasks["recurring_alarms"].append({"time": time, "days": days, "pending": pending})
                dump(tasks, f, indent=4)
            else:
                if datetime.datetime.strptime(time, "%H:%M") < datetime.datetime.now():
                    pending = True
                tasks["alarms"]["unnamed"].append({"time": time, "pending": pending})
                dump(tasks, f, indent=4)

    @staticmethod
    def get_alarms():
        with open(os.path.join(Config.config_path, "task.json"), "r") as f:
            tasks = load(f)
            return tasks["alarms"]
        
    @staticmethod
    def get_recurring_alarms():
        with open(os.path.join(Config.config_path, "task.json"), "r") as f:
            tasks = load(f)
            return tasks["recurring_alarms"]

    @staticmethod
    def remove_alarm(index):
        with open(os.path.join(Config.config_path, "task.json"), "r") as f:
            config = load(f)
            config["alarms"].remove(index)
            with open(os.path.join(Config.config_path, "task.json"), "w") as f:
                dump(config, f, indent=4)
