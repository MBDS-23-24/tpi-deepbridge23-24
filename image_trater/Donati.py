import math


class Donati:
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def resolve(self, x):
        return (self.p * x) + self.q

    def resolve_with_image(self, y):
        return (y - self.q) / self.p

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
        """
        This function takes the bound of an image.
        It returns a list of pixel that is on the donati slope.
        /!\ Take care : This solution do not cover each pixel touching the slope...

        Args:
        x: int
            The width of an image
        y: int
            The height of an image
        """
        x1 = 0
        y1 = self.q

        x2 = bound_x
        y2 = self.resolve(x2)
        if y2 > bound_y:
            x2 = self.resolve_with_image(bound_y)
            y2 = self.resolve(x2)

        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return [(x1, y1)]  # Handle case where start and end points are the same

        incr_x = dx / steps
        incr_y = dy / steps
        _l = []
        x = float(x1)
        y = float(y1)

        for _ in range(math.ceil(steps)):
            _l.append((math.floor(x) if isinstance(x, float) else x, math.floor(y) if isinstance(y, float) else y))
            x = x + incr_x
            y = y + incr_y

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
