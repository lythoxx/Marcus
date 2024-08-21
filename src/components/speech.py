import os

import azure.cognitiveservices.speech as speechsdk

from config.config import Config


class Speech:

    BUFFER_DURATION = 5  # Duration in seconds of the rolling audio buffer

    def __init__(self):
        # self.audio_buffer = queue.Queue()  # A queue to hold audio chunks
        # self.speech_config = speechsdk.SpeechConfig(subscription=Config.get_config("config")["azure_key"], region="germanywestcentral")
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.keyword_recognizer = speechsdk.KeywordRecognizer(audio_config=self.audio_config)
        self.keywordmodel = speechsdk.KeywordRecognitionModel(os.path.join(os.getcwd(), "src", "components", "models", "marcusrecognizer.table"))


    def recognize_hotword(self):
        self.keyword_recognizer.recognized.connect(self.recognize)
        print("Hotword detection enabled")
        while True:
            result_future = self.keyword_recognizer.recognize_once_async(self.keywordmodel)
            result = result_future.get()

            if result.reason == speechsdk.ResultReason.RecognizedKeyword:
                print("Hotword detected, start recognizing...")
                return self.recognize()  # call your recognize method that handles the processing

    def recognize(self):
        azure_key = Config.get_config("config")["azure_key"]
        region = "germanywestcentral"
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=region)
        speech_config.set_profanity(speechsdk.ProfanityOption.Raw)

        # Here you should specify the microphone to use if you have multiple microphones
        # Or you can use None to use the default microphone
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="de-DE")
        print("Listening...")

        try:
            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(result.text))
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
        except Exception as e:
            print(f"An error occurred: {e}")

        return None

