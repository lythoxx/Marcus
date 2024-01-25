import re

import spacy

from config.config import Config
from src.utils import phonetic_compare

from .commands import Commands


class Processor:

    def __init__(self):
        # Load English tokenizer, tagger, parser, and NER
        self.nlp = spacy.load("en_core_web_sm")

    def process_keywords(self, text):
        doc = self.nlp(text)

        time_pattern = re.compile(r'(\d{1,2})\.(\d{2})([ap]m)', re.IGNORECASE)

        sentences = list(doc.sents)

        for sentence in sentences:
            if Config.get_name() in sentence.text:
                doc = sentence
                break

        # Extract keywords based on part-of-speech tags
        keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN', 'VERB')]

        # Extract named entities
        entities = [ent.text for ent in doc.ents]

        times = [ent.text for ent in doc.ents if ent.label_ == 'TIME']

        # Combine and deduplicate
        all_keywords = list(set(keywords + entities + times))

        print("All keywords: ", all_keywords)

        for keyword in all_keywords:
            if time_pattern.match(keyword):
                keyword = keyword.replace(".", ":")
                times.append(keyword)

        return keywords, entities, times, all_keywords

    def process_command(self, keywords: list, entities: list, all_keywords: list):
        config = Config()
        if config.get_name() in all_keywords or config.get_name().lower() in all_keywords:
            print("Found name")
            return Commands.get_command(keywords, entities, all_keywords)
        else:
            for keyword in all_keywords:
                if phonetic_compare(keyword, config.get_name()):
                    print("Found name")
                    return Commands.get_command(keywords, entities, all_keywords)
            else:
                return False
