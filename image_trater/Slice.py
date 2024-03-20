import os
import numpy as np
import pydicom
from PIL import Image

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

    def _private_cut_image(self, src, pos1, pos2, debug=False):
        """
        This function takes an image from src
        and return a list of pixels and a list of coefficients
        Args:
        src: str
            The source of the image
        slice_info: tuple
            The equation of the straight line
        """
        image = Image.open(src)
        image = image.convert("RGBA")
        width, height = image.size

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

            pix_color = image.getpixel((x, y))
            pix.set_color(pix_color)

            coeff_bright = pix.get_brightness()

            if debug:
                print(
                    f"Coordonnées du pixel : ({x}, {y}), Valeur du pixel : {pix_color}, Coeff Bright : {coeff_bright}")

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


    def cut_dicom_image(self, src, slice_info, debug=False):
        """
        This function takes a DICOM image from src and returns a list of pixels and a list of coefficients
        Args:
        src: str
            The source of the DICOM image
        slice_info: tuple
            The equation of the straight line
        """
        p, q = slice_info

        # Read DICOM file
        dicom_data = pydicom.dcmread(src)

        # Extract pixel data
        image_data = dicom_data.pixel_array

        width, height = image_data.shape

        res = []

        donati = Donati(p, q)  # y = px + q
        strategy = Coeff_Strategy()

        for y in range(height):
            for x in range(width):
                index = x if p <= 1 else y
                pixel = image_data[y, x]  # Note: DICOM data is accessed in (row, column) format
                if debug:
                    print(f"Coordinates of the pixel: ({x}, {y}), Value of the pixel: {pixel}")
                if donati.is_point_on(x, y):
                    # print(f"Pixel: ({x}, {y}), is on point. Value of the pixel: {pixel}")
                    # if there is a pixel located at the index position, then return True
                    if len(res) <= index:
                        res.append([Pixel(x, y, pixel)])
                    else:
                        res[index].append(Pixel(x, y, pixel))

        if debug:
            print(f"Result array length = {len(res)}.")
        # res = [pixel if pixel is not None else self.default_pixel_color for pixel in res]
        if debug:
            print(f"Result array length after treatment = {len(res)}.")
            print(f"Result array = {res}")

        coef_list = map_coef_list(res, donati, strategy)
        # print(f"coef list = {coef_list}")
        # NOTE: BE CAREFUL with the index of the pixel
        # pixels = [pixel[0].get_color() for pixel in res]

        # print(f"pixel colors : {[pixel[0].get_color() for pixel in res]}")
        # print position
        # print(f"pixel positions : {[pixel[0].get_position() for pixel in res]}")
        return res, coef_list

    def generate_dicom_image(self, slice_info, src, dst, debug=False):
        """
        This function takes DICOM images from src, processes them, and saves the results in dst.
        Args:
        src: str
            The source directory containing DICOM files.
        dst: str
            The destination file path to save the resulting image.
        slice_info: tuple
            The equation of the straight line.
        """
        counter = 0
        # Check if the folder exists
        if not os.path.isdir(src):
            print(f"Folder '{src}' does not exist.")
            return
        
        # Get a list of files in the folder
        dicom_files = [file for file in os.listdir(src) if file.endswith('.dcm')]
        dicmlist_len = len(dicom_files)

        if dicmlist_len == 0:
            print(f"No DICOM files found in '{src}'.")
            return

        matrix_res = []

        for dicom_file in dicom_files:
            # Get the full path of the file
            file_path = os.path.join(src, dicom_file)
            # Check if the file is a DICOM file
            if os.path.isfile(file_path):
                # Read DICOM file
                dicom_data = pydicom.dcmread(file_path)
                if hasattr(dicom_data, 'SliceLocation'):
                    try:
                        # Extract pixel data
                        image_data = dicom_data.pixel_array
                        # Use cut_image to process the image
                        res, coef_list = self.cut_dicom_image(file_path, slice_info, debug)
                        # append pixel color to the list if if the position is on the line
                        matrix_res.append(list(map(lambda pix: pix[0].get_color(), res)))
                    except Exception as e:
                        print(f"Error processing '{dicom_file}': {e}")
                    counter += 1
                    print(f"Processed {counter} of {dicmlist_len} DICOM files.")

        # print(f" ------------- Matrix res -------------\n{matrix_res}")
        matrix_res = np.array(matrix_res, dtype=np.uint8)
        im = Image.fromarray(matrix_res)
        # Rotate the image 180 degrees
        im = im.rotate(180)
        im.save(dst)
        print("done")    

    def generate_image(self, slice_info, src, dst, debug=False):
        """
        This function takes an image from src
        and saves the results in dst
        Args:
        src: str
            The source of the image
        dst: str
            The destination of the image
        """
        # Check if the folder exists
        if not os.path.isdir(src):
            print(f"Folder '{src}' does not exist.")
            return

        # Get a list of files in the folder
        images = os.listdir(src)

        matrix_res = []

        for img in images:
            # Get the full path of the file
            file_path = os.path.join(src, img)
            # Check if the file is an image
            if os.path.isfile(file_path) and any(img.endswith(ext) for ext in self.ACCEPTED_IMAGES):
                # Open the image using PIL
                try:
                    img = Image.open(file_path)
                    self.res, coef_list = self._private_cut_image(file_path, pos1, pos2, debug)

                    if debug:
                        print(f"Image '{img}' size: {img.size}")
                        print(f"self.res = {self.res}")
                        print(f"coef_list = {coef_list}")

                    # appends the result to the list
                    matrix_res.append(
                        list(map(lambda pix: pix.get_color(), merge_pixels(pixels=self.res, coefs=coef_list,
                                                                           debug=debug))))
                except Exception as e:
                    print(f"Error processing '{img}': {e}")

        matrix_res = np.array(matrix_res, dtype=np.uint8)
        im = Image.fromarray(matrix_res)
        im.save(dst)
        print("done")