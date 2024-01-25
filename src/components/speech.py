import speech_recognition as sr
import queue
from config.config import Config
from src.utils import phonetic_compare

class Speech:

    BUFFER_DURATION = 5  # Duration in seconds of the rolling audio buffer

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.non_speaking_duration = 0.2
        self.microphone = sr.Microphone()
        self.audio_buffer = queue.Queue()  # A queue to hold audio chunks

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

    def recognize(self):
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

    def recognize_no_hotword(self):
        with self.microphone as source:
            print("Listening...")
            azure_key = Config.get_config("config")["azure_key"]
            audio = self.recognizer.listen(source)
            try:
                return self.recognizer.recognize_azure(audio, azure_key, location="germanywestcentral", profanity="raw")[0]
            except sr.UnknownValueError:
                print("Azure could not understand the audio")
                return None
            except sr.RequestError:
                print("Could not request results from Azure service")
                return None
