from PIL import Image
import numpy as np

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

