import itertools

import numpy as np
from numpy.typing import NDArray


def scales_permutation(scales: NDArray[np.float64]):
    """
    Generate all permutations of the scales.

    The array_permutations is a 1D array of the same length as the number of permutations.
    The iter_product is an iterator of the permutations.
    """
    scales_list = [dim_scales for dim_scales in scales]

    num_permutations = int(np.prod([len(dim_scales) for dim_scales in scales_list]))

    iter_product = itertools.product(*scales_list)

    array_permutations = np.zeros(num_permutations)

    return array_permutations, iter_product
