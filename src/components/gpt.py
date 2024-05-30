from openai import OpenAI

from config.config import Config


class GPT:

    def __init__(self):
        self.config = Config.get_config("config")
        self.model = OpenAI(api_key=Config.get_config("config")["openai_key"])
        self.history = list()
        self.history.append({"role": "system", "content": f"Your name is {Config.get_name()}. You are a voice activated AI assistant. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only. Do not read or create code. Instead explain the concepts behind the code. Do not suggest to give links to websites. Your answers will be read out, so do not add links. Answer only in German."})


    def prompt(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        completion = self.model.chat.completions.create(
            model=self.config["gpt_model"],
            messages=self.history,
            max_tokens=500
        )
        self.history.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content
