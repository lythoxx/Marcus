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
                {"role": "system", "content": f"Your name is {Config.get_name()}. You are a voice activated AI assistant. You are supposed to respond naturally, so do not read out the link to a source, but tell me the name of the source only. Do not read or create code. Instead explain the concepts behind the code. Do not suggest to give links to websites. Your answers will be read out, so do not add links. Answer only in German. When asked your list of features currently consists of: ['Playing music', 'Weather forecast', 'Setting alarms']. You do not execute these features, but instead tell the user that they have to excute the corresponding command to execute these features."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return completion.choices[0].message.content
