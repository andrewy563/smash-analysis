import sys
import os
from ubjson import DecoderException
from collections import Counter
import numpy as np

sys.path.append("..")

from replayprocessor import (
    decode_file,
    process_event_payload,
    process_game_start,
    process_game_end,
    convert_to_character,
)

long_game = 60 * 60 * 6
analysis_char = "samus"
handwarmer = 60 * 45


def check_start(start):
    if start["teams"] == 1:
        return False
    human = 0
    if start["port1"]["type"] == 0:
        human += 1
    if start["port2"]["type"] == 0:
        human += 1
    if start["port3"]["type"] == 0:
        human += 1
    if start["port4"]["type"] == 0:
        human += 1
    if human != 2:
        return False
    return True


def check_end(end):
    if end["end"] == 0:
        return False
    return True


def check_metadata(metadata):
    if metadata["lastFrame"] < handwarmer:
        return False
    return True


def add_characters(start, char_counter):
    if start["port1"]["type"] == 0:
        char_counter[start["port1"]["char_id"]] += 1
    if start["port2"]["type"] == 0:
        char_counter[start["port2"]["char_id"]] += 1
    if start["port3"]["type"] == 0:
        char_counter[start["port3"]["char_id"]] += 1
    if start["port4"]["type"] == 0:
        char_counter[start["port4"]["char_id"]] += 1


def check_puff(start):
    if start["port1"]["type"] == 0 and start["port1"]["char_id"] == analysis_char:
        return True
    if start["port2"]["type"] == 0 and start["port2"]["char_id"] == analysis_char:
        return True
    if start["port3"]["type"] == 0 and start["port3"]["char_id"] == analysis_char:
        return True
    if start["port4"]["type"] == 0 and start["port4"]["char_id"] == analysis_char:
        return True
    return False


def process_files():
    replay_count = 0
    puff_replay = 0
    non_puff_replay = 0
    puff_timeouts = 0
    non_puff_timeouts = 0
    puff_long_game = 0
    non_puff_long_game = 0
    game_time = []
    puff_game_time = []
    non_puff_game_time = []
    puff_time_character = Counter()
    non_puff_time_character = Counter()
    total_time_character = Counter()
    puff_long_character = Counter()
    long_game_character = Counter()
    total_long_game_character = Counter()
    for root, _, files in os.walk("../replays/"):
        for f in files:
            if f.endswith(".slp"):
                filename = root + "/" + f
                with open(filename, "rb") as replay:
                    index = 1
                    try:
                        decoded = decode_file(replay)
                    except DecoderException:
                        print(filename)
                        continue
                    if not check_metadata(decoded["metadata"]):
                        continue
                    event_payload = process_event_payload(decoded)
                    index += event_payload["event"]
                    start = process_game_start(
                        decoded["raw"][index : index + event_payload["start"] + 1]
                    )
                    if not check_start(start):
                        continue
                    end = process_game_end(
                        decoded["raw"][len(decoded["raw"]) - 1 - event_payload["end"] :]
                    )

                    if not check_end(end):
                        continue
                    game_time.append(decoded["metadata"]["lastFrame"])
                    if check_puff(start):
                        puff_game_time.append(decoded["metadata"]["lastFrame"])
                        if decoded["metadata"]["lastFrame"] == (60 * 60 * 8):
                            puff_timeouts += 1
                            add_characters(start, puff_time_character)
                        elif decoded["metadata"]["lastFrame"] >= (long_game):
                            puff_long_game += 1
                            add_characters(start, puff_long_character)
                        puff_replay += 1
                    else:
                        non_puff_replay += 1
                        if decoded["metadata"]["lastFrame"] == (60 * 60 * 8):
                            non_puff_timeouts += 1
                            add_characters(start, non_puff_time_character)
                        elif decoded["metadata"]["lastFrame"] >= (long_game):
                            non_puff_long_game += 1
                            add_characters(start, long_game_character)
                        non_puff_game_time.append(decoded["metadata"]["lastFrame"])
                    if decoded["metadata"]["lastFrame"] == (60 * 60 * 8):
                        add_characters(start, total_time_character)
                    elif decoded["metadata"]["lastFrame"] >= (long_game):
                        add_characters(start, total_long_game_character)
                    replay_count += 1
                if replay_count % 500 == 0:
                    print("{} replays processed".format(replay_count))
    print(
        "{} median: {:.2f} seconds".format(
            analysis_char, np.median(puff_game_time) / 60
        )
    )
    print(
        "{} mean: {:.2f} seconds".format(analysis_char, (np.mean(puff_game_time) / 60))
    )
    print("{} timeouts: {}".format(analysis_char, puff_timeouts))
    print("{} timeout characters: {}".format(analysis_char, puff_time_character))
    print("{} long game: {}".format(analysis_char, puff_long_game))
    print("{} long game characters: {}".format(analysis_char, puff_long_character))
    print("{} replay count: {}".format(analysis_char, puff_replay))
    print()
    print(
        "non-{} median: {:.2f} seconds".format(
            analysis_char, np.median(non_puff_game_time) / 60
        )
    )
    print(
        "non-{} mean: {:.2f} seconds".format(
            analysis_char, np.mean(non_puff_game_time) / 60
        )
    )
    print("non-{} timeouts: {}".format(analysis_char, non_puff_timeouts))
    print(
        "non-{} timeout characters: {}".format(analysis_char, non_puff_time_character)
    )
    print("non-{} long game: {}".format(analysis_char, non_puff_long_game))
    print("non-{} long game characters: {}".format(analysis_char, long_game_character))
    print("non-{} replay count: {}".format(analysis_char, non_puff_replay))
    print()
    print("total median: {0:.2f} seconds".format(np.median(game_time) / 60))
    print("total mean: {0:.2f} seconds".format(np.mean(game_time) / 60))
    print("total timeouts: {}".format(non_puff_timeouts + puff_timeouts))
    print("total timeout characters: {}".format(total_time_character))
    print("total long game: {}".format(puff_long_game + non_puff_long_game))
    print("total long game characters: {}".format(total_long_game_character))
    print("total replay count: {}".format(replay_count))


if __name__ == "__main__":
    process_files()

