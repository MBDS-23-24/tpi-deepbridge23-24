import os
import numpy as np
from PIL import Image, ImageDraw
import time
class Donati:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        
    def bresenhams_line_algorithm(self, x0, y0, x1, y1):
        """
        Implementation of the Bresenham's line algorithm.
        
        Args:
        x0, y0: int
            The x and y coordinates of the start point of the line
        x1, y1: int
            The x and y coordinates of the end point of the line
            
        Returns:
        A list of tuples representing the points on the line
        """
        points = []
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy  
        while True:
            points.append((x0, y0))  # Add the current point to the list
            if x0 == x1 and y0 == y1:  # Stop if we've reached the end point
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx: 
                err += dx
                y0 += sy
        return points
    
    def get_line_pixels(self, image, points_on_line):
        """
        Extracts the pixel values from the image along the points of the line.

        Args:
        image: PIL.Image
            The image from which to extract the pixel values.
        points_on_line: list of tuples
            The (x, y) coordinates of the points on the line.

        Returns:
        A numpy array of pixel values.
        """
        pixel_values = []
        for point in points_on_line:
            if point[0] < image.width and point[1] < image.height:
                pixel_values.append(image.getpixel(point))
        return (pixel_values)

    def process_images_in_folder(self, folder_path, start_point, end_point):
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                file_path = os.path.join(folder_path, filename)
                image = Image.open(file_path)
                
                # Déterminer les points de la ligne avec l'algorithme de Bresenham
                points_on_line = self.bresenhams_line_algorithm(*start_point, *end_point)

                # Dessiner la ligne sur une copie de l'image pour la visualisation
                visual_image = image.copy()
                draw = ImageDraw.Draw(visual_image)
                for point in points_on_line:
                    draw.point(point, 'black')
                visual_image.save(os.path.join(folder_path, f"visual_{filename}"))

                # Extraire les valeurs des pixels de l'image originale le long de la ligne
                pixel_values = self.get_line_pixels(image, points_on_line)
                if not pixel_values:
                    print("No pixels found on line, skipping line image creation.")
                    continue

            # Créer une nouvelle image composée uniquement des pixels le long de la ligne
            line_image_length = len(pixel_values)
            line_image = Image.new('RGB', (line_image_length, 1))
            line_image.putdata(pixel_values)
            line_image.save(os.path.join(folder_path, f"line_{filename}"), 'PNG')
            print(f"Line image saved as line_{filename}")

                
    def is_point_on(self, x, y):
        """
        This function takes a point and returns
        True if the point is on the curve, False
        otherwise

        Args:
        x: int
            The x coordinate of the point
        y: int
            The y coordinate of the point
        """
        # The equation of the curve is: y = p*x + q
        return y == self.p * x + self.q

    def get_distance_from_point(self, x, y):
        """
        This function takes a point and returns
        the distance from the point to the curve

        Args:
        x: int
            The x coordinate of the point
        y: int
            The y coordinate of the point
        """
        # The equation of the curve is: y = p*x + q
        return abs(y - (self.p * x + self.q))
    
    def get_line_coordinates(self, x0, y0, x1, y1):
        """
        This function takes two points and returns
        the coordinates of the line that connects
        the two points

        Args:
        x0, y0: int
            The x and y coordinates of the start point of the line
        x1, y1: int
            The x and y coordinates of the end point of the line
        """
        return self.bresenhams_line_algorithm(x0, y0, x1, y1)

if __name__ == "__main__":
    line = Donati(p=1, q=0)
    start_point = (0, 0)
    end_point = (341, 512)
    relative_folder_path = "examples/tests/line2D/set"
    absolute_folder_path = os.path.join(os.getcwd(), relative_folder_path)
    start_time = time.time()  
    line.process_images_in_folder(absolute_folder_path, start_point, end_point)
    # Récupérez les coordonnées de la ligne
    line_coordinates = line.get_line_coordinates(*start_point, *end_point)
    print("Line Coordinates:", line_coordinates)
    end_time = time.time()  
    elapsed_time = end_time - start_time
    print(f"Temps écoulé : {elapsed_time} secondes")
    
    