import os
import random
import librosa
import sounddevice as sd

AUTHORS = ["A-HA"]
folder = "direc-of-music/A-HA"


def play_all():

    songs = []

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            number = int(file.replace(".wav", ""))
            songs.append(number)

    songs.sort()

    for song in songs:

        path = f"{folder}/{song}.wav"

        print(f"Грає: {song}.wav")

        y, sr = librosa.load(path, sr=None)

        sd.play(y, sr)
        sd.wait()


def play_random():

    songs = []

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            number = int(file.replace(".wav", ""))
            songs.append(number)

    random.shuffle(songs)

    for song in songs:

        path = f"{folder}/{song}.wav"

        print(f"Грає: {song}.wav")

        y, sr = librosa.load(path, sr=None)

        sd.play(y, sr)
        sd.wait()


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