from image_trater.Coeff_Strategy import Coeff_Strategy
from image_trater.Donati import Donati
from image_trater.Utility import compression_coefficient
from PIL import Image


class Slice:
    default_pixel = None

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

        # Convert in RGB
        image = image.convert("RGB")

        # Get pixels
        pixels = list(image.getdata())
        res = [None for _ in range(0, len(pixels))]

        donati = Donati(p, q)  # y = px + q
        strategy = Coeff_Strategy()

        yy, xx = image.size

        for y in range(yy):
            for x in range(xx):
                pixel = image.getpixel((x, y))

                if debug:
                    print(f"Coordonnées du pixel : ({x}, {y}), Valeur du pixel : {pixel}")

                if donati.is_point_on(x, y):
                    index = x if q < 1 else y

                    if res[index] is None:
                        res[index] = pixel
                    else:
                        current_pixel = res[index]
                        c1, c2 = compression_coefficient(current_pixel, pixel, donati.get_distance_from_point,
                                                         strategy.eval_coeff_by_max_dist)
                        res[index] = (current_pixel, pixel, c1, c2)

            res = [pixel if pixel is not None else self.default_pixel for pixel in res]

            # Put the pixels into the image
            image.putdata(pixels)

            # Save the image
            image.save(dst)
