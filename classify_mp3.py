import argparse
import eyed3
import glob
import logging
import os
import pathlib
import re

logging.getLogger("eyed3").setLevel(logging.CRITICAL)


def get_data_from_filename(file_path):
    filename = os.path.basename(file_path)
    data = {
        "artist": "000 - unknown artist",
        "album": "000 - unknown album",
        "song": None,
        "track_number": 0,
        "year": "0000"
    }

    patterns = (
        # Brandy Kills - The Blackest Black - Summertime.mp3
        # Covenant - Synergy - Live In Europe - Babel.mp3
        re.compile("^(?P<artist>.*) - (?P<album>.*) - (?P<song>.*)\.mp3"),
        # Glass Apple Bonzai - In the Dark(001)Light in t.mp3
        re.compile("^(?P<artist>.*) - (?P<album>.*)\((?P<position>\d\d\d)\)(?P<song>.*).mp3"),
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

def init_argparse():
    parser = argparse.ArgumentParser(description="Classify a Google Takeout collection of Google Music MP3 files, moving them to a directory tree in the output directory as '.../artist/(year) album/track - filename.mp3'.")
    parser.add_argument("-d", "--dry-run",
        action="store_true", default=False,
        help="do not actually change files")
    parser.add_argument("-v", "--version",
        action="version", version = f"{parser.prog} version 1.0.0")
    parser.add_argument("input_dir", nargs="?",
        default="../Takeout/Google Play Music/Tracks",
        help="input directory containing files to classify, default is %(default)s")
    parser.add_argument("output_dir", nargs="?",
        help="output directory, default is input directory")
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = args.input_dir

    for mp3_path in glob.glob(os.path.join(args.input_dir, "*.mp3")):
        rename_and_move_file(args.output_dir, mp3_path, dry_run=args.dry_run)
    print("Sorting MP3 files done.")

    remove_csv_files(args.input_dir, dry_run=args.dry_run)
    print("Script finished.")

def rename_and_move_file(out_dir, mp3_path, dry_run=False):
    id3 = eyed3.load(mp3_path).tag
    filename_infos = get_data_from_filename(mp3_path)

    artist = id3.artist or filename_infos.get("artist")
    # format name only if only standard chars (don't want to rename V▲LH▲LL)
    if re.match(r'^[ a-zA-Z0-9_-]+$', artist):
        artist = artist.title()

    album = id3.album or filename_infos.get("album")
    year = id3.getBestDate() or filename_infos.get("year")
    title = id3.title or filename_infos.get("title")
    track_num = id3.track_num or filename_infos.get("track_number")

    album = (f"({year}) " if year is not None else "") + album

    filename = f"{track_num[0]:02} - " if track_num is not None else ""
    filename = f"{filename}{title}.mp3".replace(os.path.sep, "-")

    # Create directories & file
    dir_path = os.path.join(out_dir, artist, album)
    file_path = os.path.join(dir_path, filename)

    print(f"Moving {mp3_path} to {file_path}")
    if not dry_run:
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        os.rename(mp3_path, file_path)

def remove_csv_files(input_dir, dry_run=False):
    print("Removing .csv files.")

    for csv_path in glob.glob(os.path.join(input_dir, "*.csv")):
        print(f"Removing file {csv_path}")
        if not dry_run:
            os.remove(csv_path)

if __name__ == "__main__":
    main()