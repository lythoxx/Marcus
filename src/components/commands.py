import random
import sys
from enum import Enum
import requests

from dateutil import parser
from pytube import YouTube
from ytmusicapi import YTMusic

from .AudioPlayer import AudioPlayer
from config.config import Config

from src import utils

from .speech import Speech
from .tts import TTS

audio_player = AudioPlayer()
# TODO CLEAN UP COMMANDS - IMPLEMENT PROPER WAY TO HANDLE COMMANDS
class Commands:
    async def execute(intent: str, args: list) -> bool:
        if intent == "WEATHER":
            return await Commands.weather()
        elif intent == "EXIT":
            return await Commands.exit()
        elif intent == "MUSIC":
            return await Commands.play_music(args[0])
        elif intent == "ALARM":
            return await Commands.alarm(args)


    async def exit():
        tts = TTS()
        await tts.speak_openai("Auf wiedersehen! Ich hoffe ich war hilfreich.")
        sys.exit(0)

    async def alarm(times) -> bool:
        print(times)
        tts = TTS()
        if len(times) == 0:
            await tts.speak_openai("Es scheint als hättest du keine Zeit für den Wecker angegeben.")
            await tts.speak_openai("Bitte gebe eine Zeit an, um den Wecker zu starten.")
            return False
        time = times[0]
        if len(times) > 1:
            await tts.speak_openai("Es scheint als hättest du mehrere Zeiten für den Wecker angegeben.")
            await tts.speak_openai("Ich werde die erste, genannte Zeit für den Wecker verwenden.")
        try:
            alarm_time = parser.parse(time)
        except ValueError:
            await tts.speak_openai("Es scheint als sei die Zeit ungültig. Ich kann keinen Wecker mit der gegebenen Zeit stellen.")
            return False

        print(alarm_time.strftime("%H:%M"))
        await tts.speak_openai("Ist der Wecker wiederholend?")
        speech = Speech()
        answer = speech.recognize()
        if answer:
            if "no" in answer.lower():
                Config.set_alarm(alarm_time.strftime("%H:%M"))
                await tts.speak_openai("Ich habe den Wecker auf " + alarm_time.strftime("%H") + "Uhr" + alarm_time.strftime("%M") + " gesetzt.")
            elif "yes" in answer.lower():
                await tts.speak_openai("An welchen Tagen soll der Wecker wiederholt werden?")
                answer = speech.recognize()
                if not answer:
                    await tts.speak_openai("Es scheint als hättest du keine gültige Antwort gegeben. Ich habe den Wecker auf " + alarm_time.strftime("%H") + "Uhr" + alarm_time.strftime("%M") + " gesetzt.")
                    return True
                days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]
                alarm_days = ""
                for word in answer.lower():
                    if word in days:
                        alarm_days += word + ","
                Config.set_alarm(alarm_time.strftime("%H:%M"), alarm_days)
                await tts.speak_openai("Ich habe den Wecker auf " + alarm_time.strftime("%H") + "Uhr" + alarm_time.strftime("%M") + f" gesetzt. Der Wecker wird {alarm_days} wiederholt.")
        else:
            Config.set_alarm(alarm_time.strftime("%H:%M"))
            await tts.speak_openai("Ich habe den Wecker auf " + alarm_time.strftime("%H") + "Uhr" + alarm_time.strftime("%M") + " gesetzt.")
        return True

    # TODO Implement shuffle (for albums and playlists) and repeat
    # TODO Implement skip and previous
    async def play_music(query: str, filter=None, initial=True) -> bool:
        global audio_player
        if initial:
            query = query.lower().replace("spiele", "").strip()
        if "zufall" in query.lower() or "random" in query.lower() or "shuffle" in query.lower() or "zufällig" in query.lower():
            shuffle = True
            query = query.lower().replace("zufall", "").replace("random", "").replace("shuffle", "").replace("zufällig", "").strip()
        else:
            shuffle = False
        ytmusic = YTMusic()
        if "album" in query.lower() and not filter:
            filter = "albums"
            query = query.lower().replace("album", "").strip()
        if ("song" in query.lower() or "lied" in query.lower() or "track" in query.lower()) and not filter and not "songs" in query.lower() and not "lieder" in query.lower() and not "tracks" in query.lower():
            filter = "songs"
            query = query.lower().replace("song", "").replace("lied", "").replace("track", "").strip()
        if ("künstler" in query.lower() or "artist" in query.lower()) and not filter:
            filter = "artists"
            query = query.lower().replace("künstler ", "").replace("artist", "").strip()
            query = query.lower().replace("lieder", "").replace("songs", "").replace("tracks", "").strip()
        query = query.strip()
        if filter is None:
            search_results = ytmusic.search(query)
        else:
            search_results = ytmusic.search(query, filter=filter)

        if not search_results:
            print("No results found.")
            return False

        # Get the first result
        first_result = search_results[0]

        # Get the type of the first result
        result_type = first_result['resultType']

        # Handle the result based on its type
        if result_type == 'song':
            # Get the audio track URL
            audio_url = first_result['videoId']
            # Use pytube to download and play the audio
            yt = f"https://www.youtube.com/watch?v={audio_url}"
            audio_player.play(yt)

            # Play the audio
            # tts.speak_openai(f"Jetzt spiele ich {first_result['title']} von {first_result['artists'][0]['name']}.")
            # play_mp3(f'output/{first_result["title"]}.mp3')

        elif result_type == 'album':
            # Get the album's track list
            album_id = first_result['browseId']
            album = ytmusic.get_album(album_id)
            # Play each song in the album
            tracklist = album['tracks']
            for track in tracklist:
                Commands.play_music(f"{track['title']} {album['artists'][0]['name']}", filter="songs", initial=False)

        elif result_type == 'artist':
            # Get the artist's top songs
            artist_id = first_result['browseId']
            artist = ytmusic.get_artist(artist_id)
            playlist = ytmusic.get_playlist(artist["songs"]["browseId"])
            for song in playlist["tracks"]:
                Commands.play_music(f"{song['title']} {artist['name']}", filter="songs", initial=False)
        elif result_type == "video":
            search_results = ytmusic.search(query, filter="songs")

            if not search_results:
                print("No results found.")
                return False

            # Get the first result
            first_result = search_results[0]

            # Get the type of the first result
            result_type = first_result['resultType']
            # print(f"Result type: {result_type}")
                    # Get the audio track URL
            audio_url = first_result['videoId']
            # Use pytube to download and play the audio
            yt = f"https://www.youtube.com/watch?v={audio_url}"
            audio_player.play(yt)

            # Play the audio
            # play_mp3(f'output/{first_result["title"]}.mp3')
        else:
            print(f"Unsupported result type: {result_type}")
            return False

        return True

    def pause():
        global audio_player
        audio_player.pause()
        return True

    def stop():
        global audio_player
        audio_player.stop()
        return True

    def resume():
        global audio_player
        audio_player.resume()
        return True

    async def weather():
        api_key = Config.get_config("config")["weather_key"]
        # latitude and longitude for Berlin, Germany
        lat, lon = requests.get("https://ipinfo.io/json").json()["loc"].split(",")
        print(f"Using coordinates: {lat}, {lon}")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=de"

        response = requests.get(url)

        print(response.status_code)

        language = Config.get_config("config")["language"]
        if response.status_code == 200:
            data = response.json()
            print(data)
            temperature = data['main']['temp']
            description_id = data['weather'][0]['id']
            description_main = data['weather'][0]['main']
            print(f"Weather description ID: {description_id}, Main: {description_main}")
            description = utils.get_weather_descriptions(description_id, description_main)
            minimum_temperature = data['main']['temp_min']
            maximum_temperature = data['main']['temp_max']
            probability_precipitation = data.get('rain', {}).get('1h', 0)  # Get the probability of precipitation in the last hour, default to 0 if not available
            tts = TTS()
            await tts.speak_openai(Config.get_config("text")[language]["commands"]["weather"]["weather"].format(temperature, description, minimum_temperature, maximum_temperature, probability_precipitation))
            return True
        else:
            tts = TTS()
            print("Error fetching weather data:", response.status_code)
            await tts.speak_openai(Config.get_config("text")[language]["commands"]["weather"]["weather_error"])
            return False
