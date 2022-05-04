import sys
import os
import argparse
import time

# Initialize argument parser
parser = argparse.ArgumentParser(description='Runs the main program.')
parser.add_argument('-d', '--directory', type=str, required=True, help='The directory && all of its subdirectiories to be processed.')
parser.add_argument('-e', '--extension', type=str, required=True, help='File extension to be processed.')
parser.add_argument('-s', '--shift', type=int, required=True, help='The amount of days to shift the creation date in days.')
parser.add_argument('-o', '--overwrite', default=False, help="Overwrites metadata time creation to current time.", action=argparse.BooleanOptionalAction)
parser.add_argument('-r', '--relative-shift', default=False, help="If set, shifts relatively to creation date of file.", action=argparse.BooleanOptionalAction)

# main function
def main(directory, extension, shift, overwrite, relative_shift):
    # loop over all files in subdirectories in directory with extension of "extension"
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    print(f"Processing: {os.path.join(root, file)}")
                    # prints all metadata of file
                    metadata = os.stat(os.path.join(root, file))
                    # prints metadata time creation in human readible format
                    print(f"Created: {time.ctime(metadata.st_birthtime)}")
                    if overwrite:
                        try:
                            # set a variable with updated time and shift it by shift (days)
                            if relative_shift:
                                updated_time = metadata.st_birthtime + (shift * 86400)
                            else:
                                updated_time = time.time() + (shift * 86400)
                            # prints updated time in human readible format
                            print(f"Updated: {time.ctime(updated_time)}")
                            # updates creation time of file
                            os.utime(os.path.join(root, file), (updated_time, updated_time))
                        except PermissionError:
                            print("Permission denied.")
                            sys.exit(1)
                        except FileNotFoundError:
                            print("File not found.")
                            sys.exit(1)
                    else:
                        # set a variable with updated time and shift it by shift (days)
                        if relative_shift:
                                updated_time = metadata.st_birthtime + (shift * 86400)
                        else:
                                updated_time = time.time() + (shift * 86400)
                        # prints updated time in human readible format
                        print(f"NOT Updated: {time.ctime(updated_time)}")
                    print('-----------------------------------------------------')
    # Kexboard interrupt handler
    except KeyboardInterrupt as e:
        print("\nExiting...")
        exit(1)
    return 0

main(**vars(parser.parse_args()))