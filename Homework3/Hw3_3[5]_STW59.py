"""
Kirill and Stephen worked together on the coding part.
Kirill: math parts
Stephen: recursive algorithms
"""

import numpy as np


def ave_r(r1, r, kt):
    return np.exp((-4*((r1 / r)**12 - (r1 / r)**6)/kt))


def main():
    r1 = float(1)

    for kt in range(1, 11, 1):
        if kt in [1, 2, 5, 10]:
            top_sum = 0
            bottom_sum = 0
            for r in np.arange(0.01, 10.01, 0.01):
                top_sum += r * ave_r(r1, r, kt)
                bottom_sum += ave_r(r1, r, kt)

            r_avg = top_sum / bottom_sum
            print('At kt = {}, r_avg = {}.'.format(kt, r_avg))


main()
