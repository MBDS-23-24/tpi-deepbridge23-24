import os
import numpy as np
from PIL import Image, ImageDraw
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
        """
        Processes all images in the given folder path, drawing a line using
        Bresenham's line algorithm between the start_point and end_point.
        It also creates a new image with the pixels along the line.
        Args:
        folder_path: str
            The path to the folder containing images.
        start_point: tuple
            The (x, y) starting coordinates of the line.
        end_point: tuple
            The (x, y) ending coordinates of the line.
        """
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                file_path = os.path.join(folder_path, filename)
                image = Image.open(file_path)
                draw = ImageDraw.Draw(image)
                points_on_line = self.bresenhams_line_algorithm(*start_point, *end_point)
                # Draw each point on the line
                for point in points_on_line:
                    draw.point(point, 'black')
                image.save(os.path.join(folder_path, f"processed_{filename}"))
                print(f"Processed image saved as processed_{filename}")
                # Extract the pixel array along the line
                line_pixel_array = self.get_line_pixels(image, points_on_line)
                # Ensure the array is not empty
            if not line_pixel_array:
                print("No pixels found on line, skipping image creation.")
                continue
            # Determine the length of the line_image based on the number of pixels
            line_image_length = max(len(line_pixel_array), 1)
            # Create a new image with the same mode as the original and the correct size
            line_image_length = len(line_pixel_array)
            line_image = Image.new(image.mode, (line_image_length, 1))
            # Use putdata with the list of tuples to create the line image
            line_image.putdata(line_pixel_array)
            line_image.save(os.path.join(folder_path, f"line_{filename}"))
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
    # Points de départ et de fin pour la ligne à tracer
    start_point = (0, 0)  
    end_point = (10, 10) 
    relative_folder_path = "examples/tests/line2D/set"
    absolute_folder_path = os.path.join(os.getcwd(), relative_folder_path)

    line.process_images_in_folder(absolute_folder_path, start_point, end_point)
    # Récupérez les coordonnées de la ligne
    line_coordinates = line.get_line_coordinates(*start_point, *end_point)
    print("Line Coordinates:", line_coordinates)
    
    
    