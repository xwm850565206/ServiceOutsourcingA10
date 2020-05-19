import numpy as np
from numba import jit

from datahelper.utils import binary_segment


def is_binary_segment(segment):
    return segment in binary_segment


@jit()
def sub(array, other, segment):
    res = np.zeros(array.shape)

    if len(array.shape) == 1:
        for j in range(len(array)):
            if is_binary_segment(segment[j]):
                res[j] = 1 if np.bitwise_xor(int(array[j]), int(other[j])) != 0 else 0
            else:
                res[j] = array[j] - other[j]
    elif len(array.shape) > 1:
        for i in range(len(array[0])):
            if is_binary_segment(segment[i]):
                for j in range(len(array)):
                    res[j, i] = 1 if np.bitwise_xor(int(array[j, i]), int(other[j, i])) != 0 else 0
            else:
                res[:, i] = array[:, i] - other[:, i]

    return res
