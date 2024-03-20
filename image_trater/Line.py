import sys

from Xiaolin_Algo import draw_xiaolin_line


class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def get_sleep(self):
        dy = (self.y1 - self.y0)
        dx = (self.x1 - self.x0)
        return dy/dx if dx != 0 else sys.maxsize

    def draw_xiaolin(self):
        return draw_xiaolin_line(self.x0, self.y0, self.x1, self.y1)

