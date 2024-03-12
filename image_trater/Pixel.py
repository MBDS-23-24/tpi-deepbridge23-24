class Pixel:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return "Pixel(x={}, y={}, color={})".format(self.x, self.y, self.color)
    
    def get_position(self):
        return self.x, self.y
    
    def get_color(self):
        return self.color