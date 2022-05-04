# meta_writer
## Python script that lets you change creation && modified date of files in multiple subdirectories.

Usage: python3 meta_writer/ [-h] -d DIRECTORY -e EXTENSION -s SHIFT [-o | --overwrite | --no-overwrite] [-r | --relative-shift | --no-relative-shift]
 - -d/--directory -> Source directory to find files in (loops through all subdirectories)

 - -e/--extension -> File extension of files to process (txt, jpg, etc.)

 - -s/--shift -> Shift [int] in days [-7=(week before), 7=(week after)]

 - -o/--overwrite -> Overwrites metadata (Needs to be set to make changes)

 - -r/--relative-shift -> Shifts relatively to creation time of proccessed file, otherwise shifts relatively to current time

```
python3 meta_writer/ -d ~/Desktop/test -e txt -s 1 -o
Processing: /Users/1fc0nfig/Desktop/test/test.txt
Created: Wed May  4 15:51:51 2022
Updated: Thu May  5 15:51:55 2022
-----------------------------------------------------
```
