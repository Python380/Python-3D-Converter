# This is a sample Python script.
from sys import argv
from utils import *
from converter import *

if __name__ == "__main__":
    debug = False

    if len(argv) < 5:
        print(USAGE_STR)
        exit(1)

    # get the flag locations and delete the flag.
    # After operation, the flag points to the location of the flag argument
    input_flag = argv.index("-i")
    del argv[input_flag]
    input_file = argv[input_flag]

    output_flag = argv.index("-o")
    del argv[output_flag]
    output_file = argv[output_flag]

    if "-d" in argv:
        debug = True

    # get file types
    file_type = determine_filetype(input_file)
    input_file = (input_file, file_type)
    file_type = determine_filetype(output_file)
    output_file = (output_file, file_type)

    converter = Converter(input_file, output_file)
    converter.convert()
