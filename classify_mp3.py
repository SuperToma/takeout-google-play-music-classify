import eyed3
import glob
import logging
import os
import pathlib
import re

FILES_DIR = "../Takeout/Google Play Music/Tracks"

logging.getLogger("eyed3").setLevel(logging.CRITICAL)


def get_data_from_filename(file_path):
    file_name = file_path.split("/")[-1].replace(".mp3", "")
    data = {
        "artist": "000 - orphan albums"
    }

    if " - " not in file_name:
        return data

    if file_name.startswith(" - "):
        file_name = file_name.replace(" - ", "", 1)
    else:
        data.update({"artist": file_name.split(" - ")[0]})

    patterns = (
        # Brandy Kills - The Blackest Black - Summertime.mp3
        # Covenant - Synergy - Live In Europe - Babel.mp3
        re.compile("(?!^ - $) - (?P<album>.*) - (?P<song>.*)"),
        # Glass Apple Bonzai - In the Dark(001)Light in t.mp3
        re.compile(
            "(?!^ - $) - (?P<album>.*)\((?P<position>\d\d\d)\)(?P<song>.*)"
        ),
    )

    for pattern in patterns:
        result = pattern.search(file_name)
        if result is not None:
            data.update({
                "album": result.group("album") if "album" in pattern.groupindex else None,
                "song": result.group("song") if "song" in pattern.groupindex else None,
                "track_number": result.group("position")[1:] if "position" in pattern.groupindex else None,
            })
            return data

    return data

def main():
    for mp3_path in glob.glob(FILES_DIR + "/*.mp3"):
        rename_and_move_file(mp3_path)
    print("Sorting MP3 files done.")

    remove_csv_files(FILES_DIR)
    print("Script finished.")

def rename_and_move_file(mp3_path):
    id3 = eyed3.load(mp3_path).tag

    filename_infos = get_data_from_filename(mp3_path)

    artist = id3.artist
    if artist is None:
        artist = filename_infos.get("artist")

    # format name only if only standard chars (don't want to rename V▲LH▲LL)
    if re.match(r'^[ a-zA-Z0-9_-]+$', artist):
        artist = artist.title()

    album = id3.album
    if album is None:
        album = filename_infos.get("album")

    year = str(id3.getBestDate())

    title = id3.title
    if title is None:
        title = filename_infos.get("title")

    track_num = id3.track_num

    album = (f"({year}) " if year is not None else "") + album

    filename = f"{track_num[0]:02} - " if track_num is not None else ""
    filename = f"{filename}{title}.mp3".replace(os.path.sep, "-")

    # Create directories & file
    dir_path = os.path.join(FILES_DIR, artist, album)
    file_path = os.path.join(dir_path, filename)

    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    os.rename(mp3_path, file_path)

    print(f"{mp3_path} moved to {file_path}")

def remove_csv_files(files_dir):
    print("Removing .csv files.")

    for csv_path in glob.glob(files_dir + "/*.csv"):
        print(f"Removing file {csv_path}")
        os.remove(csv_path)

if __name__ == "__main__":
    main()