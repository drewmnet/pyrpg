#!/usr/bin/env python3

import sys
import os
import pep8


def check_file(filename):
    fchecker = pep8.Checker(filename, show_source=True)
    file_errors = fchecker.check_all()
    return f"Found {file_errors} errors (and warnings)"

filename = sys.argv[1]

if not os.path.exists(filename):
    print(f"file '{filename}' does not exist")
    exit()
else:
    print(check_file(filename))
