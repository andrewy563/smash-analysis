import ubjson
import struct
import sys


def decode_file(f):
    # decodes ubjson file to json
    decoded = ubjson.load(replay)
    return decoded


def process_event_payload(decoded):
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


def process_game_start(payload):
    out = {}
    if payload[0] != 0x36:
        sys.exit("Error! process_game_start() did not receive a game_start event!")
    out["event"] = "gamestart"
    out["version"] = payload[0x1]
    out["teams"] = payload[0xD]
    out["port1"] = {
        "char_id": payload[0x65],
        "type": payload[0x66],
        "stock_start": payload[0x67],
        "color": payload[0x68],
        "team_id": payload[0x6E],
    }
    out["port2"] = {
        "char_id": payload[0x65 + 0x24],
        "type": payload[0x66 + 0x24],
        "stock_start": payload[0x67 + 0x24],
        "color": payload[0x68 + 0x24],
        "team_id": payload[0x6E + 0x24],
    }
    out["port3"] = {
        "char_id": payload[0x65 + 0x24 * 2],
        "type": payload[0x66 + 0x24 * 2],
        "stock_start": payload[0x67 + 0x24 * 2],
        "color": payload[0x68 + 0x24 * 2],
        "team_id": payload[0x6E + 0x24 * 2],
    }
    out["port4"] = {
        "char_id": payload[0x65 + 0x24 * 3],
        "type": payload[0x66 + 0x24 * 3],
        "stock_start": payload[0x67 + 0x24 * 3],
        "color": payload[0x68 + 0x24 * 3],
        "team_id": payload[0x6E + 0x24 * 3],
    }
    out["seed"] = struct.unpack(">i", payload[0x13D : 0x13D + 4])[0]
    out["ucf1"] = struct.unpack(">i", payload[0x141 : 0x141 + 4])[0]
    out["ucf2"] = struct.unpack(">i", payload[0x141 + 4 : 0x141 + 8])[0]
    out["ucf3"] = struct.unpack(">i", payload[0x141 + 8 : 0x141 + 12])[0]
    out["ucf4"] = struct.unpack(">i", payload[0x141 + 12 : 0x141 + 16])[0]
    out["nametag1"] = payload[0x161 : 0x161 + 8]
    out["nametag2"] = payload[0x161 + 8 : 0x161 + 16]
    out["nametag3"] = payload[0x161 + 16 : 0x161 + 24]
    out["nametag4"] = payload[0x161 + 24 : 0x161 + 32]
    out["PAL"] = payload[0x1A1]
    if out["version"] >= 2:
        out["frozenps"] = payload[0x1A2]
    return out


if __name__ == "__main__":
    replay = open("./replays/test1.slp", "rb")
    decoded = decode_file(replay)
    length = process_event_payload(decoded)
    index = 1 + length["event"]
    start = process_game_start(decoded["raw"][index : index + length["start"]])
