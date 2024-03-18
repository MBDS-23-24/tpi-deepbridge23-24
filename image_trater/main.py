# from image_trater.Slice import Slice
from Slice import Slice
import os


def run(src, dest, slice_info=(1.5, -.33)):  # (p, q) values for line equation (px + q = y)
    _slice = Slice()
    return _slice.generate_image(slice_info, src, dest, debug=True)


if __name__ == "__main__":
    path = os.getcwd()
    run(f"{path}/examples/tests/line2D/3_div_2x", f"{path}/examples/tests/line2D/results/3_div_2x.png")
