import sys
import argparse
import subprocess

from flowchart_Parser import *

argParser = argparse.ArgumentParser()
argParser.add_argument('-m', '--mode', default="graph", choices=['graph',
                                                                 'interactive'], help="Choose to generate the graph "
                                                                                      "of the flowchart or to "
                                                                                      "navigate it interactively ("
                                                                                      "default: %(default)s)")
argParser.add_argument('-in', '--input-file', default="Flowchart/decoded.txt", help="file containing the decoded QR "
                                                                                    "code to be compiled (default: %("
                                                                                    "default)s)")
argParser.add_argument('-out', '--output-file', default="Flowchart/program.py", help="file where to store the result "
                                                                                     "of the compilation of the "
                                                                                     "QR code (default: %(default)s)")

args = argParser.parse_args()

myLex = MyLexer()
myPars = MyParser(myLex, args.mode)
myLex.init_parser(myPars)

lex = myLex.lexer
parser = myPars.parser

myFile = open(args.input_file)

if args.mode == 'graph':
    original_stdout = sys.stdout  # Save a reference to the original standard output

    with open(args.output_file, 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print("import graphviz")
        print("flowchart = graphviz.Digraph('flowchart')")
        parser.parse(myFile.read())
        sys.stdout = original_stdout
    print(f"{args.output_file} written successfully!")
    print(f"Now the new file {args.output_file} will be executed:")
    print(f"python3 {args.output_file}")
    subprocess.run(["python3", args.output_file], shell=False)
elif args.mode == 'interactive':
    parser.parse(myFile.read())
    print("session concluded successfully!")
