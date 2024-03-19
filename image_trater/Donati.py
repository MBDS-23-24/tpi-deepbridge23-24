from Xiaolin_Algo import draw_xiaolin_line


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

    def draw_xiaolin(self, bound_x, bound_y):
        x1 = 0
        y1 = self.q

        x2 = bound_x
        y2 = self.resolve(x2)
        if y2 > bound_y:
            x2 = self.resolve_with_image(bound_y)
            y2 = self.resolve(x2)

        return draw_xiaolin_line(x1, y1, x2, y2)



