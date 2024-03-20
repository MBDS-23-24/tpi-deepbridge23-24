# from image_trater.Slice import Slice
from Slice import Slice
import os
import time

def run(src, dest, slice_info=(350, 0)):
    _slice = Slice()
    return _slice.generate_dicom_image(src=src, dst=dest, slice_info=slice_info)

if __name__ == "__main__":
    # value defined for straight line equation : y = px + q
    # TODO: define p and q
    path = os.getcwd()
    start_time = time.time()  # Record start time
    run(f"{path}/examples/tests/line2D/set/patients/patient1/", dest=f"{path}/examples/tests/line2D/results/maybe.png")
    end_time = time.time()  # Record end time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
