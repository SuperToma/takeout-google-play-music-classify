import eyed3
import glob
import logging
import os
import pathlib
import re

FILES_DIR = "../Takeout/Google Play Musique/Titres"

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


for mp3_path in glob.glob(FILES_DIR + "/*.mp3"):
    id3 = eyed3.load(mp3_path).tag

    filename_infos = get_data_from_filename(mp3_path)

    artist = id3.artist
    if artist is None:
        artist = filename_infos.get("artist")

    # For compilation albums
    if id3.album_artist == "Various Artists":
        artist = "Various Artists"

    # format name only if only standard chars (don't want to rename V▲LH▲LL)
    if re.match(r'^[ a-zA-Z0-9_-]+$', artist):
        artist = artist.title()
    
    if id3.album is not None:
        album = re.sub("[<>:\"/\|?*]", "_", id3.album)
    else:
        album = filename_infos.get("album")

    year = str(id3.getBestDate())

    if id3.title is not None:
        title = re.sub("[<>:\"/\|?*]", "_", id3.title)
    else:
        title = filename_infos.get("title")

    track_num = id3.track_num

    if album is None or album == "":
        album = (f"({year})" if year is not None else "")
    else:
        album = (f"({year}) " if year is not None else "") + re.sub("[<>:\"/\|?*]", "_", album)

    filename = f"{track_num[0]:02} - " if track_num is not None else ""
    filename = f"{filename}{title}.mp3".replace(os.path.sep, "-")

    # try to handle long names
    if len(filename) > 64:
        filename = filename[0:60] + '.mp3'

    # Create directories & file
    dir_path = os.path.join(FILES_DIR, artist, album)
    file_path = os.path.join(dir_path, filename)

    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    try:
        os.rename(mp3_path, file_path)
    except FileNotFoundError: 
        print(f"couldn't move {mp3_path.encode('cp1252', errors='ignore')}, maybe the resulting filename will be too long for Windows'")
    
    print(f"{mp3_path.encode('cp1252', errors='ignore')} moved to {file_path.encode('cp1252', errors='ignore')}")
    
print("Sorting MP3 files done.")

print("Removing .csv file.")

for csv_path in glob.glob(FILES_DIR + "/*.csv"):
    print(f"Removing file {csv_path}")
    os.remove(csv_path)

print("Script finishes")
