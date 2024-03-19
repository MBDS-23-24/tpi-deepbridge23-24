class Pixel:
    def __init__(self, x, y, color, brightness=(1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.color = color
        self.brightness = brightness

    def __str__(self):
        return "Pixel(x={}, y={}, color={}, brightness={})".format(
            self.x, self.y, self.color, self.brightness
        )

    def get_position(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def get_brightness(self):
        return self.brightness

    def adjust_brightness(self, brightness_factor):
        """
        Adjust the brightness of the pixel's color.

        Args:
            brightness_factor (tuple): Brightness adjustment factors for each channel.
                                        Values greater than 1 increase brightness,
                                        values between 0 and 1 decrease brightness.
        """
        self.brightness = tuple(
            min(1.0, max(0.0, bf)) for bf in brightness_factor
        )

    def set_color(self, rgba):
        """
        Set color of the pixel.

        Args:
            rgba (tuple) : (red, green, blue, alpha)
        """
        self.color = rgba