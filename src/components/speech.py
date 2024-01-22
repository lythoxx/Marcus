import speech_recognition as sr

class Speech:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_whisper(audio, language='english')
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
