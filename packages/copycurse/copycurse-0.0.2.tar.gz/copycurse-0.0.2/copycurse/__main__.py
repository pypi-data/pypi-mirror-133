from os import walk, path, makedirs, getcwd
from copycurse import VERSION
from datetime import datetime
from shutil import copy2
from tqdm import tqdm
import argparse


def path_exist(source_path):
    if path.exists(source_path):
        return source_path
    else:
        print(f"\nThe specified source directory does not exist: {source_path}")
        exit(1)


def arguments():
    cwd = getcwd()
    parser = argparse.ArgumentParser(prog="copycurse")
    parser.add_argument("source", type=path_exist, default=cwd, help="source directory [Default=.]")
    parser.add_argument("destination", type=str, help="destination directory")
    parser.add_argument("--version", action="version", version="%(prog)s v" + VERSION)

    args = parser.parse_args()

    args.source_path = path.abspath(args.source)
    args.destination_path = path.abspath(args.destination)

    return args


def copy(src_path, dst_path):
    item_list = []  # Create empty item list

    for abs_path, dirs, files in walk(src_path):
        for directory in dirs:
            item_list.append(path.join(abs_path, directory))  # Add directories to item list
        for file in files:
            item_list.append(path.join(abs_path, file))  # Add files to item list

    for item in tqdm(item_list, unit="files", desc="Progress"):  # Progress bar
        if path.isdir(item):  # Check if any items is a directory
            relative_path = path.relpath(item, src_path)
            target_path = path.join(dst_path, relative_path)

            if path.exists(target_path):  # Check if directory already exist
                pass
            else:
                makedirs(target_path)  # If not create it
        else:
            relative_path = path.relpath(item, src_path)
            target_path = path.join(dst_path, relative_path)

            copy2(item, target_path)  # Copy files


def banner(source_path, destination_path):
    print(r"""
   ___                ___                 
  / __|___ _ __ _  _ / __|  _ _ _ ___ ___ 
 | (__/ _ \ '_ \ || | (_| || | '_(_-</ -_)
  \___\___/ .__/\_, |\___\_,_|_| /__/\___|
          |_|   |__/          by 0xrytlock                 
""")
    print(f"+ Source DIR: {source_path}\n\n"
          f"+ Destination DIR: {destination_path}\n\n"
          f"-----------------------------------------------")


def main():
    args = arguments()
    banner(args.source_path, args.destination_path)
    try:
        while True:
            prompt = input("\nDo you wish start the backup process, type y/n: ")
            if prompt == "y":
                break
            elif prompt == "n":
                print("Ok, exiting...")
                exit(0)
            else:
                continue

        print(f"\nCopy process started: ({datetime.now().replace(microsecond=0)})\n")
        copy(args.source_path, args.destination_path)
        print(f"\nCopy finished: ({datetime.now().replace(microsecond=0)})\n")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting...")
        exit(0)


if __name__ == '__main__':
    main()
