import os
import numpy as np
import pydicom
from PIL import Image
from multiprocessing import Pool

from CoeffStrategy import CoeffStrategy
from Line import Line
from Utility import map_coef_list
from Utility import merge_pixels


class Slice:
    default_pixel_color = (255, 0, 0, 1)
    ACCEPTED_IMAGES = ['.jpg', '.jpeg', '.png', '.bmp']
    last_res = {}

    def __init__(self):
        self.res = {}

    def dicom_to_rgba_array(self, dicom_file_path):
        # Read the DICOM file
        dicom_data = pydicom.dcmread(dicom_file_path)

        # Normalize pixel values to the range [0, 1]
        normalized_data = dicom_data.pixel_array.astype(float) / np.max(dicom_data.pixel_array)

        # Convert grayscale to RGBA by duplicating the pixel values across all color channels
        rgba_data = np.repeat(normalized_data[..., np.newaxis], 4, axis=-1)

        # Set alpha channel based on DICOM metadata (if available)
        if hasattr(dicom_data, 'WindowCenter') and hasattr(dicom_data, 'WindowWidth'):
            window_center = dicom_data.WindowCenter
            window_width = dicom_data.WindowWidth
            min_value = window_center - window_width / 2
            max_value = window_center + window_width / 2
            alpha_channel = ((dicom_data.pixel_array >= min_value) & (dicom_data.pixel_array <= max_value)).astype(np.uint8) * 255
            rgba_data[:, :, 3] = alpha_channel
        else:
            # Default to fully opaque if DICOM metadata is not available
            rgba_data[:, :, 3] = 255

        # Convert pixel values to uint8
        rgba_data = (rgba_data * 255).astype(np.uint8)

        return rgba_data

    def cut_dicom_image(self, src, pos1, pos2, debug=False):
        """
        This function takes a DICOM image from src and returns a list of pixels and a list of coefficients
        Args:
        src: str
            The source of the DICOM image
        slice_info: tuple
            The equation of the straight line
        """

        # Read DICOM file
        dicom_data = pydicom.dcmread(src)

        # Extract pixel data
        image = dicom_data.pixel_array

        width, height = image.shape

        self.res = {}
        x1, y1 = pos1
        x2, y2 = pos2
        line = Line(x1, y1, x2, y2)
        p = line.get_sleep()
        strategy = CoeffStrategy()

        _l = line.draw_xiaolin()  # return a list of Pixels
        _l = list(filter(lambda _p: sum(_p.get_brightness()) > 0.0, _l))

        if debug:
            print(f"Pixels returned by xiaolin : {_l}")

        for pix in _l:
            x, y = pix.get_position()

            if not (0 <= x < width) or not (0 <= y < height):
                continue

            index = x if p <= 1 else y

            if debug:
                print(f"index value is {index}")

            pixel = self.dicom_to_rgba_array(src)[x, y]
            pix.set_color(pixel)

            coeff_bright = pix.get_brightness()

            #if debug:
                #print(f"Coordonnées du pixel : ({x}, {y}), Valeur du pixel : {pix_color}, Coeff Bright : {coeff_bright}")

            # if there is a pixel located at the index position, then return True
            if index in self.res:
                self.res[index].append(pix)
            else:
                self.res[index] = [pix]

        if debug:
            print(f"Result array of pixel retrieved on images thanks to xiaolin line {self.res}")
            print(f"Result array length = {len(self.res)}.")

        # TODO: May be interesting to change the structure of res to prevent sorting ?
        self.res = dict(sorted(self.res.items()))

        coef_list = map_coef_list(list(self.res.values()), lambda _pix: _pix.get_brightness(),
                                  strategy.eval_coeff_by_density)

        if debug:
            print(f"coef list = {coef_list}")

        return list(self.res.values()), coef_list

    def process_dicom_file(self, file_path, pos1, pos2, debug=False):
        try:
            # Read DICOM file
            dicom_data = pydicom.dcmread(file_path)
            if hasattr(dicom_data, 'SliceLocation'):
                # Extract pixel data
                #image_data = dicom_data.pixel_array
                # Use cut_image to process the image
                res, coef_list = self.cut_dicom_image(file_path, pos1, pos2, debug)
                # Append pixel color to the list if the position is on the line
                return list(map(lambda pix: pix[0].get_color(), res))
        except Exception as e:
            print(f"Error processing '{file_path}': {e}")
        return []

    def generate_dicom_image(self, pos1, pos2, src, dst, debug=False):
        if not os.path.isdir(src):
            print(f"Folder '{src}' does not exist.")
            return

        dicom_files = [file for file in os.listdir(src) if file.endswith('.dcm')]
        dicmlist_len = len(dicom_files)

        if dicmlist_len == 0:
            print(f"No DICOM files found in '{src}'.")
            return

        matrix_res = []
        pool = Pool()  # Create a pool of worker processes

        # Process DICOM files in parallel
        results = [pool.apply_async(self.process_dicom_file, (os.path.join(src, file), pos1, pos2, debug)) for file in dicom_files]

        for result in results:
            matrix_res.append(result.get())

        pool.close()
        pool.join()

        matrix_res = np.array(matrix_res, dtype=np.uint8)
        im = Image.fromarray(matrix_res)
        im = im.rotate(180)
        im.save(dst)
        print("done") 
