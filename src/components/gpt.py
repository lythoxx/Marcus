from openai import OpenAI

from config.config import Config


class GPT:

    def __init__(self):
        self.config = Config.get_config("config")
        self.model = OpenAI(api_key=Config.get_config("config")["openai_key"])
        self.history = list()
        self.history.append({"role": "system", "content": "Your name is Marcus. You are a voice activated AI assistant. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only. Do not read or create code. Instead explain the concepts behind the code. Do not suggest to give links to websites. Your answers will be read out, so do not add links. Answer only in German. Give short and precise answers."})

    def cleanup_history(self):
        if len(self.history) > 50:
            system = self.history[0]
            self.history = [system]
            self.history = self.history[-50:]

    def prompt(self, prompt):
        self.cleanup_history()
        self.history.append({"role": "user", "content": prompt})
        completion = self.model.chat.completions.create(
            model=self.config["gpt_model"],
            messages=self.history,
            max_tokens=1024
        )
        self.history.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content