import sys
import os
import argparse
import time
import re
from subprocess import call


# Initialize argument parser
parser = argparse.ArgumentParser(description='Runs the main program.')
parser.add_argument('-d', '--directory', type=str, required=True, help='The directory && all of its subdirectiories to be processed.')
parser.add_argument('-sub', '--subdirectories', action='store_true', help='If set, the program will also process all subdirectories.')
parser.add_argument('-e', '--extension', type=str, required=True, help='File extension to be processed.')
parser.add_argument('-s', '--shift', type=int, required=True, help='The amount of days to shift the creation date in days.')
parser.add_argument('-o', '--overwrite', action='store_true', default=False, help="Overwrites metadata time creation to current time.")
parser.add_argument('-r', '--relative-shift', action='store_true', default=False, help="If set, shifts relatively to creation date of file.")
parser.add_argument('-v', '--verbose', action='store_true', help='If set, the program will print all metadata of file.')
parser.add_argument('-cd', '--change-creation-date', action='store_true', help='If set, the program will modify the creation date of file.')
parser.add_argument('-md', '--change-modify-date', action='store_true', help='If set, the program will modify the updated date of file.')

# main function
def main(directory, subdirectories, extension, shift, overwrite, relative_shift, verbose, change_creation_date, change_modify_date):
    filecnt = 0
    try:
        # check if subdirectories flag is set
        if subdirectories:
            # check if directory exists
            if os.path.isdir(directory):
                # loop over all files in all subdirectories
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        # process files if file has the correct extension
                        if file.endswith(extension):   
                            process_file(os.path.join(root, file), shift, overwrite, relative_shift, verbose, change_creation_date, change_modify_date)
                            filecnt += 1
            else:
                print(f"Directory {directory} does not exist.")
        else:
            # check if directory exists
            if os.path.isdir(directory):
                # loop over all files in directory
                for file in os.listdir(directory):
                     # process files if file has the correct extension
                        if file.endswith(extension):   
                            process_file(os.path.join(directory, file), shift, overwrite, relative_shift, verbose, change_creation_date, change_modify_date)
                            filecnt += 1
            else:
                print(f"Directory {directory} does not exist.")
        print(f"{filecnt} file(s) processed.")
    # Kexboard interrupt handler
    except KeyboardInterrupt as e:
        print("\nExiting...")
        exit(1)
    except Exception as e:
        print(f"Unexpected Exeption: {e}.")
        sys.exit(1)
    return 0

# function that process a file
def process_file(file_path, shift, overwrite, relative_shift, verbose, change_creation_date, change_modify_date):
    # check if file exists
    if os.path.isfile(file_path):
        print(f"Processing file: {file_path}")
        # print metadata of file if verbose flag is set
        if verbose:
            print_metadata(file_path)
        # get creation date of file
        creation_date = get_creation_date(file_path)
        # get updated date of file
        modify_date = get_updated_date(file_path)
        # if both of md and cd are not set, set both to True
        if not change_creation_date and not change_modify_date:
            change_creation_date = True
            change_modify_date = True
        # check if relative shift flag is set
        if relative_shift:
            print(f"Relative shift: {shift} days.") if verbose else None
            # calculate new creation date if modify creation date flag is set
            if change_creation_date:
                # must recalc shift
                creat_shift = shift * 24 * 60 * 60
                updated_creation_date = creation_date + creat_shift
            else:
                updated_creation_date = creation_date
            # calculate New modified date if modify updated date flag is set
            if change_modify_date:
                # recalc shift
                mod_shift = shift * 24 * 60 * 60
                updated_modified_date = modify_date + mod_shift
            else:
                updated_modified_date = modify_date
            # check if overwrite flag is set
            if overwrite:
                # overwrite creation date of file
                modify_creation_date(file_path, updated_creation_date)
                # overwrite updated date of file
                os.utime(file_path, (updated_modified_date, updated_modified_date))
                print("MODIFIED!") if verbose else None
            # prints new creation date of file
            print(f"New creation date: {time.ctime(updated_creation_date)}") if verbose else None
            # prints New modified date of file
            print(f"New modified date: {time.ctime(updated_modified_date)}") if verbose else None
                
            print('---------------------------------------------------------------------------------------------------------------------\n') if verbose else None
        else:
            print(f"Absolute shift: {shift} days.") if verbose else None
            # calculate new creation date relative to current time if modify creation date flag is set
            if change_creation_date:
                # must recalc shift
                creat_shift = shift * 24 * 60 * 60
                updated_creation_date = time.time() + creat_shift
            else:
                updated_creation_date = creation_date
            # calculate New modified date relative to current time if modify updated date flag is set
            if change_modify_date:
                # must recalc shift
                mod_shift = shift * 24 * 60 * 60
                updated_modified_date = time.time() + mod_shift
            else:
                updated_modified_date = modify_date
            # check if overwrite flag is set
            if overwrite:
                # overwrite creation date of file
                modify_creation_date(file_path, updated_creation_date)
                # overwrite updated date of file
                os.utime(file_path, (updated_modified_date, updated_modified_date))
                print("MODIFIED!") if verbose else None
            # prints new creation date of file
            print(f"New creation date: {time.ctime(updated_creation_date)}") if verbose else None
            # prints New modified date of file
            print(f"New modified date: {time.ctime(updated_modified_date)}") if verbose else None
                
            print('---------------------------------------------------------------------------------------------------------------------\n') if verbose else None 
    else:
        # Raise error if file does not exist
        raise FileNotFoundError(f"File {file_path} does not exist.")
    pass

# function that returns creation date of file
def get_creation_date(file_path):
    return os.stat(file_path).st_birthtime

# function that returns updated date of file
def get_updated_date(file_path):
    return os.stat(file_path).st_mtime

# function that prints all metadata of file
def print_metadata(file_path):
    metadata = os.stat(file_path)
    print(f"File information:")
    print(f"Created: {time.ctime(metadata.st_birthtime)}")
    print(f"Updated: {time.ctime(metadata.st_mtime)}")
    print(f"Accessed: {time.ctime(metadata.st_atime)}")
    print(f"Changed: {time.ctime(metadata.st_ctime)}") 
    print('---------------------------------------------------------------------------------------------------------------------') 
    pass

# function that changes creation time of file
def modify_creation_date(absolute_file_path, creation_date):
    # parse creation date into MM/DD/YYYY format in creation_date_str
    creation_date_str = time.strftime("%m/%d/%Y", time.gmtime(creation_date))
    # parse creation time into HH:MM:SS format in creation_time_str
    creation_time_str = time.strftime("%H:%M:%S", time.gmtime(creation_date))
    # escape spaces and special characters in absolute_file_path
    absolute_file_path = re.escape(absolute_file_path)
    # Exec time change (MacOS) specific
    try:
        command = 'SetFile -d ' + f'"{creation_date_str} "' + f'{creation_time_str} ' + absolute_file_path
        call(command, shell=True)
    except Exception as e:
        print(f"Error changing creation date of file: {e}.")
        raise e
    return

main(**vars(parser.parse_args()))