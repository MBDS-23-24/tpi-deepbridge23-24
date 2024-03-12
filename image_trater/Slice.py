# from image_trater.Coeff_Strategy import Coeff_Strategy
# from image_trater.Donati import Donati
# from image_trater.Utility import compression_coefficient, merge_pixel

from PIL import Image
from Pixel import Pixel

from Coeff_Strategy import Coeff_Strategy
from Donati import Donati
from Utility import map_coef_list
# from Utility import compression_coefficient, merge_pixel

class Slice:
    default_pixel_color = (255, 0, 0, 255)
    nb_images = 1

    def __init__(self):
        pass

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
        p, q = slice_info
        image = Image.open(src)

        height, width = image.size

        # Get pixels
        # list(image.getdata())
        res = [] 

        donati = Donati(p, q)  # y = px + q
        strategy = Coeff_Strategy()

        for y in range(height):
            for x in range(width):
                index = x if p <= 1 else y
                pixel = image.getpixel((x, y))

                if debug:
                    print(f"Coordonnées du pixel : ({x}, {y}), Valeur du pixel : {pixel}")

                if donati.is_point_on(x, y):

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
        # Put the pixels into the image
        im = Image.new('RGBA', (len(res), self.nb_images))
        # execute
        im.putdata(res)
        # Save the image
        im.save(dst)
