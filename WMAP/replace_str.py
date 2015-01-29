#!/usr/bin/python3

"""
This program is a command-line program which accepts an incoming text file, a set of arguments and a new or
search/replacement string to modify the file. For more details see docstring in the main() function.

Written by Mark Foley, January 2014.
"""

import sys
import os
import shutil
import datetime
import argparse


def add_new(file, text=None):
    """
    Adds new line of text to file. Opens the file in append mode which adds to end by default..

    :param file: The file that we are going to update
    :param text: The text line that we are going to add
    :return: Nothing but exits if IOError raised
    """
    if (not text):
        sys.exit("No replacement text.")

    try:
        with open(file, "a") as fh:
            fh.write("\n" + text + "\n")
    except IOError as e:
        sys.exit(e)


def replace_existing(file, search_text=None, new_text=None):
    """
    Looks for text string in existing file and replaces it. Does this by opening file in read mode. Reads contents of
    file into variable, modifies variable and creates new version of file. Modified variable is written to new version
    of the file.

    :param file: The file we are going to update
    :param search_text: The text string that we want to replace
    :param new_text: The text string that we are replacing 'search_text' with.
    :return: Nothing but exits if IOError raised.

    """
    if (not search_text) or (not new_text):
        sys.exit("No search or replacement text.")

    try:
        with open(file, "r") as fh:
            contents = fh.read()

        contents = contents.replace(search_text, new_text)

        with open(file, "w") as fh:
            fh.write(contents)

    except IOError as e:
        sys.exit(e)


def main():
    """
    1. Creates instance of 'argparse' module. This makes it easy to write user-friendly command-line interfaces. The
    program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The
    argparse module also automatically generates help and usage messages and issues errors when users give the program
    invalid arguments.

    2. One of the arguments is a file path. We check that this exists and if it does, we make a copy for backup purposes.

    3. Depending on the arguments (-a or -r) we decide whether we are adding to file or replacing text in the file and
    call the appropriate function.

    :return: Nothing but exits if error condition occurs.

    usage: replace_str.py [-h] [-a | -r] [-n NEW] [-s SEARCH] file

    positional arguments:
      file                  File to modify

    optional arguments:
      -h, --help            show this help message and exit
      -a, --add             Append text to file
      -r, --replace         Replace text in file
      -n NEW, --new NEW     New text: added to file or replaces search text
                            depending on -a|-r flag
      -s SEARCH, --search SEARCH
                            Target search text

    """

    try:
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()

        group.add_argument("-a", "--add", help="Append text to file", action="store_true")
        group.add_argument("-r", "--replace", help="Replace text in file", action="store_true")

        parser.add_argument("file", help="File to modify")

        parser.add_argument("-n", "--new",
                            help="New text: added to file or replaces search text depending on -a|-r flag")
        parser.add_argument("-s", "--search", help="Target search text")

        args = parser.parse_args()

        if not os.path.isfile(args.file):
            sys.exit("{} is not a valid file".format(args.file))

        try:
            shutil.copy2(args.file, args.file + "." + datetime.datetime.today().isoformat() + ".bak")
        except IOError as e:
            sys.exit(e)
        except shutil.Error as e:
            sys.exit(e)

        if args.add:
            add_new(args.file, args.new)
        elif args.replace:
            replace_existing(args.file, args.search, args.new)
        else:
            sys.exit("No valid option supplied")

        # Print completion status
        print ("\n** " + os.path.basename(__file__) + " ran successfully with:")
        print(str(args))

    except SystemExit as e:
        print("\n** " + os.path.basename(__file__) + " --> " + str(e))


if __name__ == "__main__":
    main()