import Slice


def run(src, dest, slice_info=(1, 0)):
    _slice = Slice()
    return _slice.generate_image(slice_info, src, dest, debug=True)


if __name__ == "__main__":
    # value defined for straight line equation : y = px + q
    # TODO: define p and q
    run("./examples/tests/line2D/set/example1.png", "./examples/tests/line2D/results/example1.png")
