# from image_trater.Slice import Slice
import sys

from Slice import Slice
import os


def run(src, dest):
    _slice = Slice()
    return _slice.generate_image(src, dest, debug=True)


if __name__ == "__main__":
    # value defined for straight line equation : y = px + q
    # TODO: define p and q
    path = os.getcwd()
    run(f"{path}/examples/tests/line2D/set/", f"{path}/examples/tests/line2D/results/example1.png")
