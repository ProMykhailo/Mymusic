import os
import random
import time
import librosa
import sounddevice as sd

AUTHORS = {"A-HA", "STH"}
SUPPORTED_FORMATS = (".wav", ".mp3")


def get_tracks(folder):
    songs = []
    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)
        if ext.lower() in SUPPORTED_FORMATS:
            songs.append(file)
    return songs


def play_track(path, song_name):
    y, sr = librosa.load(path, sr=None)

    position = 0
    start_time = time.time()
    paused = False

    sd.play(y, sr)

    while True:
        if not paused and not sd.get_stream().active:
            print("Track ended")
            break

        command = input("pause / resume / stop / status : ").strip().lower()

        if command == "pause":
            if paused:
                print("Already paused.")
                continue

            sd.stop()
            elapsed = time.time() - start_time
            position += int(elapsed * sr)
            paused = True
            print("Paused")

        elif command in ("resume", "="):
            if not paused:
                print("Track is already playing.")
                continue

            if position >= len(y):
                print("Track ended")
                break

            sd.play(y[position:], sr)
            start_time = time.time()
            paused = False
            print("Resumed")

        elif command == "status":
            if paused:
                current_position = position
            else:
                elapsed = time.time() - start_time
                current_position = position + int(elapsed * sr)

            print(f"Track: {song_name}")
            print(f"Second: {round(current_position / sr, 2)}")

        elif command == "stop":
            sd.stop()
            print("Stopped")
            break

        else:
            print("Unknown command.")


def play_playlist(folder, songs):
    for song in songs:
        path = os.path.join(folder, song)
        print(f"\nNow playing: {song}")
        try:
            play_track(path, song)
        except Exception as e:
            print(f"Cannot play {song}: {e}")


def main():
    print("Hello, here you can play some music")

    author = input("Which author do you want to hear? ").strip()
    random_mode = input("Randomize music? (yes/no): ").strip().lower()

    if author not in AUTHORS:
        print("Author not found")
        return

    folder = os.path.join("direc-of-music", author)

    if not os.path.isdir(folder):
        print("Folder not found")
        return

    songs = get_tracks(folder)

    if not songs:
        print("No songs found")
        return

    if random_mode in ("yes", "true", "ok"):
        random.shuffle(songs)
    else:
        songs.sort()

    play_playlist(folder, songs)


if __name__ == "__main__":
    main()
