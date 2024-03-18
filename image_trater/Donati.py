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
