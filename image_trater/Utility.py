import math


def eval_diagonal(width, height):
    return math.ceil(math.sqrt(width ** 2 + height ** 2))


def compression_coefficient(pixel1, pixel2, eval_func, strategy):
    x1, y1 = pixel1
    x2, y2 = pixel2
    d1 = eval_func(x1, y1)
    d2 = eval_func(x2, y2)
    c1, c2 = strategy(d1, d2)
    return c1, c2


def merge_pixel(current_pixel, pixel, c1, c2):
    """
    Merge two pixels with given coefficients.

    Args:
        current_pixel: Tuple representing the RGB values of the current pixel.
        pixel: Tuple representing the RGB values of the new pixel.
        c1: Coefficient for the current pixel.
        c2: Coefficient for the new pixel.

    Returns:
        Tuple representing the merged RGB values of the two pixels.
    """
    return tuple(int(c1 * m + c2 * n) for m, n in zip(current_pixel, pixel))
