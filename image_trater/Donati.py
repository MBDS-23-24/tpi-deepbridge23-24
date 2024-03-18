class Donati:
    def __init__(self, p, q):
        self.p = p
        self.q = q

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


    def dda(self, bound_x, bound_y):
        # Calculate x1 and x2 based on intercepts with x-axis
        x1 = self.p
        x2 = bound_x

        # Calculate y1 and y2 based on the equation of the line
        y1 = self.q
        y2 = bound_y

        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return [(x1, y1)]  # Handle case where start and end points are the same

        incr_x = dx / steps
        incr_y = dy / steps
        _l = []
        x = x1
        y = y1
        for _ in range(steps):
            _l.append((int(x) if isinstance(x, float) else x, int(y) if isinstance(y, float) else y))
            x += incr_x
            y += incr_y
        return _l





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
