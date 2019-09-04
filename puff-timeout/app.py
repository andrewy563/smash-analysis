import ubjson
import struct
import sys


def decode_file(file_name):
    replay = open(file_name, "rb")
    decoded = ubjson.load(replay)
    return decoded


def find_length(decoded):
    length = {"event": 0, "start": 0, "pre": 0, "post": 0, "end": 0}
    length["event"] = decoded["raw"][1]
    for i in range(0, length["event"], 3):
        if decoded["raw"][2 + i] == 0x36:
            length["start"] = struct.unpack(">h", decoded["raw"][i + 3 : i + 5])[0]
        elif decoded["raw"][2 + i] == 0x37:
            length["pre"] = struct.unpack(">h", decoded["raw"][i + 3 : i + 5])[0]
        elif decoded["raw"][2 + i] == 0x38:
            length["post"] = struct.unpack(">h", decoded["raw"][i + 3 : i + 5])[0]
        elif decoded["raw"][2 + i] == 0x39:
            length["end"] = struct.unpack(">h", decoded["raw"][i + 3 : i + 5])[0]
        else:
            sys.exit("Error reading event payload!")
    return length


if __name__ == "__main__":
    decoded = decode_file("./replays/test1.slp")
    length = find_length(decoded)
    print(length)
