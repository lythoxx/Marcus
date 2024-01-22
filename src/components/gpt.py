from gpt4all import GPT4All
from config.config import Config

class GPT:

    def __init__(self, name):
        self.name = name
        config = Config.get_config("config")
        self.model = GPT4All(config["gpt_model"], model_path=config["model_path"], device="gpu")

    def prompt(self, prompt):
        session_template = f"Your name is {self.name}. You respond only when your name is said. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only."
        with self.model.chat_session(session_template):
            response = self.model.generate(prompt, max_tokens=1024)
            return response
