from image_trater.Slice import Slice


def run(src, dest, slice_info=(1, -1)):
    _slice = Slice()
    return _slice.generate_image(slice_info, src, dest, debug=True)
    



if __name__ == "__main__":
    # value defined for straight line equation : y = px + q
    # TODO: define p and q

    src = "../examples/tests/line2D/set"
    slice_info = (1, -1)
    merged_images = "../examples/tests/line2D/results"
    run(src, merged_images, slice_info)
    # run("../examples/tests/line2D/set/example1.png", "../examples/tests/line2D/results/example1.png")

    _slice = Slice()
    
    _slice.merge_images(src, merged_images)




