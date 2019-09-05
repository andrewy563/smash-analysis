import sys
import os
import numpy as np

sys.path.append("..")

from replayprocessor import decode_file, process_event_payload, process_game_start


def check_puff(start):
    if (
        start["port1"]["char_id"] == 0x0F
        or start["port2"]["char_id"] == 0x0F
        or start["port3"]["char_id"] == 0x0F
        or start["port4"]["char_id"] == 0x0F
    ):
        return True
    else:
        return False


def process_files():
    replay_count = 0
    puff_replay = 0
    non_puff_replay = 0
    game_time = []
    puff_game_time = []
    non_puff_game_time = []
    for root, dirs, files in os.walk("../replays/Fight-Pitt-9/"):
        for f in files:
            if f.endswith(".slp"):
                filename = root + "/" + f
                with open(filename, "rb") as replay:
                    index = 1
                    decoded = decode_file(replay)
                    event_payload = process_event_payload(decoded)
                    index += event_payload["event"]
                    start = process_game_start(
                        decoded["raw"][index : index + event_payload["start"] + 1]
                    )
                    game_time.append(decoded["metadata"]["lastFrame"])
                    if check_puff(start):
                        puff_game_time.append(decoded["metadata"]["lastFrame"])
                        puff_replay += 1
                    else:
                        non_puff_replay += 1
                        non_puff_game_time.append(decoded["metadata"]["lastFrame"])
                replay_count += 1
    print("puff median: {0:.2f} seconds".format(np.median(puff_game_time) / 60))
    print("puff mean: {0:.2f} seconds".format(np.mean(puff_game_time) / 60))
    print("puff replay count: {}".format(puff_replay))
    print()
    print("non-puff median: {0:.2f} seconds".format(np.median(non_puff_game_time) / 60))
    print("non-puff mean: {0:.2f} seconds".format(np.mean(non_puff_game_time) / 60))
    print("non-puff replay count: {}".format(non_puff_replay))
    print()
    print("total median: {0:.2f} seconds".format(np.median(game_time) / 60))
    print("total mean: {0:.2f} seconds".format(np.mean(game_time) / 60))
    print("total replay count: {}".format(replay_count))


if __name__ == "__main__":
    process_files()

