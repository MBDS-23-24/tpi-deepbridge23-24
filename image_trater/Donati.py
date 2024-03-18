class Donati:
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def resolve(self, x):
        return (self.p * x) + self.q

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
        x1 = 0
        y1 = self.q

        x2 = bound_x
        y2 = self.resolve(x2)
        while y2 > 0 and y2 > bound_y: # if y2 is out of the image bounds in y axe
            x2 = x2 - 1
            y2 = self.resolve(x2)

        if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
            raise Exception(f"Coord under 0 : x1={x1}, y1={y1}, x2={x2}, y2={y2}")

        dx = x2 - x1
        dy = y2 - y1
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            return [(x1, y1)]  # Handle case where start and end points are the same

        incr_x = dx / steps
        incr_y = dy / steps
        _l = []
        x = float(x1)
        y = float(y1)

        for _ in range(steps):
            _l.append((int(x) if isinstance(x, float) else x, int(y) if isinstance(y, float) else y))
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
