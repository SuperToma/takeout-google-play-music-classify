# takeout-google-play-music-classify
A python audio files classifier after a Google Takeout export of
Google Play Music

written with Python 3.6

## Context:
After downloading my Google Play Music Takeout export (58Go)

(as Google Play Music is not available anymore)

The archive contained 12500 files in 1 folder, a mix of .mp3 and .csv

-_-

### Before:
```
export/
├── Aesthetic Perfection - Blood Spills Not Fa(001).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(002).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(003).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(004).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(005).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(006).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(007).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(008).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(009).mp3
├── Aesthetic Perfection - Blood Spills Not Fa(010).mp3
├── Aesthetic Perfection - Close To Human - Coward.mp3
├── Aesthetic Perfection - Close To Human - Ersatz.mp3
├── Aesthetic Perfection - Close To Human - Fix.mp3
├── Aesthetic Perfection - Close To Human - Human.mp3
├── Aesthetic Perfection - Close To Human - Relapse.mp3
├── Aesthetic Perfection - Close To Human - Reset.mp3
├── Aesthetic Perfection - Close To Human - Surface.mp3
├── Aesthetic Perfection - Close To Human(002)Archi.mp3
├── Aesthetic Perfection - Close To Human(005)I Bel.mp3
├── Aesthetic Perfection - Close To Human(006)Overc.mp3
└── Aesthetic Perfection - Close To Human(010)Sacri.mp3
```

### After:
```
export/
└─── Aesthetic Perfection
      ├── (2005) Close To Human
      │    ├── 01 - Human.mp3
      │    ├── 02 - Architect.mp3
      │    ├── 03 - Fix.mp3
      │    ├── 04 - Relapse.mp3
      │    ├── 05 - I Belong To You.mp3
      │    ├── 06 - Overcast.mp3
      │    ├── 07 - Coward.mp3
      │    ├── 08 - Surface.mp3
      │    ├── 09 - Ersatz.mp3
      │    ├── 10 - Sacrifice.mp3
      │    └── 11 - Reset.mp3
      └── (2015) Blood Spills Not Far from the Wound
           ├── 01 - Open Wound.mp3
           ├── 02 - Spilling Blood.mp3
           ├── 03 - Forever.mp3
           ├── 04 - Vapor.mp3
           ├── 05 - Tomorrow.mp3
           ├── 06 - Never Enough.mp3
           ├── 07 - For All the Lost.mp3
           ├── 08 - Dying in the Worst Way.mp3
           ├── 09 - Elements.mp3
           └── 10 - Devotion.mp3
```

## How it works ?

### MP3 informations
It search the mp3 informations from the ID3 tags.

If no ID3 is found a fallback in the informations given
by the filename is done.


### Organization:
* 1 folder per artist
* 1 folder per album (inside the artist folder)
* Albums are prefixed by the year (for a chronological sort)
* If the album is not found orphan albums will be found in the folder
named `000 - orphan albums`
* Songs prefixed by the track number (for sorting)

**Notes:**

It doesn't use the .csv files given by Google.

The .csv files will be removed at the end of the script.

The missing information (ID3/filename) was pretty low in my case.

During the script it moves the .mp3 files to their album directory, it
doesn't make a copy.

**Please keep your .zip archives or a backup** is something goes wrong !

## Installation:
```
$ git clone git@github.com:SuperToma/takeout-google-play-music-classify.git
$ cd takeout-google-play-music-classify
$ pip install -r requirements.txt
```
Edit the file `python classify_mp3.py` and set the variable `FILES_DIR`
to your exported folder containing the .mp3 files

Then run the script
```
python classify_mp3.py
```

## Others:
* Don't hesitate to fix/improve/fork
* Only tested on MacOS but seems working on Linux/Windows
* Star if you like


[1]: https://github.com/nicfit/eyeD3
