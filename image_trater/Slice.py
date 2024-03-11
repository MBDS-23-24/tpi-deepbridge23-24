from PIL import Image
import numpy as np
from Donati import Donati

class Slice:

    def __init__(self):
        pass

    def generate_image(self, src, dst):
        """
        This function takes an image from src
        and saves the results in dst

        Args:
        src: str
            The source of the image
        dst: str
            The destination of the image
        """
        pass

    def image_to_2d_array(path):
        """
        This function takes an image and returns
        a 2D array
        
        Args:
        path: str
            The path to the image
        """

        img = Image.open(path)
        # Convert the image to a NumPy array
        return np.array(img)
    
    def get_pixels_on_curve(self, p, q, path):
        """
        This function takes an image and returns
        the pixels on the curve
        
        Args:
        p: int
            The slope of the curve
        q: int
            The y-intercept of the curve
        path: str
            The path to the image
        """
        img = self.image_to_2d_array(path)
        pixels_on_curve = []
        for i in range(len(img)):
            for j in range(len(img[i])):
                if Donati(p, q).is_point_on(i, j):
                    pixels_on_curve.append((i, j))
        return pixels_on_curve

