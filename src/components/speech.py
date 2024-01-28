import os

import speech_recognition as sr

from config.config import Config
from src.utils import phonetic_compare
import azure.cognitiveservices.speech as speechsdk


class Speech:

    BUFFER_DURATION = 5  # Duration in seconds of the rolling audio buffer

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.non_speaking_duration = 0.2
        self.microphone = sr.Microphone()
        # self.audio_buffer = queue.Queue()  # A queue to hold audio chunks
        # self.speech_config = speechsdk.SpeechConfig(subscription=Config.get_config("config")["azure_key"], region="germanywestcentral")
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.keyword_recognizer = speechsdk.KeywordRecognizer(audio_config=self.audio_config)
        self.keywordmodel = speechsdk.KeywordRecognitionModel(os.path.join(os.getcwd(), "src", "components", "models", "marcusrecognizer.table"))
        self.keyword = Config.get_name()

    def process_buffer(self):
        """
        Process the audio in the buffer and send it to Azure for full speech recognition
        once the hotword is detected.
        """
        # Combine the audio from the buffer
        audio = sr.AudioData(b''.join(list(self.audio_buffer.queue)),
                             self.microphone.SAMPLE_RATE,
                             self.microphone.SAMPLE_WIDTH)

        # Send the buffered audio to Azure for precise recognition
        try:
            azure_key = Config.get_config("config")["azure_key"]
            return self.recognizer.recognize_azure(audio, azure_key, location="germanywestcentral", profanity="raw")[0]
        except sr.UnknownValueError:
            print("Azure could not understand the audio")
            return None
        except sr.RequestError:
            print("Could not request results from Azure service")
            return None
        except Exception as e:
            print(e)

    def recognize_dynamic_hotword(self):
        with self.microphone as source:
            print("Listening...")

            while True:
                audio = self.recognizer.listen(source, phrase_time_limit=self.BUFFER_DURATION)
                self.audio_buffer.put(audio.get_raw_data())

                # If the buffer is too large, remove the oldest audio
                if self.audio_buffer.qsize() * self.BUFFER_DURATION > self.BUFFER_DURATION:
                    self.audio_buffer.get()

                # Check the audio chunk for the hotword using whisper and phonetic matching
                try:
                    text = self.recognizer.recognize_whisper(audio, "tiny")
                    for word in text.lower().split(" "):
                        if phonetic_compare(word, Config.get_name()):
                            print(f"Hotword detected: {text}")
                            return self.process_buffer()
                    else:
                        print("No hotword detected")
                        print(text)
                except sr.UnknownValueError:
                    print("No hotword detected")
                    pass  # Hotword not detected in this chunk

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

