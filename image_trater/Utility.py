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
