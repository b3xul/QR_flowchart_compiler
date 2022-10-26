import sys
import argparse

from miniC_Parser import *

# create objects MY LEXER and MY PARSER
myLex = MyLexer()
myPars = MyParser(myLex)
myLex.init_parser(myPars)

lex = myLex.lexer
parser = myPars.parser

argParser = argparse.ArgumentParser()
argParser.add_argument('-in', '--input-file', default="miniC/source.c", help="file to be encoded into the QR "
                                                                             "code (default: %(default)s)")
argParser.add_argument('-out', '--output-file', default="miniC/source.asm", help="file where to store the "
                                                                                 "generated QR code (default: %("
                                                                                 "default)s)")

args = argParser.parse_args()
myFile = open(args.input_file)

original_stdout = sys.stdout  # Save a reference to the original standard output

with open(args.output_file, 'w') as f:
    sys.stdout = f  # Change the standard output to the file we created.
    parser.parse(myFile.read())
    sys.stdout = original_stdout

print(f"{args.input_file} was successfully compiled into {args.output_file}!")
