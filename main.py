import os
import random
import time
import librosa
import sounddevice as sd

AUTHORS = ["A-HA", "Testing"]



print("Hello, here you can play some music")

auth = input("Which author do you want to hear? ").strip()
is_random = input("Randomize music? (yes/no): ").strip().lower()

folder = f"direc-of-music/{auth}"

def play_track(path, song_name):
    y, sr = librosa.load(path, sr=None)

    position = 0
    start_time = time.time()
    paused = False

    sd.play(y[position:], sr)

    while True:

        if paused is False and sd.get_stream().active is False:
            print("Track ended")
            break

        command = input("pause / resume / stop / status : ").strip().lower()

        if command == "pause":

            if paused is False:
                sd.stop()
                elapsed = time.time() - start_time
                position += int(elapsed * sr)
                paused = True
                print("Paused")

        elif command == "resume" or command == "=":

            if paused is True:

                if position >= len(y):
                    print("Track ended")
                    break

                sd.play(y[position:], sr)
                start_time = time.time()
                paused = False
                print("Resumed")

        elif command == "stop":
            sd.stop()
            print("Stopped")
            break

        elif command == "status":

            if paused is False:
                elapsed = time.time() - start_time
                current_position = position + int(elapsed * sr)
            else:
                current_position = position

            print(f"Track: {song_name}")
            print(f"Second: {round(current_position / sr, 2)}")



def play_all():
    songs = []

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            songs.append((file.replace(".wav", "")))
        elif file.endswith(".mp3"):
            songs.append((file.replace(".mp3", "")))

    songs.sort()

    for song in songs:
        try:
            path = f"{folder}/{song}.wav"
            print(f"\nNow playing: {song}.wav")
            play_track(path, f"{song}.wav")
        except Exception:
            path = f"{folder}/{song}.mp3"
            play_track(path, f"{song}.mp3")


def play_random():
    songs = []

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            songs.append((file.replace(".wav", "")))
        elif file.endswith(".mp3"):
            songs.append((file.replace(".mp3", "")))

    random.shuffle(songs)

    for song in songs:
        try:
            path = f"{folder}/{song}.wav"
            print(f"\nNow playing: {song}")
            play_track(path, f"{song}.wav")
        except Exception:
            path = f"{folder}/{song}.mp3"
            play_track(path, f"{song}.mp3")




if auth in AUTHORS:
    if is_random in ["yes", "ok", "true"]:
        play_random()
    else:
        play_all()
else:
    print("Author not found")