from image_trater.Coeff_Strategy import Coeff_Strategy
from image_trater.Donati import Donati
from image_trater.Utility import compression_coefficient, eval_diagonal, merge_pixel
from PIL import Image


class Slice:
    default_pixel = (255, 0, 0)
    nb_images = 1

    def __init__(self):
        pass

    def generate_image(self, slice_info, src, debug=False):
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

        yy, xx = image.size

        # Get pixels
        list(image.getdata())
        res = [None for _ in range(0, eval_diagonal(xx, yy))]

        donati = Donati(p, q)  # y = px + q
        strategy = Coeff_Strategy()

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
                        res[index] = merge_pixel(current_pixel, pixel, c1, c2)

        # if debug:
        #     print(f"Result array length = {len(res)}.")
        # res = [pixel if pixel is not None else self.default_pixel for pixel in res]
        # if debug:
        #     print(f"Result array length after treatment = {len(res)}.")

        # Prepare the resulting image
        res = [pixel if pixel is not None else self.default_pixel for pixel in res]
        im = Image.new('RGB', (len(res), self.nb_images))
        im.putdata(res)

        # Return the generated image
        return im
    
        ## Put the pixels into the image
        #im = Image.new('RGB', (len(res), self.nb_images))
        #im.putdata(res)
        ## Save the image
        #im.save(dst)

    def merge_images(self, src, merged_images):
        """
        Merge images from the provided paths vertically.
        Args:
            src (list): List of paths to the images to be merged.
            generated_images (str): Path where the merged image will be saved.
        """

        # Prepare the merged image
        images = src
        first_image = images[0]
        max_width = first_image.width
        total_height = 512
        merged_image = Image.new('RGB', (max_width, total_height))

        # Paste each image into the merged image
        y_offset = 0
        for img in images:
            merged_image.paste(img, (0, y_offset))
            y_offset += img.size[1]

        # Save the merged image
            merged_image.save(merged_images)


