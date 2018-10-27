#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess
import zipfile

"""Copy Special exercise
"""


# Write functions and modify main() to call them

def get_special_paths(dir):
    filenames = os.listdir(dir)
    listOfNames = []
    for filename in filenames:
        if re.search(r'__\w+__', filename) != None:
            listOfNames.append(os.path.abspath(os.path.join(dir, filename)))
    return listOfNames


def copy_to(paths, dir):
    for path in paths:
        shutil.copy(path, dir)


def zip_to(paths, zippath):
    zip = zipfile.ZipFile(dir, 'w')
    for path in paths:
        zip.write(path, compress_type=zipfile.ZIP_DEFLATED)
    zip.close()


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]");
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        # del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        # del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    if (todir != ''):
        copy_to(get_special_paths("./"), todir)
    if (tozip != ''):
        tozip(get_special_paths("./"), tozip)


if __name__ == "__main__":
    main()
