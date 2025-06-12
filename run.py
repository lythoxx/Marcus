from src import main

import asyncio

import spacy.util
import spacy.cli

def ensure_spacy_models(models):
    """
    Checks if the required spaCy models are installed, and downloads them if missing.
    """
    for model in models:
        if not spacy.util.is_package(model):
            print(f"spaCy model '{model}' not found. Downloading...")
            spacy.cli.download(model)
        else:
            print(f"spaCy model '{model}' is already installed.")

if __name__ == "__main__":
    ensure_spacy_models(["de_core_news_md", "en_core_web_md"])
    asyncio.run(main.main())