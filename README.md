# meta_writer
## Python script that lets you change creation && modified date of files in multiple subdirectories.
```
Usage: . [-h] -d DIRECTORY [-sub] -e EXTENSION -s SHIFT [-o] [-r] [-v] [-cd] [-md]

Mass change creation/modification date of files with certain extension.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory to be processed.
  -sub, --subdirectories
                        If set, the program will also process all files in all subdirectories.
  -e EXTENSION, --extension EXTENSION
                        File extension to be processed. (* for everything)
  -s SHIFT, --shift SHIFT
                        The amount of days to shift the creation date.
  -o, --overwrite       Overwrites metadata. (otherwise wont commit changes)
  -r, --relative-shift  If set, shifts relatively to creation date of file.
  -v, --verbose         If set, the program will print all metadata of file + some debug info.
  -cd, --change-creation-date
                        If set, the program will modify the creation date of file.
  -md, --change-modify-date
                        If set, the program will modify the updated date of file.
```
note:
-cd and -md are both set by default
if you set just one, only that one will be modified :)

```
python3 meta_writer/ -d ~/Desktop/test -e txt -s 1 -o
Processing: /Users/1fc0nfig/Desktop/test/test.txt
Created: Wed May  4 15:51:51 2022
Updated: Thu May  5 15:51:55 2022
-----------------------------------------------------
```
