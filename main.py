import os
import random
import time
import librosa
import sounddevice as sd

AUTHORS = ["A-HA"]
folder = "direc-of-music/A-HA"

def play_track(path, song_name):
    y, sr = librosa.load(path, sr=None)
    position = 0
    start_time = 0
    paused = False

    sd.play(y[position:], sr)
    start_time = time.time()

    while True:
        command = input("pause / resume / stop / status : ").lower()
        if command == "pause" and paused == False:
            sd.stop()
            elapsed = time.time() - start_time
            position += int(elapsed * sr)
            paused = True
            print("Paused")

        elif command == "resume" and paused == True:
            sd.play(y[position:], sr)
            start_time = time.time()
            paused = False
            print("Resumed")

        elif command == "stop":
            sd.stop()
            print("Stopped")
            break

        elif command == "status":
            current_sec = position / sr
            print(f"Track: {song_name}")
            print(f"Second: {round(current_sec, 2)}")

        if paused == False and sd.get_stream().active == False:
            print("Track ended")
            break

def play_all():
    songs = []
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            number = int(file.replace(".wav", ""))
            songs.append(number)
    songs.sort()

    for song in songs:
        path = f"{folder}/{song}.wav"
        print(f"\nNow playing: {song}.wav")
        play_track(path, f"{song}.wav")

def play_random():

    songs = []

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            number = int(file.replace(".wav", ""))
            songs.append(number)

    random.shuffle(songs)

    for song in songs:
        path = f"{folder}/{song}.wav"
        print(f"\nNow playing: {song}.wav")
        play_track(path, f"{song}.wav")

print("Hello, here you can play some music")
auth = input("Which author do you want to hear? ")
is_random = input("Randomize music? (yes/no): ")

if auth in AUTHORS:
    if is_random.lower() in ["yes", "ok", "true"]:
        play_random()
    else:
        play_all()
else:
    print("Author not found")