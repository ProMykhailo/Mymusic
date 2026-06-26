import os
import random
import time
import librosa
import sounddevice as sd

AUTHORS = {"A-HA", "STH"}
SUPPORTED_FORMATS = (".wav", ".mp3")

def get_tracks(folder):
    songs = []
    for file in folder.iterdir():
        if file.suffix.lower() in SUPPORTED_FORMATS:
            songs.append(file)

    return songs

def play_track(path, song_name):
    y, sr = librosa.load(path,sr=None)

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



def play_all(folder, songs):
    for song in songs:
        path = os.path.join(folder, song)
        print(f"\nNow playing: {song}")
        try:
            play_track(path, song)
        except Exception as e:
            print(f"Cannot play {song}: {e}")

def main():
    print("Hello, here you can play some music")

    auth = input("Which author do you want to hear? ").strip()
    is_random = input("Randomize music? (yes/no): ").strip().lower()
    folder = os.path.join("direc-of-music", auth)

    if not os.path.isdir(folder):
        print("Folder not found")
        return

    songs = get_tracks(folder)

    if not songs:
        print("No songs found")
        return
    if auth in AUTHORS:
        if is_random in ["yes", "ok", "true"]:
            random.shuffle(songs)
        else:
            songs.sort()
    else:
        print("Author not found")
    play_all(folder, songs)

if __name__ == "__main__":
    main()


