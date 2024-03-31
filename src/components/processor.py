import re

import spacy

from src import utils

from .commands import Commands


class Processor:

    def __init__(self):
        # Load English tokenizer, tagger, parser, and NER
        self.nlp = spacy.load("en_core_web_sm")

    def process_keywords(self, text):

        text = utils.translate_en(text)

        doc = self.nlp(text)

        time_pattern = re.compile(r'(\d{1,2})\.(\d{2})([ap]m)', re.IGNORECASE)

        # Extract keywords based on part-of-speech tags
        keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN', 'VERB')]

        # Extract named entities
        entities = [ent.text for ent in doc.ents]

        times = [ent.text for ent in doc.ents if ent.label_ == 'TIME']

        for time in times:
            match = time_pattern.search(time)
            if match:
                times[times.index(time)] = f"{match.group(1)}:{match.group(2)}"

        # Combine and deduplicate
        all_keywords = list(set(keywords + entities + times))

        print("All keywords: ", all_keywords)

        return keywords, entities, times, all_keywords

    def process_command(self, keywords: list, entities: list, all_keywords: list):
        return Commands.get_command(keywords, entities, all_keywords)
