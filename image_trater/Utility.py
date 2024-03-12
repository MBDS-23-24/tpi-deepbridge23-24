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


def merge_pixel(pixels:list, coefs:list):
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

    return tuple(int(sum(c * p[i] for i, c in enumerate(coefs))) for p in zip(*pixels))

def map_coef_list(ls, donati:Donati, strategy:Coeff_Strategy):
    return list(map(lambda x: [1] if len(x) == 1
                    else compression_coefficient(
                        x, donati.get_distance_from_point, 
                        strategy.eval_coeff_by_max_dist)
                        , ls))
