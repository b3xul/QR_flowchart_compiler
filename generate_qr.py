import argparse
import pyqrcode
import math


def create_qr(content, format):
    """
    This method creates a QR with the smallest possible QR code version number
    that will fit the specified data (in the specified format) with the highest possible error level.
    Possible formats values: 'numeric', 'alphanumeric', 'binary', 'kanji'
    """

    selected_version = 0
    capacity = 0
    for selected_error in ['H', 'Q', 'M', 'L']:
        for version in range(1, 41):
            # Get the maximum possible capacity
            capacity = pyqrcode.tables.data_capacity[version][selected_error][pyqrcode.tables.modes[format]]
            # Check the capacity
            # Kanji's count in the table is "characters" which are two bytes
            if format == 'kanji' and capacity >= math.ceil(len(content) / 2):
                selected_version = version
                break
            if capacity >= len(content):
                selected_version = version
                break
        if selected_version != 0:
            break

    if selected_version == 0:
        raise ValueError(f"The data has a size of {len(content)} {format} characters, while the max capacity of a QR "
                         f"code with {format} format is {capacity}")

    res = pyqrcode.create(content=content, error=selected_error, version=selected_version, mode=format)
    # print(res)
    print(f"To store {len(content)} {format} characters, the lowest version qr code with the highest error "
          f"correction we can obtain is {selected_version}-{selected_error}")

    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('format', nargs='?', default="binary", choices=['numeric',
                                                                        'alphanumeric',
                                                                        'binary',
                                                                        'kanji'], help="format of the file to be "
                                                                                       "encoded. Note that "
                                                                                       "alphanumeric only "
                                                                                       "supports uppercase letters, "
                                                                                       "digits and the special "
                                                                                       "characters: ' $%%*+-./:' ("
                                                                                       "default: %(default)s)")
    parser.add_argument('-in', '--input-file', default="miniC/source.asm", help="file to be encoded into the QR "
                                                                                "code (default: %(default)s)")
    parser.add_argument('-out', '--output-file', default="miniC/source.png", help="file where to store the "
                                                                                  "generated QR code (default: %("
                                                                                  "default)s)")

    args = parser.parse_args()

    source = open(args.input_file).read()
    if args.format == "alphanumeric" and '\n' in source:
        print("The alphanumeric format only supports ' $%*+-./:', but your input file contains the newline character. "
              "It will be replaced by $")
        source = source.replace("\n", '$')
    try:
        qr = create_qr(source, format=args.format)
        qr.png(args.output_file, scale=2)  # scale=2 necessary because otherwise the pyzbar library is not always
        # able to decode it
        print(f"The {args.format} content of {args.input_file} was successfully encoded in a QR in {args.output_file}!")
    except ValueError as e:
        print(f"ERROR: {e}")
