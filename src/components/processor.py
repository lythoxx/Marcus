import os

import spacy

from config.config import Config

from .commands import Commands


class Processor:

    def __init__(self):
        # Load English tokenizer, tagger, parser, and NER
        self.nlp = spacy.load("de_core_news_md")

    def process_keywords(self, text):

        # text = utils.translate_en(text)

        doc = self.nlp(text)

        # time_pattern = re.compile(r'(\d{1,2})\.(\d{2})([ap]m)', re.IGNORECASE)

        # Extract keywords based on part-of-speech tags
        keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN', 'VERB')]

        # Extract named entities
        entities = [ent.text for ent in doc.ents]

        times = [ent.text for ent in doc.ents if ent.label_ == 'TIME']

        # for time in times:
            # match = time_pattern.search(time)
            # if match:
                # times[times.index(time)] = f"{match.group(1)}:{match.group(2)}"

        # Combine and deduplicate
        all_keywords = list(set(keywords + entities + times))

        print("All keywords: ", all_keywords)

        return keywords, entities, times, all_keywords


    def process_input(self, text: str):
        # Load the trained intent model
        model_path = os.path.join(os.path.dirname(__file__), "models", f"intent_model_{Config.get_config('config')['language']}")
        nlp_intent = spacy.load(model_path)

        doc = nlp_intent(text)
        # Get the label with the highest score
        if "textcat" in nlp_intent.pipe_names:
            scores = doc.cats
            best_label = max(scores, key=scores.get)
            return best_label, scores[best_label]
        else:
            return None, 0.0


    def process_command(self, keywords: list, entities: list, all_keywords: list):
        return Commands.get_command(keywords, entities, all_keywords)
