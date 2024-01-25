from openai import OpenAI

from config.config import Config


class GPT:

    def __init__(self):
        self.config = Config.get_config("config")
        self.model = OpenAI(api_key=Config.get_config("config")["openai_key"])

    def prompt(self, prompt):
        completion = self.model.chat.completions.create(
            model=self.config["gpt_model"],
            messages=[
                {"role": "system", "content": f"Your name is {Config.get_name()}. You are a voice activated AI assistant. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only. Do not read or create code. Instead explain the concepts behind the code. Do not suggest to give links to websites. Your answers will be read out, so do not add links. Make sure that your answer stays below 500 tokens. Being below 200 tokens would be optimal."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return completion.choices[0].message.content
