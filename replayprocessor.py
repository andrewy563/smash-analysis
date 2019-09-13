import ubjson
import struct
import sys

char_dict = {
    0: "falcon",
    1: "dk",
    2: "fox",
    3: "gnw",
    4: "kirby",
    5: "bowser",
    6: "link",
    7: "luigi",
    8: "mario",
    9: "marth",
    10: "mewtwo",
    11: "ness",
    12: "peach",
    13: "pikachu",
    14: "ic",
    15: "puff",
    16: "samus",
    17: "yoshi",
    18: "zelda",
    19: "sheik",
    20: "falco",
    21: "yl",
    22: "drmario",
    23: "roy",
    24: "pichu",
    25: "ganon",
}


def decode_file(replay):
    # decodes ubjson file to json
    decoded = ubjson.load(replay)
    return decoded


def convert_to_character(char_id):
    if char_id > 25:
        return "other"
    return char_dict[char_id]


def process_event_payload(decoded):
    length = {"event": 0, "start": 0, "pre": 0, "post": 0, "end": 0}
    length["event"] = decoded["raw"][1]
    for i in range(2, length["event"], 3):
        if decoded["raw"][i] == 0x36:
            length["start"] = struct.unpack(">h", decoded["raw"][i + 1 : i + 3])[0]
        elif decoded["raw"][i] == 0x37:
            length["pre"] = struct.unpack(">h", decoded["raw"][i + 1 : i + 3])[0]
        elif decoded["raw"][i] == 0x38:
            length["post"] = struct.unpack(">h", decoded["raw"][i + 1 : i + 3])[0]
        elif decoded["raw"][i] == 0x39:
            length["end"] = struct.unpack(">h", decoded["raw"][i + 1 : i + 3])[0]
        else:
            sys.exit("Error reading event payload!")
    return length


def process_game_start(payload):
    out = {}
    if payload[0] != 0x36:
        sys.exit("Error! process_game_start() did not receive a game_start event!")
    out["event"] = "gamestart"
    out["version"] = {
        "major": payload[0x1],
        "minor": payload[0x2],
        "build": payload[0x3],
    }
    out["teams"] = payload[0xD]
    out["port1"] = {
        "char_id": convert_to_character(payload[0x65]),
        "type": payload[0x66],
        "stock_start": payload[0x67],
        "color": payload[0x68],
        "team_id": payload[0x6E],
    }
    out["port2"] = {
        "char_id": convert_to_character(payload[0x65 + 0x24]),
        "type": payload[0x66 + 0x24],
        "stock_start": payload[0x67 + 0x24],
        "color": payload[0x68 + 0x24],
        "team_id": payload[0x6E + 0x24],
    }
    out["port3"] = {
        "char_id": convert_to_character(payload[0x65 + 0x24 * 2]),
        "type": payload[0x66 + 0x24 * 2],
        "stock_start": payload[0x67 + 0x24 * 2],
        "color": payload[0x68 + 0x24 * 2],
        "team_id": payload[0x6E + 0x24 * 2],
    }
    out["port4"] = {
        "char_id": convert_to_character(payload[0x65 + 0x24 * 3]),
        "type": payload[0x66 + 0x24 * 3],
        "stock_start": payload[0x67 + 0x24 * 3],
        "color": payload[0x68 + 0x24 * 3],
        "team_id": payload[0x6E + 0x24 * 3],
    }
    out["seed"] = struct.unpack(">i", payload[0x13D : 0x13D + 4])[0]
    if out["version"]["major"] < 1:
        return out
    out["dashback1"] = struct.unpack(">i", payload[0x141 : 0x141 + 4])[0]
    out["dashback2"] = struct.unpack(">i", payload[0x141 + 4 : 0x141 + 8])[0]
    out["dashback3"] = struct.unpack(">i", payload[0x141 + 8 : 0x141 + 12])[0]
    out["dashback4"] = struct.unpack(">i", payload[0x141 + 12 : 0x141 + 16])[0]
    out["shielddrop1"] = struct.unpack(">i", payload[0x145 : 0x145 + 4])[0]
    out["shielddrop2"] = struct.unpack(">i", payload[0x145 + 4 : 0x145 + 8])[0]
    out["shielddrop3"] = struct.unpack(">i", payload[0x145 + 8 : 0x145 + 12])[0]
    out["shielddrop4"] = struct.unpack(">i", payload[0x145 + 12 : 0x145 + 16])[0]
    if out["version"]["major"] == 1 and out["version"]["minor"] <= 3:
        return out
    out["nametag1"] = payload[0x161 : 0x161 + 8]
    out["nametag2"] = payload[0x161 + 8 : 0x161 + 16]
    out["nametag3"] = payload[0x161 + 16 : 0x161 + 24]
    out["nametag4"] = payload[0x161 + 24 : 0x161 + 32]
    if out["version"]["major"] == 1 and out["version"]["minor"] <= 5:
        return out
    out["PAL"] = payload[0x1A1]
    if out["version"]["major"] < 2:
        return out
    out["frozenps"] = payload[0x1A2]
    return out


def process_game_end(payload):
    out = {}
    if payload[0] != 0x39:
        sys.exit("Error! process_game_end() did not receive a game_end event!")
    out["end"] = payload[1]
    if len(payload) == 3:
        out["lras"] = payload[2]
    return out


if __name__ == "__main__":
    replay = open("./replays/test1.slp", "rb")
    decoded = decode_file(replay)
    length = process_event_payload(decoded)
    print(length)
    index = 1 + length["event"]
    start = process_game_start(decoded["raw"][index : index + length["start"] + 1])
    end = process_game_end(decoded["raw"][len(decoded["raw"]) - 1 - length["end"] :])
    print(end)
