from gpt4all import GPT4All
from config.config import Config
from openai import OpenAI

class GPT:

    # def __init__(self, name):
    #     self.name = name
    #     config = Config.get_config("config")
    #     self.model = GPT4All(config["gpt_model"], model_path=config["model_path"], device="gpu")

    # def prompt(self, prompt):
    #     session_template = f"Your name is {self.name}. You respond only when your name is said. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only."
    #     with self.model.chat_session(session_template):
    #         response = self.model.generate(prompt, max_tokens=500)
    #         return response

    def __init__(self):
        config = Config.get_config("config")
        self.model = OpenAI(api_key=config["openai_api_key"])

    def prompt(self, prompt):
        completion = self.model.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Your name is {Config.get_name()}. You respond only when your name is said. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return completion.choices[0].message.content

