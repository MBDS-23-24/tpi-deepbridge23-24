import math
from Pixel import Pixel
from Coeff_Strategy import Coeff_Strategy
from Donati import Donati

# NOTE : Deprecated
# def eval_diagonal(width, height):
#     return math.ceil(math.sqrt(width ** 2 + height ** 2))


def compression_coefficient(x:list, eval_func, strategy):
    """
    Compute the compression coefficient of a list of pixels.

    Args:
        x: List of pixels.
        eval_func: Function to compute the distance from a point.
        strategy: Strategy to compute the compression coefficient.

    Returns:
        The compression coefficient.
    """

    distance_list = list(map(lambda y: eval_func(y[0].get_position()), x))
    return strategy(distance_list)


def merge_pixels(pixels:list, coefs:list, debug=False):
    """
    Merge a list of pixels with given coefficients respectives in coefs.

    Args:
        pixels : List of pixels.
        coefs : List of coefficients.

    Returns:
        List representing the merged RGBA values of the pixel list.
    """
    if len(pixels) != len(coefs):
        raise ValueError("Number of pixels and coefficients must be the same.")
    res = []
    for i in range(0, len(pixels)):
        res.append(merge_pixel(pixels[i], coefs[i], debug))

    return res

def merge_pixel(pixel, coef, debug=False):
    pcs = list(zip(pixel, coef))
    _p, _c = pcs[0]
    x, y = _p.get_position()
    col = tuple(_pigment * _c for _pigment in _p.get_color())
    for i in range(1, len(pcs)):
        p, c = pcs[i]
        new_pigment = tuple(pigment * c for pigment in p.get_color())
        col += tuple(a + b for a, b in zip(col, new_pigment))
    if debug and len(pixel) > 1:
        print(f"final color {col} for coord {(x,y)}!")
    return Pixel(x, y, col)

def map_coef_list(ls, donati:Donati, strategy:Coeff_Strategy):
    return list(map(lambda x: [1] if len(x) == 1
                    else compression_coefficient(
                        x, donati.get_distance_from_point, 
                        strategy.eval_coeff_by_max_dist)
                        , ls))
