"""
Kirill and Stephen worked together on the coding part.
Kirill: math parts
Stephen: recursive algorithms
"""

import numpy as np


def ave_r(r, kt):
    return np.exp(-r / kt)


def main():
    for kt in range(1, 11, 1):
        if kt in [1, 2, 5, 10]:
            top_sum = 0
            bottom_sum = 0
            for r in np.arange(0.01, 10.01, 0.01):
                top_sum += r * ave_r(r, kt)
                bottom_sum += ave_r(r, kt)

            r_avg = top_sum / bottom_sum
            print('At kt = {}, r_avg = {}.'.format(kt, r_avg))


main()
