import numpy as np


def find_max_friends(candys):
    nunique = np.unique(candys, return_counts=True)[1]
    return min(nunique)

