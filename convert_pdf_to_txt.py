#!/usr/bin/env python


import sys, os
from subprocess import call
from optparse import OptionParser


def main():

    """
    Converts a pdf or worddoc into a plain text file. Takes -f as the file being converted
    to alltext.txt.
    """

    parser = OptionParser()
    parser.add_option("-f", "--filename")

    options, arguments = parser.parse_args()

    call(['pdftotext', options.filename, 'alltext.txt'])

    print("Conversion of", options.filename, "to plain txt. [Completed]")

main()
