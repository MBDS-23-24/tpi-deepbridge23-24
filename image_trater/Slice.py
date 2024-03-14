# from image_trater.Coeff_Strategy import Coeff_Strategy
# from image_trater.Donati import Donati
# from image_trater.Utility import compression_coefficient, merge_pixel

from PIL import Image
from Pixel import Pixel

from Coeff_Strategy import Coeff_Strategy
from Donati import Donati
from Utility import map_coef_list
from Utility import merge_pixels

class Slice:
    default_pixel_color = (255, 0, 0, 1)
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
        image = image.convert("RGBA")

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
        print(f"coef list = {coef_list}")
        # NOTE : BE CAREFUL with the index of the pixel
        # pixels = [pixel[0].get_color() for pixel in res]

        print(f"pixel colors : {[pixel[0].get_color() for pixel in res]}")
        # print position
        print(f"pixel positions : {[pixel[0].get_position() for pixel in res]}")
        
        # Put the pixels into the image
        im = Image.new('RGBA', (len(res), self.nb_images))
        im.putdata(list(map(lambda pix: pix.get_color(), merge_pixels(pixels=res, coefs=coef_list, debug=True))))
        # Save the image
        im.save(dst)
        print("done")
