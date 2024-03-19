import math

from Pixel import Pixel


def plot(x, y, c):
    assert (1 >= c >= 0)
    return Pixel(x, y, (0, 0, 0), (c, c, c))


def fractional_part(x):
    return x - math.floor(x)


def reverse_fractional_part(x):
    return 1 - fractional_part(x)


def swap(a, b):
    return b, a


def draw_xiaolin_line(x0, y0, x1, y1):
    pixels_history = []
    is_steep = abs(y1 - y0) > abs(x1 - x0)

    if is_steep:
        x0, y0 = swap(x0, y0)
        x1, y1 = swap(x1, y1)

    if x0 > x1:
        x0, x1 = swap(x0, x1)
        y0, y1 = swap(y0, y1)

    dx = x1 - x0
    dy = y1 - y0

    gradient = 1.0
    if dx != 0.0:
        gradient = dy / dx

    # handle first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = reverse_fractional_part(xend + 0.5)
    xpxl1 = xend  # this will be used in the main loop
    ypxl1 = math.floor(yend)

    if is_steep:
        pixels_history.append(plot(ypxl1, xpxl1, reverse_fractional_part(yend) * xgap))
        pixels_history.append(plot(ypxl1 + 1, xpxl1, fractional_part(yend) * xgap))
    else:
        pixels_history.append(plot(xpxl1, ypxl1, reverse_fractional_part(yend) * xgap))
        pixels_history.append(plot(xpxl1, ypxl1 + 1, fractional_part(yend) * xgap))
    intery = yend + gradient  # first y-intersection for the main loop

    # handle second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = reverse_fractional_part(xend + 0.5)
    xpxl2 = xend  # this will be used in the main loop
    ypxl2 = math.floor(yend)

    if is_steep:
        pixels_history.append(plot(ypxl2, xpxl2, reverse_fractional_part(yend) * xgap))
        pixels_history.append(plot(ypxl2 + 1, xpxl2, fractional_part(yend) * xgap))
    else:
        pixels_history.append(plot(xpxl2, ypxl2, reverse_fractional_part(yend) * xgap))
        pixels_history.append(plot(xpxl2, ypxl2 + 1, fractional_part(yend) * xgap))

    # main loop
    for x in range(xpxl1 + 1, xpxl2):
        if is_steep:
            pixels_history.append(plot(math.floor(intery), x, reverse_fractional_part(intery)))
            pixels_history.append(plot(math.floor(intery) + 1, x, fractional_part(intery)))
        else:
            pixels_history.append(plot(x, math.floor(intery), reverse_fractional_part(intery)))
            pixels_history.append(plot(x, math.floor(intery) + 1, fractional_part(intery)))

        intery += gradient

    return pixels_history
