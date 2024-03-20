import os
import numpy as np
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

    def generate_image(self, pos1, pos2, src, dst, debug=False):
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

