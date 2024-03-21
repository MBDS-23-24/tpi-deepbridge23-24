# from image_trater.Slice import Slice
import sys

from Slice import Slice
import os
import time


def run(posa, posb, src, dest):
    _slice = Slice()
    return _slice.generate_dicom_image(posa, posb, src, dest, debug=True)


if __name__ == "__main__":
    # value defined for straight line equation : y = px + q
    # TODO: define p and q
    path = os.getcwd()
    pos1 = (0, 0)
    pos2 = (511, 511)
    start_time = time.time()  # Record start time
    # run(pos1, pos2, f"{path}/examples/tests/line2D/set/1.2.840.113619.2.359.3.1695209168.411.1506489095.532.1.dcm", f"{path}/examples/tests/line2D/results/example1.png")
    run(pos1, pos2, f"{path}/examples/tests/line2D/set/patients/patient1/", dest=f"{path}/examples/tests/line2D/results/maybe.png")
    end_time = time.time()  # Record end time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
