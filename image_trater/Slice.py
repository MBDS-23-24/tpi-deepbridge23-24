# from image_trater.Coeff_Strategy import Coeff_Strategy
# from image_trater.Donati import Donati
# from image_trater.Utility import compression_coefficient, merge_pixel
import math
import os

import numpy as np
from PIL import Image

from Coeff_Strategy import Coeff_Strategy
from Line import Line
from Utility import map_coef_list
from Utility import merge_pixels


class Slice:
    default_pixel_color = (255, 0, 0, 1)

    # nb_images = 3

    def __init__(self):
        pass

    def cut_image(self, src, debug=False):
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

        res = {}
        line = Line(1, 0, 1, 2)
        p = line.get_sleep()
        strategy = Coeff_Strategy()

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
            if index in res:
                res[index].append(pix)
            else:
                res[index] = [pix]

        if debug:
            print(f"Result array of pixel retrieved on images thanks to xiaolin line {res}")
            print(f"Result array length = {len(res)}.")

        res = dict(sorted(res.items()))

        coef_list = map_coef_list(list(res.values()), lambda _pix: _pix.get_brightness(),
                                  strategy.eval_coeff_by_density)

        if debug:
            print(f"coef list = {coef_list}")
        # NOTE : BE CAREFUL with the index of the pixel
        # pixels = [pixel[0].get_color() for pixel in res]

        return list(res.values()), coef_list

    def generate_image(self, src, dst, debug=False):
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
            if os.path.isfile(file_path) and any(img.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp']):
                # Open the image using PIL
                try:
                    img = Image.open(file_path)
                    res, coef_list = self.cut_image(file_path, debug)
                    print(f"Image '{img}' size: {img.size}")
                    print(f"res = {res}")
                    print(f"coef_list = {coef_list}")
                    # appends the result to the list
                    matrix_res.append(
                        list(map(lambda pix: pix.get_color(), merge_pixels(pixels=res, coefs=coef_list, debug=True))))
                except Exception as e:
                    print(f"Error processing '{img}': {e}")

        print(f" -------------Matrix res = -------------\n{matrix_res}")
        matrix_res = np.array(matrix_res, dtype=np.uint8)
        im = Image.fromarray(matrix_res)
        im.save(dst)
        print("done")
