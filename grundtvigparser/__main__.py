"""
TEIParser
Usage:
    GrundtvigParser (-a | -o) [-r] [-n] [-o] [<file or folder]

Options:
-a          : Extract all files from folder
-o          : Extract from file
-r          : Recursive search through folders
-n          : Only extract "new" files
-o          : Only extract "old" files
"""
import docopt
import sys

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting")

if __name__ == "__main__":
    main()