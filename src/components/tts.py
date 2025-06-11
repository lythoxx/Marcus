import os

import audioread
import pyaudio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

from config.config import Config


class TTS:

    def __init__(self):
        self.gpt = AsyncOpenAI(api_key=Config.get_config("config")["openai_key"])

    # def speak_openai(self, text):
    #     # Ensure the output directory exists
    #     if not os.path.exists(os.path.join(os.getcwd(), 'output')):
    #         os.makedirs(os.path.join(os.getcwd(),'output'))

    #     response = self.gpt.audio.speech.create(
    #         model="tts-1",
    #         voice="onyx",
    #         input=text,
    #         response_format="mp3"
    #     )

    #     # Specify the path to the file
    #     output_file_path = os.path.join(os.getcwd(), 'output', 'tts.mp3')

    #     # Write the response to the file
    #     response.write_to_file(output_file_path)

    #     # Play the sound
    #     self.play_mp3(output_file_path)

    async def speak_openai(self, text: str) -> None:
        async with self.gpt.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions="You are a bilingual voice assistant. Speak in a calm, deep, natural tone with clear enunciation and a steady rhythm. Use a friendly, helpful, and professional demeanor. Keep answers concise, natural, and expressive but never overly emotional. When giving factual information or answering questions, speak with quiet confidence. Avoid monotone or robotic phrasing. Match your speech cadence to the user's pace when possible.",
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)

    def play_mp3(self, file_path):
        with audioread.audio_open(file_path) as audio_file:
            # Initialize PyAudio
            py_audio = pyaudio.PyAudio()

            # Open an audio stream with the appropriate settings
            stream = py_audio.open(
                format=py_audio.get_format_from_width(2),
                channels=audio_file.channels,
                rate=audio_file.samplerate,
                output=True
            )

            # Read and play the audio file in chunks
            for audio_chunk in audio_file:
                stream.write(audio_chunk)

            # Close the stream
            stream.stop_stream()
            stream.close()

            # Terminate PyAudio
            py_audio.terminate()