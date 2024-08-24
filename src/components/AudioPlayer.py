import threading
import time
import queue
import os
from yt_dlp import YoutubeDL
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks

class AudioPlayer:
    def __init__(self):
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.audio_queue = queue.Queue()
        self.song_queue = queue.Queue()
        self.stream_thread = None
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.channels = None
        self.rate = None
        self.sample_width = None

    def stream_audio(self, video_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': 'output/downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio...")
            ydl.download([video_url])
            audio_file = 'output/downloaded_audio.mp3'

            print("Creating audio segment...")
            audio_segment = AudioSegment.from_file(audio_file, format="mp3")

            self.sample_width = audio_segment.sample_width
            self.channels = audio_segment.channels
            self.rate = audio_segment.frame_rate

            print("Making chunks...")
            # Split the audio segment into chunks and put them into the queue
            buffer_size = 4096
            for chunk in make_chunks(audio_segment, buffer_size):
                self.audio_queue.put(chunk.raw_data)

            print("Finished streaming audio.")

    def play_audio(self):
        while not self.stop_event.is_set():
            if self.pause_event.is_set():
                time.sleep(0.1)
                continue

            if self.audio_queue.empty() and not self.song_queue.empty():
                video_url = self.song_queue.get()
                self.stream_audio(video_url)

            if self.channels is None or self.rate is None or self.sample_width is None:
                time.sleep(0.1)
                continue

            if self.stream is None:
                self.stream = self.pyaudio_instance.open(format=self.pyaudio_instance.get_format_from_width(self.sample_width),
                                                         channels=self.channels,
                                                         rate=self.rate,
                                                         output=True)

            try:
                data = self.audio_queue.get(timeout=1)
                self.stream.write(data)
            except queue.Empty:
                if self.audio_queue.empty() and self.song_queue.empty():
                    os.remove("output/downloaded_audio.mp3")
                    print("All songs finished.")
                    self.stop()
                elif self.audio_queue.empty():
                    print("Loading next song...")
                    self.play_next_song()

    def play(self, video_url):
        self.song_queue.put(video_url)
        if not self.stream_thread or not self.stream_thread.is_alive():
            self.stop_event.clear()
            self.pause_event.clear()
            self.stream_thread = threading.Thread(target=self.play_audio)
            self.stream_thread.start()

    def play_next_song(self):
        self.audio_queue.queue.clear()
        self.channels = None
        self.rate = None
        self.sample_width = None
        if not self.song_queue.empty():
            video_url = self.song_queue.get()
            self.stream_audio(video_url)

    def stop(self):
        self.stop_event.set()
        if self.stream_thread and self.stream_thread.is_alive():
            if threading.current_thread() == self.stream_thread:
                print("Same threads")
                return
            self.stream_thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if os.path.exists("output/downloaded_audio.mp3"):
            os.remove("output/downloaded_audio.mp3")
        self.pyaudio_instance.terminate()

    def pause(self):
        self.pause_event.set()

    def resume(self):
        self.pause_event.clear()

    def get_threads(self):
        return self.stream_thread

    def get_audio_queue(self):
        return self.audio_queue

    def get_song_queue(self):
        return self.song_queue

# Example usage
if __name__ == "__main__":
    player = AudioPlayer()
    # player.play("https://www.youtube.com/watch?v=NR3xVQy8ccM")
    player.play("https://www.youtube.com/watch?v=X7f2SdZey-Y")
    player.play("https://www.youtube.com/watch?v=NNWaHH9W-HA")
    # player.play("https://www.youtube.com/watch?v=SIGqnneLUWc")
    # player.play("https://www.youtube.com/watch?v=29x2hCviWcw")
    # player.play("https://www.youtube.com/watch?v=KCffKIZV82w")
    # player.play("https://www.youtube.com/watch?v=gi4H5gQDuug")
    # player.play("https://www.youtube.com/watch?v=-IjkSMXywgg")
    # player.play("https://www.youtube.com/watch?v=MnaHnj4HrGk")
    # player.play("https://www.youtube.com/watch?v=eT-QlZjVmgI")
    # player.play("https://www.youtube.com/watch?v=NacdOheIHRE")
    # player.play("https://www.youtube.com/watch?v=XMXJ-xvrXM8")
    # player.play("https://www.youtube.com/watch?v=Pb3G_JIKxdk")

    while True:
        command = input("Enter a command (stop, pause, resume): ")
        if command == "stop":
            player.stop()
            break
        elif command == "pause":
            player.pause()
        elif command == "resume":
            player.resume()
        elif command == "queue":
            print(player.get_song_queue().queue)
        elif command == "audio":
            print(player.get_audio_queue().queue)
        elif command == "quit":
            import sys
            sys.exit(0)
        elif command == "threads":
            print(player.get_threads())
        elif command == "next":
            player.play_next_song()