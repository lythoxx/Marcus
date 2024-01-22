import speech_recognition as sr

class Speech:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.non_speaking_duration = 0.2

    def recognize(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_whisper(audio, language='english')
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
