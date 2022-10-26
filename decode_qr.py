import sys
from PIL import Image
from pyzbar.pyzbar import decode
import subprocess
import argparse


def camera_decode():
    from imutils.video import VideoStream
    import cv2
    import time

    # initialize the video stream and allow the camera sensor to warm up
    print("Starting video stream...(press q to interrupt)")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    content_ = []
    while len(content_) == 0:
        # grab the frame from the threaded video stream and resize it to have a maximum width of 400 pixels
        frame = vs.read()
        # frame = imutils.resize(frame, width=400)
        # find the barcodes in the frame and decode each of the barcodes
        content_ = decode(frame)
        cv2.imshow("QR Scanner", frame)
        print('.', end='')
        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        key = cv2.waitKey(1)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print()
            break

    # closing all open windows
    cv2.destroyAllWindows()
    vs.stop()
    return content_


if __name__ == "__main__":

    valid_commands = {"pseudoassembly": ["java", "-jar", "miniC/interpreter.jar"], "python3": ["python3"]}

    argParser = argparse.ArgumentParser()
    argParser.add_argument('-m', '--mode', default="image", choices=['image',
                                                                     'camera'],
        help="Choose to read the QR from an image file or directly from the camera (default: %(default)s)")
    argParser.add_argument('-in', '--input-file', default="miniC/source.png", help="file containing the QR code "
                                                                                   "to be decoded (default: %("
                                                                                   "default)s)")
    argParser.add_argument('-out', '--output-file', default="miniC/decoded.asm", help="file where to store the    "
                                                                                      "decoded "
                                                                                      "QR code (default: %(default)s)")

    args = argParser.parse_args()
    if args.mode == "image":
        content = decode(Image.open(args.input_file))
    else:
        content = camera_decode()

    if len(content) != 0:
        with open(args.output_file, 'w') as f_output:
            print(content[0].data.decode('ascii'), file=f_output, end='')
            # print(f"Recognized QR:{content}")
            print("The content of the QR ", end='')
            if args.mode == "image":
                print(f"in {args.input_file} ", end='')
            print(f"was successfully decoded in {args.output_file}!")
    else:
        print("ERROR: QR was not recognized")
