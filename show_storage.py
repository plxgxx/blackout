import datetime
import os
import pathlib
import pickle
import pprint
import sys
import time

import bot

sys.modules["bot"] = bot


storage = pathlib.Path(__file__).with_name("storage")


def _print_storage():
    with open(storage, "rb") as fp:  # pylint: disable=invalid-name
        obj = pickle.load(fp)
    pprint.pprint(obj)


def stream_pickle():
    stream = input("Stream storage data? [Y/N]: ") == "Y"
    print()

    if not stream:
        _print_storage()
    else:
        try:
            while True:
                os.system("clear")
                print("Time:", datetime.datetime.now().strftime("%M:%S"), "\n")
                _print_storage()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStream suspended")


if __name__ == "__main__":
    stream_pickle()
