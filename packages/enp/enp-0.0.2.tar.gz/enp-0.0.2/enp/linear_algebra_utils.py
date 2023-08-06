import numpy as np


def aproximately_zero_to_zero(x):
    mask = np.isclose(x, 0, atol=1e-04)
    x[mask] = 0
    return x
