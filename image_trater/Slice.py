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

    def image_to_2d_array(self, path):
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
    
    def generate_image_from_array(self, array, path):
        """
        This function takes an array and saves
        the results in path as an image (size height:1px, width:len(array)px)
        
        Args:
        array: np.array
            The 2D array
        path: str
            The path to the image
        """
        img = Image.fromarray(array)
        img.save(path)
        
    
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
                    # append the pixel content to pixels_on_curve
                    pixels_on_curve.append(img[i][j])
        pixels_on_curve = np.array(pixels_on_curve)
        self.generate_image_from_array(pixels_on_curve, "result.jpg")
        return pixels_on_curve

    