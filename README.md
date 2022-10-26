# Setup python environment

```console
sudo apt-get install python3 python3-pip
pip3 install virtualenv
git clone ...
cd QR_Project
virtualenv .
source bin/activate
pip3 install -r requirements.txt
```

# miniC

## Usage

1. Create text file in the chosen language (`miniC/source.c`)
2. Compile it to pseudo assembly using `python3 miniC/miniC_compiler.py`. It will internally use `miniC_Lexer.py` and `miniC_Parser.py` to compile `source.c` into `source.asm`
    1. Input and output files can be customized using `python3 miniC/miniC_compiler.py -in <input-file> -out <output-file>`
3. Use `python3 generate_qr.py` to generate the qr corresponding to `miniC/source.asm` and place it into `miniC/source.png`
    1. The input file format can be specified using `python3 generate_qr.py <format>` (Tested formats are `binary` and `alphanumeric`)
    2. Input and output files can be customized using `python3 generate_qr.py -in <input-file> -out <output-file>`
4. Use `python3 decode_qr.py` to decode the qr contained in `miniC/source.png` into `miniC/decoded.asm`
    1. Input and output files can be customized using `python3 decode_and_execute_QR.py -in <input-file> -out <output-file>`
5. Alternatively, use `python3 decode_qr.py -m camera` to decode the qr read from the pc webcam into `miniC/decoded.asm`
    1. Output file can be customized using `python3 decode_qr.py -m camera -out <output-file>`
6. Execute the decoded pseudoassembly with `java -jar miniC/interpreter.jar miniC/decoded.asm`

# flowchart

## Language

The language is intended to be a simple textual representation of a flowchart. A valid file is composed of 2 parts separated by an empty line: node list and links list.

- Each node ("1D:ARE YOU USING THE LATEST VERSION OF THE PLUGIN X") is represented by:
    - An integer (id of the node)
    - P | D | T to indicate if the node is a Process, Decision, Terminal node
    - `:` symbol
    - The string label of the node. We can choose to write the string labels in 2 ways:
        - (ex1,ex2): Using only alphanumeric, uppercase symbols, ` %*+./` special symbols and newlines. This allows us to create a QR in alphanumeric mode ( the newline is not accepted by the QR encoding, but I substitute it using the '$' symbol so that the text file is more readable ). In alphanumeric mode we can encode up to 4,296 characters.
        - (ex3): Using any character (except for the special characters used by the language: `$:-`). In binary mode we can encode up to 2,953 characters.
- Each link links 2 nodes referred by their id using the `-` symbol:
    - 3-4 indicates a link without label
    - 1-YES-2 indicates a link with a label
    - 1-NO-3-4-YES-2 indicates a chain of links

## Usage

1. Create text file in the chosen language (`Flowchart/ex2.txt`)
2. Use `python3 generate_qr.py alphanumeric -in Flowchart/ex2.txt -out Flowchart/ex2.png` to generate the qr corresponding to `Flowchart/ex2.txt` and place it into `Flowchart/ex2.png`
    1. The input file format can be specified using `python3 generate_qr.py <format>` (Tested formats are `binary` and `alphanumeric`)
    2. Input and output files can be customized using `python3 generate_qr.py -in <input-file> -out <output-file>`
3. Use `python3 decode_qr.py -in Flowchart/ex2.png -out Flowchart/decoded.txt` to decode the qr contained in `Flowchart/ex2.png` into `Flowchart/decoded.py`
    1. Input and output files can be customized using `python3 decode_and_execute_QR.py -in <input-file> -out <output-file>`
4. Alternatively, use `python3 decode_qr.py -m camera -out Flowchart/decoded.txt` to decode the qr read from the pc webcam into `Flowchart/decoded.txt`
    1. Output file can be customized using `python3 decode_and_execute_QR.py -m camera -out <output-file>`
5. Now compile a python script from the decoded QR and execute it using `python3 Flowchart/flowchart_compiler.py -m graph` or `python3 Flowchart/flowchart_compiler.py -m interactive`. This will internally use `flowchart_Lexer.py` and `flowchart_Parser.py` to compile `Flowchart/decoded.txt` into `Flowchart/program.py` and then execute the resulting script.
    1. The script that will be generated depends on the mode selected:`graph` will generate a png containing the flowchart described by the content of the QR. `interactive` will start an interactive session on the console to navigate the flowchart.
    2. Input and output files can be customized using `python3 Flowchart/flowchart_compiler.py -in <input-file> -out <output-file>`