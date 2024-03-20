from Pixel import Pixel
from Criteria import CriteriaBrightness


def compression_coefficient(x: list[any], eval_func, strategy):
    """
    Compute the compression coefficient of a list of pixels.

    Args:
        x: List of pixels.
        eval_func: Function to compute the criteria from a pixel.
        strategy: Strategy to compute the compression coefficient.

    Returns:
        The compression coefficient.
    """

    criteria_list = list(map(lambda elem: eval_func(elem), x))
    criteria_object = CriteriaBrightness(criteria_list)
    return strategy(criteria_object)


def merge_pixels(pixels: list, coefs: list, debug=False):
    """
    Merge a list of pixels with given coefficients respectives in coefs.

    Args:
        pixels : List of pixels.
        coefs : List of coefficients.

    Returns:
        List representing the merged RGBA values of the pixel list.
        :param coefs:
        :param pixels:
        :param debug:
    """
    if len(pixels) != len(coefs):
        raise ValueError("Number of pixels and coefficients must be the same.")
    res = []
    for i in range(0, len(pixels)):
        res.append(merge_pixel(pixels[i], coefs[i], debug))

    return res


def merge_pixel(pixel, coef, debug=False):
    for i in range(0, len(coef)):  # handle alpha
        if i == 0:
            coef[i].append(1.0)
        else:
            coef[i].append(0.0)

    pcs = list(zip(pixel, coef))
    _p, _c = pcs[0]
    x, y = _p.get_position()
    col = tuple(_pigment * _fact for _pigment, _fact in zip(_p.get_color(), _c))
    for i in range(1, len(pcs)):
        p, c = pcs[i]
        new_pigment = tuple(pigment * fact for pigment, fact in zip(p.get_color(), c))
        col = tuple(sum(item) for item in zip(col, new_pigment))
    if debug and len(pixel) > 1:
        print(f"final color {col} for coord {(x, y)}!")
    return Pixel(x, y, col)


def map_coef_list(ls, eval_func, strategy):
    return list(
        map(
            lambda x:
                compression_coefficient(x, eval_func, strategy), ls
        )
    )
